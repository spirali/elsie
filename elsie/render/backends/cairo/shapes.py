import cairocffi


def reflect(cp, anchor):
    """
    Reflect the point `cp` through the anchor.
    """
    vec = (cp[0] - anchor[0], cp[1] - anchor[1])
    neg = (-vec[0], -vec[1])
    return (anchor[0] + neg[0], anchor[1] + neg[1])


def draw_path(ctx: cairocffi.Context, commands):
    last_cubic_cp = None
    last_quadratic_cp = None
    for name, args in commands:
        location = ctx.get_current_point()
        if name == "M":
            last_cubic_cp = None
            last_quadratic_cp = None
            ctx.move_to(*args[0])
        elif name == "L":
            last_cubic_cp = None
            last_quadratic_cp = None
            ctx.line_to(*args[0])
        elif name == "C":
            last_cubic_cp = args[1]
            last_quadratic_cp = None
            ctx.curve_to(*args[0], *args[1], *args[2])
        elif name == "S":
            last_cubic_cp = reflect(last_cubic_cp or location, location)
            last_quadratic_cp = None
            ctx.curve_to(*last_cubic_cp, *args[0], *args[1])
        elif name == "Q":
            last_cubic_cp = None
            last_quadratic_cp = args[0]
            draw_quadratic_bezier(ctx, location, args[1], last_quadratic_cp)
        elif name == "T":
            last_cubic_cp = None
            last_quadratic_cp = reflect(last_quadratic_cp or location, location)
            draw_quadratic_bezier(ctx, location, args[0], last_quadratic_cp)


def draw_quadratic_bezier(ctx, p1, p2, cp):
    # http://caffeineowl.com/graphics/2d/vectorial/cubic2quad01.html
    c1 = ((2 * cp[0] + p1[0]) / 3, (2 * cp[1] + p1[1]) / 3)
    c2 = ((2 * cp[0] + p2[0]) / 3, (2 * cp[1] + p2[1]) / 3)
    ctx.curve_to(*c1, *c2, *p2)
