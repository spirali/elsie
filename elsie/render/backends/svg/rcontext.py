from ....utils.geom import Rect
from ....utils.sxml import Xml
from ..rcontext import RenderingContext
from .draw import draw_bitmap, draw_text, set_paint_style
from .utils import apply_rotation, svg_begin, svg_end


class SvgRenderingContext(RenderingContext):
    def __init__(self, slide, fs_cache, step, debug_boxes):
        super().__init__(step, debug_boxes)
        self.xml = Xml()
        svg_begin(self.xml, slide.width, slide.height, slide.view_box)
        self.fs_cache = fs_cache

    def draw_rect(self, rect: Rect, rx=None, ry=None, rotation=None, **kwargs):
        self.xml.element("rect")
        self.xml.set("x", rect.x)
        self.xml.set("y", rect.y)
        self.xml.set("width", rect.width)
        self.xml.set("height", rect.height)
        if rx:
            self.xml.set("rx", rx)
        if ry:
            self.xml.set("ry", ry)
        if rotation:
            apply_rotation(self.xml, rotation, rect.mid_point)
        set_paint_style(self.xml, **kwargs)
        self.xml.close("rect")

    def draw_text(self, *args, **kwargs):
        draw_text(self.xml, *args, **kwargs)

    def draw_bitmap(self, *args, **kwargs):
        draw_bitmap(self.xml, *args, **kwargs)

    def render(self) -> str:
        svg_end(self.xml)
        return self.xml.to_string()
