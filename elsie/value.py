import re
from copy import copy

from .lazy import LazyValue


class SizeValue:

    parser = re.compile(
        r"^(?P<min_size>\d+)$|^(?P<ratio>\d+)%$|^(?P<fill_1>fill)$|^fill[(](?P<fill>\d+)[)]+$")  # noqa

    def __init__(self, min_size=0, ratio=None, fill=0, lazy_value=None):
        self.min_size = min_size
        self.ratio = ratio
        self.fill = fill
        self.lazy_value = lazy_value

    @classmethod
    def parse(cls, obj):
        if isinstance(obj, int) or isinstance(obj, float):
            return SizeValue(min_size=obj)

        if isinstance(obj, LazyValue):
            return SizeValue(lazy_value=obj)

        if isinstance(obj, int) or isinstance(obj, float):
            return SizeValue(min_size=obj)

        if not isinstance(obj, str) or not str:
            raise Exception("{!r} cannot be used as as size value", obj)

        m = cls.parser.match(obj)
        if m is None:
            raise Exception("Invalid format of size string")
        m = m.groupdict()

        if m["min_size"] is not None:
            return SizeValue(min_size=float(m["min_size"]))

        if m["ratio"] is not None:
            ratio = float(m["ratio"]) / 100
            return SizeValue(ratio=ratio)

        if m["fill_1"] is not None:
            return SizeValue(fill=1)

        if m["fill"] is not None:
            return SizeValue(fill=int(m["fill"]))

        raise Exception("Invalid string as size value")

    def ensure(self, size):
        if size <= self.min_size:
            return self
        s = copy(self)
        s.min_size = size
        return s

    def compute(self, full_size, fill_unit):
        if self.lazy_value:
            return self.lazy_value.eval()
        if self.fill:
            if fill_unit is None:
                return full_size
            else:
                return fill_unit * self.fill
        if self.ratio:
            return max(full_size * self.ratio, self.min_size)
        return self.min_size

    def __repr__(self):
        return "<SizeValue min_size={} ratio={} fill={} lazy_value={}>".format(
            self.min_size, self.ratio, self.fill, self.lazy_value is not None)


class PosValue:

    parser = re.compile(
        r"^(?P<fix_pos>^\d+$)|^(?P<ratio>^\d+)%$|^\[(?P<align>\d+)%\]$")

    def __init__(self, fix_pos=None, ratio=None, align=None, lazy_value=None):
        self.fix_pos = fix_pos
        self.ratio = ratio
        self.align = align
        self.lazy_value = lazy_value

    @classmethod
    def parse(cls, obj):
        if obj is None:
            return PosValue()

        if isinstance(obj, int) or isinstance(obj, float):
            return PosValue(fix_pos=obj)

        if isinstance(obj, LazyValue):
            return PosValue(lazy_value=obj)

        if not isinstance(obj, str) or not str:
            raise Exception("{!r} cannot be used as as size value", obj)

        m = cls.parser.match(obj)
        if m is None:
            raise Exception("Invalid format of position string")
        m = m.groupdict()

        if m["fix_pos"] is not None:
            return PosValue(fix_pos=float(m["fix_pos"]))

        if m["ratio"] is not None:
            ratio = float(m["ratio"]) / 100
            return PosValue(ratio=ratio)

        if m["align"] is not None:
            align = float(m["align"]) / 100
            return PosValue(align=align)

        raise Exception("Invalid string as position request")

    def compute(self, origin, full_size, self_size):
        if self.lazy_value:
            return self.lazy_value.eval()
        if self.ratio is not None:
            return origin + full_size * self.ratio
        if self.align is not None:
            return origin + (full_size - self_size) * self.align
        if self.fix_pos is not None:
            return origin + self.fix_pos
        raise Exception("Invalid pos")
