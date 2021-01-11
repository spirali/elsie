from ....utils.geom import Rect
from ....utils.sxml import Xml
from ..rcontext import RenderingContext
from .draw import (
    draw_bitmap,
    draw_ellipse,
    draw_path,
    draw_polygon,
    draw_polyline,
    draw_rect,
    draw_text,
)
from .utils import svg_begin, svg_end


class SvgRenderingContext(RenderingContext):
    def __init__(self, slide, step, debug_boxes):
        super().__init__(step, debug_boxes)
        self.xml = Xml()
        svg_begin(self.xml, slide.width, slide.height, slide.view_box)

    def draw_rect(self, rect: Rect, rx=None, ry=None, rotation=None, **kwargs):
        draw_rect(self.xml, rect, rx=rx, ry=ry, rotation=rotation, **kwargs)

    def draw_ellipse(self, rect: Rect, rotation=None, **kwargs):
        draw_ellipse(self.xml, rect, rotation=rotation, **kwargs)

    def draw_polygon(self, points, rotation=None, **kwargs):
        draw_polygon(self.xml, points, rotation=rotation, **kwargs)

    def draw_polyline(self, points, **kwargs):
        draw_polyline(self.xml, points, **kwargs)

    def draw_path(self, commands, **kwargs):
        draw_path(self.xml, commands, **kwargs)

    def draw_text(self, rect, *args, **kwargs):
        draw_text(self.xml, *args, **kwargs)

    def draw_bitmap(self, *args, **kwargs):
        draw_bitmap(self.xml, *args, **kwargs)

    def render(self) -> str:
        svg_end(self.xml)
        return self.xml.to_string()
