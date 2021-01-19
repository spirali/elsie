from ....utils.sxml import Xml
from ...inkscape import InkscapeShell
from .utils import svg_begin, svg_end


def compute_query(inkscape: InkscapeShell, method: str, data: str):
    xml = Xml()
    svg_begin(xml)
    xml.raw_text(data)
    svg_end(xml)

    if method == "inkscape-w":
        return inkscape.get_width(xml.to_string(), "target")
    elif method == "inkscape-h":
        return inkscape.get_height(xml.to_string(), "target")
    elif method == "inkscape-x":
        return inkscape.get_x(xml.to_string(), "target")
    else:
        raise Exception("Invalid method: " + repr(method))
