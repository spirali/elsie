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

    def draw_text(
        self,
        rect,
        x,
        y,
        parsed_text,
        style,
        styles,
        rotation=None,
        scale=None,
        **kwargs,
    ):
        if scale is not None:
            x /= scale
            y /= scale

        transforms = []
        if rotation:
            transforms.append(
                f"rotate({rotation} {rect.mid_point[0]} {rect.mid_point[1]})"
            )
        if scale:
            transforms.append(f"scale({scale})")
        transform = " ".join(transforms) if transforms else None
        draw_text(
            self.xml,
            x=x,
            y=y,
            parsed_text=parsed_text,
            style=style,
            styles=styles,
            transform=transform,
            **kwargs,
        )

    def draw_bitmap(self, *args, **kwargs):
        draw_bitmap(self.xml, *args, **kwargs)

    def draw_svg(self, svg, x, y, scale, rotation=None, rotation_center=None, **kwargs):
        xml = Xml()
        xml.element("g")
        transform = []

        # First scale, then rotate (https://gamedev.stackexchange.com/a/16721/73578).
        # Applied in opposite order in transform.
        if rotation is not None:
            assert rotation_center is not None
            transform.append(
                f"rotate({rotation} {rotation_center[0]} {rotation_center[1]})"
            )

        transform.append(f"translate({x}, {y})")
        if scale != 1.0:
            transform.append(f"scale({scale})")
        xml.set("transform", " ".join(transform))
        xml.raw_text(svg)
        xml.close("g")
        xml_string = xml.to_string()
        self.xml.raw_text(xml_string)

    def render(self) -> str:
        svg_end(self.xml)
        return self.xml.to_string()
