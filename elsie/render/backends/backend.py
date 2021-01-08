from typing import TYPE_CHECKING

from ..render import RenderUnit

if TYPE_CHECKING:
    from ...slides.slide import Slide

DEFAULT_CACHE_DIR = "./elsie-cache"


class Backend:
    """Represents a rendering backend that can render Elsie primitives into PDF."""

    def get_version(self, elsie_version: str) -> str:
        """
        Returns unique version of the backend.

        It should combine the Elsie version with the version of the backend software (e.g. Inkscape
        or Cairo).
        """
        return elsie_version

    def create_render_unit(self, slide: "Slide", step: int) -> RenderUnit:
        raise NotImplementedError

    def compute_text_width(self, parsed_text, style, styles, **kwargs) -> float:
        raise NotImplementedError

    def compute_text_x(self, parsed_text, style, styles, **kwargs) -> float:
        raise NotImplementedError

    def prune_cache(self):
        pass

    def save_cache(self):
        pass
