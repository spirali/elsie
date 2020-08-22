from .boxitem import BoxItem
from .draw import draw_text
from .lazy import LazyValue
from .query import Query
from .sxml import Xml
from .textparser import number_of_lines, extract_line


def text_x_in_rect(rect, style):
    align = style["align"]
    if align == "left":
        return rect.x
    elif align == "middle":
        return rect.x + rect.width / 2
    elif align == "right":
        return rect.x + rect.width
    else:
        raise Exception("Invalid value of align: " + repr(align))


class TextBoxItem(BoxItem):
    def __init__(self, box, parsed_text, style, styles, scale_to_fit):
        super().__init__(box)
        self._text_size = None
        self._text_scale = 1
        self._scale_to_fit = scale_to_fit
        self._style = style
        self._styles = styles
        self._parsed_text = parsed_text
        box._queries.append(self._make_query())

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

        y = rect.y + (rect.height - self._text_size[1]) / 2 + style["size"] * scale

        if self._scale_to_fit:
            print("SCALE", scale, y, rect.y, rect.height, self._text_size)

        if self._scale_to_fit:
            transform = "scale({})".format(scale)
        else:
            transform = None
        if scale > 0.00001:
            draw_text(
                ctx.xml,
                x / scale,
                y / scale,
                self._parsed_text,
                style,
                self._styles,
                transform=transform,
            )

    def _make_query(self):
        def on_query(width):
            layout = self._box.layout
            style = self._style
            line_height = style["size"] * style["line_spacing"]
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

        xml = Xml()
        draw_text(xml, 0, 0, self._parsed_text, self._style, self._styles, id="target")
        key = xml.to_string()
        del xml
        return Query(("inkscape", key), on_query)

    def line_box(self, index, n_lines=1, **kwargs):
        def compute_y():
            text_lines = number_of_lines(self._parsed_text)
            line_height = self._text_size[1] / text_lines
            rect = self._box.layout.rect
            y = rect.y + (rect.height - self._text_size[1]) / 2
            return y + line_height * index

        def compute_height():
            text_lines = number_of_lines(self._parsed_text)
            return n_lines * self._text_size[1] / text_lines + 1

        kwargs.setdefault("width", "fill")
        kwargs.setdefault("x", 0)
        kwargs.setdefault("y", LazyValue(compute_y))
        kwargs.setdefault("height", LazyValue(compute_height))
        return self._box.box(**kwargs)

    def inline_box(self, style_name, n_th=1, **box_args):
        """ Create a box around a styled text """
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
        def on_query_x(x):
            query_result[0] = x

        def on_query_h(width):
            query_result[1] = width

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

        query_result = [None, None]

        line, index_in_line = extract_line(self._parsed_text, index)
        xml = Xml()
        draw_text(
            xml,
            0,
            0,
            line,
            self._style,
            self._styles,
            id="target",
            id_index=index_in_line,
        )
        text = xml.to_string()
        del xml

        self._box._queries.append(Query(("inkscape-x", text), on_query_x))
        self._box._queries.append(Query(("inkscape", text), on_query_h))

        box_args.setdefault(
            "x",
            LazyValue(
                lambda: text_x_in_rect(self._box.layout.rect, self._style)
                + query_result[0] * self._text_scale
            ),
        )
        box_args.setdefault("y", LazyValue(compute_y))
        box_args.setdefault(
            "width", LazyValue(lambda: query_result[1] * self._text_scale)
        )
        box_args.setdefault("height", LazyValue(compute_height))

        return self._box.box(**box_args)
