from typing import TYPE_CHECKING

from ..boxtree.boxitem import BoxItem
from ..boxtree.lazy import LazyValue
from ..render.backends.backend import Backend
from .textparser import extract_line, number_of_lines

if TYPE_CHECKING:
    from ..boxtree import box


def text_x_in_rect(rect, style):
    align = style.align
    if align == "left":
        return rect.x
    elif align == "middle":
        return rect.x + rect.width / 2
    elif align == "right":
        return rect.x + rect.width
    else:
        raise Exception("Invalid value of align: " + repr(align))


class TextBoxItem(BoxItem):
    def __init__(self, box, parsed_text, style, styles, scale_to_fit, rotation):
        super().__init__(box)
        self._text_size = None
        self._text_scale = 1
        self._scale_to_fit = scale_to_fit
        self.rotation = rotation
        self._style = style
        self._styles = styles
        self._parsed_text = parsed_text
        self._make_query(box.slide.slides.backend)

        if scale_to_fit:

            def callback(rect):
                tw, th = self._text_size
                if tw > 0.00001 and th > 0.00001:
                    scale = min(rect.width / tw, rect.height / th)
                    self._text_size = (tw * scale, th * scale)
                    self._text_scale = scale

            box.layout.add_callback(callback)

    def render(self, ctx):
        rect = self._box.layout.rect
        scale = self._text_scale
        style = self._style
        x = text_x_in_rect(rect, style)
        y = rect.y + (rect.height - self._text_size[1]) / 2 + style.size * scale

        if scale > 0.00001:
            ctx.draw_text(
                rect=rect,
                x=x,
                y=y,
                parsed_text=self._parsed_text,
                style=style,
                styles=self._styles,
                scale=scale if self._scale_to_fit else None,
                rotation=self.rotation,
            )

    def _make_query(self, backend: Backend):
        width = backend.compute_text_width(self._parsed_text, self._style, self._styles)
        layout = self._box.layout
        style = self._style
        line_height = style.size * style.line_spacing
        height = number_of_lines(self._parsed_text) * line_height

        if not self._scale_to_fit:
            layout.ensure_width(width)
            layout.ensure_height(height)
        else:
            if layout.width_definition is None:
                layout.ensure_width(width)
            if layout.height_definition is None:
                layout.ensure_height(height)
        self._text_size = (width, height)

    def line_box(self, index: int, n_lines=1, **box_args) -> "box.Box":
        """
        Creates a box that wraps the specified number of lines starting at `index`.

        Parameters
        ----------
        index: int
            Index of the first line.
        n_lines: int
            Number of items that will be included in the box.
        box_args
            Parameters passed to the Box constructor.
        """

        def compute_y():
            text_lines = number_of_lines(self._parsed_text)
            line_height = self._text_size[1] / text_lines
            rect = self._box.layout.rect
            y = rect.y + (rect.height - self._text_size[1]) / 2
            return y + line_height * index

        def compute_height():
            text_lines = number_of_lines(self._parsed_text)
            return n_lines * self._text_size[1] / text_lines + 1

        box_args.setdefault("width", "fill")
        box_args.setdefault("x", 0)
        box_args.setdefault("y", LazyValue(compute_y))
        box_args.setdefault("height", LazyValue(compute_height))
        return self._box.box(**box_args)

    def inline_box(self, style_name, n_th=1, **box_args) -> "box.Box":
        """
        Creates a box that will wrap a section of text which is enclosed by the given inline style.

        Parameters
        ----------
        style_name: str
            Name of the (inline) style that should be found inside the text.
        n_th: int
            If there are multiple instances of the passed inline style, this parameter selects
            which instance should be wrapped with the newly created box.
        box_args
            Parameters passed to the Box constructor.
        """
        assert n_th > 0
        count = n_th
        for (i, token) in enumerate(self._parsed_text):
            if token[0] == "begin" and token[1] == style_name:
                count -= 1
                if count == 0:
                    return self._text_box_helper(i, box_args)
        raise Exception(
            "Style {}. occurence of style '{}' not found".format(n_th, style_name)
        )

    def _text_box_helper(self, index, box_args):
        def compute_y():
            line_number = number_of_lines(self._parsed_text[:index]) - 1
            text_lines = number_of_lines(self._parsed_text)
            line_height = self._text_size[1] / text_lines
            rect = self._box.layout.rect
            y = rect.y + (rect.height - self._text_size[1]) / 2
            return y + line_height * line_number

        def compute_height():
            text_lines = number_of_lines(self._parsed_text)
            return self._text_size[1] / text_lines + 1

        line, index_in_line = extract_line(self._parsed_text, index)

        backend = self._box.slide.slides.backend
        query_x = backend.compute_text_x(
            line, self._style, self._styles, id_index=index_in_line
        )
        query_w = backend.compute_text_width(
            line, self._style, self._styles, id_index=index_in_line
        )

        box_args.setdefault(
            "x",
            LazyValue(
                lambda: text_x_in_rect(self._box.layout.rect, self._style)
                + query_x * self._text_scale
            ),
        )
        box_args.setdefault("y", LazyValue(compute_y))
        box_args.setdefault("width", LazyValue(lambda: query_w * self._text_scale))
        box_args.setdefault("height", LazyValue(compute_height))

        return self._box.box(**box_args)
