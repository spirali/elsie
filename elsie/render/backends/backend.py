import os
from typing import TYPE_CHECKING

from ..render import RenderUnit

if TYPE_CHECKING:
    from ...slides.slide import Slide

DEFAULT_CACHE_DIR = "./elsie-cache"


class Backend:
    """Represents a rendering backend that can render Elsie primitives into PDF."""

    def __init__(self, cache_dir: str):
        self.dimensions = None
        self.cache_dir = os.path.abspath(cache_dir)

    def set_dimensions(self, width: int, height: int):
        self.dimensions = (width, height)

    def get_version(self, elsie_version: str) -> str:
        """
        Returns unique version of the backend.

        It should combine the Elsie version with the version of the backend software (e.g. Inkscape
        or Cairo).
        """
        return elsie_version

    def create_render_unit(
        self, slide: "Slide", step: int, export_type: str
    ) -> RenderUnit:
        """
        Create a render unit that can export itself to PDF or PNG.
        """
        raise NotImplementedError

    def compute_text_width(self, parsed_text, style, styles, **kwargs) -> float:
        """
        Compute the width of the given text that would be rendered with the given style.
        """
        raise NotImplementedError

    def compute_text_height(self, parsed_text, style, styles, **kwargs) -> float:
        """
        Compute the height of the given text that would be rendered with the given style.
        """
        raise NotImplementedError

    def compute_text_x(self, parsed_text, style, styles, **kwargs) -> float:
        """
        Compute the x position of the given text that would be rendered with the given style.
        """
        raise NotImplementedError

    def prune_cache(self):
        pass

    def save_cache(self):
        pass
