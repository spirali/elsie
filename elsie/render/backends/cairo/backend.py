from ...render import PdfRenderUnit, RenderUnit
from ..backend import Backend
from .rcontext import CairoRenderingContext


class CairoBackend(Backend):
    def create_render_unit(self, slide, step: int) -> RenderUnit:
        ctx = CairoRenderingContext(
            *self.dimensions, slide.view_box, step, slide.debug_boxes
        )
        painters = slide._box.get_painters(ctx, 0)
        painters.sort(key=lambda painter: painter.z_level)
        for p in painters:
            p.render(ctx)
        pdf_path = ctx.render()
        return PdfRenderUnit(slide, step, pdf_path)

    def compute_text_width(self, parsed_text, style, styles, *args, **kwargs) -> float:
        return (
            CairoRenderingContext(*self.dimensions)
            .compute_text_extents(parsed_text, style, styles)
            .width
        )

    def compute_text_x(self, parsed_text, style, styles, *args, **kwargs) -> float:
        return (
            CairoRenderingContext(*self.dimensions)
            .compute_text_extents(parsed_text, style, styles)
            .x
        )
