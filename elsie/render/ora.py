import base64
import io
import zipfile

import lxml.etree as et
from PIL import Image

from ..render.backends.svg.utils import svg_begin, svg_end
from ..utils.sxml import Xml
from .backends.svg.draw import draw_bitmap


def convert_ora_to_svg(filename):
    with zipfile.ZipFile(filename, "r") as archive:
        with archive.open("mimetype") as f:
            mimetype = f.read().rstrip()
            if mimetype != b"image/openraster":
                raise Exception("Invalid mime type, found: {}".format(mimetype))
        with archive.open("stack.xml") as f:
            root = et.fromstring(f.read())

        sources = {}
        for element in root.getiterator():
            src = element.get("src")
            if src is not None and src not in sources:
                with archive.open(src) as f:
                    img = Image.open(f)
                    box = img.getbbox()

                    if box is None:
                        sources[src] = None
                        continue

                    img = img.crop(box)
                    temp = io.BytesIO()
                    img.save(temp, "png")
                    mime = "image/png"

                    data = temp.getvalue()
                    data = base64.b64encode(data).decode("ascii")

                    if len(data) > 10_0000_000:
                        raise Exception(
                            "Layer in ORA is file too big, consider rescaling image"
                        )

                    sources[src] = (
                        data,
                        mime,
                        box[0],
                        box[1],
                        box[2] - box[0],
                        box[3] - box[1],
                    )

    width, height = root.get("w"), root.get("h")
    xml = Xml()
    svg_begin(xml, width, height, inkscape_namespace=True)
    _children_to_svg(root, xml, sources)
    svg_end(xml)
    return xml.to_string()


def _check_visibility(element):
    return element.get("visibility") == "visible"


def _stack_to_svg(element, xml, sources):
    if not _check_visibility(element):
        return
    xml.element("g")
    x, y = element.get("x"), element.get("y")
    if x != "0" or y != "0":
        xml.set("transform", "translate({}, {})".format(x, y))
    opacity = float(element.get("opacity"))
    if opacity < 0.9999:
        xml.set("opacity", opacity)
    xml.set("inkscape:label", element.get("name"))
    _children_to_svg(element, xml, sources)
    xml.close("g")


def _layer_to_svg(element, xml, sources):
    if not _check_visibility(element):
        return
    source = sources[element.get("src")]
    if source is None:
        return
    data, mime, x, y, image_width, image_height = source
    extra_args = [("inkscape:label", element.get("name"))]
    opacity = float(element.get("opacity"))
    if opacity is not None and opacity < 0.9999:
        extra_args.append(("opacity", opacity))
    draw_bitmap(
        xml,
        float(element.get("x")) + x,
        float(element.get("y")) + y,
        image_width,
        image_height,
        mime,
        data,
        rotation=None,
        extra_args=extra_args,
    )


def _children_to_svg(element, xml, sources):
    for e in reversed(element):
        if e.tag == "stack":
            _stack_to_svg(e, xml, sources)
        elif e.tag == "layer":
            _layer_to_svg(e, xml, sources)
