import contextlib
import logging
import os
import queue
import subprocess
import tempfile
import threading

PROMPT = "> "


class ProcessReader:
    def __init__(self, stdout, queue):
        self.thread = threading.Thread(
            target=self.read, args=(stdout, queue), daemon=True
        )

    def start(self):
        self.thread.start()

    def read(self, stdout, queue):
        line = ""

        while True:
            character = stdout.read(1)
            line += character
            if character == "\n" or line == PROMPT:
                queue.put(line)
                line = ""


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
        self.queue = queue.Queue()
        self.reader = ProcessReader(self.process.stdout, self.queue)
        self.reader.start()
        self.wait_for_prompt()

        self.run_command("file-close")

    def wait_for_prompt(self):
        lines = []

        while True:
            line = self.queue.get().strip("\n")
            logging.debug(f"Received {line} from Inkscape")
            if line == PROMPT:
                break
            else:
                lines.append(line)
        return lines

    def convert_to_pdf(self, source, target: str, type: str):
        with svg_file_input(self, source, binary=True):
            self.run_command("export-area-page")
            self.run_command(f"export-type:{type}")
            self.run_command(f"export-filename:{target}")
            self.run_command("export-do")

    def get_width(self, svg: str, id: str):
        return self.run_query(svg, "query-width", id)

    def get_x(self, svg: str, id: str):
        return self.run_query(svg, "query-x", id)

    def run_query(self, svg: str, query: str, id: str):
        with svg_file_input(self, svg):
            self.run_command(f"select:{id}")
            output = self.run_command(query)

            value = output[0]
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
        return "\n".join(self.run_command("inkscape-version"))


def export_by_inkscape(inkscape: InkscapeShell, source: str, target: str, type: str):
    inkscape.convert_to_pdf(source, target, type)
    if not os.path.isfile(target):
        raise Exception(
            "Inkscape should produced file '{}' but it is not found".format(target)
        )
