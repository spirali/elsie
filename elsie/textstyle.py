
attributes = ("font",
              "size",
              "align",
              "line_spacing",
              "color",
              "bold",
              "italic")


def check_style(style):
    # TODO: Check type of values
    for key in style:
        if key not in attributes:
            raise Exception("Invalid attribute of style:", key)
