

import zipfile
import lxml.etree as et
from PIL import Image
import io
from .show import ShowInfo


class OpenRaster:

    def __init__(self, filename):
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
                        image = Image.open(io.BytesIO(f.read()))
                    sources[src] = image

        self.root = root
        self.size = (int(self.root.get("w")), int(self.root.get("h")))
        self.sources = sources

    def get_steps(self):
        steps = 1
        for element in self.root.iter():
            show_info = ShowInfo.from_label(element.get("name"))
            if show_info is not None:
                steps = max(steps, show_info.min_steps())
        return steps

    def render(self, fragments, step):

        def _check_visibility(element):
            if element.get("visibility") != "visible":
                return False
            if fragments:
                show_info = ShowInfo.from_label(element.get("name"))
                if show_info is not None and not show_info.is_visible(step):
                    return False
            return True

        def _render_layout(element):
            if not _check_visibility(element):
                return None
            result = self.sources[element.get("src")]
            return result

        def _merge(prev_image, new_image, offset, opacity):
            if prev_image is None:
                return new_image
            if new_image is None:
                return prev_image
            #prev_image.paste(new_image, offset, mask=new_image)
            return Image.alpha_composite(prev_image, new_image)

            #return prev_image

        def _render_stack(stack):
            if not _check_visibility(stack):
                return None
            return _process_stack_children(stack)

        def _process_stack_children(stack):
            result = None
            for element in reversed(stack):
                if element.tag == "stack":
                    r = _render_stack(element)
                elif element.tag == "layer":
                    r = _render_layout(element)
                else:
                    continue
                x = int(element.get("x", "0"))
                y = int(element.get("y", "0"))
                opacity = float(element.get("opacity", "1"))

                if opacity < 0.999:
                    raise Exception("Opacity is not yet supported")

                if x != 0 or y != 0:
                    raise Exception("Offsets are not supported")

                result = _merge(result, r, (x, y), opacity)
            return result

        return _process_stack_children(self.root)
