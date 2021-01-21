import cairocffi as cairo
from cairosvg.colors import color
from cairosvg.helpers import node_format, size
from cairosvg.parser import Tree
from cairosvg.surface import Surface

from .draw import transform


class CairoSurface(Surface):
    def __init__(
        self,
        surface,
        x,
        y,
        tree,
        dpi,
        output=None,
        parent_surface=None,
        parent_width=None,
        parent_height=None,
        scale=1,
        output_width=None,
        output_height=None,
        background_color=None,
        map_rgba=None,
        map_image=None,
        rotation=None,
    ):
        self.surface = surface
        self.cairo = None
        self.context_width, self.context_height = parent_width, parent_height
        self.cursor_position = [0, 0]
        self.cursor_d_position = [0, 0]
        self.text_path_width = 0
        self.tree_cache = {(tree.url, tree.get("id")): tree}
        if parent_surface:
            self.markers = parent_surface.markers
            self.gradients = parent_surface.gradients
            self.patterns = parent_surface.patterns
            self.masks = parent_surface.masks
            self.paths = parent_surface.paths
            self.filters = parent_surface.filters
            self.images = parent_surface.images
        else:
            self.markers = {}
            self.gradients = {}
            self.patterns = {}
            self.masks = {}
            self.paths = {}
            self.filters = {}
            self.images = {}
        self._old_parent_node = self.parent_node = None
        self.output = output
        self.dpi = dpi
        self.font_size = size(self, "12pt")
        self.stroke_and_fill = True
        width, height, viewbox = node_format(self, tree)
        if viewbox is None:
            viewbox = (0, 0, width, height)

        if output_width and output_height:
            width, height = output_width, output_height
        elif output_width:
            if width:
                # Keep the aspect ratio
                height *= output_width / width
            width = output_width
        elif output_height:
            if height:
                # Keep the aspect ratio
                width *= output_height / height
            height = output_height
        else:
            width *= scale
            height *= scale

        # Actual surface dimensions: may be rounded on raster surfaces types
        self.cairo, self.width, self.height = self._create_surface(
            width * self.device_units_per_user_units,
            height * self.device_units_per_user_units,
        )

        if 0 in (self.width, self.height):
            raise ValueError("The SVG size is undefined")

        self.context = cairo.Context(self.cairo)
        # We must scale the context as the surface size is using physical units
        self.context.scale(
            self.device_units_per_user_units, self.device_units_per_user_units
        )
        center = (x + width / 2, y + height / 2)
        transform(self.context, center, rotation=rotation)
        self.context.translate(x, y)

        # Initial, non-rounded dimensions
        self.set_context_size(width, height, viewbox, tree)

        if background_color:
            self.context.set_source_rgba(*color(background_color))
            self.context.paint()

        self.map_rgba = map_rgba
        self.map_image = map_image

    def _create_surface(self, width, height):
        return self.surface, width, height


def render_svg(
    surface: cairo.Surface, svg: str, x, y, width, height, rotation=None, dpi=96
):
    tree = Tree(bytestring=svg.encode())
    instance = CairoSurface(
        surface=surface,
        rotation=rotation,
        x=x,
        y=y,
        tree=tree,
        dpi=dpi,
        output_width=width,
        output_height=height,
    )
    instance.draw(tree)
