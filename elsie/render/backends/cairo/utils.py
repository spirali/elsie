from typing import Tuple

import lxml.etree as et
import webcolors


def get_rgb_color(color) -> Tuple[float, float, float]:
    if isinstance(color, str):
        if color and color[0] == "#":
            color = webcolors.normalize_hex(color)
            return normalize_color(webcolors.hex_to_rgb(color))
        else:
            return normalize_color(webcolors.name_to_rgb(color))

    assert len(color) == 3
    for v in color:
        assert isinstance(v, float)
    return tuple(color)


def normalize_color(color: Tuple[int, int, int]) -> Tuple[float, float, float]:
    return tuple(v / 255 for v in color)


SVG_QUERY = et.XPath(".//*[starts-with(name(), 'flow')]")


def normalize_svg(root: et.Element) -> et.Element:
    for el in SVG_QUERY(root):
        el.getparent().remove(el)
    return root
