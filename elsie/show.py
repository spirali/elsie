import re


class ShowInfo:

    parser = re.compile(
        r"^(?P<exact>\d+)$|^(?P<from>\d+)\+$|^(?P<begin>^\d+)\-(?P<end>\d+)$")

    def __init__(self, begin=1, end=None, min_steps=None):
        assert begin >= 1
        assert end is None or end >= 1
        self.begin = begin
        self.end = end
        if min_steps:
            self._min_steps = min_steps
        else:
            self._min_steps = max(begin, end if end else 1)

    @classmethod
    def parse(cls, obj):
        if obj is None:
            return ShowInfo()
        if isinstance(obj, int):
            return ShowInfo(obj, obj)
        if isinstance(obj, str):
            m = cls.parser.match(obj)
            if m is None:
                raise Exception("Invalid format of 'show' string: {!r}"
                                .format(obj))
            m = m.groupdict()

            if m["exact"] is not None:
                exact = int(m["exact"])
                return ShowInfo(exact, exact)

            if m["from"] is not None:
                return ShowInfo(int(m["from"]))
            return ShowInfo(int(m["begin"]), int(m["end"]))
        else:
            raise Exception("Invalid show argument")

    def min_steps(self):
        return self._min_steps

    def ensure_steps(self, steps):
        min_steps = max(self._min_steps, steps)
        return ShowInfo(self.begin, self.end, min_steps)

    def is_visible(self, step):
        return self.begin <= step and (self.end is None or step <= self.end)

    def __repr__(self):
        return "<ShowInfo begin={} end={} min={}>".format(
            self.begin, self.end, self._min_steps)
