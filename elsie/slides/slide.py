import os.path
from typing import TYPE_CHECKING

from ..boxtree.box import Box
from ..boxtree.layout import Layout
from ..render import jupyter
from ..render.render import ExportedRenderUnit
from ..utils.geom import Rect
from .show import ShowInfo

if TYPE_CHECKING:
    from . import slidedeck


class Slide:
    def __init__(
        self,
        slides: "slidedeck.SlideDeck",
        index: int,
        width: int,
        height: int,
        styles,
        fs_cache,
        temp_cache,
        view_box,
        name: str,
        debug_boxes: bool,
    ):
        self.slides = slides
        self.name = name
        self.width = width
        self.height = height
        self.index = index
        self.view_box = view_box
        self.debug_boxes = debug_boxes
        self._box = Box(
            self,
            layout=Layout(x=0, y=0, width=width, height=height),
            styles=styles,
            show_info=ShowInfo(),
            name=name,
        )
        self.max_step = 1
        self.temp_cache = temp_cache
        self.fs_cache = fs_cache

    def box(self):
        return self._box

    def current_fragment(self) -> int:
        """Returns the current maximum fragment."""
        return self.max_step

    def prepare(self):
        rect = Rect(0, 0, self.width, self.height)
        self._box.layout.set_rect(rect)

    def steps(self):
        shows = [1]
        self._box._traverse(lambda box: shows.append(box._min_steps()))
        return max(value for value in shows if value)

    def make_render_unit(self, backend, step, export_type: str):
        return backend.create_render_unit(self, step, export_type)

    def _repr_html_(self):
        return jupyter.render_slide_html(self)


class ExternPdfSlide:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

    def prepare(self):
        pass

    def steps(self):
        return 1

    def make_render_unit(self, backend, step, export_type):
        assert export_type == "pdf"
        return ExportedRenderUnit(self, step, self.filename, "pdf")
