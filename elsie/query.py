from collections import namedtuple

from .latex import render_latex
from .svg import svg_begin, svg_end, run_inkscape_get_width, run_inkscape_get_x
from .sxml import Xml

Query = namedtuple("Query", ["key", "callback"])


def compute_query(key):
    method, data = key
    if method == "inkscape" or method == "inkscape-x":
        xml = Xml()
        svg_begin(xml)
        xml.raw_text(data)
        svg_end(xml)
        if method == "inkscape":
            return run_inkscape_get_width(xml.to_string())
        else:  # == inkscape-x
            return run_inkscape_get_x(xml.to_string())
    elif method == "latex":
        try:
            return render_latex(data)
        except Exception as e:
            print(e)
            return """<svg height="30" width="200">
                      <text x="0" y="15" fill="red">pdflatex failed</text>
                      </svg>"""
    else:
        raise Exception("Invalid method: " + repr(method))
