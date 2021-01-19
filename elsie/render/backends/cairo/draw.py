import cairocffi as cairo

from .utils import get_rgb_color


def rounded_rectangle(ctx: cairo.Context, x, y, w, h, rx, ry):
    # https://www.cairographics.org/cookbook/roundedrectangles/
    arc_to_bezier = 0.55228475
    if rx > w - rx:
        rx = w / 2
    if ry > h - ry:
        ry = h / 2

    c1 = arc_to_bezier * rx
    c2 = arc_to_bezier * ry

    ctx.new_path()
    ctx.move_to(x + rx, y)
    ctx.rel_line_to(w - 2 * rx, 0.0)
    ctx.rel_curve_to(c1, 0.0, rx, c2, rx, ry)
    ctx.rel_line_to(0, h - 2 * ry)
    ctx.rel_curve_to(0.0, c2, c1 - rx, ry, -rx, ry)
    ctx.rel_line_to(-w + 2 * rx, 0)
    ctx.rel_curve_to(-c1, 0, -rx, -c2, -rx, -ry)
    ctx.rel_line_to(0, -h + 2 * ry)
    ctx.rel_curve_to(0.0, -c2, rx - c1, -ry, rx, -ry)
    ctx.close_path()


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
