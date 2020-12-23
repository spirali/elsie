from .boxmixin import BoxMixin
from .draw import set_paint_style
from .textstyle import TextStyle, compose_style


class Box(BoxMixin):
    def __init__(
        self,
        slide,
        layout,
        styles,
        show_info,
        z_level=0,
        name=None,
    ):

        self.slide = slide
        self.layout = layout
        self.name = name
        self.children = []
        self._styles = styles
        self._show_info = show_info

        self.z_level = z_level

    def _get_box(self):
        return self

    def current_step(self) -> int:
        """Returns the current step (the step with the highest number defined so far)."""
        return self.slide.current_step()

    def add_child(self, obj, prepend=False, above=None, below=None):
        """Semi-internal function, you can add your child if you know
        what you are doing."""
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

    def update_style(self, style_name, style):
        assert isinstance(style_name, str)
        old_style = self.get_style(style_name, full_style=False)
        old_style.update(style)
        self._styles = self._styles.copy()
        self._styles[style_name] = old_style

    def set_style(self, style_name, style, base="default"):
        assert isinstance(style_name, str)
        assert isinstance(style, TextStyle)
        if base != "default":
            base_style = self.get_style(base)
            base_style.update(style)
            style = base_style
        self._styles = self._styles.copy()
        self._styles[style_name] = style

    def get_style(self, style, full_style=False):
        return compose_style(self._styles, style, full_style)

    def _debug_paint(self, ctx, depth):
        rect = self.layout.rect
        xml = ctx.xml
        xml.element("rect")
        xml.set("x", rect.x)
        xml.set("y", rect.y)
        xml.set("width", max(rect.width, 0.1))
        xml.set("height", max(rect.height, 0.1))
        set_paint_style(xml, "#ff00ff", None, 2, [None, "4 2", "1 2"][depth % 3])
        xml.close("rect")

        text = " {}[{:.2f},{:.2f}]".format(
            self.name + " " if self.name else "", rect.width, rect.height
        )
        size = 14
        if depth % 2 == 1:
            text = "↖" + text
            y = rect.y + 14 * 0.9
        else:
            text = "↙" + text
            y = rect.y + rect.height - size * 0.1

        xml.element("text")
        xml.set("x", rect.x)
        xml.set("y", y)
        xml.set(
            "style",
            "fill: #ff00ff,fill-opacity:1;stroke:#000000;stroke-width:0.2px;stroke-linecap:butt"
            ";stroke-linejoin:miter;stroke-opacity:1;",
        )
        xml.element("tspan")
        xml.text(text)
        xml.close("tspan")
        xml.close("text")

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
