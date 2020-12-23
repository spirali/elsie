from typing import Tuple


class LazyValue:
    """
    Value that will be resolved after layout is computed.
    """

    def __init__(self, fn):
        self.fn = fn

    def map(self, fn) -> "LazyValue":
        """Lazily maps the result of this value."""
        return LazyValue(lambda: fn(self.eval()))

    def add(self, value: float) -> "LazyValue":
        """Lazily adds the given number to this value."""
        return self.map(lambda v: v + value)

    def eval(self):
        """Evaluates the actual value."""
        return self.fn()


class LazyPoint:
    """
    2D point that will be resolved after layout is computed.
    """

    def __init__(self, x, y):
        assert isinstance(x, LazyValue)
        assert isinstance(y, LazyValue)
        self.x = x
        self.y = y

    def add(self, x: float, y: float) -> "LazyPoint":
        """
        Creates a new point moved by the given (x, y) offset.

        Parameters
        ----------
        x: float
            x offset
        y: float
            y offset
        """
        return LazyPoint(self.x.map(lambda v: v + x), self.y.map(lambda v: v + y))

    def eval(self) -> Tuple[float, float]:
        """Evaluates the actual point."""
        return self.x.eval(), self.y.eval()


def unpack_point(obj, box):
    if isinstance(obj, LazyPoint):
        return obj.x, obj.y
    if (isinstance(obj, tuple) or isinstance(obj, list)) and len(obj) == 2:
        return box.x(obj[0]), box.y(obj[1])
    raise Exception("Invalid point: {!r}".format(obj))


def eval_value(obj):
    if isinstance(obj, LazyValue):
        return obj.eval()
    else:
        return obj


def eval_pair(pair):
    return eval_value(pair[0]), eval_value(pair[1])
