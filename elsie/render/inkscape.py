import contextlib
import logging
import os
import subprocess
import tempfile


@contextlib.contextmanager
def svg_file_input(inkscape, svg: str, binary=False):
    with tempfile.NamedTemporaryFile("wb" if binary else "w", suffix=".svg") as f:
        f.write(svg)
        f.flush()
        inkscape.run_command(f"file-open:{f.name}")
        yield
        inkscape.run_command("file-close")


class InkscapeShell:
    def __init__(self, inkscape_bin: str):

        self.process = subprocess.Popen(
            [inkscape_bin, "--shell"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        self.wait_for_prompt()

        self.run_command("file-close")

    def close(self):
        self.process.stdout.close()

    def wait_for_prompt(self):
        chars = []
        stdout = self.process.stdout
        while True:
            character = stdout.read(1)
            if (
                character == " "
                and chars
                and chars[-1] == ">"
                and (len(chars) == 1 or chars[-2] == "\n")
            ):
                line = "".join(chars[:-2])
                return line
            else:
                chars.append(character)

    def convert_to_pdf(self, source, target: str, type: str):
        with svg_file_input(self, source, binary=True):
            self.run_command("export-area-page")
            self.run_command(f"export-type:{type}")
            self.run_command(f"export-filename:{target}")
            self.run_command("export-do")

    def get_width(self, svg: str, id: str):
        return self.run_query(svg, "query-width", id)

    def get_height(self, svg: str, id: str):
        return self.run_query(svg, "query-height", id)

    def get_x(self, svg: str, id: str):
        return self.run_query(svg, "query-x", id)

    def run_query(self, svg: str, query: str, id: str):
        with svg_file_input(self, svg):
            self.run_command(f"select:{id}")
            value = self.run_command(query)
            try:
                return float(value)
            except ValueError:
                raise Exception(
                    f"Inkscape query executed ({query}) and should return "
                    f"float but returned {repr(value)}"
                )

    def run_command(self, command: str):
        logging.debug(f"Sending {command} to Inkscape")
        self.process.stdin.write(f"{command}\n")
        self.process.stdin.flush()
        return self.wait_for_prompt()

    def get_version(self):
        return self.run_command("inkscape-version")


def export_by_inkscape(inkscape: InkscapeShell, source: str, target: str, type: str):
    inkscape.convert_to_pdf(source, target, type)
    if not os.path.isfile(target):
        raise Exception(
            "Inkscape should produced file '{}' but it is not found".format(target)
        )
