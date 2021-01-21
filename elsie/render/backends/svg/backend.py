import json
import os
import re
from typing import Union

from ....utils.sxml import Xml
from ....version import VERSION
from ...inkscape import InkscapeShell
from ...render import SvgRenderUnit
from ..backend import DEFAULT_CACHE_DIR, Backend
from .draw import draw_text
from .query import compute_query
from .rcontext import SvgRenderingContext

VERSION_REGEX = re.compile(r"Inkscape\s+(\d+\..*)")


class InkscapeBackend(Backend):
    """Backend that maps Elsie primitives to SVG and renders them to PDF using Inkscape."""

    def __init__(
        self,
        inkscape: Union[str, InkscapeShell] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        """
        Parameters
        ----------
        inkscape: Union[str, InkscapeShell]
            Either a path to the Inkscape binary or an instance of the InkscapeShell class.
        cache_dir: str
            Cache directory for caching SVG files.
        """
        super().__init__(cache_dir)
        if isinstance(inkscape, InkscapeShell):
            self.inkscape = inkscape
        else:
            inkscape_bin = (
                inkscape or os.environ.get("ELSIE_INKSCAPE") or "/usr/bin/inkscape"
            )
            self.inkscape = InkscapeShell(inkscape_bin)

        self.inkscape_version = self.inkscape.get_version()
        match = VERSION_REGEX.search(self.inkscape_version)
        if not match:
            print(f"WARNING: Unknown Inkscape version ({self.inkscape_version})")
        else:
            version = match.group(1)
            major_version = version.split(".")[0]
            if int(major_version) < 1:
                print(
                    f"WARNING: You are using Inkscape {version}, which might be incompatible "
                    f"with Elsie. Please consider upgrading to Inkscape 1.0+."
                )

        self.query_cache = self._load_query_cache()
        self.used_query_cache = {}

    def get_version(self, elsie_version: str) -> str:
        return f"{elsie_version}/{self.inkscape_version}"

    def create_render_unit(self, slide, step, export_type):
        ctx = SvgRenderingContext(slide, step, slide.debug_boxes)
        painters = slide._box.get_painters(ctx, 0)
        painters.sort(key=lambda painter: painter.z_level)
        for p in painters:
            p.render(ctx)
        return SvgRenderUnit(slide, step, ctx.render(), self.inkscape)

    def prune_cache(self):
        self.query_cache = self.used_query_cache
        self.used_query_cache = {}

    def save_cache(self):
        self._save_query_cache(self.query_cache)

    def compute_text_width(self, parsed_text, style, styles, id_index=None):
        return self._text_query("inkscape-w", parsed_text, style, styles, id_index)

    def compute_text_height(self, parsed_text, style, styles, id_index=None):
        return self._text_query("inkscape-h", parsed_text, style, styles, id_index)

    def compute_text_x(self, parsed_text, style, styles, id_index=None):
        return self._text_query("inkscape-x", parsed_text, style, styles, id_index)

    def _text_query(self, query, parsed_text, style, styles, id_index):
        xml = Xml()
        draw_text(xml, 0, 0, parsed_text, style, styles, id="target", id_index=id_index)
        key = xml.to_string()
        return self.process_query(query, key)

    def process_query(self, method: str, data: str):
        key = (method, data)
        value = self.query_cache.get(key)
        if value is None:
            value = compute_query(self.inkscape, method, data)
            self.query_cache[key] = value
        self.used_query_cache[key] = value
        return value

    def _query_cache_file(self):
        return os.path.join(self.cache_dir, "queries3.cache")

    def _load_query_cache(self):
        cache_file = self._query_cache_file()
        if os.path.isfile(cache_file):
            with open(cache_file) as f:
                cache_config = json.load(f)
            if cache_config.get("version") != VERSION:
                print("Elsie version changed; cache dropped")
                return {}
            if cache_config.get("inkscape") != self.inkscape_version:
                print("Inkscape version changed; cache dropped")
                return {}
            return dict(
                (tuple(key), value) for key, value in cache_config.get("queries", ())
            )
        else:
            return {}

    def _save_query_cache(self, cache):
        cache_file = self._query_cache_file()
        cache_config = {
            "version": VERSION,
            "inkscape": self.inkscape_version,
            "queries": list(cache.items()),
        }
        with open(cache_file, "w") as f:
            json.dump(cache_config, f)
