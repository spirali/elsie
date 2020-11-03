import base64
import io
import logging

import lxml.etree as et
from PIL import Image

from .draw import draw_bitmap
from .draw import set_paint_style
from .highlight import highlight_code
from .image import get_image_steps, create_image_data
from .lazy import eval_value, unpack_point, eval_pair
from .path import (
    check_and_unpack_path_commands,
    eval_path_commands,
    path_points_for_end_arrow,
    path_update_end_point,
)

from .show import ShowInfo
from .svg import svg_size_to_pixels
from .textparser import parse_text, add_line_numbers
from .textparser import tokens_merge, tokens_to_text_without_style
from .ora import convert_ora_to_svg


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
    def _get_box(self):
        raise NotImplementedError

    def box(
        self,
        x=None,
        y=None,
        width=None,
        height=None,
        *,
        show=None,
        p_left=None,  # padding left
        p_right=None,  # padding right
        p_top=None,  # padding top
        p_bottom=None,  # padding bottom
        p_x=None,  # horizontal padding (sets p_left & p_right)
        p_y=None,  # vertical padding (sets p_top & p_bottom)
        padding=None,  # sets the same padding to all directions
        horizontal=False,
        z_level=None,
        prepend=False,
        above=None,
        below=None,
        name=None,
    ):
        """ Create a new child box """
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

    def overlay(self, **kwargs):
        """ Alias over 'box()' that creates a fixed box over the box """
        kwargs.setdefault("x", 0)
        kwargs.setdefault("y", 0)
        kwargs.setdefault("width", "100%")
        kwargs.setdefault("height", "100%")
        return self.box(**kwargs)

    def fbox(self, **kwargs):
        """ Alias over 'box()' that sets width and height to "fill" """
        kwargs.setdefault("width", "fill")
        kwargs.setdefault("height", "fill")
        return self.box(**kwargs)

    def sbox(self, **kwargs):
        """/Spread box/ - Alias over 'box()' that sets width/height to "fill"
        if vertical/horizontal"""
        if self.layout.horizontal:
            kwargs.setdefault("height", "fill")
        else:
            kwargs.setdefault("width", "fill")
        return self.box(**kwargs)

    def rect(
        self,
        color=None,
        bg_color=None,
        stroke_width=1,
        stroke_dasharray=None,
        rx=None,
        ry=None,
    ):
        """ Draw a rect around the box """

        def draw(ctx):
            rect = self._get_box().layout.rect
            xml = ctx.xml
            xml.element("rect")
            xml.set("x", rect.x)
            xml.set("y", rect.y)
            xml.set("width", rect.width)
            xml.set("height", rect.height)
            if rx:
                xml.set("rx", rx)
            if ry:
                xml.set("ry", ry)
            set_paint_style(xml, color, bg_color, stroke_width, stroke_dasharray)
            xml.close("rect")

        return self._create_simple_box_item(draw)

    def polygon(
        self, points, color=None, bg_color=None, stroke_width=1, stroke_dasharray=None
    ):
        """ Draw a polygon """

        def draw(ctx):
            xml = ctx.xml
            xml.element("polygon")
            xml.set(
                "points",
                " ".join(
                    "{},{}".format(eval_value(x), eval_value(y)) for x, y in points
                ),
            )
            set_paint_style(xml, color, bg_color, stroke_width, stroke_dasharray)
            xml.close("polygon")

        points = [unpack_point(p, self) for p in points]
        return self._create_simple_box_item(draw)

    def path(
        self,
        commands,
        color="black",
        bg_color=None,
        stroke_width=1,
        stroke_dasharray=None,
        end_arrow=None,
    ):
        commands = check_and_unpack_path_commands(commands, self)
        if not commands:
            return

        def command_to_str(command):
            name, pairs = command
            return name + " ".join("{},{}".format(p[0], p[1]) for p in pairs)

        def draw(ctx):
            cmds = eval_path_commands(commands)
            if end_arrow:
                end_p1, end_p2 = path_points_for_end_arrow(cmds)
                end_new_p2 = end_arrow.move_end_point(end_p1, end_p2)
                path_update_end_point(cmds, end_new_p2)

            xml = ctx.xml
            xml.element("path")
            xml.set("d", " ".join(command_to_str(c) for c in cmds))
            set_paint_style(xml, color, bg_color, stroke_width, stroke_dasharray)
            xml.close("path")

            if end_arrow:
                end_arrow.render(xml, end_p1, end_p2, color)

        return self._create_simple_box_item(draw)

    def line(
        self,
        points,
        color="black",
        stroke_width=1,
        stroke_dasharray=None,
        start_arrow=None,
        end_arrow=None,
    ):
        """ Draw a line """

        def draw(ctx):
            p = [eval_pair(p) for p in points]
            p2 = p[:]

            if start_arrow:
                p2[0] = start_arrow.move_end_point(p[1], p[0])
            if end_arrow:
                p2[-1] = end_arrow.move_end_point(p[-2], p[-1])

            xml = ctx.xml
            xml.element("polyline")
            xml.set("points", " ".join("{},{}".format(x, y) for x, y in p2))
            set_paint_style(xml, color, None, stroke_width, stroke_dasharray)
            xml.close("polyline")

            if start_arrow:
                start_arrow.render(xml, p[1], p[0], color)

            if end_arrow:
                end_arrow.render(xml, p[-2], p[-1], color)

        assert len(points) >= 2
        points = [unpack_point(p, self) for p in points]
        return self._create_simple_box_item(draw)

    def _create_simple_box_item(self, render_fn):
        box = self._get_box()
        item = SimpleBoxItem(box, render_fn)
        box.add_child(item)
        return item

    def _render_svg(self, ctx, x, y, scale, data):
        ctx.xml.element("g")
        transform = ["translate({}, {})".format(x, y)]
        if scale != 1.0:
            transform.append("scale({})".format(scale))
        ctx.xml.set("transform", " ".join(transform))
        ctx.xml.raw_text(data)
        ctx.xml.close()

    def image(
        self, filename, scale=None, fragments=True, show_begin=1, select_steps=None
    ):
        """ Draw an svg/png/jpeg image, detect by extension """
        if filename.endswith(".svg"):
            return self._image_svg(filename, scale, fragments, show_begin, select_steps)
        elif filename.endswith(".ora"):
            return self._image_ora(filename, scale, fragments, show_begin, select_steps)
        elif any(filename.endswith(ext) for ext in [".png", ".jpeg", ".jpg"]):
            return self._image_bitmap(filename, scale)
        else:
            raise Exception("Unkown image extension")

    def _image_bitmap(self, filename, scale):
        key = (filename, "bitmap")
        entry = self._get_box().slide.temp_cache.get(key)

        if entry is None:
            with open(filename, "rb") as f:
                data = f.read()

            img = Image.open(io.BytesIO(data))
            mime = Image.MIME[img.format]
            image_width, image_height = img.size
            del img

            data = base64.b64encode(data).decode("ascii")
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
                        "dimension for the parent box".format(filename)
                    )
            else:
                s = scale

            w = image_width * s
            h = image_height * s
            x = rect.x + (rect.width - w) / 2
            y = rect.y + (rect.height - h) / 2
            draw_bitmap(ctx.xml, x, y, w, h, mime, data)

        return self._create_simple_box_item(draw)

    def _image_ora(self, filename, scale, fragments, show_begin, select_steps):
        key = (filename, "svg")
        slide = self._get_box().slide
        if key not in slide.temp_cache:

            def constructor(_content, output):
                svg = convert_ora_to_svg(filename)
                with open(output, "w") as f:
                    f.write(svg)

            cache_file = slide.fs_cache.ensure_by_file(filename, "svg", constructor)
            self._get_box().slide.temp_cache[key] = et.parse(cache_file).getroot()
        return self._image_svg(filename, scale, fragments, show_begin, select_steps)

    def _image_svg(
        self, filename, scale=None, fragments=True, show_begin=1, select_steps=None
    ):
        """ Draw an svg image """

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

        if select_steps is not None:
            image_steps = len(select_steps)
        else:
            if fragments:
                image_steps = get_image_steps(root)
            else:
                image_steps = 1

        self._get_box()._ensure_steps(show_begin - 1 + image_steps)

        image_data = None

        if image_steps == 1 and not select_steps:
            image_data = et.tostring(root).decode()

        def draw(ctx):
            rect = self._get_box().layout.rect

            if image_data is None:
                step = ctx.step - show_begin + 1
                if select_steps is not None:
                    if 0 < step <= len(select_steps):
                        step = select_steps[step - 1]
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
            self._render_svg(ctx, x, y, s, data)

        return self._create_simple_box_item(draw)

    def code(
        self,
        language,
        text,
        *,
        tabsize=4,
        line_numbers=False,
        style="code",
        use_styles=False,
        escape_char="~",
        scale_to_fit=False,
    ):
        """ Draw a code with syntax highlighting """

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

        style = self._get_box().get_style(style)
        return self._text_helper(parsed_text, style, scale_to_fit)

    def text(self, text, style="default", *, escape_char="~", scale_to_fit=False):
        """Draw a text

        "style" can be string with the name of style or dict defining the style
        """
        result_style = self._get_box().get_style(style)
        parsed_text = parse_text(text, escape_char=escape_char)
        return self._text_helper(parsed_text, result_style, scale_to_fit)

    def _text_helper(self, parsed_text, style, scale_to_fit):
        box = self._get_box()
        item = TextBoxItem(box, parsed_text, style, box._styles, scale_to_fit)
        box.add_child(item)
        return item

    def latex(self, text, scale=1.0, header=None, tail=None):
        """ Renders LaTeX text into box. """

        if header is None:
            header = """
\\documentclass[varwidth,border=1pt]{standalone}
\\usepackage[utf8x]{inputenc}
\\usepackage{ucs}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\begin{document}"""

        if tail is None:
            tail = "\\end{document}"

        tex_text = "\n".join((header, text, tail))

        container = [None, None, None]

        def on_query(svg):
            root = et.fromstring(svg)
            svg_width = svg_size_to_pixels(root.get("width")) * scale
            svg_height = svg_size_to_pixels(root.get("height")) * scale

            self._get_box().layout.ensure_width(svg_width)
            self._get_box().layout.ensure_height(svg_height)

            container[0] = svg_width
            container[1] = svg_height
            container[2] = svg

        def draw(ctx):
            rect = self._get_box().layout.rect
            svg_width, svg_height, data = container
            x = rect.x + (rect.width - svg_width) / 2
            y = rect.y + (rect.height - svg_height) / 2
            self._render_svg(ctx, x, y, scale, data)

        self._get_box().slide.add_query("latex", tex_text, on_query)
        return self._create_simple_box_item(draw)

    def x(self, value):
        """ Create position on x-axis relative to the box """
        return self._get_box().layout.x(value)

    def y(self, value):
        """ Create position on y-axis relative to the box """
        return self._get_box().layout.y(value)

    def p(self, x, y):
        """ Create a point relative to the box """
        return self._get_box().layout.point(x, y)

    def mid_point(self):
        """ Create a point in the center of the box """
        return self.p("50%", "50%")


from .boxitem import SimpleBoxItem  # noqa
from .textboxitem import TextBoxItem  # noqa
