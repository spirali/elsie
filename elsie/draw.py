def set_font_from_style(xml, style):
    if "font" in style:
        xml.set("font-family", style["font"])
    if "size" in style:
        xml.set("font-size", style["size"])

    s = ""
    if "color" in style:
        s += "fill:{};".format(style["color"])
    if style.get("bold", False):
        s += "font-weight: bold;"
    if style.get("italic", False):
        s += "font-style: italic;"
    if s:
        xml.set("style", s)


def draw_text(xml, x, y, parsed_text, style, styles, id=None, id_index=None):
    xml.element("text")

    if id is not None and id_index is None:
        xml.set("id", id)

    xml.set("x", x)
    xml.set("y", y)

    anchor = {
        "left": "start",
        "middle": "middle",
        "right": "end"
    }

    xml.set("text-anchor", anchor[style["align"]])

    set_font_from_style(xml, style)

    line_size = style["size"] * style["line_spacing"]
    active_styles = [style]

    xml.element("tspan")

    for i, (token_type, value) in enumerate(parsed_text):
        if token_type == "text":
            xml.text(value)
        elif token_type == "newline":
            for s in active_styles:
                xml.close("tspan")  # tspan
            for i, s in enumerate(active_styles):
                if s is None:
                    continue
                xml.element("tspan")
                xml.set("xml:space", "preserve")
                if i == 0:
                    xml.set("x", x)
                    xml.set("dy", line_size * value)
                set_font_from_style(xml, s)
        elif token_type == "begin":
            is_dummy = value and value[0] == "#"
            s = styles.get(value, None)
            if s is None and not is_dummy:
                raise Exception("Style '{}' not found".format(value))
            active_styles.append(s)
            xml.element("tspan")
            if id is not None and id_index == i:
                xml.set("id", id)
            xml.set("xml:space", "preserve")
            if not is_dummy:
                set_font_from_style(xml, s)
        elif token_type == "end":
            xml.close("tspan")
            active_styles.pop()
        else:
            raise Exception("Invalid token")

    for s in active_styles:
        if s is not None:
            xml.close("tspan")
    xml.close("text")


def draw_bitmap(xml, x, y, width, height, mime, data):
    xml.element("image")
    xml.set("x", x)
    xml.set("y", y)
    xml.set("width", width)
    xml.set("height", height)
    xml.set("xlink:href", "data:{};base64,{}".format(mime, data), escape=False)
    xml.close("image")
