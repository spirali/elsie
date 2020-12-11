import json
import os
import sys

from .highlight import make_highlight_styles
from .jupyter import is_inside_notebook
from .pdfmerge import get_pdf_merger_by_name
from .query import compute_query
from .slidecls import Slide, DummyPdfSlide
from .inkscape import InkscapeShell
from .textstyle import TextStyle, compose_style
from .version import VERSION
from .cache import FsCache


class Slides:
    def __init__(
        self,
        width=1024,
        height=768,
        *,
        debug=False,
        pygments_theme="default",
        bg_color=None,
        cache_dir="./elsie-cache",
        inkscape_bin=None,
        name_policy="auto",
    ):
        inkscape_bin = (
            inkscape_bin or os.environ.get("ELSIE_INKSCAPE") or "/usr/bin/inkscape"
        )
        self.inkscape = InkscapeShell(inkscape_bin)
        self.inkscape_version = self.inkscape.get_version()
        assert "Inkscape" in self.inkscape_version
        self.cache_dir = cache_dir

        if name_policy not in ("auto", "unique", "ignore", "replace"):
            raise Exception("Invalid value for name_policy")
        if name_policy == "auto":
            if is_inside_notebook():
                name_policy = "replace"
            else:
                name_policy = "unique"
        self.name_policy = name_policy

        if not os.path.isdir(cache_dir):
            print("Creating cache directory:", cache_dir)
            os.makedirs(cache_dir)

        self.width = width
        self.height = height
        self.debug = debug
        self.bg_color = bg_color
        self._slides = []
        self._styles = {
            "default": TextStyle(
                font="sans-serif",
                color="black",
                size=28,
                line_spacing=1.20,
                align="middle",
                variant_numeric="lining-nums",
            ),
            "tt": TextStyle(font="monospace"),
            "emph": TextStyle(italic=True),
            "alert": TextStyle(bold=True, color="red"),
            "code": TextStyle(
                font="monospace",
                align="left",
                color="#222",
                line_spacing=1.20,
                size=20,
            ),
            "code_lineno": TextStyle(color="gray"),
        }
        self.temp_cache = {}
        self.query_cache = None
        self._styles.update(make_highlight_styles(pygments_theme))
        self.fs_cache = FsCache(cache_dir, VERSION, self.inkscape_version)

    def update_style(self, style_name, style):
        assert isinstance(style_name, str)
        old_style = self.get_style(style_name, full_style=False)
        old_style.update(style)
        self._styles = self._styles.copy()
        self._styles[style_name] = old_style

    def set_style(self, style_name, style, base="default"):
        assert isinstance(style_name, str)
        assert isinstance(style, TextStyle)
        if base != "default":
            base_style = self.get_style(base)
            base_style.update(style)
            style = base_style
        self._styles = self._styles.copy()
        self._styles[style_name] = style

    def get_style(self, style, full_style=True):
        return compose_style(self._styles, style, full_style)

    def get_slide_by_name(self, name):
        for slide in self._slides:
            if slide.name == name:
                return slide

    def new_slide(self, bg_color=None, *, view_box=None, name=None, debug_boxes=False):
        if view_box is not None and not (
            isinstance(view_box, tuple)
            and len(view_box) == 4
            and all(isinstance(v, (int, float)) for v in view_box)
        ):
            raise Exception(
                "view_box has to be None or tuple of four numbers (x, y, width, height)"
            )

        self._apply_name_policy(name)

        slide = Slide(
            self,
            len(self._slides),
            self.width,
            self.height,
            self._styles.copy(),
            self.fs_cache,
            self.temp_cache,
            view_box,
            name,
            debug_boxes,
        )
        self._slides.append(slide)
        box = slide.box()
        if bg_color is None:
            bg_color = self.bg_color
        if bg_color:
            box.box(x=0, y=0, width="100%", height="100%", z_level=-1000000).rect(
                bg_color=bg_color
            )
        return box

    def slide(self, bg_color=None, view_box=None, name=None, debug_boxes=False):
        def _helper(fn, *args, **kwargs):
            if name is None:
                _name = fn.__name__
            else:
                _name = name
            slide = self.new_slide(
                bg_color=bg_color,
                view_box=view_box,
                name=_name,
                debug_boxes=debug_boxes,
            )
            fn(slide, *args, **kwargs)
            return slide.slide

        return _helper

    def add_pdf(self, filename):
        """ Just add pdf without touches into resulting slides """
        self._slides.append(DummyPdfSlide(filename))

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

    def _show_progress(self, name, value=0, max_value=0, first=False, last=False):
        if not first:
            prefix = "\r"
        else:
            prefix = ""
        if last:
            progress = "done"
            suffix = "\n"
        else:
            if max_value != 0 and not first:
                progress = str(int(value * 100.0 / max_value)) + "%"
            else:
                progress = ""
            suffix = ""
        if self.debug:
            prefix = ""
            suffix = "\n"
        name = name.ljust(30, ".")
        sys.stdout.write("{}{} {}{}".format(prefix, name, progress, suffix))
        sys.stdout.flush()

    def _process_queries(self, slides, prune):
        cache = self.query_cache or self._load_query_cache()
        queries = sum((s.get_queries() for s in slides), [])

        self._show_progress("Preprocessing", first=True)
        need_compute = list(set(q.key for q in queries if q.key not in cache))
        if prune:
            new_cache = dict((q.key, cache[q.key]) for q in queries if q.key in cache)
        else:
            new_cache = cache
        for i, result in enumerate(
            map(lambda q: compute_query(self.inkscape, q), need_compute)
        ):
            key = need_compute[i]
            new_cache[key] = result
            self._show_progress("Preprocessing", i, len(need_compute))
        self._show_progress(
            "Preprocessing", len(need_compute), len(need_compute), last=True
        )

        for q in queries:
            q.callback(new_cache[q.key])
        self.query_cache = new_cache
        self._save_query_cache(new_cache)

    def _apply_name_policy(self, name):
        if self.name_policy == "ignore":
            return
        if name is None:
            raise Exception(
                "Slide needs an explicit name (name policy is now '{}')".format(
                    self.name_policy
                )
            )
        if not isinstance(name, str):
            raise Exception(
                "Slide name has to be a string, not {}".format(repr(type(name)))
            )
        slide = self.get_slide_by_name(name)
        if slide:
            if self.name_policy == "unique":
                raise Exception("Slide with name '{}' already exists".format(name))
            elif self.name_policy == "replace":
                self._slides.remove(slide)
            else:
                assert 0

    def render(
        self,
        output="slides.pdf",
        return_svg=False,
        export_type="pdf",
        pdf_merger="pypdf",
        drop_duplicates=False,
        slide_postprocessing=None,
        prune_cache=True,
        select_slides=None,
    ):
        if select_slides is None:
            select_slides = self._slides

        if not select_slides:
            raise Exception("No slides to render")

        if slide_postprocessing:
            slide_postprocessing([slide.box() for slide in select_slides])

        self._process_queries(select_slides, prune_cache)
        renders = []
        for slide in select_slides:
            slide.prepare()
            renders += [(slide, step) for step in range(1, slide.steps() + 1)]

        if return_svg:
            svgs = [(slide, step, slide.make_svg(step)) for slide, step in renders]
            return svgs

        if export_type == "pdf" and pdf_merger is not None:
            merger = get_pdf_merger_by_name(pdf_merger)
        else:
            merger = []
        self._show_progress("Building", first=True)
        prev_pdf = None
        for i, pdf in enumerate(
            map(
                lambda x: x[0].render(x[1], self.debug, export_type, self.inkscape),
                renders,
            )
        ):
            if not drop_duplicates or prev_pdf != pdf:
                merger.append(pdf)
                prev_pdf = pdf
            self._show_progress("Building", i, len(renders))
        self._show_progress("Building", len(renders), len(renders), last=True)

        if export_type == "pdf" and pdf_merger is not None:
            merger.write(output, self.debug)
            if prune_cache:
                self.fs_cache.remove_unused()
            print("Slides written into '{}'".format(output))
        else:
            if prune_cache:
                self.fs_cache.remove_unused()
            return merger
