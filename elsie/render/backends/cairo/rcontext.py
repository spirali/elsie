import contextlib
import io
import math
import os
import tempfile
from typing import Tuple

import cairocffi as cairo
import pangocairocffi
from PIL import Image

from ....text.textstyle import TextStyle
from ....utils.geom import Rect, find_centroid
from ..rcontext import RenderingContext
from .shapes import draw_path
from .text import build_layout, get_extents
from .utils import get_rgb_color

# DPI scaling: 72 (cairo) vs 96 (Inkscape)
RESOLUTION_SCALE = 0.75

# TODO: SVG/ORA images


@contextlib.contextmanager
def ctx_scope(ctx: cairo.Context):
    try:
        ctx.save()
        yield ctx
    finally:
        ctx.restore()


def transform(
    ctx: cairo.Context,
    point: Tuple[float, float],
    rotation: float = None,
    scale_x=1.0,
    scale_y=1.0,
):
    ctx.translate(point[0], point[1])
    if rotation is not None:
        ctx.rotate(math.radians(rotation))
    if scale_x != 1.0 or scale_y != 1.0:
        ctx.scale(sx=scale_x, sy=scale_y)
    ctx.translate(-point[0], -point[1])


def fill_shape(ctx, callback, bg_color):
    ctx.set_source_rgb(*get_rgb_color(bg_color))
    callback()
    ctx.fill()


def stroke_shape(ctx, callback, color, stroke_width=None, stroke_dasharray=None):
    ctx.set_source_rgb(*get_rgb_color(color))
    stroke_width = stroke_width or 1
    ctx.set_line_width(stroke_width)
    if stroke_dasharray:
        ctx.set_dash([float(v) for v in stroke_dasharray.split()])
    callback()
    ctx.stroke()


def fill_stroke_shape(
    ctx, callback, color=None, bg_color=None, stroke_width=None, stroke_dasharray=None
):
    if bg_color:
        fill_shape(ctx, callback, bg_color=bg_color)
    if color:
        stroke_shape(
            ctx,
            callback,
            color=color,
            stroke_width=stroke_width,
            stroke_dasharray=stroke_dasharray,
        )


def apply_viewbox(ctx: cairo.Context, width: float, height: float, viewbox):
    viewbox_width = viewbox[2]
    viewbox_height = viewbox[3]
    scale = min(width / viewbox_width, height / viewbox_height)
    ctx.translate(-viewbox[0] * scale, -viewbox[1] * scale)
    ctx.scale(scale, scale)
    translate_x = (width / scale - viewbox_width) / 2
    translate_y = (height / scale - viewbox_height) / 2
    ctx.translate(translate_x, translate_y)


class CairoRenderingContext(RenderingContext):
    def __init__(
        self, width: int, height: int, viewbox=None, step=1, debug_boxes=False
    ):
        super().__init__(step, debug_boxes)

        # TODO: PDF path
        device_width = width * RESOLUTION_SCALE
        device_height = height * RESOLUTION_SCALE
        temp_path = os.path.join(
            tempfile.gettempdir(), next(tempfile._get_candidate_names())
        )
        self.filename = f"{temp_path}.pdf"
        self.surface = cairo.PDFSurface(self.filename, device_width, device_height)
        self.ctx = cairo.Context(self.surface)
        self.ctx.scale(RESOLUTION_SCALE, RESOLUTION_SCALE)
        if viewbox:
            apply_viewbox(self.ctx, width, height, viewbox)

    def draw_rect(
        self,
        rect: Rect,
        rx=None,
        ry=None,
        rotation=None,
        **kwargs,
    ):
        with ctx_scope(self.ctx):
            transform(self.ctx, rect.mid_point, rotation)

            def draw():
                self.ctx.rectangle(rect.x, rect.y, rect.width, rect.height)

            fill_stroke_shape(self.ctx, draw, **kwargs)

    def draw_ellipse(
        self, rect: Rect, rotation=None, color=None, bg_color=None, **kwargs
    ):
        dim_larger = rect.width
        dim_smaller = rect.height
        if dim_larger < dim_smaller:
            dim_larger, dim_smaller = dim_smaller, dim_larger
        scale_x = 1.0 if dim_larger == rect.width else dim_smaller / dim_larger
        scale_y = 1.0 if dim_larger == rect.height else dim_smaller / dim_larger
        center = rect.mid_point

        with ctx_scope(self.ctx):
            transform(
                self.ctx, center, rotation=rotation, scale_x=scale_x, scale_y=scale_y
            )

            def draw():
                self.ctx.arc(center[0], center[1], dim_larger / 2.0, 0, 2 * math.pi)

            fill_stroke_shape(self.ctx, draw, color=color, bg_color=bg_color)

    def draw_polygon(self, points, rotation=None, **kwargs):
        with ctx_scope(self.ctx):
            transform(self.ctx, find_centroid(points), rotation=rotation)

            def draw():
                self.ctx.move_to(*points[0])
                for p in points[1:] + [points[0]]:
                    self.ctx.line_to(*p)

            fill_stroke_shape(self.ctx, draw, **kwargs)

    def draw_polyline(self, points, **kwargs):
        with ctx_scope(self.ctx):

            def draw():
                self.ctx.move_to(*points[0])
                for p in points[1:]:
                    self.ctx.line_to(*p)

            stroke_shape(self.ctx, draw, **kwargs)

    def draw_path(self, commands, **kwargs):
        with ctx_scope(self.ctx):

            def draw():
                draw_path(self.ctx, commands)

            fill_stroke_shape(self.ctx, draw, **kwargs)

    def compute_text_extents(self, parsed_text, style: TextStyle, styles) -> Rect:
        layout = build_layout(self.ctx, parsed_text, style, styles)
        return get_extents(layout)

    def draw_text(
        self, rect, x, y, parsed_text, style: TextStyle, styles, *args, **kwargs
    ):
        # TODO: move to correct location
        with ctx_scope(self.ctx):
            layout = build_layout(self.ctx, parsed_text, style, styles)
            extents = get_extents(layout)
            self.ctx.move_to(rect.x - extents.x, rect.y - extents.y)
            pangocairocffi.show_layout(self.ctx, layout)

    def draw_bitmap(self, x, y, width, height, mime, data, rotation=None):
        assert isinstance(data, bytes)
        image = Image.open(io.BytesIO(data))
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        img_width, img_height = image.width, image.height

        data = bytearray(image.tobytes("raw", "BGRa"))
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, width=img_width, height=img_height, data=data
        )
        surface.set_device_scale(img_width / width, img_height / height)

        center = (x + width / 2, y + height / 2)
        with ctx_scope(self.ctx):
            transform(self.ctx, center, rotation=rotation)
            self.ctx.set_source_surface(surface, x, y)
            self.ctx.move_to(x, y)
            self.ctx.paint()

    def render(self) -> str:
        self.surface.finish()
        return self.filename
