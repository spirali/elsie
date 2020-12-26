import copy


def _check_string(name, value):
    if value is not None and not isinstance(value, str):
        raise Exception(
            "Attribute '{}' has to be a string or None, not {}.".format(
                name, repr(type(value))
            )
        )
    return value


def _check_number(name, value):
    if (
        value is not None
        and not isinstance(value, int)
        and not isinstance(value, float)
    ):
        raise Exception(
            "Attribute '{}' has to be a number or None, not {}.".format(
                name, repr(type(value))
            )
        )
    return value


def _check_bool(name, value):
    if value is not None and not isinstance(value, bool):
        raise Exception(
            "Attribute '{}' has to be a bool or None, not {}.".format(
                name, repr(type(value))
            )
        )
    return value


def _check_choice(name, value, choices):
    if value not in choices:
        raise Exception(
            "Attribute '{}' has to be one of {}, not {}.".format(
                name, choices, repr(value)
            )
        )
    return value


class TextStyle:
    """
    Holds information about the style of text.
    """

    ALIGN_VALUES = (None, "left", "middle", "right")
    VARIANT_NUMERIC_VALUES = (
        None,
        "normal",
        "ordinal",
        "slashed-zero",
        "lining-nums",
        "oldstyle-nums",
        "proportinal-nums",
        "tabular-nums",
        "diagonal-fractions",
        "stacked-fractions",
    )

    __slots__ = (
        "_font",
        "_size",
        "_align",
        "_line_spacing",
        "_color",
        "_bold",
        "_italic",
        "_variant_numeric",
    )

    def __init__(
        self,
        *,
        font=None,
        size=None,
        align=None,
        line_spacing=None,
        color=None,
        bold=None,
        italic=None,
        variant_numeric=None
    ):
        """
        Parameters
        ----------
        font: str
            Font used to render the text.
        size: float
            Size of the font.
        align: {"center", "left", "right"}
            Alignment of the text.
        line_spacing: float
            Space between lines. Scales with font size.
        color: str
            Color of the text.
        bold: bool
            If True, the text will be rendered as bold.
        italic: bool
            If True, the text will be rendered as italic.
        variant_numeric: str
            SVG mode for rendering of digits (e.g. "lining-nums").
        """
        self.font = font
        self.size = size
        self.align = align
        self.line_spacing = line_spacing
        self.color = color
        self.bold = bold
        self.italic = italic
        self.variant_numeric = variant_numeric

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = _check_string("font", value)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = _check_number("size", value)

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        self._align = _check_choice("align", value, self.ALIGN_VALUES)

    @property
    def line_spacing(self):
        return self._line_spacing

    @line_spacing.setter
    def line_spacing(self, value):
        self._line_spacing = _check_number("line_spacing", value)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = _check_string("color", value)

    @property
    def bold(self):
        return self._bold

    @bold.setter
    def bold(self, value):
        self._bold = _check_bool("bold", value)

    @property
    def italic(self):
        return self._italic

    @italic.setter
    def italic(self, value):
        self._italic = _check_bool("italic", value)

    @property
    def variant_numeric(self):
        return self._variant_numeric

    @variant_numeric.setter
    def variant_numeric(self, value):
        self._variant_numeric = _check_choice(
            "variant_numeric", value, self.VARIANT_NUMERIC_VALUES
        )

    def copy(self) -> "TextStyle":
        """Copies the text style."""
        return copy.copy(self)

    def update(self, style: "TextStyle"):
        """Updates the text style in-place."""
        assert isinstance(style, TextStyle)
        for slot in self.__slots__:
            value = getattr(style, slot)
            if value is not None:
                setattr(self, slot, value)

    def compose(self, style: "TextStyle") -> "TextStyle":
        """Create a new style that will be the combination of the current and the given style."""
        copy = self.copy()
        copy.update(style)
        return copy


def compose_style(styles, style, full_style):
    if isinstance(style, str):
        style_name = style
        style = styles.get(style_name)
        if style is None:
            raise Exception("Style '{}' not found".format(style_name))
        if style_name == "default":
            return style.copy()
    elif not isinstance(style, TextStyle):
        raise Exception("Invalid type used as a style: {}".format(repr(type(style))))

    if not full_style:
        return style.copy()

    return styles["default"].compose(style)
