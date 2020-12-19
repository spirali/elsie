"""
This plugin allows you to use Elsie code in MkDocs documentation.

Use a code block with language `elsie` in Markdown.
Each slide has access to `slides` and `slide` variables.
You can use steps in the code block.

You can optionally use the following parameters:
- width=<int>: Width of the resulting image.
- height=<int>: Height of the resulting image.
- type=<lib, render>: If `type` is `lib`, do not render the code block as a slide, but use it as
a library function for futher slides on the page.
- border=<yes, no>: Whether to draw a border around the slide.

Example:
```elsie,width=300,height=300
slide.box().text("Hello world")
```
"""
import contextlib
import os
from typing import List

from mkdocs.plugins import BasePlugin


def is_fence_delimiter(line):
    return line.strip().startswith("```")


def parse_fence_header(header):
    items = header.strip(" `").split(",")
    lang = items[0]
    args = dict(item.split("=") for item in items[1:])
    return (lang, args)


def elsie_to_python_header(header):
    start = header.index("```elsie")
    return header[:start] + "```python"


class CodeContext:
    def __init__(self):
        self.lib = []

    def add_lib_code(self, code_lines):
        self.lib += code_lines

    def get_lib_code(self):
        return "\n".join(self.lib)


def trim_indent(lines):
    min_indent = min(len(line) - len(line.lstrip()) for line in lines)
    return [line[min_indent:] for line in lines]


@contextlib.contextmanager
def change_cwd(directory: str):
    cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(cwd)


def render_slide(code: List[str],
                 docs_dir: str,
                 ctx: CodeContext,
                 width: int,
                 height: int,
                 border: bool) -> str:
    # TODO: render to PNG
    border_str = """slide.rect(color="black")""" if border else ""
    code = "\n".join(trim_indent(code))
    template = f"""
import elsie
from elsie.box import Box
from elsie.jupyter import render_slide

{ctx.get_lib_code()}

slides = elsie.Slides(width={width}, height={height}, name_policy="ignore")
slide = slides.new_slide()
{border_str}
{code}

result = render_slide(slide.slide)
""".strip()

    locals = {}
    code_object = compile(template, "elsie_render.py", "exec")

    with change_cwd(docs_dir):
        exec(code_object, locals)  # Sorry
    return locals["result"]


def iterate_fences(src: str, handle_fence):
    lines = []
    fence_content = []
    inside_fence = False
    fence_header = None

    for line in src.splitlines(keepends=False):
        if is_fence_delimiter(line):
            if inside_fence:
                assert line.strip() == "```"
                assert fence_header is not None
                header, after = handle_fence(fence_header, fence_content)
                lines.append(header)
                lines += fence_content
                lines.append(line)
                lines += after or []

                fence_content = []
                inside_fence = False
                fence_header = None
            else:
                inside_fence = True
                fence_header = line
        elif inside_fence:
            fence_content.append(line)
        else:
            lines.append(line)

    return "\n".join(lines)


class ElsiePlugin(BasePlugin):
    def on_page_markdown(self, src: str, page, config, *args, **kwargs):
        # TODO: use Markdown parser

        docs_dir = config["docs_dir"]
        ctx = CodeContext()

        def handle_fence(header, fence_lines):
            lang, args = parse_fence_header(header)
            if lang == "elsie":
                lines = []
                type = args.get("type", "render")
                if type == "lib":
                    ctx.add_lib_code(fence_lines)
                elif type == "render":
                    width = args.get("width", 300)
                    height = args.get("height", 300)
                    border = args.get("border", "yes")

                    lines = render_slide(fence_lines,
                                         docs_dir,
                                         ctx,
                                         width=width,
                                         height=height,
                                         border=border == "yes").splitlines(
                        keepends=False)
                return elsie_to_python_header(header), lines
            return header, []

        return iterate_fences(src, handle_fence)
