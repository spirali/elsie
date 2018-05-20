import math


class Rect:

    def __init__(self,
                 x=None,
                 y=None,
                 width=None,
                 height=None,
                 position=None, size=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if position:
            self.x, self.y = position

        if size:
            self.width, self.height = size

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def mid_x(self):
        return self.x + self.width / 2

    @property
    def mid_y(self):
        return self.y + self.height / 2

    @property
    def x2(self):
        return self.x + self.width

    @property
    def y2(self):
        return self.y + self.height

    def shrink(self, left=0, right=0, top=0, bottom=0):
        return Rect(self.x + left,
                    self.y + top,
                    self.width - left - right,
                    self.height - top - bottom)

    def __eq__(self, other):
        if not isinstance(other, Rect):
            return False
        return self.x == other.x and \
            self.y == other.y and \
            self.width == other.width and \
            self.height == other.height

    def __repr__(self):
        return "<Rect x={0.x} y={0.y} w={0.width} h={0.height}>".format(self)


def segment_delta(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])


def segment_len(p1, p2):
    dx, dy = segment_delta(p1, p2)
    return math.sqrt(dx * dx + dy * dy)


def segment_resize(p1, p2, len_change):
    dx, dy = segment_delta(p1, p2)
    ln = segment_len(p1, p2)
    t = 1 + (len_change / ln)
    return (p1[0] + dx * t, p1[1] + dy * t)
