from pygments import highlight
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

from .style import Style
from .textparser import normalize_tokens, NEWLINE_1


class MyFormatter(Formatter):

    def __init__(self):
        super().__init__()
        self.stream = []

    def format(self, tokensource, outfile):
        stream = self.stream
        for ttype, value in tokensource:
            if value == "\n":
                stream.append(NEWLINE_1)
            else:
                stream.append(("begin", "pygments-" + str(ttype)))
                if value.endswith("\n"):
                    stream.append(("text", value[:-1]))
                    stream.append(NEWLINE_1)
                else:
                    stream.append(("text", value))
                stream.append(("end", None))


def highlight_code(code, language):
    lexer = get_lexer_by_name(language)
    formatter = MyFormatter()
    highlight(code, lexer, formatter)
    stream = formatter.stream
    if stream and stream[-1] == (("newline", None)):
        stream = stream[:-1]
    return normalize_tokens(stream)


def make_highlight_styles(pygments_style):
    results = {}
    for token, s in get_style_by_name(pygments_style):
        style = Style()
        if s["color"]:
            style = style.update(color="#" + s["color"])
        if s["bold"]:
            style = style.update(bold=True)
        if s["italic"]:
            style = style.update(italic=True)
        results["pygments-" + str(token)] = style
    return results
