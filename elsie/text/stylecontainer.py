from typing import Union

from .textstyle import TextStyle, compose_style


class StyleContainer:
    def __init__(self, styles):
        self._styles = styles

    def has_style(self, style_name: str) -> bool:
        """Returns True if the box has a style with the given name."""
        return style_name in self._styles

    def update_style(self, style_name: str, style: TextStyle) -> TextStyle:
        """Updates the style associated with the given name and returns it."""
        assert isinstance(style_name, str)
        old_style = self.get_style(style_name, full_style=False)
        old_style.update(style)
        self._styles = self._styles.copy()
        self._styles[style_name] = old_style
        return old_style

    def set_style(self, style_name: str, style: TextStyle, base="default"):
        """
        Assigns the style to the given name.
        If `base` is specified, the style will be first composed with `base`.

        Parameters
        ----------
        style_name: str
            Name of the style.
        style: TextStyle
            Definition of the style.
        base: str
            Name of a style that will be composed with the given style.
        """
        assert isinstance(style_name, str)
        assert isinstance(style, TextStyle)
        if base != "default":
            base_style = self.get_style(base)
            base_style.update(style)
            style = base_style
        self._styles = self._styles.copy()
        self._styles[style_name] = style
        return style

    def get_style(self, style: Union[str, TextStyle], full_style=False) -> TextStyle:
        """
        Returns a style associated with the given name.

        If `full_style=True`, you can also pass a text style to this function to compose it with
        the default style.
        """
        return compose_style(self._styles, style, full_style)
