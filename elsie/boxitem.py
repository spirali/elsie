from .boxmixin import BoxMixin


class BoxItem(BoxMixin):
    """
    Leaf child of the box layout hierarchy.

    When you call a method from `BoxMixin` that creates a new box (like text, image, etc.), it will
    add the new box to the parent of the box item.
    """

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
