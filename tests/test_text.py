from elsie.highlight import highlight_code
from elsie.textparser import number_of_lines

def test_line_highlight(test_env):
    slide = test_env.slide

    slide.box().text("Line Highlighting")
    slide.box(height="20%")
    b = slide.box(height="70%")
    b.rect(bg_color="#DEDEDE")
    b.line_box(4, show="1-3").rect(bg_color="#D0D0FF")
    b.line_box(5, show="2-3").rect(bg_color="#D0D0FF")
    b.line_box(6, show="3").rect(bg_color="#D0D0FF")

    b.line_box(4, lines=4, show="4").rect(color="blue")

    b.code("c", """#include <stdio.h>

    /* Hello world program */

    int main() {
        printf("Hello world!\\n");
        return 0;
    }""")

    label = slide.box(100, 400, 200, 130, show="5+")
    label.update_style("default", color="white")
    label.rect(bg_color="green", rx=10, ry=10)
    label.text("Comment for\nline")
    label.polygon([label.p("99%", "40%"),
                   label.p("99%", "60%"),
                   b.line_box(4).p(0, "50%")], bg_color="green")

    test_env.check("linehighlight", 5)


def test_line_numbers(test_env):
    slide = test_env.slide

    slide.box().text("Line Highlighting")
    slide.box().code("c", """#include <stdio.h>
/* Hello world program */


int main() {
    printf("Hello world!\\n");
    return 0;



}

""", line_numbers=True)

    test_env.check("linenumbers", 1)


def test_console(test_env):
    slide = test_env.slide
    slide.derive_style("code", "shell", color="white")
    slide.new_style("prompt", color="#aaaaff")
    slide.new_style("cmd", color="yellow")

    slide.box().text("Console demo")
    slide.box(height=30)

    b = slide.box()
    b.rect(bg_color="black")
    b.box(p_x=10, p_y=5).text(
        "!prompt{~/path/to/elphie/example$} !cmd{ls}\n"
        "example.py\n\n"
        "!prompt{~/path/to/elphie/example$} !cmd{python3 example.py}\n"
        "Preprocessing................. done\n"
        "Building...................... done\n"
        "Creating 'example.pdf'........ done\n", "shell", escape_char="!")

    test_env.check("console")


def test_list(test_env):
    slide = test_env.slide

    def list_item(parent):
        b = parent.box(x=0, horizontal=True)
        b.box(width=25, y=0).text("•")
        return b.box(width="fill")

    main = slide.box()
    main.update_style("default", align="left")
    list_item(main).text("This is LIST DEMO")
    list_item(main).text("This is multi\nline\nitem")
    list_item(main).text("Last item")

    test_env.check("list")


def test_styles(test_env):
    slide = test_env.slide

    slide.new_style("h1", size=60)
    slide.new_style("h2", size=50)
    slide.new_style("h3", size=40)

    slide.new_style("my_red", color="red")
    slide.new_style("my_green", color="green")
    slide.new_style("my_blue", color="blue")

    slide.box().text("Header 1", "h1")
    slide.box().text("Header 2", "h2")
    slide.box().text("Header 3", "h3")

    # Build in styles
    text = "Normal text | ~tt{Type writer} | ~emph{emphasis} | ~alert{alert}"
    slide.box().text(text)

    slide.box().text("~my_red{red} ~my_green{green} ~my_blue{blue}")

    # Inline style
    slide.box().text("~my_red{red} gray ~my_blue{blue}", {"size": 7, "color": "gray"})

    test_env.check("styles")


def test_pygments_single_line_comment():
    test = """
{
    // do something
}
    """.strip()

    c = highlight_code(test, "rust")
    assert number_of_lines(c) == 3


