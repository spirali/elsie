from pygments import highlight
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

from .textparser import NEWLINE_1, normalize_tokens
from .textstyle import TextStyle


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
                if "\n" in value:
                    for t in value.split("\n"):
                        if t:
                            stream.append(("text", t))
                        stream.append(NEWLINE_1)
                    stream.pop()
                else:
                    stream.append(("text", value))
                stream.append(("end", None))


def highlight_code(code, language):
    lexer = get_lexer_by_name(language)
    formatter = MyFormatter()
    highlight(code, lexer, formatter)
    return normalize_tokens(formatter.stream)


def make_highlight_styles(pygments_style):
    results = {}
    for token, s in get_style_by_name(pygments_style):
        style = TextStyle()
        if s["color"]:
            style.color = "#" + s["color"]
        if s["bold"]:
            style.bold = True
        if s["italic"]:
            style.italic = True
        results["pygments-" + str(token)] = style
    return results
