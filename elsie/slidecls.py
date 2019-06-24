
# The file is not named "slide.py" because of class of "slide" import in __init__.py

import os.path
import hashlib

from .box import Box
from .sxml import Xml
from .geom import Rect
from .svg import svg_begin, svg_end, convert_to_pdf
from .rcontext import RenderingContext
from .show import ShowInfo


class Slide:

    def __init__(self, index, width, height, styles, temp_cache):
        self.width = width
        self.height = height
        self.index = index
        self._box = Box(self, 0, 0, width, height, styles, ShowInfo())
        self._box._styles = styles
        self.max_step = 1
        self.temp_cache = temp_cache

    def box(self):
        return self._box

    def queries(self):
        queries = []
        self._box._traverse(lambda box: queries.extend(box._queries))
        return queries

    def prepare(self):
        rect = Rect(0, 0, self.width, self.height)
        self._box._set_rect(rect)

    def steps(self):
        shows = [1]
        self._box._traverse(lambda box: shows.append(box._min_steps()))
        return max(value for value in shows if value)

    def make_svg(self, step):
        xml = Xml()
        svg_begin(xml, self.width, self.height)
        ctx = RenderingContext(xml, step)
        painters = self._box._get_painters(ctx)
        painters.sort(key=lambda p: p.z_level)
        for p in painters:
            p.render(ctx)
        svg_end(xml)
        return xml.to_string()

    def render(self, step, cache_dir, pdfs_in_dir, debug):
        svg = self.make_svg(step)

        h = hashlib.sha1()
        h.update(svg.encode())
        pdf_name = h.hexdigest() + ".pdf"

        if pdf_name in pdfs_in_dir:
            return pdf_name

        if debug:
            svg_file = os.path.join(
                cache_dir, "{}-{}.svg".format(self.index, step))
            with open(svg_file, "w") as f:
                f.write(svg)

        full_name = os.path.join(cache_dir, pdf_name)
        convert_to_pdf(svg, full_name)
        return pdf_name


class DummyPdfSlide:

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

    def queries(self):
        return []

    def prepare(self):
        pass

    def steps(self):
        return 1

    def make_svg(self):
        return None

    def render(self, step, cache_dir, pdfs_in_dir, debug):
        return self.filename
