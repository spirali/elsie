from typing import List

from ..boxtree.box import Box


class ListBuilder:
    def __init__(
        self,
        parent: Box,
        label_render_fn,
        default_indent,
        *,
        label_padding: int,
        level=None,
        start=1,
        total_indent=0,
        **box_args
    ):
        self.parent = parent
        self.default_indent = default_indent
        self.label_padding = label_padding
        self.box_args = dict(box_args)
        if "show" not in self.box_args:
            self.box_args["show"] = "last+"

        self.level = [] if level is None else list(level)
        self.level.append(start - 1)
        self.total_indent = total_indent
        self.label_render_fn = label_render_fn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def ul(self, indent=None, label_render_fn=None, **box_args):
        indent = indent if indent is not None else self.default_indent
        box, total_indent = self._create_box(self.parent, indent=indent, **box_args)
        return ListBuilder(
            box,
            label_render_fn or default_ul_render_fn,
            indent,
            level=self.level,
            total_indent=total_indent,
            label_padding=self.label_padding,
            **self.box_args
        )

    def ol(self, level=None, *, start=1, indent=None, label_render_fn=None, **box_args):
        assert start >= 1

        indent = indent if indent is not None else self.default_indent
        box, total_indent = self._create_box(self.parent, indent=indent, **box_args)
        level = level if level is not None else self.level
        return ListBuilder(
            box,
            label_render_fn or default_ol_render_fn,
            indent,
            level=level,
            total_indent=total_indent,
            start=start,
            label_padding=self.label_padding,
            **self.box_args
        )

    def item(self, label: str = None, label_padding: int = None, **box_args):
        self.level[-1] += 1

        label = label if label is not None else self.label_render_fn(self.level)
        label_padding = (
            label_padding if label_padding is not None else self.label_padding
        )

        args = dict(self.box_args)
        args.update(box_args)
        box_args["horizontal"] = True
        box, _ = self._create_box(self.parent, indent=0, **box_args)

        if label is not None:
            box.box().text(label)
        return box.box(p_left=label_padding, width="fill")

    def _create_box(self, parent: Box, indent=None, **box_args):
        new_indent = self.default_indent if indent is None else indent
        total_indent = self.total_indent + new_indent

        args = dict(self.box_args)
        args.update(box_args)
        return parent.box(x="[0%]", p_left=total_indent, **args), total_indent


def unordered_list(
    parent: Box, indent=10, label_padding=25, label_render_fn=None, **default_box_args
) -> ListBuilder:
    return ListBuilder(
        parent,
        default_indent=indent,
        label_padding=label_padding,
        label_render_fn=label_render_fn or default_ul_render_fn,
        **default_box_args
    )


def ordered_list(
    parent: Box,
    indent=10,
    start=1,
    label_padding=25,
    label_render_fn=None,
    **default_box_args
) -> ListBuilder:
    return ListBuilder(
        parent,
        default_indent=indent,
        label_padding=label_padding,
        start=start,
        label_render_fn=label_render_fn or default_ol_render_fn,
        **default_box_args
    )


def arabic_digit_render_fn(level: List[int]) -> str:
    return ".".join(str(item) for item in level) + "."


def bullet_point_render_fn(level: List[int]) -> str:
    return "•"


default_ul_render_fn = bullet_point_render_fn
default_ol_render_fn = arabic_digit_render_fn
