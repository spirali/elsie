import os

from .slide import Slide, DummyPdfSlide
from .query import compute_query
from .textstyle import check_style
from .highlight import make_highlight_styles
from .pdfmerge import get_pdf_merger_by_name
from concurrent.futures import ThreadPoolExecutor
import sys
import json


class Slides:

    def __init__(self,
                 width=1024,
                 height=768,
                 debug=False,
                 pygments_theme="default"):

        self.width = width
        self.height = height
        self.debug = debug
        self._slides = []
        self._styles = {
            "default": {
                "font": "Ubuntu",
                "color": "black",
                "size": 28,
                "line_spacing": 1.20,
                "align": "middle",
            },
            "tt": {
                "font": "Ubuntu mono",
            },
            "emph": {
                "italic": True,
            },
            "alert": {
                "bold": True,
                "color": "red",
            },
            "code": {
                "font": "Ubuntu Mono",
                "align": "left",
                "color": "#222",
                "line_spacing": 1.20,
                "size": 20,
            },
        }
        self._styles.update(make_highlight_styles(pygments_theme))

    def new_style(self, name, **kwargs):
        if name in self._styles:
            raise Exception("Style already exists")
        check_style(kwargs)
        self._styles[name] = kwargs

    def update_style(self, name, **kwargs):
        check_style(kwargs)
        new_style = self._styles[name].copy()
        new_style.update(kwargs)
        self._styles[name] = new_style

    def derive_style(self, old_style_name, new_style_name, **kwargs):
        """ Copy an existing style under a new name and modify it. """
        check_style(kwargs)
        new_style = self._styles[old_style_name].copy()
        new_style.update(kwargs)
        self._styles[new_style_name] = new_style

    def new_slide(self):
        slide = Slide(
            len(self._slides), self.width, self.height, self._styles.copy())
        self._slides.append(slide)
        return slide.box()

    def add_pdf(self, filename):
        """ Just add pdf without touches into resulting slides """
        self._slides.append(DummyPdfSlide(filename))

    def _load_query_cache(self, cache_file):
        if os.path.isfile(cache_file):
            with open(cache_file) as f:
                return json.load(f)
        else:
            return {}

    def _save_query_cache(self, cache, cache_file):
        with open(cache_file, "w") as f:
            json.dump(cache, f)

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
               threads=None, return_svg=False, pdf_merger="pypdf"):
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

        cache_file = os.path.join(cache_dir, "queries.cache")
        cache = self._load_query_cache(cache_file)
        queries = sum((s.queries() for s in self._slides), [])

        self._show_progress("Preprocessing", first=True)
        need_compute = list(set(key for key, callback in queries
                                if key not in cache))
        new_cache = dict((key, cache[key]) for key, callback in queries
                         if key in cache)
        for i, result in enumerate(pool.map(compute_query, need_compute)):
            key = need_compute[i]
            new_cache[key] = result
            self._show_progress("Preprocessing", i, len(need_compute))
        self._show_progress(
            "Preprocessing", len(need_compute), len(need_compute), last=True)

        for key, callback in queries:
            callback(new_cache[key])

        self._save_query_cache(new_cache, cache_file)

        renders = []
        for slide in self._slides:
            slide.prepare()
            renders += [(slide, step) for step in range(1, slide.steps() + 1)]

        if return_svg:
            return [slide.make_svg(step) for slide, step in renders]

        merger = get_pdf_merger_by_name(pdf_merger)
        self._show_progress("Building", first=True)
        computed_pdfs = set()
        for i, pdf in enumerate(pool.map(
                lambda x: x[0].render(
                    x[1], cache_dir, pdfs_in_dir, self.debug),
                renders)):
            merger.append(os.path.join(cache_dir, pdf))
            computed_pdfs.add(pdf)
            self._show_progress("Building", i, len(renders))
        self._show_progress("Building", len(renders), len(renders), last=True)

        merger.write(output, self.debug)
        print("Slides written into '{}'".format(output))

        for pdf in pdfs_in_dir.difference(computed_pdfs):
            os.remove(os.path.join(cache_dir, pdf))
