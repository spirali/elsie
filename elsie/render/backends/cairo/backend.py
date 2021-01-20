from ....utils.cache import FsCache
from ....utils.geom import Rect
from ...render import RenderUnit
from ..backend import Backend
from .rcontext import CairoRenderingContext
from .utils import get_temp_path


class CairoBackend(Backend):
    """
    Backend that maps Elsie primitives to Cairo commands and renders them to PDF using a Cairo
    surface.
    """

    def create_render_unit(self, slide, step: int) -> RenderUnit:
        ctx = CairoRenderingContext(
            *self.dimensions, slide.view_box, step, slide.debug_boxes
        )
        painters = slide._box.get_painters(ctx, 0)
        painters.sort(key=lambda painter: painter.z_level)
        for p in painters:
            p.render(ctx)
        return CairoRenderUnit(slide, step, ctx)

    def compute_text_width(
        self, parsed_text, style, styles, id_index=None, *args, **kwargs
    ) -> float:
        return self._text_extents(parsed_text, style, styles, id_index=id_index).width

    def compute_text_x(
        self, parsed_text, style, styles, *args, id_index=None, **kwargs
    ) -> float:
        return self._text_extents(parsed_text, style, styles, id_index=id_index).x

    def _text_extents(self, parsed_text, style, styles, id_index=None) -> Rect:
        ctx = CairoRenderingContext(*self.dimensions)
        if id_index is None:
            return ctx.compute_text_extents(parsed_text, style, styles)
        return ctx.compute_subtext_extents(parsed_text, style, styles, id_index)


class CairoRenderUnit(RenderUnit):
    def __init__(self, slide, step, ctx: CairoRenderingContext):
        super().__init__(slide, step)
        self.ctx = ctx

    def export(self, fs_cache: FsCache, export_type: str):
        if export_type == "pdf":
            self.ctx.surface.finish()
            return self.ctx.filename
        elif export_type == "png":
            path = get_temp_path("png")
            self.ctx.surface.write_to_png(path)
            return path
