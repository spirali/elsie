from .boxmixin import BoxMixin


class BoxItem(BoxMixin):
    def __init__(self, box):
        self._box = box
        self.z_level = box.z_level

    def _get_box(self):
        return self._box

    def draw(self, ctx):
        raise NotImplementedError


class SimpleBoxItem(BoxItem):
    def __init__(self, box, render_fn):
        super().__init__(box)
        self.render = render_fn
