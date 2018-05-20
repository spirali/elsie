from .sxml import Xml
from .svg import svg_begin, svg_end, run_inkscape_get_width


def compute_query(key):
    xml = Xml()
    svg_begin(xml)
    xml.raw_text(key)
    svg_end(xml)
    return run_inkscape_get_width(xml.to_string())
