class Style:
    def __init__(self,
                 bold=None,
                 size=None,
                 italic=None,
                 font=None,
                 color=None,
                 line_spacing=None,
                 align=None):
        self.bold = bold
        self.size = size
        self.italic = italic
        self.font = font
        self.color = color
        self.line_spacing = line_spacing
        self.align = align

    def update(self,
               bold=None,
               size=None,
               italic=None,
               font=None,
               color=None,
               line_spacing=None,
               align=None):
        data = self.to_dict()
        params = {
            "bold": bold,
            "size": size,
            "italic": italic,
            "font": font,
            "color": color,
            "line_spacing": line_spacing,
            "align": align
        }
        data.update({k: v for (k, v) in params.items() if v is not None})

        return Style(**data)

    def update_from(self, style):
        return self.update(**style.to_dict())

    def to_dict(self):
        return {
            "bold": self.bold,
            "size": self.size,
            "italic": self.italic,
            "font": self.font,
            "color": self.color,
            "line_spacing": self.line_spacing,
            "align": self.align
        }
