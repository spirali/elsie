import subprocess


def svg_begin(xml, width=None, height=None):
    xml.element("svg")
    xml.set("xmlns", "http://www.w3.org/2000/svg")
    if width is not None:
        xml.set("width", width)
    if height is not None:
        xml.set("height", height)


def svg_end(xml):
    xml.close("svg")


def run_inkscape(extra_args, filename=None, stdin=None):
    if filename is None:
        filename = "/dev/stdin"
    with open("/dev/null", "w") as devnull:
        args = ("/usr/bin/inkscape",
                "--without-gui") + extra_args + (filename,)
        p = subprocess.Popen(args,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=devnull)
        stdout, stderr = p.communicate(stdin.encode("utf-8"))
        return stdout


def run_inkscape_get_width(svg):
    return float(run_inkscape(("--query-id=target", "-W"), None, svg))


def convert_to_pdf(source, target):
    run_inkscape(("-A", target), stdin=source)


def svg_size_to_pixels(text):
    suffix = ""
    while text and text[-1].isalpha():
        suffix = text[-1] + suffix
        text = text[:-1]
    if suffix == "mm":
        factor = 3.543307
    elif suffix == "cm":
        factor = 35.43307
    else:
        factor = 1.0
    return float(text) * factor
