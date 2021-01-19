import cairocffi as cairo


# https://www.cairographics.org/cookbook/roundedrectangles/
def rounded_rectangle(ctx: cairo.Context, x, y, w, h, rx, ry):
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
