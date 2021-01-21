from typing import List, Tuple

import cairocffi as cairo
import pangocairocffi
import pangocffi
from pangocffi import Attribute, AttrList, FontDescription, Layout, Rectangle, ffi

from ....text.textstyle import TextStyle
from ....utils.geom import Rect
from .utils import get_rgb_color


def to_pango_units(size: float) -> int:
    return pangocffi.units_from_double(size)


def from_pango_units(size: int) -> float:
    return pangocffi.units_to_double(size)


def to_pango_color(color: Tuple[float, float, float]) -> Tuple[int, int, int]:
    r, g, b = color
    max = 2 ** 16 - 1
    return (int(r * max), int(g * max), int(b * max))


def attr_from_scale(scale_factor: float, start_index: int, end_index: int):
    scale_factor = ffi.cast("double", scale_factor)
    attr = Attribute._init_pointer(
        pangocffi.pango.pango_attr_scale_new(scale_factor),
    )
    attr.start_index = start_index
    attr.end_index = end_index
    return attr


def style_to_attributes(
    style: TextStyle, text_scale: float, start_index: int, end_index: int
) -> List[Attribute]:
    kwargs = dict(start_index=start_index, end_index=end_index)
    attrs = [
        Attribute.from_size_absolute(to_pango_units(style.size), **kwargs),
        Attribute.from_family(style.font, **kwargs),
        Attribute.from_foreground_color(
            *to_pango_color(get_rgb_color(style.color)), **kwargs
        ),
    ]
    if text_scale is not None:
        attrs.append(attr_from_scale(text_scale, **kwargs))

    weight = pangocffi.Weight.BOLD if style.bold else pangocffi.Weight.NORMAL
    attrs.append(Attribute.from_weight(weight, **kwargs))

    style = pangocffi.Style.ITALIC if style.italic else pangocffi.Style.NORMAL
    attrs.append(Attribute.from_style(style, **kwargs))
    return attrs


INVISIBLE_SPACE = "⠀"  # this is not a normal space, but U+2800


def byte_length(text):
    return len(text.encode("utf8"))


def get_text_and_attributes(
    parsed_text, style: TextStyle, styles, text_scale: float
) -> Tuple[str, AttrList]:
    attr_list = AttrList()
    base_style = [styles["default"].compose(style)]
    start = 0
    text = ""

    def push_attrs(style, start_index, end_index):
        for attr in style_to_attributes(style, text_scale, start_index, end_index):
            attr_list.insert(attr)

    def active_style():
        return [style for style in reversed(base_style) if style is not None][0]

    line = ""
    for (token, value) in parsed_text:
        if token == "text":
            line += value
            text += value
        elif token == "newline":
            for _ in range(value):
                if not line:
                    # This fixes the height of empty lines
                    text += INVISIBLE_SPACE
                text += "\n"
                line = ""
        elif token == "begin":
            push_attrs(active_style(), start, byte_length(text))
            start = byte_length(text)
            if value.startswith("#"):
                base_style.append(None)
            else:
                base_style.append(active_style().compose(styles[value]))
        elif token == "end":
            push_attrs(active_style(), start, byte_length(text))
            start = byte_length(text)
            base_style.pop()

    if start < byte_length(text):
        push_attrs(base_style[0], start, byte_length(text))
    assert len(base_style) == 1
    assert base_style[0] is not None
    return text, attr_list


def get_text_height(pctx: pangocffi.Context, style: TextStyle, resolution_scale: float):
    font = FontDescription()
    font.set_family(style.font)
    font.set_absolute_size(to_pango_units(style.size))
    ret = pangocffi.pango.pango_context_get_metrics(
        pctx.get_pointer(), font.get_pointer(), pangocffi.ffi.NULL
    )

    descent = from_pango_units(pangocffi.pango.pango_font_metrics_get_descent(ret))
    ascent = from_pango_units(pangocffi.pango.pango_font_metrics_get_ascent(ret))
    return (ascent + descent) * resolution_scale


def build_layout(
    ctx: cairo.Context,
    pctx: pangocffi.Context,
    parsed_text,
    style: TextStyle,
    styles,
    resolution_scale: float,
    spacing_scale: float = 1.0,
    text_scale: float = 1.0,
) -> pangocffi.Layout:
    # TODO: fix letter spacing
    style = styles["default"].compose(style)
    layout = pangocairocffi.create_layout(ctx)
    layout.set_ellipsize(pangocffi.EllipsizeMode.NONE)

    layout.set_alignment(get_pango_alignment(style))
    text, attributes = get_text_and_attributes(parsed_text, style, styles, text_scale)
    layout.set_text(text)
    layout.set_attributes(attributes)

    height = get_text_height(pctx, style, resolution_scale)

    assert style.line_spacing >= 1.0
    spacing = (style.line_spacing * style.size) - height
    layout.set_spacing(to_pango_units(spacing * spacing_scale))

    return layout


def from_pango_rect(rect: Rectangle) -> Rect:
    return Rect(
        x=from_pango_units(rect.x),
        y=from_pango_units(rect.y),
        width=from_pango_units(rect.width),
        height=from_pango_units(rect.height),
    )


def get_extents(layout: pangocffi.Layout, ink=True) -> Rect:
    rect_logical, rect_ink = layout.get_extents()
    return from_pango_rect(rect_ink if ink else rect_logical)


def get_byte_range(parsed_text, id_index) -> Tuple[int, int]:
    stack = []
    byte_count = 0
    start = None

    for i, (type, value) in enumerate(parsed_text):
        if type == "text":
            byte_count += byte_length(value)
        elif type == "newline":
            assert False
        elif type == "begin":
            if i == id_index:
                start = byte_count
            stack.append(value)
        elif type == "end":
            stack.pop()
            if start is not None and not stack:
                return (start, byte_count)
    assert False


def compute_subtext_extents(
    layout: Layout, parsed_text, id_index: int
) -> Tuple[float, float]:
    """
    Returns the x coordinate and width of a subtext of a single line.
    """
    assert layout.get_line_count() == 1
    (start, end) = get_byte_range(parsed_text, id_index)
    iter = layout.get_iter()
    x = None
    width = 0

    while True:
        byte_offset = iter.get_index()
        if start <= byte_offset < end:
            extents = from_pango_rect(iter.get_char_extents())
            if x is None:
                assert start == byte_offset
                x = extents.x
            width += extents.width

        if byte_offset >= end or not iter.next_char():
            break
    assert x is not None
    return (x, width)


PANGO_ALIGNMENTS = {
    "middle": pangocffi.Alignment.CENTER,
    "left": pangocffi.Alignment.LEFT,
    "right": pangocffi.Alignment.RIGHT,
}


def get_pango_alignment(style: TextStyle):
    return PANGO_ALIGNMENTS[style.align]
