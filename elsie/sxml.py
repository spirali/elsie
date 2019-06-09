

class Xml:

    def __init__(self):
        self.chunks = []
        self.stack = []
        self.is_open = False

    def _close(self):
        if self.is_open:
            self.chunks.append(">")
            self.is_open = False

    def raw_text(self, text):
        self._close()
        self.chunks.append(text)

    def element(self, name):
        self._close()
        self.chunks.append("<")
        self.chunks.append(name)
        self.stack.append(name)
        self.is_open = True

    def set(self, name, value, escape=True):
        assert self.is_open
        if escape:
            value = str(value).replace("'", "\\'")
        self.chunks.append(" {}='{}'".format(name, escape_text(value)))

    def text(self, text):
        self._close()
        text = escape_text(str(text))
        text = text.replace(" ", "&#160;")
        self.chunks.append(text)

    def close(self, text=None):
        assert self.stack, "At least one element has to be opened"
        if text is not None and self.stack[-1] != text:
            raise Exception("Expects '{}' on stack but found '{}'"
                            .format(text, self.stack[-1]))
        if self.is_open:
            self.is_open = False
            self.stack.pop()
            self.chunks.append(" />")
        else:
            self.chunks.append("</")
            self.chunks.append(self.stack.pop())
            self.chunks.append(">")

    def to_string(self):
        assert len(self.stack) == 0, "Empty stack"
        return "".join(self.chunks)

    def write(self, filename):
        assert len(self.stack) == 0, "Empty stack"
        with open(filename, "w") as f:
            for chunk in self.chunks:
                f.write(chunk)


def escape_text(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text
