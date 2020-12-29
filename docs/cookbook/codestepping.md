# Code stepping
*Elsie* makes it easy to create interactive walkthroughs of code snippets. You can e.g.
highlight each line in succession, show arrows pointing to different lines or gradually reveal the
snippet line-by-line.

For inspiration, here we show a function that will take a code snippet and display selected lines
from it in successive fragments, according to the passed `line_fragments` parameter.

```elsie,type=lib
def code_step(parent: Box, code: str, language: str, line_fragments, **code_args):
    # Split the code into lines
    code = code.strip()
    lines = code.split("\n")

    # Return either a line with the given index or an empty line
    def get_line(lines, visible):
        if visible is None:
            return ""
        elif isinstance(visible, int):
            return lines[visible]

    last = None
    for (step, visible_lines) in enumerate(line_fragments):
        # Overlay the whole parent box at each step
        wrapper = parent.overlay(show=str(step + 1))
        current_lines = [get_line(lines, visible) for visible in visible_lines]
        last = wrapper.code(language, "\n".join(current_lines), **code_args)
    return last
```

```elsie,height=200
code_step(slide.box(width=200, height=200), """
def my_abs(x):
  if x < 0:
     x = -x
  assert x >= 0
""", "python", (
    [0, None, None, 3],    # Show only the first and last line
    [0, 1, None, 3],       # Show first two lines and the last line
    [0, 1, 2, 3]           # Show all lines
))
```
