import lxml.etree as et

from .geom import Rect
from .draw import draw_text
from .sxml import Xml
from .textparser import parse_text, number_of_lines, add_line_numbers
from .textstyle import check_style
from .highlight import highlight_code
from .show import ShowInfo
from .image import get_image_steps, create_image_data
from .svg import svg_size_to_pixels
from .lazy import LazyValue, eval_value, LazyPoint, unpack_point
from .value import SizeValue, PosValue
from .latex import render_latex
from .query import Query

class Painter:

    def __init__(self, fn, rect, z_level):
        self.fn = fn
        self.z_level = z_level
        self.rect = rect

    def render(self, ctx):
        self.fn(ctx, self.rect)


def set_paint_style(xml, color, bg_color, stroke_width, stroke_dasharray):
    styles = []
    if bg_color:
        styles.append("fill:{}".format(bg_color))
    else:
        styles.append("fill:none")

    if color:
        styles.append("stroke:{}".format(color))
        styles.append("stroke-width:{}".format(stroke_width))
        if stroke_dasharray:
            styles.append("stroke-dasharray:{}".format(stroke_dasharray))
    else:
        styles.append("stroke:none")

    xml.set("style", ";".join(styles))


class Box:

    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 styles,
                 show_info,
                 p_left=0,
                 p_right=0,
                 p_top=0,
                 p_bottom=0,
                 horizontal=False,
                 z_level=0):

        if x is not None:
            self._x = PosValue.parse(x)
        else:
            self._x = None

        if y is not None:
            self._y = PosValue.parse(y)
        else:
            self._y = None

        self._width = SizeValue.parse(width or 0)
        self._height = SizeValue.parse(height or 0)
        self.childs = []
        self._rect = None
        self._queries = []
        self._styles = styles
        self._show_info = show_info
        self._text_lines = 0
        self._text_height = 0

        self.p_left = p_left
        self.p_right = p_right
        self.p_top = p_top
        self.p_bottom = p_bottom

        self.horizontal = horizontal
        self.z_level = z_level

    def box(self,
            x=None,
            y=None,
            width=None,
            height=None,
            show=None,
            p_left=None,       # padding left
            p_right=None,      # padding right
            p_top=None,        # padding top
            p_bottom=None,     # padding bottom
            p_x=None,          # horizontal padding (sets p_left & p_right)
            p_y=None,          # vertical padding (sets p_top & p_bottom)
            padding=None,      # sets the same padding to all directions
            horizontal=False,
            z_level=None):
        """ Create a new child box """

        def set_padding(a, b):
            if a is not None:
                return a
            if b is not None:
                return b
            return padding or 0

        p_left = set_padding(p_left, p_x)
        p_right = set_padding(p_right, p_x)
        p_top = set_padding(p_top, p_y)
        p_bottom = set_padding(p_bottom, p_y)

        if z_level is None:
            z_level = self.z_level

        box = Box(x,
                  y,
                  width,
                  height,
                  self._styles.copy(),
                  ShowInfo.parse(show),
                  p_left,
                  p_right,
                  p_top,
                  p_bottom,
                  horizontal,
                  z_level)
        self.add_child(box)
        return box

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
        """ /Spread box/ - Alias over 'box()' that sets width/height to "fill"
            if vertical/horizontal """
        if self.horizontal:
            kwargs.setdefault("height", "fill")
        else:
            kwargs.setdefault("width", "fill")
        return self.box(**kwargs)

    def line_box(self, index, lines=1, **kwargs):
        """ Create a box around a line of text.
            'self' has to contain a text """
        def compute_y():
            if not self._text_lines:
                raise Exception("line_box() called on box with no text")
            line_height = self._text_height / self._text_lines
            y = self._rect.y + (self._rect.height - self._text_height) / 2
            return y + line_height * index

        def compute_height():
            if not self._text_lines:
                raise Exception("line_box() called on box with no text")
            return lines * self._text_height / self._text_lines + 1

        kwargs.setdefault("width", "fill")
        kwargs.setdefault("x", 0)
        kwargs.setdefault("y", LazyValue(compute_y))
        kwargs.setdefault("height", LazyValue(compute_height))
        return self.box(**kwargs)

    def rect(self,
             color=None, bg_color=None,
             stroke_width=1, stroke_dasharray=None,
             rx=None, ry=None):
        """ Draw a rect around the box """

        def draw_rect(ctx, rect):
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
        self.add_child(draw_rect)

    def polygon(self,
                points,
                color=None, bg_color=None,
                stroke_width=1, stroke_dasharray=None):
        """ Draw a polygon """

        def draw_rect(ctx, rect):
            xml = ctx.xml
            xml.element("polygon")
            xml.set("points", " ".join("{},{}".format(
                eval_value(x), eval_value(y)) for x, y in points))
            set_paint_style(xml, color, bg_color, stroke_width, stroke_dasharray)
            xml.close("polygon")
        points = [unpack_point(p) for p in points]
        self.add_child(draw_rect)

    def line(self, points, color="black", stroke_width=1, stroke_dasharray=None,
             start_arrow=None, end_arrow=None):
        """ Draw a line """

        def draw_rect(ctx, rect):
            p = [(eval_value(x), eval_value(y)) for x, y in points]
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
        points = [unpack_point(p) for p in points]
        self.add_child(draw_rect)

    def _render_svg(self, ctx, x, y, scale, data):
        ctx.xml.element("g")
        transform = ["translate({}, {})".format(x, y)]
        if scale != 1.0:
            transform.append("scale({})".format(scale))
        ctx.xml.set("transform", " ".join(transform))
        ctx.xml.raw_text(data)
        ctx.xml.close()

    def image(self, filename, scale=None, fragments=True, show_begin=1):
        """ Draw an svg image """

        root = et.parse(filename).getroot()
        image_width = svg_size_to_pixels(root.get("width"))
        image_height = svg_size_to_pixels(root.get("height"))

        if fragments:
            image_steps = get_image_steps(root)
        else:
            image_steps = 1

        self._show_info = self._show_info.ensure_steps(
            show_begin + image_steps - 1)

        image_data = None
        if image_steps == 1:
            image_data = et.tostring(root).decode()

        def draw(ctx, rect):
            if image_data is None:
                step = ctx.step - show_begin + 1
                if step < 1:
                    return
                data = create_image_data(root, ctx.step - show_begin + 1)
            else:
                if ctx.step < show_begin:
                    return
                data = image_data

            if scale is None:
                scale_x = rect.width / image_width
                scale_y = rect.height / image_height
                s = min(scale_x, scale_y)
            else:
                s = scale
            w = image_width * s
            h = image_height * s
            x = rect.x + (rect.width - w) / 2
            y = rect.y + (rect.height - h) / 2
            self._render_svg(ctx, x, y, s, data)

        self.add_child(draw)

    def code(self, language, text, tabsize=4, line_numbers=False):
        """ Draw a code with syntax highlighting """

        text = text.replace("\t", " " * tabsize)
        if language:
            parsed_text = highlight_code(text, language)
        else:
            parsed_text = parse_text(text, escape_char=None)

        if line_numbers:
            parsed_text = add_line_numbers(parsed_text)

        style = self._styles["code"]
        self._text_helper(parsed_text, style)

    def _get_style(self, style):
        result_style = self._styles["default"]
        if style == "default":
            return result_style
        elif isinstance(style, str):
            style_name = style
            style = self._styles.get(style_name)
            if style is None:
                raise Exception("Style '{}' not found".format(style_name))
        elif isinstance(style, dict):
            check_style(style)
        else:
            raise Exception("Invalid type used as style")
        result_style = result_style.copy()
        result_style.update(style)
        return result_style

    def text(self, text, style="default", escape_char="~"):
        """ Draw a text

            "style" can be string with the name of style or dict defining the style
        """
        result_style = self._get_style(style)
        parsed_text = parse_text(text, escape_char=escape_char)
        self._text_helper(parsed_text, result_style)

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

            self._ensure_width(svg_width)
            self._ensure_height(svg_height)

            container[0] = svg_width
            container[1] = svg_height
            container[2] = svg

        def draw(ctx, rect):
            svg_width, svg_height, data = container
            x = rect.x + (rect.width - svg_width) / 2
            y = rect.y + (rect.height - svg_height) / 2
            self._render_svg(ctx, x, y, scale, data)

        self._queries.append(Query(("latex", tex_text), on_query))
        self.add_child(draw)

    def new_style(self, name, **kwargs):
        """ Define a new style, it is an error if it already exists. """
        if name in self._styles:
            raise Exception("Style already exists")
        check_style(kwargs)
        self._styles[name] = kwargs

    def update_style(self, name, **kwargs):
        """ Update a style, it is an error if style does not exists. """
        check_style(kwargs)
        new_style = self._styles[name].copy()
        new_style.update(kwargs)
        self._styles[name] = new_style

    def derive_style(self, old_style_name, new_style_name, **kwargs):
        """ Copy an existing style under a new name and modify it. """
        check_style(kwargs)
        new_style = self._styles[old_style_name].copy()
        new_style.update(kwargs)
        self._styles[new_style_name] = new_style

    def x(self, value):
        """ Create position on x-axis relative to the box """
        value = PosValue.parse(value)
        return LazyValue(
            lambda: value.compute(self._rect.x, self._rect.width, 0))

    def y(self, value):
        """ Create position on y-axis relative to the box """
        value = PosValue.parse(value)
        return LazyValue(
            lambda: value.compute(self._rect.y, self._rect.height, 0))

    def p(self, x, y):
        """ Create a point realtive to the box """
        return LazyPoint(self.x(x), self.y(y))

    def mid_point(self):
        """ Create a point in the center of the box """
        return self.p("50%", "50%")

    def add_child(self, obj):
        """ Semi-internal function, you can add your child if you know
            what you are doing. """
        self.childs.append(obj)

    def _min_child_size(self):
        managed_childs = self._managed_childs
        if not managed_childs:
            return (0, 0)
        rqs = [c._compute_size_request() for c in managed_childs]
        if not self.horizontal:
            return (max(rq[0].min_size for rq in rqs),
                    sum(rq[1].min_size for rq in rqs))
        else:
            return (sum(rq[0].min_size for rq in rqs),
                    max(rq[1].min_size for rq in rqs))

    def _compute_size_request(self):
        minx, miny = self._min_child_size()
        minx += self.p_left + self.p_right
        miny += self.p_top + self.p_bottom
        return (self._width.ensure(minx), self._height.ensure(miny))

    def _ensure_width(self, width):
        self._width = self._width.ensure(width + self.p_left + self.p_right)

    def _ensure_height(self, height):
        self._height = self._height.ensure(height + self.p_top + self.p_bottom)

    def _text_helper(self, parsed_text, style):
        def on_query(width):
            line_height = style["size"] * style["line_spacing"]
            height = lines * line_height
            self._ensure_width(width)
            self._ensure_height(height)

            real_size[0] = width
            real_size[1] = height
            self._text_height = height

        def draw(ctx, rect):
            y = rect.y + (rect.height - real_size[1]) / 2 + style["size"]
            if style["align"] == "left":
                x = rect.x
            elif style["align"] == "middle":
                x = rect.x + rect.width / 2
            elif style["align"] == "right":
                x = rect.x + rect.width
            else:
                raise Exception(
                    "Invalid value of align: " + repr(style["align"]))
            draw_text(ctx.xml, x, y, parsed_text, style, self._styles)

        lines = number_of_lines(parsed_text)
        self._text_lines = lines

        real_size = [None, None]
        xml = Xml()
        draw_text(xml, 0, 0, parsed_text, style, self._styles, id="target")
        self._queries.append(Query(("inkscape", xml.to_string()), on_query))
        self.add_child(draw)

    def _set_rect(self, rect):
        rect = rect.shrink(
            self.p_left, self.p_right, self.p_top, self.p_bottom)
        self._rect = rect

        if not self.horizontal:
            axis = 1
            rect_size = rect.height
            rect_start = rect.y
        else:
            axis = 0
            rect_size = rect.width
            rect_start = rect.x

        fills = 0
        free = rect_size

        for child in self._managed_childs:
            rq = child._compute_size_request()[axis]
            if rq.fill:
                fills += rq.fill
            elif rq.ratio:
                free -= max(rq.min_size, rq.ratio * rect_size)
            else:
                free -= rq.min_size

        if fills:
            fill_unit = free / fills
            free = 0
        else:
            fill_unit = 0

        dd = rect_start + free / 2  # dynamic dimension

        for child in self._box_childs:
            w, h = child._compute_size_request()
            if not self.horizontal:
                w = w.compute(rect.width, None)
                h = h.compute(rect.height, fill_unit)
                if child._x is not None:
                    x = child._x.compute(rect.x, rect.width, w)
                else:
                    x = rect.x + (rect.width - w) / 2
                if child._y is None:
                    y = dd
                    dd += h
                else:
                    y = child._y.compute(rect.y, rect.height, h)
            else:
                w = w.compute(rect.width, fill_unit)
                h = h.compute(rect.height, None)
                if child._y is not None:
                    y = child._y.compute(rect.y, rect.width, h)
                else:
                    y = rect.y + (rect.height - h) / 2
                if child._x is None:
                    x = dd
                    dd += w
                else:
                    x = child._x.compute(rect.x, rect.width, w)
            child._set_rect(Rect(x, y, w, h))

    @property
    def _managed_childs(self):
        if not self.horizontal:
            return [child for child in self.childs
                    if isinstance(child, Box) and child._y is None]
        else:
            return [child for child in self.childs
                    if isinstance(child, Box) and child._x is None]

    @property
    def _box_childs(self):
        return [child for child in self.childs if isinstance(child, Box)]

    def _min_steps(self):
        return self._show_info.min_steps()

    def _get_painters(self, ctx):
        painters = []
        if not self._show_info.is_visible(ctx.step):
            return painters
        for child in self.childs:
            if not isinstance(child, Box):
                painters.append(Painter(child, self._rect, self.z_level))
            else:
                painters += child._get_painters(ctx)
        return painters

    def _traverse(self, fn):
        fn(self)
        for child in self._box_childs:
            child._traverse(fn)
