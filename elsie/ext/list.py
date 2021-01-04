from typing import Callable, List, Union

from ..boxtree.box import Box
from ..text.textstyle import TextStyle

LabelFnType = Callable[[Box, List[int]], None]
LabelType = Union[str, LabelFnType]


class ListBuilder:
    """
    This holds information about the counters and nesting level of a (sub)list.

    Do not create instances of this class directly, instead use the `unordered_list` and
    `ordered_list` functions.
    """

    def __init__(
        self,
        parent: Box,
        label: LabelType,
        default_indent: float,
        label_padding: float,
        level: List[int] = None,
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
        self.label = label

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def ul(
        self, indent: float = None, label: LabelType = None, **box_args
    ) -> "ListBuilder":
        """
        Create a new unordered sublist.

        Parameters
        ----------
        indent: float
            The sublist will be indented by the specified amount of pixels from the left.
            If `None`, the indent will be taken from the default indent of the current list.
        label: LabelType
            Either a string or a function.
            If `label` is a string, it will be used as a label for each list item in the sublist.
            If `label` is a function, it will be called for each label. It will be passed a Box and
            a list of counter values for each nesting level and it should fill the box with the
            contents of the label.
        box_args: kwargs
            Additional arguments that will be passed to the box of each list item in the sublist.
            These arguments will be combined with the `box_args` of the current list.
        """
        return self._create_sublist(
            indent=indent, label=label, default_label=default_ul_label, **box_args
        )

    def ol(
        self,
        level: List[int] = None,
        *,
        start=1,
        indent: float = None,
        label: LabelType = None,
        **box_args
    ):
        """
        Create a new ordered sublist.

        Parameters
        ----------
        level: List[int]
            Override the parent counter values of the sublist.
            For example:
                lst.ol(level=(1, 3), start=5)
            would be rendered as "1.3.5" with the default label renderer.
        start: int
            The counter value at which will the new sublist start.
        indent: float
            The sublist will be indented by the specified amount of pixels from the left.
            If `None`, the indent will be taken from the default indent of the current list.
        label: LabelType
            Either a string or a function.
            If `label` is a string, it will be used as a label for each list item in the sublist.
            If `label` is a function, it will be called for each label. It will be passed a Box and
            a list of counter values for each nesting level and it should fill the box with the
            contents of the label.
        box_args: kwargs
            Additional arguments that will be passed to the box of each list item in the sublist.
            These arguments will be combined with the `box_args` of the current list.
        """
        return self._create_sublist(
            start=start,
            level=level,
            indent=indent,
            label=label,
            default_label=default_ol_label,
            **box_args
        )

    def item(self, label: LabelType = None, label_padding: float = None, **box_args):
        """
        Create a new item in the list.

        Parameters
        ----------
        label: LabelType
            Either a string or a function.
            If `label` is a string, it will be used as a label for each list item in the sublist.
            If `label` is a function, it will be called for each label. It will be passed a Box and
            a list of counter values for each nesting level and it should fill the box with the
            contents of the label.
        label_padding: float
            Horizontal gap between the label and the item.
            If `None`, the padding will be taken from `label_padding` of the current list.
        box_args: kwargs
            Additional arguments that will be passed to the box of the list item.
            These arguments will be combined with the `box_args` of the current list.
        """
        self.level[-1] += 1

        label_padding = (
            label_padding if label_padding is not None else self.label_padding
        )

        args = dict(self.box_args)
        args.update(box_args)
        box_args["horizontal"] = True
        box, _ = self._create_box(self.parent, indent=0, **box_args)
        box.update_style("default", TextStyle(align="left"))

        actual_label = label if label is not None else self.label
        if actual_label is not None:
            label_box = box.box(y="[0%]")
            if callable(actual_label):
                actual_label(label_box, self.level)
            elif isinstance(actual_label, str):
                label_box.text(actual_label)
            else:
                raise Exception("Label must be either a string or a function")
        return box.box(p_left=label_padding, width="fill")

    def _create_sublist(
        self, default_label, start=None, indent=None, label=None, level=None, **box_args
    ):
        start = start if start is not None else 1
        assert start >= 1
        indent = indent if indent is not None else self.default_indent
        level = level if level is not None else self.level

        box, total_indent = self._create_box(self.parent, indent=indent, **box_args)
        args = dict(self.box_args)
        args.update(box_args)

        return ListBuilder(
            box,
            label or default_label,
            indent,
            level=level,
            total_indent=total_indent,
            start=start,
            label_padding=self.label_padding,
            **args
        )

    def _create_box(self, parent: Box, indent=None, **box_args):
        new_indent = self.default_indent if indent is None else indent
        total_indent = self.total_indent + new_indent

        args = dict(self.box_args)
        args.update(box_args)
        return parent.box(x="[0%]", p_left=total_indent, **args), total_indent


def unordered_list(
    parent: Box,
    indent: float = 10,
    label_padding: float = 25,
    label: LabelType = None,
    **default_box_args
) -> ListBuilder:
    """
    Create a new unordered list.

    Parameters
    ----------
    parent: Box
        Box that will contain the list.
    indent: float
        Default indentation used when creating sublists.
    label_padding: float
        Default horizontal gap between each label and its corresponding item.
    label: LabelType
        Either a string or a function.
        If `label` is a string, it will be used as a label for each list item in the list.
        If `label` is a function, it will be called for each label. It will be passed a Box and
        a list of counter values for each nesting level and it should fill the box with the
        contents of the label.
    default_box_args: kwargs
        Additional arguments that will be passed to the box of each list item in the list.
    """
    return ListBuilder(
        parent.sbox(),
        label=label or default_ul_label,
        default_indent=indent,
        label_padding=label_padding,
        **default_box_args
    )


def ordered_list(
    parent: Box,
    indent: float = 10,
    start: int = 1,
    label_padding: float = 25,
    label: LabelType = None,
    **default_box_args
) -> ListBuilder:
    """
    Create a new ordered list.

    Parameters
    ----------
    parent: Box
        Box that will contain the list.
    indent: float
        Default indentation used when creating sublists.
    start: int
        The counter value at which will the list start.
    label_padding: float
        Default horizontal gap between each label and its corresponding item.
    label: LabelType
        Either a string or a function.
        If `label` is a string, it will be used as a label for each list item in the list.
        If `label` is a function, it will be called for each label. It will be passed a Box and
        a list of counter values for each nesting level and it should fill the box with the
        contents of the label.
    default_box_args: kwargs
        Additional arguments that will be passed to the box of each list item in the list.
    """
    return ListBuilder(
        parent.sbox(),
        label=label or default_ol_label,
        default_indent=indent,
        label_padding=label_padding,
        start=start,
        **default_box_args
    )


def arabic_digit_render_fn(box: Box, level: List[int]):
    label = ".".join(str(item) for item in level) + "."
    box.text(label)


default_ul_label = "•"
default_ol_label = arabic_digit_render_fn
