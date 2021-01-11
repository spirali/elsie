from ...utils.geom import Rect


class RenderingContext:
    """
    Used for rendering a single slide page.

    Contains drawing primitives (text, rectangles, images etc.).
    """

    def __init__(self, step: int, debug_boxes: True):
        self.step = step
        self.debug_boxes = debug_boxes

    def draw_rect(self, rect: Rect, rx=None, ry=None, rotation=None, **kwargs):
        raise NotImplementedError

    def draw_ellipse(self, rect: Rect, rotation=None, **kwargs):
        raise NotImplementedError

    def draw_polygon(self, points, rotation=None, **kwargs):
        raise NotImplementedError

    def draw_polyline(self, points, **kwargs):
        raise NotImplementedError

    def draw_path(self, commands, **kwargs):
        raise NotImplementedError

    def draw_text(self, *args, **kwargs):
        raise NotImplementedError

    def draw_bitmap(self, *args, **kwargs):
        raise NotImplementedError
