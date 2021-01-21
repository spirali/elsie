import io
import math

import cairocffi as cairo
import lxml.etree as et
import pangocairocffi
from PIL import Image

from ....text.textstyle import TextStyle
from ....utils.geom import Rect, find_centroid
from ..rcontext import RenderingContext
from .draw import (
    apply_viewbox,
    ctx_scope,
    fill_shape,
    fill_stroke_shape,
    rounded_rectangle,
    stroke_shape,
    transform,
)
from .shapes import draw_path
from .svg import render_svg
from .text import (
    build_layout,
    compute_subtext_extents,
    from_pango_units,
    get_extents,
    to_pango_units,
)
from .utils import normalize_svg

TARGET_DPI = 96
CAIRO_DPI = 72

# DPI scaling: 72 (cairo) vs 96 (Inkscape)
RESOLUTION_SCALE = CAIRO_DPI / TARGET_DPI


class CairoRenderingContext(RenderingContext):
    def __init__(
        self,
        width: int,
        height: int,
        filename: str = None,
        export_format: str = "pdf",
        viewbox=None,
        step=1,
        debug_boxes=False,
    ):
        super().__init__(step, debug_boxes)

        self.width = width
        self.height = height
        self.device_width = width * RESOLUTION_SCALE
        self.device_height = height * RESOLUTION_SCALE
        self.filename = filename

        if export_format == "pdf":
            self.surface = cairo.PDFSurface(
                self.filename, self.device_width, self.device_height
            )
            self.reference_ctx = self.ctx = cairo.Context(self.surface)
            self.ctx.scale(RESOLUTION_SCALE, RESOLUTION_SCALE)
            self.cairosvg_dpi = TARGET_DPI
        elif export_format == "png":
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
            self.ctx = cairo.Context(self.surface)
            self.ctx.set_source_rgba(0, 0, 0, 255)
            reference_surface = cairo.PDFSurface(
                None, self.device_width, self.device_height
            )
            self.reference_ctx = cairo.Context(reference_surface)
            self.reference_ctx.scale(RESOLUTION_SCALE, RESOLUTION_SCALE)
            self.cairosvg_dpi = CAIRO_DPI
        else:
            assert False

        self.line_scaling = 1.0
        if viewbox:
            self.line_scaling = apply_viewbox(self.ctx, width, height, viewbox)

        self.pctx = pangocairocffi.create_context(self.reference_ctx)

    def draw_rect(
        self,
        rect: Rect,
        rx=None,
        ry=None,
        rotation=None,
        **kwargs,
    ):
        if rx is None:
            rx = ry
        if ry is None:
            ry = rx

        with ctx_scope(self.ctx):
            transform(self.ctx, rect.mid_point, rotation)

            def draw():
                self.ctx.rectangle(rect.x, rect.y, rect.width, rect.height)

            def draw_rounded():
                rounded_rectangle(
                    self.ctx, rect.x, rect.y, rect.width, rect.height, rx, ry
                )

            draw_fn = draw_rounded if rx or ry else draw
            fill_stroke_shape(self.ctx, draw_fn, **kwargs)

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

        def draw():
            self.ctx.arc(center[0], center[1], dim_larger / 2.0, 0, 2 * math.pi)

        with ctx_scope(self.ctx):
            transform(
                self.ctx, center, rotation=rotation, scale_x=scale_x, scale_y=scale_y
            )
            if bg_color:
                fill_shape(self.ctx, draw, bg_color=bg_color)
            if color:
                draw()
        # Do not apply transform to stroke (https://www.cairographics.org/cookbook/ellipses/)
        if color:
            stroke_shape(self.ctx, lambda: ..., color=color, **kwargs)

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
        layout = build_layout(
            self.ctx, self.pctx, parsed_text, style, styles, RESOLUTION_SCALE
        )
        return get_extents(layout)

    def compute_subtext_extents(
        self, parsed_text, style: TextStyle, styles, id_index: int
    ) -> Rect:
        from ....text.textboxitem import text_x_in_rect

        layout = build_layout(
            self.ctx, self.pctx, parsed_text, style, styles, RESOLUTION_SCALE
        )
        extents = get_extents(layout)
        start_x = text_x_in_rect(Rect(x=0, width=extents.width), style)
        x, width = compute_subtext_extents(layout, parsed_text, id_index)
        return Rect(x=x - start_x, width=width)

    def draw_text(
        self,
        rect,
        x,
        y,
        parsed_text,
        style: TextStyle,
        styles,
        rotation=None,
        scale=None,
        **kwargs,
    ):
        # TODO: try basic Cairo text API
        with ctx_scope(self.ctx):
            layout = build_layout(
                self.reference_ctx,
                self.pctx,
                parsed_text,
                style,
                styles,
                resolution_scale=RESOLUTION_SCALE,
                spacing_scale=self.line_scaling,
                text_scale=scale,
            )
            layout.set_width(to_pango_units(rect.width))
            baseline = from_pango_units(layout.get_baseline())

            if rotation is not None:
                transform(self.ctx, rect.mid_point, rotation=rotation)
            self.ctx.move_to(rect.x, y - baseline)
            pangocairocffi.show_layout(self.ctx, layout)

    def draw_bitmap(self, x, y, width, height, data, rotation=None, **kwargs):
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

    def draw_svg(
        self,
        svg,
        x,
        y,
        width,
        height,
        rotation=None,
        **kwargs,
    ):
        root = et.fromstring(svg)
        normalized = normalize_svg(root)
        normalized_svg = et.tostring(normalized, encoding="utf8")
        render_svg(
            self.surface,
            svg=normalized_svg.decode(),
            x=x,
            y=y,
            width=width,
            height=height,
            rotation=rotation,
            dpi=self.cairosvg_dpi,
        )
