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


def get_inkscape_version():
    args = ("/usr/bin/inkscape", "--version")
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode().strip()


def run_inkscape_get_width(svg):
    return float(run_inkscape(("--query-id=target", "-W"), None, svg))


def run_inkscape_get_x(svg):
    return float(run_inkscape(("--query-id=target", "-X"), None, svg))


def convert_to_pdf(source, target):
    run_inkscape(("--export-pdf", target, "--export-area-page"), stdin=source)


def svg_size_to_pixels(text):
    suffix = ""
    while text and text[-1].isalpha():
        suffix = text[-1] + suffix
        text = text[:-1]
    if suffix == "mm":
        factor = 3.77953
    elif suffix == "cm":
        factor = 37.7953
    elif suffix == "pt":
        factor = 1.33333
    else:
        factor = 1.0
    return float(text) * factor


def rename_ids(root, suffix):
    ids = []
    for e in root.iter():
        e_id = e.get("id")
        if e_id:
            ids.append("#" + e_id)
            e.set("id", e_id + suffix)

    for e in root.iter():
        for name, value in e.attrib.items():
            for e_id in ids:
                if e_id in value:
                    e.set(name, value.replace(e_id, e_id + suffix))
