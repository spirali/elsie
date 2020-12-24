import json
import os
import sys
from typing import Callable, List, TYPE_CHECKING, Tuple, Union

from .highlight import make_highlight_styles
from .jupyter import is_inside_notebook
from .pdfmerge import get_pdf_merger_by_name
from .query import compute_query
from .render import per_page_groupping
from .slide import Slide, ExternPdfSlide
from .inkscape import InkscapeShell
from .textstyle import TextStyle, compose_style
from .version import VERSION
from .cache import FsCache

if TYPE_CHECKING:
    from . import box
    from .render import RenderUnit


class Slides:
    """
    Presentation containing slides.
    """

    def __init__(
        self,
        width=1024,
        height=768,
        *,
        debug=False,
        pygments_theme="default",
        bg_color: str = None,
        cache_dir="./elsie-cache",
        name_policy="auto",
        inkscape: Union[str, InkscapeShell] = None,
    ):
        """
        Parameters
        ----------
        width: int
            Width of the slides.
        height: int
            Height of the slides.
        debug: bool
            Enable debugging mode.
        pygments_theme: str
            Theme used for syntax highlighting.
        bg_color: str
            Default background color of each slide.
        cache_dir: str
            Directory where slide cache will be stored.
        name_policy: {"auto", "ignore", "replace", "unique"}
            Policy used to handle slides with the same name.
            "unique" -> Slides with the same name are not allowed.
            "replace" -> If there was a slide with the same name, it will be removed prior to
            adding the new slide.
            "ignore" -> Slide names are ignored.
            "auto" -> Uses "replace" behaviour when running inside Jupyter, otherwise uses
            "unique".
        inkscape: Union[str, InkscapeShell]
            Either a path to the Inkscape binary or an instance of the InkscapeShell class.
        """
        if isinstance(inkscape, InkscapeShell):
            self.inkscape = inkscape
        else:
            inkscape_bin = (
                inkscape or os.environ.get("ELSIE_INKSCAPE") or "/usr/bin/inkscape"
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
        self.query_cache = self._load_query_cache()
        self.used_query_cache = {}
        self._styles.update(make_highlight_styles(pygments_theme))
        self.fs_cache = FsCache(cache_dir, VERSION, self.inkscape_version)

    def update_style(self, style_name: str, style: TextStyle):
        """Updates the style with the given name in-place."""
        assert isinstance(style_name, str)
        old_style = self.get_style(style_name, full_style=False)
        old_style.update(style)
        self._styles = self._styles.copy()
        self._styles[style_name] = old_style

    def set_style(self, style_name: str, style: TextStyle, base="default"):
        """Sets the value of the style with the given name."""
        assert isinstance(style_name, str)
        assert isinstance(style, TextStyle)
        if base != "default":
            base_style = self.get_style(base)
            base_style.update(style)
            style = base_style
        self._styles = self._styles.copy()
        self._styles[style_name] = style

    def get_style(self, style, full_style=False) -> TextStyle:
        return compose_style(self._styles, style, full_style)

    def get_slide_by_name(self, name: str) -> Union[Slide, None]:
        """Returns a slide with the given name."""
        for slide in self._slides:
            if slide.name == name:
                return slide

    def new_slide(
        self, name=None, *, bg_color=None, view_box=None, debug_boxes=False
    ) -> "box.Box":
        """
        Creates a new slide and returns its root Box.

        Parameters
        ----------
        name: str
            Name of the slide
        bg_color: str
            Background color of the slide.
        view_box: tuple
            SVG viewbox of the slide. Has to be a 4-element tuple (x, y, width, height).
        debug_boxes: bool
            If True, debugging information about each box will be drawn on the slide.
        """
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

    def slide(self, name=None, *, bg_color=None, view_box=None, debug_boxes=False):
        """
        Decorator which creates a new slide and passes its root box to the decorated function.

        Examples:
        slides = elsie.Slides()

        @slides.slide()
        def slide1(slide: elsie.Box):
            slide.box().text("Hello")

        Parameters
        ----------
        name: str
            Name of the slide.
            If `name` is `None`, the name of the slide will be set to the name of the decorated
            function.
        bg_color: str
            Background color of the slide.
        view_box: tuple
            SVG viewbox of the slide. Has to be a 4-element tuple (x, y, width, height).
        debug_boxes: bool
            If True, debugging information about each box will be drawn on the slide.
        """

        def _helper(fn, *args, **kwargs):
            if name is None:
                _name = fn.__name__
            else:
                _name = name
            slide = self.new_slide(
                name=_name,
                bg_color=bg_color,
                view_box=view_box,
                debug_boxes=debug_boxes,
            )
            fn(slide, *args, **kwargs)
            return slide.slide

        return _helper

    def add_pdf(self, filename: str):
        """Adds raw PDF into the resulting slides."""
        self._slides.append(ExternPdfSlide(filename))

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

    """
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
    """

    def _apply_name_policy(self, name):
        if self.name_policy == "ignore":
            return
        if name is None:
            if self.name_policy == "unique":
                return
            raise Exception(
                "Slide needs an explicit name (name policy is now '{}')".format(
                    self.name_policy
                )
            )
        if not isinstance(name, str):
            raise Exception(
                "Slide name has to be a string or None, not {}".format(repr(type(name)))
            )
        slide = self.get_slide_by_name(name)
        if slide:
            if self.name_policy == "unique":
                raise Exception("Slide with name '{}' already exists".format(name))
            elif self.name_policy == "replace":
                self._slides.remove(slide)
            else:
                assert 0

    def process_query(self, method: str, data: str):
        key = (method, data)
        value = self.query_cache.get(key)
        if value is None:
            value = compute_query(self.inkscape, method, data)
            self.query_cache[key] = value
        self.used_query_cache[key] = value
        return value

    def render(
        self,
        output: Union[str, None] = "slides.pdf",
        return_units=False,
        export_type="pdf",
        pdf_merger="pypdf",
        slide_postprocessing: "Callable[[List[box.Box]], ...]" = None,
        prune_cache=True,
        save_cache=True,
        select_slides: List[Slide] = None,
        slides_per_page: Tuple[int, int] = None,
    ) -> "Union[None, List[RenderUnit], List[str]]":
        """
        Renders the presentation into a PDF file.

        Parameters
        ----------
        output: str
            Output PDF file path where the slides will be rendered.
        return_units: bool
            If True, this function will return a list of (either SVG or PDF) render units.
            In this case the presentation will not be rendered into the `output` file.
        export_type: str
            Output format of slides; it supports all formats supported by Inkscape export 
            (e.g. "pdf", "png", etc.)
            If export_type is "pdf" then it is merged into one
            final PDF file defined by parameter `output`. 
            For other formats, `output` is ignored and returns a list of filenames
            with exported files. The files are placed into cache directory and could be
            removed by another call of render with `prune_cache=True`.
        pdf_merger: {"pypdf", "pdfunite"}
            Method used to merge PDFs together. It is used when export_type is "pdf".
        slide_postprocessing: Callable[[List[Box]], ...]
            This function will be called just before the slides are rendered.
            It will be passed a list of root boxes, one for each slide.
        select_slides: List[Slide]
            List of slides to be rendered.
            If `None`, then all slides are rendered.
        slides_per_page: Tuple[int, int]
            Must be a 2-element tuple (R, C) of integers.
            Renders a grid of (R, C) slides per each page.
            If not defined, then each slide is rendered on a single page.

        Other Parameters
        ----------------

        prune_cache: bool
            If True, then after a successful render, all data that was not used for this render
            will be removed fromthe cache directory.
            Otherwise unused data will not be touched.

        save_cache: bool
            If True, the query cache will be updated when all queries are computed.
        """
        if select_slides is None:
            select_slides = self._slides

        if not select_slides:
            raise Exception("No slides to render")

        if slides_per_page is not None:
            if (
                len(slides_per_page) != 2
                or not isinstance(slides_per_page[0], int)
                or not isinstance(slides_per_page[1], int)
            ):
                raise Exception(
                    f"slides_per_page has to be None or pair of two integers, not {slides_per_page}"
                )

        if slide_postprocessing:
            slide_postprocessing([slide.box() for slide in select_slides])

        if prune_cache:
            self.query_cache = self.used_query_cache
            self.used_query_cache = {}

        if save_cache:
            self._save_query_cache(self.query_cache)

        units = []
        for slide in select_slides:
            slide.prepare()
            for step in range(1, slide.steps() + 1):
                units.append(slide.make_render_unit(step))

        if self.debug:
            for unit in units:
                unit.write_debug(self.fs_cache.cache_dir)

        if slides_per_page is not None:
            units = per_page_groupping(
                units, slides_per_page[0], slides_per_page[1], self.width, self.height
            )

        if return_units:
            return units

        if export_type == "pdf" and pdf_merger is not None:
            merger = get_pdf_merger_by_name(pdf_merger)
        else:
            merger = []

        self._show_progress("Building", first=True)
        for i, unit in enumerate(units):
            unit_output = unit.export(self.fs_cache, export_type, self.inkscape)
            if unit_output is not None:
                merger.append(unit_output)
            self._show_progress("Building", i, len(units))
        self._show_progress("Building", len(units), len(units), last=True)

        if export_type == "pdf" and pdf_merger is not None:
            merger.write(output, self.debug)
            if prune_cache:
                self.fs_cache.remove_unused()
            print("Slides written into '{}'".format(output))
        else:
            if prune_cache:
                self.fs_cache.remove_unused()
            return merger
