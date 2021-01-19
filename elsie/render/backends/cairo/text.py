from typing import List, Tuple

import cairocffi as cairo
import pangocairocffi
import pangocffi
from pangocffi import Attribute, AttrList, FontDescription, Rectangle

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


def style_to_attributes(
    style: TextStyle, start_index: int, end_index: int
) -> List[Attribute]:
    kwargs = dict(start_index=start_index, end_index=end_index)
    attrs = [
        Attribute.from_size_absolute(to_pango_units(style.size), **kwargs),
        Attribute.from_family(style.font, **kwargs),
        Attribute.from_foreground_color(
            *to_pango_color(get_rgb_color(style.color)), **kwargs
        ),
    ]
    weight = pangocffi.Weight.BOLD if style.bold else pangocffi.Weight.NORMAL
    attrs.append(Attribute.from_weight(weight, **kwargs))

    style = pangocffi.Style.ITALIC if style.italic else pangocffi.Style.NORMAL
    attrs.append(Attribute.from_style(style, **kwargs))
    return attrs


def get_text_and_attributes(
    parsed_text, style: TextStyle, styles
) -> Tuple[str, AttrList]:
    attr_list = AttrList()
    base_style = [styles["default"].compose(style)]
    start = 0
    text = ""

    def length(t):
        return len(t.encode("utf8"))

    def push_attrs(style, start_index, end_index):
        for attr in style_to_attributes(style, start_index, end_index):
            attr_list.insert(attr)

    def active_style():
        return [style for style in reversed(base_style) if style is not None][0]

    for (token, value) in parsed_text:
        if token == "text":
            text += value
        elif token == "newline":
            newline_text = "\n" * value
            text += newline_text
        elif token == "begin":
            push_attrs(active_style(), start, length(text))
            start = length(text)
            if value.startswith("#"):
                base_style.append(None)
            else:
                base_style.append(active_style().compose(styles[value]))
        elif token == "end":
            push_attrs(active_style(), start, length(text))
            start = length(text)
            base_style.pop()

    if start < length(text):
        push_attrs(base_style[0], start, length(text))
    assert len(base_style) == 1
    assert base_style[0] is not None
    return text, attr_list


def get_text_height(pctx: pangocffi.Context, style: TextStyle, resolution_scale: float):
    # TODO: optimize
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
) -> pangocffi.Layout:
    # TODO: fix letter spacing
    style = styles["default"].compose(style)
    layout = pangocairocffi.create_layout(ctx)
    layout.set_ellipsize(pangocffi.EllipsizeMode.NONE)

    layout.set_alignment(get_pango_alignment(style))
    text, attributes = get_text_and_attributes(parsed_text, style, styles)
    layout.set_text(text)
    layout.set_attributes(attributes)

    height = get_text_height(pctx, style, resolution_scale)

    assert style.line_spacing >= 1.0
    spacing = (style.line_spacing * style.size) - height
    layout.set_spacing(to_pango_units(spacing))

    return layout


def from_pango_rect(rect: Rectangle) -> Rect:
    return Rect(
        x=from_pango_units(rect.x),
        y=from_pango_units(rect.y),
        width=from_pango_units(rect.width),
        height=from_pango_units(rect.height),
    )


def get_extents(layout: pangocffi.Layout, ink=False) -> Rect:
    rect_l, rect_i = layout.get_extents()
    return from_pango_rect(rect_i if ink else rect_l)


PANGO_ALIGNMENTS = {
    "middle": pangocffi.Alignment.CENTER,
    "left": pangocffi.Alignment.LEFT,
    "right": pangocffi.Alignment.RIGHT,
}


def get_pango_alignment(style: TextStyle):
    return PANGO_ALIGNMENTS[style.align]
