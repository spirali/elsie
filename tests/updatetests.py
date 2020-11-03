import base64
import glob
import os
import subprocess
import tempfile
from pathlib import Path

import click

from conftest import DATA_DIR

CHECKS = os.path.join(DATA_DIR, "checks")


def get_png(filename):
    with open(filename, "rb") as f:
        data = f.read()
    with open("tmp.svg", "wb") as f:
        f.write(data)
    subprocess.check_call(
        ["inkscape", "-b", "#ffffff", "--export-type", "png", "tmp.svg"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with open("tmp.png", "rb") as f:
        png_data = f.read()
    return (
        '<img width=500 style="border: solid 1px black" '
        + 'src="data:image/png;base64,{}" />\n'.format(
            base64.b64encode(png_data).decode()
        )
    )


def do_report(differences, test_svg_paths):
    cwd = os.getcwd()

    out = [
        """<html>
        <body>
        <table>
        <tr>
        <td>Original result</td>
        <td>New result</td>
        </tr>
    """
    ]
    try:
        with tempfile.TemporaryDirectory(prefix="elsie-update-") as tmpdir:
            print("Workdir: ", tmpdir)
            os.chdir(tmpdir)
            for i, name in enumerate(sorted(differences)):
                print("{}/{}".format(i, len(differences)))
                out.append(
                    "<tr><td>{}/{}</td><td>{}<td></tr>".format(
                        i + 1, len(differences), name
                    )
                )

                out.append("<tr>")
                check_name = os.path.join(CHECKS, name)

                out.append("<td>")
                png = get_png(check_name)
                out.append(png)
                out.append("</td>")

                out.append("<td>")
                png = get_png(test_svg_paths[name])
                out.append(png)
                out.append("</td>")

                out.append("<tr>")

    finally:
        os.chdir(cwd)
    out.append(
        """
        </table></body></html>
    """
    )

    print("Writing 'out.html'")
    with open("out.html", "w") as f:
        f.write("".join(out))


def run_update(differences, test_svg_paths):
    for name in sorted(differences):
        source = test_svg_paths[name]
        target = os.path.join(CHECKS, name)
        print("Copying\n\tFROM: {}\n\tTO: {}".format(source, target))
        with open(source, "rb") as f:
            data = f.read()
        with open(target, "wb") as f:
            f.write(data)


@click.command()
@click.argument("testpath")
@click.option("--do-update/--do-not-update", default=False)
def test_path(testpath, do_update):
    testpath = os.path.abspath(testpath)
    check_names = set(path.name for path in Path(CHECKS).rglob("*.svg"))
    test_svg_paths = {
        os.path.basename(path): path
        for path in glob.glob(os.path.join(testpath, "**/*.svg"))
    }
    test_names = set(test_svg_paths.keys())

    differences = check_names.intersection(test_names)
    print("SVGs in test dir: ", len(test_names))
    print("SVGs in check dir: ", len(check_names))
    print("SVGs to update: ", len(differences))
    if not do_update:
        do_report(differences, test_svg_paths)
    else:
        run_update(differences, test_svg_paths)


if __name__ == "__main__":
    test_path()
