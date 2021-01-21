import cairocffi as cairo

from ....utils.cache import FsCache, get_cache_file_path
from ....utils.geom import Rect
from ...render import RenderUnit
from ..backend import DEFAULT_CACHE_DIR, Backend
from .rcontext import RESOLUTION_SCALE, CairoRenderingContext


class CairoBackend(Backend):
    """
    Backend that maps Elsie primitives to Cairo commands and renders them to PDF using a Cairo
    surface.
    """

    def __init__(self, cache_dir: str = DEFAULT_CACHE_DIR):
        super().__init__(cache_dir)

    def create_render_unit(self, slide, step: int) -> RenderUnit:
        ctx = CairoRenderingContext(
            *self.dimensions,
            viewbox=slide.view_box,
            step=step,
            debug_boxes=slide.debug_boxes
        )
        painters = slide._box.get_painters(ctx, 0)
        painters.sort(key=lambda painter: painter.z_level)
        for p in painters:
            p.render(ctx)
        return CairoRenderUnit(slide, step, self.cache_dir, ctx)

    def compute_text_width(
        self, parsed_text, style, styles, id_index=None, *args, **kwargs
    ) -> float:
        return self._text_extents(parsed_text, style, styles, id_index=id_index).width

    def compute_text_height(
        self, parsed_text, style, styles, id_index=None, *args, **kwargs
    ) -> float:
        return self._text_extents(parsed_text, style, styles, id_index=id_index).height

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
    def __init__(self, slide, step, cache_dir: str, ctx: CairoRenderingContext):
        super().__init__(slide, step)
        self.cache_dir = cache_dir
        self.ctx = ctx

    def export(self, fs_cache: FsCache, export_type: str):
        def render(surface, scale=None):
            ctx = cairo.Context(surface)
            if scale:
                ctx.scale(scale, scale)
            ctx.set_source_surface(self.ctx.surface)
            ctx.paint()

        path = None
        if export_type == "pdf":
            path = get_cache_file_path(self.cache_dir, "pdf")
            surface = cairo.PDFSurface(
                path, self.ctx.device_width, self.ctx.device_height
            )
            render(surface)
            surface.finish()
        elif export_type == "png":
            surface = cairo.ImageSurface(
                cairo.FORMAT_ARGB32, self.ctx.width, self.ctx.height
            )
            # Reverse PDF scaling
            render(surface, scale=1 / RESOLUTION_SCALE)
            path = get_cache_file_path(self.cache_dir, "png")
            surface.write_to_png(path)
        return path
