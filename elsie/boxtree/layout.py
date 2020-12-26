from ..utils.geom import Rect
from .lazy import LazyPoint, LazyValue
from .value import PosValue, SizeValue


def _set_padding(a, b, c):
    if a is not None:
        return a
    if b is not None:
        return b
    return c or 0


class Layout:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        p_left=0,
        p_right=0,
        p_top=0,
        p_bottom=0,
        horizontal=False,
    ):

        if x is not None:
            self._x = PosValue.parse(x)
        else:
            self._x = None

        if y is not None:
            self._y = PosValue.parse(y)
        else:
            self._y = None

        self.width_definition = width
        self.height_definition = height
        self._width = SizeValue.parse(width or 0)
        self._height = SizeValue.parse(height or 0)

        self.p_left = p_left
        self.p_right = p_right
        self.p_top = p_top
        self.p_bottom = p_bottom

        self.horizontal = horizontal

        self.callbacks = None
        self.children = []
        self.rect = None

    def add(
        self,
        x=None,
        y=None,
        width=None,
        height=None,
        p_left=None,  # padding left
        p_right=None,  # padding right
        p_top=None,  # padding top
        p_bottom=None,  # padding bottom
        p_x=None,  # horizontal padding (sets p_left & p_right)
        p_y=None,  # vertical padding (sets p_top & p_bottom)
        padding=None,  # sets the same padding to all directions
        horizontal=False,
        prepend=False,
    ):

        p_left = _set_padding(p_left, p_x, padding)
        p_right = _set_padding(p_right, p_x, padding)
        p_top = _set_padding(p_top, p_y, padding)
        p_bottom = _set_padding(p_bottom, p_y, padding)

        layout = Layout(
            x=x,
            y=y,
            width=width,
            height=height,
            p_left=p_left,
            p_right=p_right,
            p_top=p_top,
            p_bottom=p_bottom,
            horizontal=horizontal,
        )

        if prepend:
            self.children.insert(0, layout)
        else:
            self.children.append(layout)

        return layout

    def add_callback(self, callback):
        if self.callbacks is None:
            self.callbacks = []
        self.callbacks.append(callback)

    def is_managed(self, horizontal):
        if horizontal:
            return self._x is None
        else:
            return self._y is None

    def managed_children(self):
        return [child for child in self.children if child.is_managed(self.horizontal)]

    def set_rect(self, rect):
        # assert self.rect is None
        rect = rect.shrink(self.p_left, self.p_right, self.p_top, self.p_bottom)
        self.rect = rect

        if self.callbacks:
            for callback in self.callbacks:
                callback(rect)

        if not self.horizontal:
            axis = 1
            rect_size = rect.height
            rect_start = rect.y
        else:
            axis = 0
            rect_size = rect.width
            rect_start = rect.x

        fills = 0
        free = rect_size

        for child in self.managed_children():
            rq = child.compute_size_request()[axis]
            if rq.fill:
                fills += rq.fill
            elif rq.ratio:
                free -= max(rq.min_size, rq.ratio * rect_size)
            else:
                free -= rq.min_size

        if fills:
            fill_unit = free / fills
            free = 0
        else:
            fill_unit = 0

        dd = rect_start + free / 2  # dynamic dimension

        for child in self.children:
            w, h = child.compute_size_request()
            if not self.horizontal:
                w = w.compute(rect.width, None)
                h = h.compute(rect.height, fill_unit)
                if child._x is not None:
                    x = child._x.compute(rect.x, rect.width, w)
                else:
                    x = rect.x + (rect.width - w) / 2
                if child._y is None:
                    y = dd
                    dd += h
                else:
                    y = child._y.compute(rect.y, rect.height, h)
            else:
                w = w.compute(rect.width, fill_unit)
                h = h.compute(rect.height, None)
                if child._y is not None:
                    y = child._y.compute(rect.y, rect.width, h)
                else:
                    y = rect.y + (rect.height - h) / 2
                if child._x is None:
                    x = dd
                    dd += w
                else:
                    x = child._x.compute(rect.x, rect.width, w)
            child.set_rect(Rect(x, y, w, h))

    def compute_size_request(self):
        minx, miny = self.min_children_size()
        minx += self.p_left + self.p_right
        miny += self.p_top + self.p_bottom
        return self._width.ensure(minx), self._height.ensure(miny)

    def min_children_size(self):
        managed_children = self.managed_children()
        if not managed_children:
            return 0, 0
        rqs = [c.compute_size_request() for c in managed_children]
        if not self.horizontal:
            return (
                max(rq[0].min_size for rq in rqs),
                sum(rq[1].min_size for rq in rqs),
            )
        else:
            return (
                sum(rq[0].min_size for rq in rqs),
                max(rq[1].min_size for rq in rqs),
            )

    def ensure_width(self, width):
        self._width = self._width.ensure(width + self.p_left + self.p_right)

    def ensure_height(self, height):
        self._height = self._height.ensure(height + self.p_top + self.p_bottom)

    def x(self, value):
        """Creates position on x-axis relative to the box."""
        value = PosValue.parse(value)
        return LazyValue(lambda: value.compute(self.rect.x, self.rect.width, 0))

    def y(self, value):
        """Creates position on y-axis relative to the box."""
        value = PosValue.parse(value)
        return LazyValue(lambda: value.compute(self.rect.y, self.rect.height, 0))

    def point(self, x, y):
        """Creates a point relative to the box."""
        return LazyPoint(self.x(x), self.y(y))

    def set_image_size_request(self, image_width, image_height):
        if self.width_definition is None and self.height_definition is None:
            self.ensure_width(image_width)
            self.ensure_height(image_height)
            return
        minx, miny = self.min_children_size()
        size_x = max(self._width.min_size, minx)
        size_y = max(self._height.min_size, miny)
        self.ensure_width(size_y * image_width / image_height)
        self.ensure_height(size_x * image_height / image_width)
