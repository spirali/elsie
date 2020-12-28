from contextlib import contextmanager
from typing import Optional

from ..boxtree.box import Box


class ListBuilder:
    """
    This class serves as a helper for creating simple unordered bullet lists.
    It can draw list items in a column with a specified bullet point and it also handles
    indentation of sublists.

    Individual list items are created with the `item` method.
    Parameters passed to the `item` method override the default list item attributes from the
    constructor.

    Example:
        lst = ListBuilder(slide.box())
        lst.item().text("Item 1")
        lst.item(level=1).text("Nested item")
        lst.item().text("Item 2")
    """

    def __init__(
        self,
        parent: Box,
        *,
        bullet: Optional[str] = "•",
        bullet_width=25,
        level_indent=25,
        show="last+",
        **box_args
    ):
        """
        Parameters
        ----------
        parent: Box
            Box parent of the list.
        bullet: str
            Default character for the bullet point. If you do not want to draw bullet points,
            pass `None`.
        bullet_width: float
            Width of the bullet box in pixels.
        level_indent: float
            Horizontal gap before each indentation level.
        show: str
            Default fragment selector for a list item.
        box_args: kwargs
            Additional parameters passed to each list item box.
        """
        self.parent = parent
        self.bullet = bullet
        self.bullet_width = bullet_width
        self.level_indent = level_indent
        self.show = show
        self.level = 0
        self.box_args = box_args

    def item(
        self, level: int = None, show: str = None, bullet: str = None, **box_args
    ) -> Box:
        """
        Create a new list item.

        If the indentation level is not specified, the current indentation level of the ListBuilder
        will be used.

        Parameters
        ----------
        level: int
            Indentation level of the item.
        show: str
            Fragment selector of the item.
        bullet: str
            Bullet character of the item.
        box_args: kwargs
            Additional parameters pass to the box of the item.
        """
        args = dict(self.box_args)
        args.update(box_args)
        level = self.level if level is None else level
        show = self.show if show is None else show
        bullet = self.bullet if bullet is None else bullet

        b = self.parent.box(
            x=level * self.level_indent, horizontal=True, show=show, **args
        )
        if bullet is not None:
            b.box(width=self.bullet_width, y=0).text(bullet)
        return b.box(width="fill")

    @contextmanager
    def indent_scope(self, levels=1):
        """
        Context manager that changes the indentation level in its scope.

        Example:
            lst = ListBuilder(slide.box())
            with lst.indent_scope():
                # items created here will have level = 1
                with lst.indent_scope():
                    # items created here will have level = 1
        Parameters
        ----------
        levels: int
            How many levels of indentation to apply in the scope of the context manager.
        """
        self.indent(levels)
        try:
            yield
        finally:
            self.dedent(levels)

    def indent(self, levels=1):
        """
        Increate the indentation level of the builder by the given amount of levels.

        Parameters
        ----------
        levels: int
            Amount of levels to increase the current indetation level.
        """
        self.level += levels

    def dedent(self, levels=1):
        """
        Decrease the indentation level of the builder by the given amount of levels.

        Parameters
        ----------
        levels: int
            Amount of levels to decrease the current indetation level.
        """
        if self.level - levels < 0:
            raise Exception("Cannot change indent level below zero")
        self.level -= levels
