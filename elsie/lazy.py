
class LazyValue:

    def __init__(self, fn):
        self.fn = fn

    def map(self, fn):
        return LazyValue(lambda: fn(self.eval()))

    def add(self, value):
        return self.map(lambda v: v + value)

    def eval(self):
        return self.fn()


class LazyPoint:

    def __init__(self, x, y):
        assert isinstance(x, LazyValue)
        assert isinstance(y, LazyValue)
        self.x = x
        self.y = y

    def add(self, x, y):
        return LazyPoint(self.x.map(lambda v: v + x),
                         self.y.map(lambda v: v + y))

    def eval(self):
        return (self.x.eval(), self.y.eval())


def unpack_point(obj):
    if isinstance(obj, LazyPoint):
        return (obj.x, obj.y)
    if (isinstance(obj, tuple) or isinstance(obj, list)) and len(obj) == 2:
        return tuple(obj)
    raise Exception("Invalid point: {:r}".format(obj))


def eval_value(obj):
    if isinstance(obj, LazyValue):
        return obj.eval()
    else:
        return obj
