import functools
import hashlib
import os
import subprocess
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import lxml.etree as et

from ..boxtree.boxitem import SimpleBoxItem
from ..boxtree.boxmixin import BoxMixin
from ..render.backends.svg.utils import rename_ids, svg_size_to_pixels

if TYPE_CHECKING:
    from . import boxitem


def latex(
    parent: BoxMixin, text: str, scale=1.0, header: str = None, tail: str = None
) -> "boxitem.BoxItem":
    """
    Renders LaTeX.

    Parameters
    ----------
    parent: BoxMixin

    text: str
        Source code of the LaTeX snippet.
    scale: float
        Scale of the rendered output.
    header: str
        Prelude of the LaTeX source (for example package imports).
        Will be included at the beginning of the source code.
    tail: str
        End of the LaTeX source (for example end of the document).
        Will be included at the end of the source code.
    """

    if header is None:
        header = """
\\documentclass[varwidth,border=1pt]{standalone}
\\usepackage[utf8x]{inputenc}
\\usepackage{ucs}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\begin{document}"""

    if tail is None:
        tail = "\\end{document}"

    tex_text = "{}\n{}\n{}".format(header, text, tail)

    box = parent._get_box()
    svg = box.slide.fs_cache.get(tex_text, "svg", _render_latex)
    root = et.fromstring(svg)
    svg_width = svg_size_to_pixels(root.get("width")) * scale
    svg_height = svg_size_to_pixels(root.get("height")) * scale

    box.layout.ensure_width(svg_width)
    box.layout.ensure_height(svg_height)

    draw = functools.partial(_draw, parent, svg, svg_width, svg_height, scale)
    item = SimpleBoxItem(box, draw)
    box.add_child(item)
    return item


def _draw(parent, svg, svg_width, svg_height, scale, ctx):
    box = parent._get_box()
    rect = box.layout.rect
    x = rect.x + (rect.width - svg_width) / 2
    y = rect.y + (rect.height - svg_height) / 2
    ctx.draw_svg(
        svg=svg,
        x=x,
        y=y,
        width=rect.width,
        height=rect.height,
        scale=scale,
    )


def _render_latex(text):
    args = ("/usr/bin/pdflatex", "-interaction=batchmode", "content.tex")

    with TemporaryDirectory(prefix="elsie-") as wdir:
        with open(os.path.join(wdir, "content.tex"), "w") as f:
            f.write(text)

        p = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=wdir,
        )

        _stdout, _stderr = p.communicate()
        if p.returncode != 0:
            with open(os.path.join(wdir, "content.log")) as f:
                error = f.read()
            raise Exception("pdflatex failed:\n" + error)

        svg_name = os.path.join(wdir, "content.svg")

        args = ("/usr/bin/pdf2svg", os.path.join(wdir, "content.pdf"), svg_name)

        p = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=wdir,
        )

        _stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception("pdf2svg failed:\n" + stderr.decode())

        root = et.parse(svg_name).getroot()

    h = hashlib.md5()
    h.update(text.encode())
    suffix = "-" + h.hexdigest()
    rename_ids(root, suffix)
    return et.tostring(root).decode()
