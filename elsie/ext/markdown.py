import marko
from marko.block import BlankLine, FencedCode, Heading, List, ListItem, Paragraph, Quote
from marko.inline import Emphasis, LineBreak, Link, RawText, StrongEmphasis

from ..boxtree.box import Box
from ..text.textparser import trim_indent
from ..text.textstyle import TextStyle as s
from . import ordered_list, unordered_list


def md_heading_style_name(level: int) -> str:
    """Returns the name of the text style used for Markdown headings of the given level."""
    assert 1 <= level <= 6
    return f"md-h{level}"


MD_PARAGRAPH_STYLE = "md-paragraph"
MD_BOLD_STYLE = "md-bold"
MD_ITALIC_STYLE = "md-italic"
MD_LINK_STYLE = "md-link"
MD_BLOCKQUOTE_STYLE = "md-blockquote"
MD_HEADING_1_STYLE = md_heading_style_name(1)
MD_HEADING_2_STYLE = md_heading_style_name(2)
MD_HEADING_3_STYLE = md_heading_style_name(3)
MD_HEADING_4_STYLE = md_heading_style_name(4)
MD_HEADING_5_STYLE = md_heading_style_name(5)
MD_HEADING_6_STYLE = md_heading_style_name(6)


class MarkdownContext:
    def __init__(self, box: Box, escape_char: str, active_list=None):
        self.box = box
        self.escape_char = escape_char
        self.text_kwargs = {"escape_char": escape_char}
        self.active_list = active_list

    def copy(self, **kwargs):
        args = dict(
            box=self.box, escape_char=self.escape_char, active_list=self.active_list
        )
        args.update(kwargs)
        return MarkdownContext(**args)

    def wrap_text_with_style(self, text: str, style: str):
        return f"{self.escape_char}{style}{{{text}}}"


def get_raw_text(ctx: MarkdownContext, node) -> str:
    text = ""
    for child in node.children:
        if isinstance(child, RawText):
            text += child.children
        elif isinstance(child, Emphasis):
            text += ctx.wrap_text_with_style(get_raw_text(ctx, child), MD_ITALIC_STYLE)
        elif isinstance(child, StrongEmphasis):
            text += ctx.wrap_text_with_style(get_raw_text(ctx, child), MD_BOLD_STYLE)
        elif isinstance(child, Link):
            text += ctx.wrap_text_with_style(get_raw_text(ctx, child), MD_LINK_STYLE)
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
        MD_LINK_STYLE: default.compose(s(color="#0EBFE9")),
        MD_BLOCKQUOTE_STYLE: default.compose(s(color="#A9A9A9")),
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
    container = ctx.box.sbox()
    container.update_style("default", container.get_style(MD_BLOCKQUOTE_STYLE))
    parent_ctx = ctx.copy(box=container)
    for child in quote.children:
        build(parent_ctx, child)


def build_fenced_code(ctx: MarkdownContext, fenced_code: FencedCode):
    container = ctx.box.sbox()
    container.code(fenced_code.lang, get_raw_text(ctx, fenced_code))


def build_list_top(ctx: MarkdownContext, list_node: List):
    container = ctx.box.sbox()
    if list_node.ordered:
        if ctx.active_list:
            new_list = ctx.active_list.ol(start=list_node.start, level=())
        else:
            new_list = ordered_list(container, start=list_node.start)
    else:
        if ctx.active_list:
            new_list = ctx.active_list.ul(label=list_node.bullet)
        else:
            new_list = unordered_list(container, label=list_node.bullet)
    for child in list_node.children:
        assert isinstance(child, ListItem)
        box = new_list.item()
        build_children(ctx.copy(box=box, active_list=new_list), child)


MD_BUILD_FNS = {
    Heading: build_heading,
    Paragraph: build_paragraph,
    BlankLine: build_blank_line,
    Quote: build_quote,
    FencedCode: build_fenced_code,
    List: build_list_top,
}


def build(ctx: MarkdownContext, node):
    cls = node.__class__
    if cls in MD_BUILD_FNS:
        MD_BUILD_FNS[cls](ctx, node)
    else:
        print(f"Warning: ignoring markdown node {node}")


def build_children(ctx: MarkdownContext, parent):
    for node in parent.children:
        build(ctx, node)


def markdown(root: Box, markup: str, escape_char="~") -> Box:
    """
    Render Markdown markup into the given box.

    The Markdown syntax has to adhere to the CommonMark spec, but only
    a subset of the Markdown syntax is supported (see user guide).

    Parameters
    ----------
    root: Box
        Parent box into which will the markup be rendered.
    markup: str
        Markdown markup.
    escape_char: str
        Escape character used for marking inline styles.
    """
    markup = trim_indent(markup).strip()
    document = marko.parse(markup)

    wrapper = create_root_md_box(root)

    ctx = MarkdownContext(wrapper, escape_char)
    build_children(ctx, document)
    return root
