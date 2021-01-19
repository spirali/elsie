from typing import TYPE_CHECKING

from ..text.stylecontainer import StyleContainer
from .boxmixin import BoxMixin

if TYPE_CHECKING:
    from ..render.backends.rcontext import RenderingContext
    from ..slides import show, slide
    from . import layout


class Box(BoxMixin, StyleContainer):
    """
    Box is the main layout element of Elsie.

    Its most useful methods actually come from `BoxMixin`.
    """

    def __init__(
        self,
        slide: "slide.Slide",
        layout: "layout.Layout",
        styles,
        show_info: "show.ShowInfo",
        z_level=0,
        name: str = None,
    ):
        """
        Parameters
        ----------
        slide: slide.Slide
            Slide that contains this box.
        layout: layout.Layout
            Layout of the box (vertical/horizontal).
        name: str
            Name of the box (useful for debugging and name policy).
        show_info: show.ShowInfo
            Contains information about fragments in which the box should be shown.
        z_level: int
            Z-level of the box (useful for changing render order).
        """
        StyleContainer.__init__(self, styles)
        self.slide = slide
        self.layout = layout
        self.name = name
        self.children = []
        self._show_info = show_info

        self.z_level = z_level

    def _get_box(self):
        return self

    def current_fragment(self) -> int:
        """Returns the current fragment (the fragment with the highest number defined so far)."""
        return self.slide.current_fragment()

    def add_child(self, obj, prepend=False, above=None, below=None):
        """Semi-internal function, you can add your child if you know what you are doing."""
        assert isinstance(obj, Box) or isinstance(obj, BoxItem)

        if above is not None and below is not None:
            raise Exception("'above' and 'below' cannot be both set")
        if below is not None:
            self.children.insert(self.children.index(below), obj)
        elif above is not None:
            self.children.insert(self.children.index(above) + 1, obj)
        elif prepend:
            self.children.insert(0, obj)
        else:
            self.children.append(obj)

    @property
    def _box_children(self):
        return [child for child in self.children if isinstance(child, Box)]

    def _min_steps(self):
        return self._show_info.min_steps()

    def get_painters(self, ctx, depth):
        painters = []
        if not self._show_info.is_visible(ctx.step):
            return painters
        depth += 1
        for child in self.children:
            if not isinstance(child, Box):
                painters.append(child)
            else:
                painters += child.get_painters(ctx, depth)
        if ctx.debug_boxes:
            from .boxitem import SimpleBoxItem

            painters.append(
                SimpleBoxItem(self, lambda ctx: self._debug_paint(ctx, depth - 1))
            )
        return painters

    def _debug_paint(self, ctx: "RenderingContext", depth):
        from ..text.textstyle import TextStyle

        rect = self.layout.rect.copy()
        rect.width = max(rect.width, 0.1)
        rect.height = max(rect.height, 0.1)
        ctx.draw_rect(
            rect,
            color="#ff00ff",
            stroke_width=2,
            stroke_dasharray=[None, "4 2", "1 2"][depth % 3],
        )

        def format_num(v):
            if int(v) == v:
                return str(v)
            return f"{v:.2f}"

        name = self.name + " " if self.name else ""
        text = f" {name}[{format_num(rect.width)},{format_num(rect.height)}]"
        size = 14
        if depth % 2 == 1:
            text = "↖" + text
            y = rect.y + size * 0.9
        else:
            text = "↙" + text
            y = rect.y + rect.height - size * 0.1

        style = TextStyle(color="#ff00ff", size=size, align="left")
        style = self.get_style(style, full_style=True)
        rect.y = y
        ctx.draw_text(
            rect=rect,
            x=rect.x,
            y=y,
            parsed_text=[("text", text)],
            style=style,
            styles=self._styles,
        )

    def _traverse(self, fn):
        fn(self)
        for child in self._box_children:
            child._traverse(fn)

    def _ensure_steps(self, steps):
        self._show_info = self._show_info.ensure_steps(steps)
        self.slide.max_step = max(self.slide.max_step, steps)

    def _repr_html_(self):
        return self.slide._repr_html_()


from .boxitem import BoxItem  # noqa
