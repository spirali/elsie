import os

from elsie.inkscape import export_by_inkscape


class RenderUnit:
    def __init__(self, slide, step):
        self.slide = slide
        self.step = step

    def write_debug(self, out_dir):
        pass

    def get_svg(self):
        return None


class SvgRenderUnit(RenderUnit):
    def __init__(self, slide, step, svg):
        super().__init__(slide, step)
        self.svg = svg

    def write_debug(self, out_dir):
        svg_file = os.path.join(
            out_dir, "{}-{}.svg".format(self.slide.index, self.step)
        )
        with open(svg_file, "w") as f:
            f.write(self.svg)

    def export(self, fs_cache, export_type, inkscape):
        return fs_cache.ensure(
            self.svg.encode(),
            export_type,
            lambda source, target, et: export_by_inkscape(inkscape, source, target, et),
        )

    def get_svg(self):
        return self.svg


class PdfRenderUnit(RenderUnit):
    def __init__(self, slide, step, filename):
        super().__init__(slide, step)
        self.filename = filename

    def export(self, fs_cache, export_type, inkscape):
        if export_type == "pdf":
            return self.filename
        else:
            return None
