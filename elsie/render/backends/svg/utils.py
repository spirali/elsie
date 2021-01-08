from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from ....utils.sxml import Xml


def svg_begin(xml, width=None, height=None, view_box=None, inkscape_namespace=False):
    xml.element("svg")
    xml.set("xmlns", "http://www.w3.org/2000/svg")
    xml.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
    if inkscape_namespace:
        xml.set("xmlns:inkscape", "http://www.inkscape.org/namespaces/inkscape")
    if width is not None:
        xml.set("width", width)
    if height is not None:
        xml.set("height", height)
    if view_box:
        xml.set("viewBox", " ".join(str(v) for v in view_box))


def svg_end(xml):
    xml.close("svg")


def svg_size_to_pixels(text):
    suffix = ""
    while text and text[-1].isalpha():
        suffix = text[-1] + suffix
        text = text[:-1]
    if suffix == "mm":
        factor = 3.77953
    elif suffix == "cm":
        factor = 37.7953
    elif suffix == "pt":
        factor = 1.33333
    else:
        factor = 1.0
    return float(text) * factor


def rename_ids(root, suffix):
    ids = []
    for e in root.iter():
        e_id = e.get("id")
        if e_id:
            ids.append("#" + e_id)
            e.set("id", e_id + suffix)

    for e in root.iter():
        for name, value in e.attrib.items():
            for e_id in ids:
                if e_id in value:
                    e.set(name, value.replace(e_id, e_id + suffix))


def apply_rotation(xml: "Xml", rotation: float, center: Tuple[float, float]):
    xml.set("transform", f"rotate({rotation} {center[0]} {center[1]})")
