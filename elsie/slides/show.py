import re


def replace_relative_steps(match, current_max):
    item = match.get("from")
    if item:
        if item in ("next", "last") and current_max is None:
            raise Exception(
                "You have to pass the current maximum fragment if you use relative values"
            )

        if item == "next":
            match["from"] = str(current_max + 1)
        if item == "last":
            match["from"] = str(current_max)


class ShowInfo:
    parser = re.compile(r"^(?P<from>\d+|next|last)(?:(?P<open>\+)|-(?P<end>\d+))?$")

    def __init__(self, steps=None, open_step=None, min_steps=None):
        if steps is None:
            if open_step is None:
                open_step = 1
            steps = ()
        self.steps = tuple(steps)
        self.open_step = open_step

        if min_steps:
            self._min_steps = min_steps
        else:
            self._min_steps = self.max_step()

    @classmethod
    def from_label(cls, label):
        if label is None or "**" not in label:
            return None
        show = label.split("**", 2)[1]
        return cls.parse(show)

    @classmethod
    def parse(cls, obj, current_max=None):
        if obj is None:
            return ShowInfo()
        if isinstance(obj, int):
            return ShowInfo((obj,))
        if isinstance(obj, str):
            steps = set()
            open_step = None
            intervals = [i.strip() for i in obj.split(",")]
            if not intervals:
                raise Exception("Invalid format of 'show' string: {!r}".format(obj))

            for interval in intervals:
                m = cls.parser.match(interval)
                if m is None:
                    raise Exception("Invalid format of 'show' string: {!r}".format(obj))
                m = m.groupdict()
                replace_relative_steps(m, current_max)
                if m["open"] is not None:
                    if open_step is not None:
                        raise Exception(
                            "Multiple open steps ({}, {}) in input {!r}".format(
                                open_step, m["open"], obj
                            )
                        )
                    open_step = int(m["from"])
                    continue

                start = int(m["from"])
                end = start
                if m["end"] is not None:
                    end = int(m["end"])
                assert start <= end
                steps.update(range(start, end + 1))
            return ShowInfo(sorted(steps), open_step)
        else:
            raise Exception("Invalid show argument")

    def min_steps(self):
        return self._min_steps

    def max_step(self):
        return max(max(self.steps, default=1), self.open_step if self.open_step else 1)

    def ensure_steps(self, steps):
        min_steps = max(self._min_steps, steps)
        return ShowInfo(self.steps, self.open_step, min_steps)

    def is_visible(self, step):
        return step in self.steps or (
            self.open_step is not None and self.open_step <= step
        )

    def __repr__(self):
        return "<ShowInfo steps={} open_step={} min={}>".format(
            self.steps, self.open_step, self._min_steps
        )
