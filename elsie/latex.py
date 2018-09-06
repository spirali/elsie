
from .svg import rename_ids

from tempfile import TemporaryDirectory

import subprocess
import os
import hashlib
import lxml.etree as et


def render_latex(text):
    args = ("/usr/bin/pdflatex",
            "-interaction=batchmode",
            "content.tex")

    with TemporaryDirectory(prefix="elphie-") as wdir:
        with open(os.path.join(wdir, "content.tex"), "w") as f:
            f.write(text)

        p = subprocess.Popen(args,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=wdir)

        _stdout, _stderr = p.communicate()
        if p.returncode != 0:
            with open(os.path.join(wdir, "content.log")) as f:
                error = f.read()
            raise Exception("pdflatex failed:\n" + error)

        svg_name = os.path.join(wdir, "content.svg")

        args = ("/usr/bin/pdf2svg",
                os.path.join(wdir, "content.pdf"),
                svg_name)

        p = subprocess.Popen(args,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=wdir)

        _stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception("pdf2svg failed:\n" + stderr.decode())

        root = et.parse(svg_name).getroot()

    h = hashlib.md5()
    h.update(text.encode())
    suffix = "-" + h.hexdigest()

    rename_ids(root, suffix)

    return et.tostring(root).decode()
