from collections import namedtuple

from .inkscape import InkscapeShell
from .latex import render_latex
from .svg import svg_begin, svg_end
from .sxml import Xml

Query = namedtuple("Query", ["key", "callback"])


def compute_query(inkscape: InkscapeShell, key: str):
    method, data = key
    if method == "inkscape" or method == "inkscape-x":
        xml = Xml()
        svg_begin(xml)
        xml.raw_text(data)
        svg_end(xml)
        if method == "inkscape":
            return inkscape.get_width(xml.to_string(), "target")
        else:  # == inkscape-x
            return inkscape.get_x(xml.to_string(), "target")
    elif method == "latex":
        return render_latex(data)
    else:
        raise Exception("Invalid method: " + repr(method))
