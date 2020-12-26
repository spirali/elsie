import subprocess


class ExternalMerger:
    def __init__(self, command):
        self.command = command
        self.filenames = []

    def append(self, filename):
        self.filenames.append(filename)

    def write(self, output, debug):
        args = []
        for c in self.command:
            if c == "INPUTS":
                args += self.filenames
            elif c == "OUTPUT":
                args.append(output)
            else:
                args.append(c)
        if not debug:
            stdout = stderr = subprocess.DEVNULL
        else:
            stdout = stderr = None
        subprocess.check_call(args, stdout=stdout, stderr=stderr)


class PyPdfMerger:
    def __init__(self):
        from PyPDF2 import PdfFileMerger

        self.inner = PdfFileMerger()

    def append(self, filename):
        self.inner.append(filename)

    def write(self, output, debug):
        with open(output, "wb") as f:
            self.inner.write(f)


def get_pdf_merger_by_name(name):
    if name == "pypdf":
        return PyPdfMerger()
    if name == "pdfunite":
        return ExternalMerger(("pdfunite", "INPUTS", "OUTPUT"))
    raise Exception("Unknown pdfmerger: {}".format(name))
