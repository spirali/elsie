import io
import logging
from typing import TYPE_CHECKING, BinaryIO, List, Union

import lxml.etree as et
from PIL import Image

from ..render.backends.svg.utils import svg_size_to_pixels
from ..render.image import create_image_data, get_image_steps
from ..render.ora import convert_ora_to_svg
from ..shapes import arrow
from ..shapes.path import (
    check_and_unpack_path_commands,
    eval_path_commands,
    path_points_for_end_arrow,
    path_update_end_point,
)
from ..slides.show import ShowInfo
from ..text.highlight import highlight_code
from ..text.textparser import (
    add_line_numbers,
    parse_text,
    tokens_merge,
    tokens_to_text_without_style,
)
from ..utils.files import read_helper
from .lazy import eval_pair, eval_value, unpack_point

if TYPE_CHECKING:
    from ..text import textboxitem
    from . import boxitem, lazy
    from .box import Box


def scaler(rect, image_width, image_height):
    scale_x = rect.width / image_width
    scale_y = rect.height / image_height

    if rect.width and rect.height:
        return min(scale_x, scale_y)
    elif rect.width:
        return scale_x
    elif rect.height:
        return scale_y
    return None


class BoxMixin:
    """This mixin contains the most important methods of box-like elements (boxes and box
    items).
    """

    def _get_box(self):
        raise NotImplementedError

    def box(
        self,
        *,
        x: Union[float, str] = None,
        y: Union[float, str] = None,
        width: Union[float, str] = None,
        height: Union[float, str] = None,
        show: str = None,
        p_left: float = None,
        p_right: float = None,
        p_top: float = None,
        p_bottom: float = None,
        p_x: float = None,
        p_y: float = None,
        padding: float = None,
        horizontal=False,
        z_level: int = None,
        prepend=False,
        above: "BoxMixin" = None,
        below: "BoxMixin" = None,
        name: str = None,
    ) -> "Box":
        """
        Creates a new child box.

        Parameters
        ----------
        x: Union[float, str]
            X position of the box.
        y: Union[float, str]
            Y position of the box.

            Possible values: None, number, "NN", "NN%", "[NN%]", or a dynamic coordinate,
            where NN is a number.
        width: Union[float, str]
            Width of the box.
        height: Union[float, str]
            Height of the box.

            Possible values: None, number, "NN", "NN%", "fill", "fill(NN)".

        show: str
            Fragment selector that decides in which fragments should the box be visible.

            Possible values: None, a number, "XX-XX", "XX+" where XX is a number, "next" or "last"
        p_left: float
            Left padding of the box.
        p_right: float
            Right padding of the box.
        p_top: float
            Top padding of the box.
        p_bottom: float
            Bottom padding of the box.
        p_x: float
            Sets both left and right padding of the box.
        p_y: float
            Sets both top and bottom padding of the box.
        padding: float
            Sets all four padding values of the box (left, right, top, bottom):
        horizontal: bool
            If True, use horizontal layout: children will be placed in a row.
            If False, use vertical layout (the default): children will be placed in a column.
        z_level: int
            Sets the Z-level of the box.
                If None, the parent z_level will be used.
                z_level of the top-level box is 0.
                If z_level is X then all boxes with a *smaller* z_level than X is painted before
                this box.
        prepend: bool
            If True, the new box is inserted as the first child of its parent.
            Otherwise it is inserted as the last child.
        above: Box
            The new box will be inserted into its parent right after the passed box.
            The passed box has to be a child of the parent box.
        below: Box
            The new box will be inserted into its parent right before the passed box.
            The passed box has to be a child of the parent box.
        name: str
            Name of the box (used for debugging purposes).
        """
        box = self._get_box()
        layout = box.layout.add(
            x=x,
            y=y,
            width=width,
            height=height,
            p_left=p_left,
            p_right=p_right,
            p_top=p_top,
            p_bottom=p_bottom,
            p_x=p_x,
            p_y=p_y,
            padding=padding,
            horizontal=horizontal,
            prepend=prepend,
        )

        if z_level is None:
            z_level = box.z_level

        show = ShowInfo.parse(show, box.slide.max_step)
        box.slide.max_step = max(box.slide.max_step, show.max_step())

        new_box = box.__class__(box.slide, layout, box._styles, show, z_level, name)
        box.add_child(new_box, prepend, above, below)
        return new_box

    def overlay(self, **kwargs) -> "Box":
        """
        Shortcut for `box(x=0, y=0, width="100%", height="100%")`.

        The resulting box will overlay the whole area of the current box."""
        kwargs.setdefault("x", 0)
        kwargs.setdefault("y", 0)
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        return self.box(**kwargs)

    def fbox(self, **kwargs) -> "Box":
        """
        Shortcut for `box(width="fill", height="fill")`.

        fbox means "fill box"."""
        kwargs.setdefault("width", "fill")
        kwargs.setdefault("height", "fill")
        return self.box(**kwargs)

    def sbox(self, **kwargs) -> "Box":
        """
        Shortcut for `box(height="fill")` if the layout is horizontal or `box(width="fill")`
        if the layout is vertical.

        sbox means "spread box"."""
        if self._get_box().layout.horizontal:
            kwargs.setdefault("height", "fill")
        else:
            kwargs.setdefault("width", "fill")
        return self.box(**kwargs)

    def rect(
        self,
        color: str = None,
        bg_color: str = None,
        stroke_width=1,
        stroke_dasharray: str = None,
        rx: float = None,
        ry: float = None,
        rotation: float = None,
    ) -> "boxitem.BoxItem":
        """
        Draws a rectangle around the box.

        Parameters
        ----------
        color: str
            Color of the rectangle edge.
        bg_color: str
            Color of the rectangle background.
        stroke_width: float
            Width of the rectangle edge.
        stroke_dasharray: str
            SVG dash effect of the rectangle edge.
        rx: float
            x-axis radius of the rectangle. Use it if you want rounded corners.
        ry: float
            x-axis radius of the rectangle. Use it if you want rounded corners.
        rotation: float
            Rotate the rectangle by the given amount of degrees clockwise around the center of the
            rectangle.
        """

        def draw(ctx):
            rect = self._get_box().layout.rect
            ctx.draw_rect(
                rect,
                rx,
                ry,
                color=color,
                bg_color=bg_color,
                stroke_width=stroke_width,
                stroke_dasharray=stroke_dasharray,
                rotation=rotation,
            )

        return self._create_simple_box_item(draw)

    def ellipse(
        self,
        color=None,
        bg_color=None,
        stroke_width=1,
        stroke_dasharray=None,
        rotation: float = None,
    ) -> "boxitem.BoxItem":
        """
        Draws an ellipse. The dimensions of the ellipse will be set to the dimensions of its parent
        box. If you want to draw a circle, use a square parent box.

        Parameters
        ----------
        color: str
            Color of the ellipse edge.
        bg_color: str
            Color of the ellipse background.
        stroke_width: float
            Width of the ellipse edge.
        stroke_dasharray: str
            SVG dash effect of the ellipse edge.
        rotation: float
            Rotate the ellipse by the given amount of degrees clockwise around the center of the
            ellipse.
        """

        def draw(ctx):
            rect = self._get_box().layout.rect
            ctx.draw_ellipse(
                rect,
                rotation=rotation,
                color=color,
                bg_color=bg_color,
                stroke_width=stroke_width,
                stroke_dasharray=stroke_dasharray,
            )

        return self._create_simple_box_item(draw)

    def polygon(
        self,
        points,
        color: str = None,
        bg_color: str = None,
        stroke_width=1,
        stroke_dasharray: str = None,
        rotation=None,
    ) -> "boxitem.BoxItem":
        """
        Draws a polygon.

        Parameters
        ----------
        points: list
            List of points of the polygon.
            Each point can be either a 2-element tuple/list with (x, y) coordinates or a
            `value.LazyPoint`.
        color: str
            Color of the edge of the polygon.
        bg_color: str
            Color of the background of the polygon.
        stroke_width: float
            Width of the edge of the polygon.
        stroke_dasharray: str
            SVG dash effect of the edge of the polygon.
        rotation: float
            Rotate the polygon by the given amount of degrees clockwise around the centroid of the
            polygon.
        """
        points = [unpack_point(p, self) for p in points]

        def draw(ctx):
            points_values = [(eval_value(x), eval_value(y)) for x, y in points]
            ctx.draw_polygon(
                points_values,
                rotation=rotation,
                color=color,
                bg_color=bg_color,
                stroke_width=stroke_width,
                stroke_dasharray=stroke_dasharray,
            )

        return self._create_simple_box_item(draw)

    def path(
        self,
        commands,
        color="black",
        bg_color: str = None,
        stroke_width=1,
        stroke_dasharray: str = None,
        end_arrow: "arrow.Arrow" = None,
    ) -> "boxitem.BoxItem":
        """
        Draws a SVG path.

        Parameters
        ----------
        commands: List[str]
            SVG draw commands.
        color: str
            Color of the path.
        bg_color: str
            Background color of the path.
        stroke_width: float
            Width of the path.
        stroke_dasharray: str
            SVG dash effect of the path.
        end_arrow: "arrow.Arrow"
            End arrow of the path.
        """
        commands = check_and_unpack_path_commands(commands, self)
        if not commands:
            return self

        def draw(ctx):
            cmds = eval_path_commands(commands)
            if end_arrow:
                end_p1, end_p2 = path_points_for_end_arrow(cmds)
                end_new_p2 = end_arrow.move_end_point(end_p1, end_p2)
                path_update_end_point(cmds, end_new_p2)

            ctx.draw_path(
                cmds,
                color=color,
                bg_color=bg_color,
                stroke_width=stroke_width,
                stroke_dasharray=stroke_dasharray,
            )

            if end_arrow:
                end_arrow.render(ctx, end_p1, end_p2, color)

        return self._create_simple_box_item(draw)

    def line(
        self,
        points,
        color="black",
        stroke_width=1,
        stroke_dasharray: str = None,
        start_arrow: "arrow.Arrow" = None,
        end_arrow: "arrow.Arrow" = None,
    ) -> "boxitem.BoxItem":
        """
        Draws a line.

        Parameters
        ----------
        points: List[(float, float) | "value.LazyPoint"]
            List of at least two points.
        color: str
            Color of the line.
        stroke_width: float
            Width of the lne.
        stroke_dasharray: str
            SVG dash effect of the lne.
        start_arrow: "arrow.Arrow"
            Start arrow of the line.
        end_arrow: "arrow.Arrow"
            End arrow of the line.
        """

        def draw(ctx):
            p = [eval_pair(p) for p in points]
            p2 = p[:]

            if start_arrow:
                p2[0] = start_arrow.move_end_point(p[1], p[0])
            if end_arrow:
                p2[-1] = end_arrow.move_end_point(p[-2], p[-1])

            ctx.draw_polyline(
                p2,
                color=color,
                stroke_width=stroke_width,
                stroke_dasharray=stroke_dasharray,
            )

            if start_arrow:
                start_arrow.render(ctx, p[1], p[0], color)

            if end_arrow:
                end_arrow.render(ctx, p[-2], p[-1], color)

        assert len(points) >= 2
        points = [unpack_point(p, self) for p in points]
        return self._create_simple_box_item(draw)

    def _create_simple_box_item(self, render_fn):
        box = self._get_box()
        item = SimpleBoxItem(box, render_fn)
        box.add_child(item)
        return item

    def image(
        self,
        source: Union[str, BinaryIO, bytes],
        *,
        image_type: str = None,
        scale: float = None,
        fragments=True,
        show_begin=1,
        select_fragments: List[Union[int, None]] = None,
        rotation: float = None,
    ) -> "boxitem.BoxItem":
        """Draws an SVG/PNG/JPEG/ORA image, detected by the extension of the `filename`.

        Parameters
        ----------
        source: str or BinaryIO or bytes
            Filename of the image or file-like object. If file-like object is used, image_type has
            to be defined.
        image_type: str
            Possible values: "svg", "ora", "jpeg", "png" or None (= autodetect from filename).
        scale: float
            Scale of the resulting image.
            < 1.0 -> Smaller size.
            = 1.0 -> Original size.
            > 1.0 -> Larger size.
        fragments: bool
            Load fragments from the image (only applicable for SVG and ORA images).
        show_begin: int
            Fragment from which will the image fragments be shown.
            Only applicable if `fragments` is set to True.
        select_fragments: List[Union[int, None]]
            Select which fragments of the image should be drawn at the given fragments of the
            slide.

            `select_fragments=[1, 3, None, 2]`
            Would render the first image fragment in the first slide fragment, the third image
            fragment in the second slide fragment, no image fragment in the third slide fragment
            and the second image fragment in the fourth slide fragment.
        rotation: float
            Rotate the image by the given amount of degrees clockwise around the center of the
            image.
        """

        if image_type is None:
            if not isinstance(source, str):
                raise Exception(
                    "When first argument of .image() is not a filename, "
                    "then image_type has to be specified"
                )
            if source.endswith(".svg"):
                image_type = "svg"
            elif source.endswith(".ora"):
                image_type = "ora"
            elif source.endswith(".png"):
                image_type = "png"
            elif source.endswith(".jpeg") or source.endswith(".jpg"):
                image_type = "jpeg"
            else:
                raise Exception("Cannot detect image type from extension")

        if image_type == "svg":
            if not isinstance(source, str):
                raise Exception("In this version, source of SVG has to be filename")
            return self._image_svg(
                source, scale, fragments, show_begin, select_fragments, rotation
            )
        elif image_type == "ora":
            if not isinstance(source, str):
                raise Exception("In this version, source of ORA has to be filename")
            return self._image_ora(
                source, scale, fragments, show_begin, select_fragments, rotation
            )
        elif image_type == "png" or image_type == "jpeg":
            return self._image_bitmap(source, scale, rotation)
        else:
            raise Exception("Unknown image type: {}".format(image_type))

    def _image_bitmap(self, source, scale: float, rotation: float):
        if isinstance(source, str) or isinstance(source, bytes):
            key = (source, "bitmap")
            entry = self._get_box().slide.temp_cache.get(key)
        else:
            key = None
            entry = None

        if entry is None:
            data = read_helper(source)
            img = Image.open(io.BytesIO(data))
            mime = Image.MIME[img.format]
            image_width, image_height = img.size
            del img

            if key is not None:
                self._get_box().slide.temp_cache[key] = (
                    image_width,
                    image_height,
                    mime,
                    data,
                )
        else:
            image_width, image_height, mime, data = entry

        self._get_box().layout.set_image_size_request(
            image_width * (scale or 1), image_height * (scale or 1)
        )

        def draw(ctx):
            rect = self._get_box().layout.rect
            if scale is None:
                s = scaler(rect, image_width, image_height)
                if s is None:
                    s = 0
                    logging.warning(
                        "Scale of image {} is 0, set scale explicitly or set at least one "
                        "dimension for the parent box".format(source)
                    )
            else:
                s = scale

            w = image_width * s
            h = image_height * s
            x = rect.x + (rect.width - w) / 2
            y = rect.y + (rect.height - h) / 2
            ctx.draw_bitmap(
                x=x, y=y, width=w, height=h, data=data, mime=mime, rotation=rotation
            )

        return self._create_simple_box_item(draw)

    def _image_ora(
        self, filename, scale, fragments, show_begin, select_fragments, rotation
    ):
        key = (filename, "svg")
        slide = self._get_box().slide
        if key not in slide.temp_cache:

            def constructor(_content, output, _data_type):
                svg = convert_ora_to_svg(filename)
                with open(output, "w") as f:
                    f.write(svg)

            cache_file = slide.fs_cache.ensure_by_file(filename, "svg", constructor)
            self._get_box().slide.temp_cache[key] = et.parse(cache_file).getroot()
        return self._image_svg(
            filename, scale, fragments, show_begin, select_fragments, rotation
        )

    def _image_svg(
        self,
        filename: str,
        scale: float = None,
        fragments=True,
        show_begin=1,
        select_fragments: List[int] = None,
        rotation: float = None,
    ):
        key = (filename, "svg")
        root = self._get_box().slide.temp_cache.get(key)
        if root is None:
            root = et.parse(filename).getroot()
            self._get_box().slide.temp_cache[key] = root

        image_width = svg_size_to_pixels(root.get("width"))
        image_height = svg_size_to_pixels(root.get("height"))

        self._get_box().layout.set_image_size_request(
            image_width * (scale or 1), image_height * (scale or 1)
        )

        if select_fragments is not None:
            image_steps = len(select_fragments)
        else:
            if fragments:
                image_steps = get_image_steps(root)
            else:
                image_steps = 1

        self._get_box()._ensure_steps(show_begin - 1 + image_steps)

        image_data = None

        if image_steps == 1 and not select_fragments:
            image_data = et.tostring(root).decode()

        def draw(ctx):
            rect = self._get_box().layout.rect

            if image_data is None:
                step = ctx.step - show_begin + 1
                if select_fragments is not None:
                    if 0 < step <= len(select_fragments):
                        step = select_fragments[step - 1]
                    else:
                        return
                    if step is None:
                        return
                if step < 1:
                    return
                data = create_image_data(root, step)
            else:
                if ctx.step < show_begin:
                    return
                data = image_data

            if scale is None:
                s = scaler(rect, image_width, image_height)
                if s is None:
                    s = 0
                    logging.warning(
                        "Scale of image {} is 0, set scale explicitly or set at least one "
                        "dimension for the parent box".format(filename)
                    )
            else:
                s = scale

            w = image_width * s
            h = image_height * s
            x = rect.x + (rect.width - w) / 2
            y = rect.y + (rect.height - h) / 2
            ctx.draw_svg(
                svg=data,
                x=x,
                y=y,
                width=w,
                height=h,
                scale=s,
                rotation=rotation,
                rotation_center=(x + w / 2, y + h / 2),
            )

        return self._create_simple_box_item(draw)

    def code(
        self,
        language: str,
        text: str,
        *,
        tabsize=4,
        line_numbers=False,
        style="code",
        use_styles=False,
        escape_char="~",
        scale_to_fit=False,
        rotation: float = None,
    ) -> "textboxitem.TextBoxItem":
        """
        Draws a code snippet with syntax highlighting.

        Parameters
        ----------
        language: str
            Language used for syntax highlighting.
        text: str
            Content of the code snippet.
        tabsize: int
            Number of spaces generated by tab characeters.
        line_numbers: bool
            If True, line numbers will be drawn in the code snippet.
        style: str
            Name of style used for drawing the code snippet.
        use_styles: bool
            If True, inline styles will be evaluated in the code snippet.
        escape_char: str
            Escape character for creating inline styles in the code snippet.
        scale_to_fit: bool
            If True, scales the code snippet to fit its parent box.
        rotation: float
            Rotate the code snippet by the given amount of degrees clockwise around the center
            of the snippet.
        """
        text = text.replace("\t", " " * tabsize)

        if language:
            if use_styles:
                # pygments strips newlines at the beginning
                # of whole text
                # and it makes a problem with mering styles
                # therefore we strips newlines right away

                start_newlines = 0
                while text.startswith("\n"):
                    start_newlines += 1
                    text = text[1:]

                ptext = parse_text(text, escape_char)
                text = tokens_to_text_without_style(ptext)
            parsed_text = highlight_code(text, language)
            if use_styles:
                parsed_text = tokens_merge(parsed_text, ptext)
                if start_newlines:
                    parsed_text.insert(0, ("newline", start_newlines))
        else:
            parsed_text = parse_text(
                text, escape_char=escape_char if use_styles else None
            )

        if line_numbers:
            parsed_text = add_line_numbers(parsed_text)

        style = self._get_box().get_style(style, full_style=True)
        return self._text_helper(parsed_text, style, scale_to_fit, rotation)

    def text(
        self,
        text: str,
        style="default",
        *,
        escape_char="~",
        scale_to_fit=False,
        rotation: float = None,
    ) -> "textboxitem.TextBoxItem":
        """
        Draws text.

        Parameters
        ----------
        text: str
            Text content that will be drawn.
        style: str | `textstyle.TextStyle`
            Name of a style or an instance of `textstyle.TextStyle` that will be used to style the
            text.
        escape_char: str
            Escape character for creating inline styles in the text.
        scale_to_fit:
            If True, scales the text to fit its parent box.
        rotation: float
            Rotate the text by the given amount of degrees clockwise around the center of the
            text.
        """
        result_style = self._get_box().get_style(style, full_style=True)
        parsed_text = parse_text(text, escape_char=escape_char)
        return self._text_helper(parsed_text, result_style, scale_to_fit, rotation)

    def _text_helper(self, parsed_text, style, scale_to_fit, rotation=None):
        box = self._get_box()
        item = TextBoxItem(box, parsed_text, style, box._styles, scale_to_fit, rotation)
        box.add_child(item)
        return item

    def x(self, value) -> "lazy.LazyValue":
        """Create a lazy value relative to the left edge of the box."""
        return self._get_box().layout.x(value)

    def y(self, value) -> "lazy.LazyValue":
        """Create a lazy value relative to the top edge of the box."""
        return self._get_box().layout.y(value)

    def p(self, x, y) -> "lazy.LazyPoint":
        """Create a lazy point relative to the top-left corner of the box."""
        return self._get_box().layout.point(x, y)

    def mid_point(self) -> "lazy.LazyPoint":
        """Create a lazy point that resolves to the center of the box."""
        return self.p("50%", "50%")


from ..text.textboxitem import TextBoxItem  # noqa
from .boxitem import SimpleBoxItem  # noqa
