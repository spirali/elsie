import itertools
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from .highlight import make_highlight_styles
from .pdfmerge import get_pdf_merger_by_name
from .query import compute_query
from .slidecls import Slide, DummyPdfSlide
from .svg import get_inkscape_version
from .textstyle import TextStyle, compose_style
from .version import VERSION
from .cache import FsCache


class Slides:
    def __init__(
        self,
        width=1024,
        height=768,
        debug=False,
        pygments_theme="default",
        bg_color=None,
        cache_dir="./elsie-cache",
    ):
        self.inkscape_version = get_inkscape_version()
        self.cache_dir = cache_dir

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
                font="Ubuntu",
                color="black",
                size=28,
                line_spacing=1.20,
                align="middle",
                variant_numeric="lining-nums",
            ),
            "tt": TextStyle(font="Ubuntu mono"),
            "emph": TextStyle(italic=True),
            "alert": TextStyle(bold=True, color="red"),
            "code": TextStyle(
                font="Ubuntu Mono",
                align="left",
                color="#222",
                line_spacing=1.20,
                size=20,
            ),
            "code_lineno": TextStyle(color="gray"),
        }
        self.temp_cache = {}
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
            style = self.get_style(base).update(style)
        self._styles = self._styles.copy()
        self._styles[style_name] = style

    def get_style(self, style, full_style=True):
        return compose_style(self._styles, style, full_style)

    def new_slide(self, bg_color=None, *, view_box=None, name=None, debug_boxes=False):
        if view_box is not None and not (
            isinstance(view_box, tuple)
            and len(view_box) == 4
            and all(isinstance(v, (int, float)) for v in view_box)
        ):
            raise Exception(
                "view_box has to be None or tuple of four numbers (x, y, width, height)"
            )
        slide = Slide(
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

    def add_pdf(self, filename):
        """ Just add pdf without touches into resulting slides """
        self._slides.append(DummyPdfSlide(filename))

    def _load_query_cache(self, cache_file):
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

    def _save_query_cache(self, cache, cache_file):
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

    def render(
        self,
        output,
        threads=None,
        return_svg=False,
        pdf_merger="pypdf",
        drop_duplicates=False,
        slide_postprocessing=None,
    ):
        if not self._slides:
            raise Exception("No slides to render")

        if slide_postprocessing:
            slide_postprocessing([slide.box() for slide in self._slides])

        if threads is None:
            threads = os.cpu_count() or 1
        pool = ThreadPoolExecutor(threads)

        cache_file = os.path.join(self.cache_dir, "queries3.cache")
        cache = self._load_query_cache(cache_file)
        queries = sum((s.get_queries() for s in self._slides), [])

        self._show_progress("Preprocessing", first=True)
        need_compute = list(set(q.key for q in queries if q.key not in cache))
        new_cache = dict((q.key, cache[q.key]) for q in queries if q.key in cache)
        for i, result in enumerate(pool.map(compute_query, need_compute)):
            key = need_compute[i]
            new_cache[key] = result
            self._show_progress("Preprocessing", i, len(need_compute))
        self._show_progress(
            "Preprocessing", len(need_compute), len(need_compute), last=True
        )

        for q in queries:
            q.callback(new_cache[q.key])

        self._save_query_cache(new_cache, cache_file)

        renders = []
        for slide in self._slides:
            slide.prepare()
            renders += [(slide, step) for step in range(1, slide.steps() + 1)]

        if return_svg:
            svgs = [slide.make_svg(step) for slide, step in renders]
            if drop_duplicates:
                return [x[0] for x in itertools.groupby(svgs)]
            return svgs

        merger = get_pdf_merger_by_name(pdf_merger)
        self._show_progress("Building", first=True)
        prev_pdf = None
        for i, pdf in enumerate(
            pool.map(lambda x: x[0].render(x[1], self.debug), renders)
        ):
            if not drop_duplicates or prev_pdf != pdf:
                merger.append(pdf)
                prev_pdf = pdf
            self._show_progress("Building", i, len(renders))
        self._show_progress("Building", len(renders), len(renders), last=True)

        merger.write(output, self.debug)
        print("Slides written into '{}'".format(output))

        self.fs_cache.remove_unused()


_global_slides = None


def set_global_slides(slides):
    """Set global slides (used in @slide decorator)"""
    assert isinstance(slides, Slides)
    global _global_slides
    _global_slides = slides


def get_global_slides():
    """Get global slides

    If not exists, default slides is created
    """
    global _global_slides
    if _global_slides is None:
        _global_slides = Slides()
    return _global_slides


def update_style(style_name, style):
    """Call update_style method on global slides"""
    get_global_slides().update_style(style_name, style)


def get_style(style, full_style=True):
    """Get style from global slides"""
    return get_global_slides().get_style(style, full_style)


def set_style(style_name, style, base=None):
    """Call set_style method on global slides"""
    get_global_slides().set_style(style_name, style, base)


# Decorator
def slide(*, bg_color=None, view_box=None, name=None, debug_boxes=False):
    slides = get_global_slides()

    def _helper(fn):
        if name is None:
            _name = fn.__name__
        else:
            _name = name
        slide = slides.new_slide(
            bg_color=bg_color, view_box=view_box, name=_name, debug_boxes=debug_boxes
        )
        fn(slide)
        return fn

    return _helper


def render(
    output="output.pdf",
    threads=None,
    return_svg=False,
    pdf_merger="pypdf",
    drop_duplicates=False,
    slide_postprocessing=None,
):
    """Render global slides"""
    if _global_slides is None:
        raise Exception("No slides to render")
    return _global_slides.render(
        output,
        threads,
        return_svg,
        pdf_merger,
        drop_duplicates,
        slide_postprocessing,
    )
