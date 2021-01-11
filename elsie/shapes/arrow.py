import math

from ..render.backends.rcontext import RenderingContext
from ..utils.geom import segment_delta, segment_resize


class Arrow:
    """
    Represents an SVG arrow head.

    Can be attached to the start or end points of lines.

    Attributes
    ----------
    size : float
        Size of the arrow head in pixels.
    angle : float
        Angle of the arrow head.
    stroke_width : float
        Width of the arrow head edge.
    inner : float
        Shape of the arrow head.
        < 1.0 -> Sharper arrow.
        = 1.0 -> Normal arrow.
        > 1.0 -> Diamond shape arrow.
    """

    def __init__(self, size=10, angle=40, stroke_width=None, inner=None):
        self.size = size
        self.angle = angle * math.pi / 180
        self.stroke_width = stroke_width
        self.inner = inner

    def render(self, ctx: RenderingContext, p1, p2, color):
        dx, dy = segment_delta(p1, p2)
        a = math.atan2(dx, dy) + math.pi
        px, py = p2
        x1 = px + self.size * math.sin(a - self.angle)
        y1 = py + self.size * math.cos(a - self.angle)
        x2 = px + self.size * math.sin(a + self.angle)
        y2 = py + self.size * math.cos(a + self.angle)

        points = [(x1, y1), p2, (x2, y2)]

        if self.inner and not self.stroke_width:
            points.append(
                segment_resize(p1, p2, -self.inner * self.size * math.cos(self.angle))
            )

        if self.stroke_width is not None:
            ctx.draw_polyline(points, color=color, stroke_width=self.stroke_width)
        else:
            ctx.draw_polygon(points, bg_color=color)

    def move_end_point(self, p1, p2):
        if not self.stroke_width:
            shift = math.cos(self.angle) * self.size / 2
        else:
            shift = self.stroke_width / 2
        return segment_resize(p1, p2, -shift)
