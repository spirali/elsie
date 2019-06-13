def set_font_from_style(xml, style):
    if style.font is not None:
        xml.set("font-family", style.font)
    if style.size is not None:
        xml.set("font-size", style.size)

    s = ""
    if style.color is not None:
        s += "fill:{};".format(style.color)
    if style.bold:
        s += "font-weight: bold;"
    if style.italic:
        s += "font-style: italic;"
    if s:
        xml.set("style", s)


def draw_text(xml, x, y, parsed_text, style, styles, id=None):
    xml.element("text")

    if id is not None:
        xml.set("id", id)

    xml.set("x", x)
    xml.set("y", y)

    anchor = {
        "left": "start",
        "middle": "middle",
        "right": "end"
    }

    xml.set("text-anchor", anchor[style.align])

    set_font_from_style(xml, style)

    line_size = style.size * style.line_spacing
    active_styles = [style]

    xml.element("tspan")

    for token_type, value in parsed_text:
        if token_type == "text":
            xml.text(value)
        elif token_type == "newline":
            for s in active_styles:
                xml.close("tspan")  # tspan
            for i, s in enumerate(active_styles):
                xml.element("tspan")
                xml.set("xml:space", "preserve")
                if i == 0:
                    xml.set("x", x)
                    xml.set("dy", line_size * value)
                set_font_from_style(xml, s)
        elif token_type == "begin":
            s = styles[value]
            active_styles.append(s)
            xml.element("tspan")
            xml.set("xml:space", "preserve")
            set_font_from_style(xml, s)
        elif token_type == "end":
            xml.close("tspan")
            active_styles.pop()
        else:
            raise Exception("Invalid token")

    for s in active_styles:
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
