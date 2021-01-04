import marko
from marko.block import BlankLine, FencedCode, Heading, List, ListItem, Paragraph, Quote
from marko.inline import Emphasis, LineBreak, RawText, StrongEmphasis

from ..boxtree.box import Box
from ..text.textparser import trim_indent
from ..text.textstyle import TextStyle as s
from . import ordered_list, unordered_list

MD_PARAGRAPH_STYLE = "md-paragraph"
MD_BOLD_STYLE = "md-bold"
MD_ITALIC_STYLE = "md-italic"


def md_heading_style_name(level: int) -> str:
    assert 1 <= level <= 6
    return f"md-heading-{level}"


class MarkdownContext:
    def __init__(self, box: Box, escape_char: str):
        self.box = box
        self.escape_char = escape_char
        self.text_kwargs = {"escape_char": escape_char}

    def copy(self, **kwargs):
        args = dict(box=self.box, escape_char=self.escape_char)
        args.update(kwargs)
        return MarkdownContext(**args)

    def wrap_text_with_style(self, text: str, style: str):
        return f"{self.escape_char}{style}{{{text}}}"


def get_raw_text(ctx: MarkdownContext, node):
    text = ""
    for child in node.children:
        if isinstance(child, RawText):
            text += child.children
        elif isinstance(child, Emphasis):
            text += ctx.wrap_text_with_style(get_raw_text(ctx, child), MD_ITALIC_STYLE)
        elif isinstance(child, StrongEmphasis):
            text += ctx.wrap_text_with_style(get_raw_text(ctx, child), MD_BOLD_STYLE)
        elif isinstance(child, LineBreak):
            text += "\n"
    return text


def create_root_md_box(box: Box) -> Box:
    box = box.box()
    default = s(align="left")
    styles = {
        MD_PARAGRAPH_STYLE: default.compose(s()),
        MD_BOLD_STYLE: default.compose(s(bold=True)),
        MD_ITALIC_STYLE: default.compose(s(italic=True)),
    }
    for i in range(6):
        styles[md_heading_style_name(i + 1)] = default.compose(s(size=40 - i * 2))

    for (name, style) in styles.items():
        if not box.has_style(name):
            box.set_style(name, style)

    return box


def build_text(ctx: MarkdownContext, text: str, style: str):
    container = ctx.box.sbox()
    container.text(text, style=style, **ctx.text_kwargs)


def build_heading(ctx: MarkdownContext, heading: Heading):
    build_text(ctx, get_raw_text(ctx, heading), md_heading_style_name(heading.level))


def build_paragraph(ctx: MarkdownContext, paragraph: Paragraph):
    build_text(ctx, get_raw_text(ctx, paragraph), MD_PARAGRAPH_STYLE)


def build_blank_line(ctx: MarkdownContext, blank_line: BlankLine):
    build_text(ctx, "\n", MD_PARAGRAPH_STYLE)


def build_quote(ctx: MarkdownContext, quote: Quote):
    for child in quote.children:
        build(ctx, child)


def build_fenced_code(ctx: MarkdownContext, fenced_code: FencedCode):
    container = ctx.box.sbox()
    container.code(fenced_code.lang, get_raw_text(ctx, fenced_code))


# TODO: nested lists, alignment of multi-line paragraphs in a list item
def build_list_top(ctx: MarkdownContext, list_node: List):
    container = ctx.box.sbox()
    if list_node.ordered:
        list = ordered_list(container, start=list_node.start)
    else:
        list = unordered_list(container, label=list_node.bullet)
    for child in list_node.children:
        assert isinstance(child, ListItem)
        box = list.item()
        build_children(ctx.copy(box=box), child)


MD_BUILD_FNS = {
    Heading: build_heading,
    Paragraph: build_paragraph,
    BlankLine: build_blank_line,
    Quote: build_quote,
    FencedCode: build_fenced_code,
    List: build_list_top,
}


def build(ctx: MarkdownContext, node):
    if node.__class__ in MD_BUILD_FNS:
        MD_BUILD_FNS[node.__class__](ctx, node)
    else:
        print(f"Warning: ignoring markdown node {node}")


def build_children(ctx: MarkdownContext, parent):
    for node in parent.children:
        build(ctx, node)


def markdown(root: Box, markup: str, escape_char="~") -> Box:
    markup = trim_indent(markup).strip()

    wrapper = create_root_md_box(root)
    document = marko.parse(markup)
    ctx = MarkdownContext(wrapper, escape_char)
    build_children(ctx, document)
    return root
