from .sxml import Xml
from .svg import svg_begin, svg_end, run_inkscape_get_width
from .latex import render_latex
from collections import namedtuple

Query = namedtuple("Query", ["key", "callback"])


def compute_query(key):
    method, data = key
    if method == "inkscape":
        xml = Xml()
        svg_begin(xml)
        xml.raw_text(data)
        svg_end(xml)
        return run_inkscape_get_width(xml.to_string())
    elif method == "latex":
        return render_latex(data)
    else:
        raise Exception("Invalid method: " + repr(method))