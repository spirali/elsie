import itertools
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from .highlight import make_highlight_styles
from .pdfmerge import get_pdf_merger_by_name
from .query import compute_query
from .slide import Slide, DummyPdfSlide
from .style import Style
from .svg import get_inkscape_version
from .version import VERSION


class Slides:

    def __init__(self,
                 width=1024,
                 height=768,
                 debug=False,
                 pygments_theme="default",
                 bg_color=None):

        self.width = width
        self.height = height
        self.debug = debug
        self.bg_color = bg_color
        self._slides = []
        self._styles = {
            "default": Style(font="Ubuntu",
                             color="black",
                             size=28,
                             line_spacing=1.2,
                             align="middle"),
            "tt": Style(font="Ubuntu mono"),
            "emph": Style(italic=True),
            "alert": Style(bold=True, color="red"),
            "code": Style(font="Ubuntu Mono",
                          align="left",
                          color="#222",
                          line_spacing=1.2,
                          size=20),
            "code_lineno": Style(color="gray")
        }
        self.temp_cache = {}
        self._styles.update(make_highlight_styles(pygments_theme))

    def new_style(self, name, style=None, **kwargs):
        if style is not None:
            assert isinstance(style, Style)
            source = style
        else:
            source = Style()

        if name in self._styles:
            raise Exception("Style already exists")
        self._styles[name] = source.update(**kwargs)

    def update_style(self, name, style=None, **kwargs):
        source = self._styles[name]

        if style is not None:
            assert isinstance(style, Style)
            source = source.update_from(style)

        self._styles[name] = source.update(**kwargs)

    def new_slide(self, bg_color=None):
        slide = Slide(
            len(self._slides), self.width, self.height, self._styles.copy(), self.temp_cache)
        self._slides.append(slide)
        box = slide.box()
        if bg_color is None:
            bg_color = self.bg_color
        if bg_color:
            box.box(x=0, y=0, width="100%", height="100%", z_level=-1000000) \
                .rect(bg_color=bg_color)
        return box

    def add_pdf(self, filename):
        """ Just add pdf without touches into resulting slides """
        self._slides.append(DummyPdfSlide(filename))

    def _load_query_cache(self, cache_file, inkscape_version):
        if os.path.isfile(cache_file):
            with open(cache_file) as f:
                cache_config = json.load(f)
            if cache_config.get("version") != VERSION:
                print("Elsie version changed; cache dropped")
                return {}
            if cache_config.get("inkscape") != inkscape_version:
                print("Inkscape version changed; cache dropped")
                return {}
            return dict((tuple(key), value) for key, value in cache_config.get("queries", ()))
        else:
            return {}

    def _save_query_cache(self, cache, cache_file, inkscape_version):
        cache_config = {
            "version": VERSION,
            "inkscape": inkscape_version,
            "queries": list(cache.items()),
        }
        with open(cache_file, "w") as f:
            json.dump(cache_config, f)

    def _show_progress(
            self, name, value=0, max_value=0, first=False, last=False):
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

    def render(self, output, cache_dir="./elsie-cache",
               threads=None, return_svg=False, pdf_merger="pypdf",
               drop_duplicates=False):
        inkscape_version = get_inkscape_version()
        if not os.path.isdir(cache_dir):
            print("Creating cache directory:", cache_dir)
            os.makedirs(cache_dir)

        if not self._slides:
            raise Exception("No slides to render")

        pdfs_in_dir = set(name for name in os.listdir(cache_dir)
                          if name.endswith(".pdf"))

        if threads is None:
            threads = os.cpu_count() or 1
        pool = ThreadPoolExecutor(threads)

        cache_file = os.path.join(cache_dir, "queries3.cache")
        cache = self._load_query_cache(cache_file, inkscape_version)
        queries = sum((s.queries() for s in self._slides), [])

        self._show_progress("Preprocessing", first=True)
        need_compute = list(set(q.key for q in queries
                                if q.key not in cache))
        new_cache = dict((q.key, cache[q.key]) for q in queries
                         if q.key in cache)
        for i, result in enumerate(pool.map(compute_query, need_compute)):
            key = need_compute[i]
            new_cache[key] = result
            self._show_progress("Preprocessing", i, len(need_compute))
        self._show_progress(
            "Preprocessing", len(need_compute), len(need_compute), last=True)

        for q in queries:
            q.callback(new_cache[q.key])

        self._save_query_cache(new_cache, cache_file, inkscape_version)

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
        computed_pdfs = set()
        prev_pdf = None
        for i, pdf in enumerate(pool.map(
                lambda x: x[0].render(
                    x[1], cache_dir, pdfs_in_dir, self.debug),
                renders)):
            if not drop_duplicates or prev_pdf != pdf:
                merger.append(os.path.join(cache_dir, pdf))
                computed_pdfs.add(pdf)
                prev_pdf = pdf
            self._show_progress("Building", i, len(renders))
        self._show_progress("Building", len(renders), len(renders), last=True)

        merger.write(output, self.debug)
        print("Slides written into '{}'".format(output))

        for pdf in pdfs_in_dir.difference(computed_pdfs):
            os.remove(os.path.join(cache_dir, pdf))
