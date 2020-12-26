from ..render.inkscape import InkscapeShell
from ..render.latex import render_latex
from ..svg.svg import svg_begin, svg_end
from ..utils.sxml import Xml


def compute_query(inkscape: InkscapeShell, method: str, data: str):
    if method == "inkscape-w" or method == "inkscape-x":
        xml = Xml()
        svg_begin(xml)
        xml.raw_text(data)
        svg_end(xml)
        if method == "inkscape-w":
            return inkscape.get_width(xml.to_string(), "target")
        else:  # == inkscape-x
            return inkscape.get_x(xml.to_string(), "target")
    elif method == "latex":
        return render_latex(data)
    else:
        raise Exception("Invalid method: " + repr(method))
