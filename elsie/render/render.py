import os

from ..render.backends.svg.utils import svg_begin, svg_end
from ..utils.sxml import Xml
from .inkscape import export_by_inkscape


class RenderUnit:
    """
    A single presentation page that can render itself using a backend.
    """

    def __init__(self, slide, step):
        self.slide = slide
        self.step = step

    def write_debug(self, out_dir):
        pass

    def export(self, fs_cache, export_type: str):
        raise NotImplementedError

    def get_svg(self):
        return None


class SvgRenderUnit(RenderUnit):
    def __init__(self, slide, step, svg, inkscape):
        super().__init__(slide, step)
        self.svg = svg
        self.inkscape = inkscape

    def write_debug(self, out_dir):
        svg_file = os.path.join(
            out_dir, "{}-{}.svg".format(self.slide.index, self.step)
        )
        with open(svg_file, "w") as f:
            f.write(self.svg)

    def export(self, fs_cache, export_type):
        return fs_cache.ensure(
            self.svg.encode(),
            export_type,
            lambda source, target, et: export_by_inkscape(
                self.inkscape, source, target, et
            ),
        )

    def get_svg(self):
        return self.svg


class ExportedRenderUnit(RenderUnit):
    def __init__(self, slide, step, filename, export_type="pdf"):
        super().__init__(slide, step)
        self.filename = filename
        self.export_type = export_type

    def export(self, fs_cache, export_type):
        if export_type == self.export_type:
            return self.filename


def per_page_grouping(backend, units, count_x, count_y, width, height):
    from .backends import InkscapeBackend

    assert isinstance(backend, InkscapeBackend)

    # TODO: reimplement using RenderingContext
    def new():
        tmp_xml = Xml()
        svg_begin(tmp_xml, width * count_x, height * count_y)
        return tmp_xml

    def close():
        if idx > 0:
            svg_end(xml)
            new_units.append(
                SvgRenderUnit(None, None, xml.to_string(), backend.inkscape)
            )

    assert count_x > 0
    assert count_y > 0
    limit = count_x * count_y
    if limit == 1:
        return units

    new_units = []
    xml = new()
    idx = 0
    for unit in units:
        svg = unit.get_svg()
        if svg is None:
            new_units.append(unit)
            continue

        if idx == limit:
            close()
            xml = new()
            idx = 0

        x = (idx % count_x) * width
        y = (idx // count_x) * height

        xml.element("g")
        xml.set("transform", f"translate({x}, {y})")
        xml.raw_text(svg)
        xml.close("g")
        idx += 1
    close()

    return new_units
