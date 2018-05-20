import math

from .geom import segment_delta, segment_resize


class Arrow:

    def __init__(self, size=10, angle=40, stroke_width=None, inner=None):
        self.size = size
        self.angle = angle * math.pi / 180
        self.stroke_width = stroke_width
        self.inner = inner

    def render(self, xml, p1, p2, color):
        dx, dy = segment_delta(p1, p2)
        a = math.atan2(dx, dy) + math.pi
        px, py = p2
        x1 = px + self.size * math.sin(a - self.angle)
        y1 = py + self.size * math.cos(a - self.angle)
        x2 = px + self.size * math.sin(a + self.angle)
        y2 = py + self.size * math.cos(a + self.angle)

        if self.stroke_width is not None:
            xml.element("polyline")
            xml.set("style", "fill:none;stroke:{};stroke-width: {}".format(
                color, self.stroke_width))
        else:
            xml.element("polygon")
            xml.set("style", "fill:{};stroke:none;".format(color))
        points = [(x1, y1), p2, (x2, y2)]

        if self.inner and not self.stroke_width:
            points.append(segment_resize(
                p1, p2, - self.inner * self.size * math.cos(self.angle)))
        xml.set("points", " ".join("{},{}".format(x, y) for x, y in points))
        xml.close()

    def move_end_point(self, p1, p2):
        if not self.stroke_width:
            shift = math.cos(self.angle) * self.size / 2
        else:
            shift = self.stroke_width / 2
        return segment_resize(p1, p2, -shift)
