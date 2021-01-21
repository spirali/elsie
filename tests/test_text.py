import pytest
from conftest import check

import elsie
from elsie.text.highlight import highlight_code
from elsie.text.textparser import (
    extract_line,
    number_of_lines,
    parse_text,
    tokens_merge,
    tokens_to_text_without_style,
)


@check("linehighlight", expect_count=5)
def test_line_highlight_1(test_env):
    slide = test_env.slide

    slide.box().text("Line Highlighting")
    slide.box(height="20%")
    b = slide.box(height="70%")
    b.rect(bg_color="#DEDEDE")
    t = b.box().code(
        "c",
        """#include <stdio.h>

    /* Hello world program */

    int main() {
        printf("Hello world!\\n");
        return 0;
    }""",
    )

    t.line_box(4, show="1-3", prepend=1).rect(bg_color="#D0D0FF")
    t.line_box(5, show="2-3", below=t).rect(bg_color="#D0D0FF")
    t.line_box(6, show="3", below=t).rect(bg_color="#D0D0FF")
    t.line_box(4, n_lines=4, show="4", below=t).rect(color="blue")

    label = slide.box(x=100, y=400, width=200, height=130, show="5+")
    label.update_style("default", elsie.TextStyle(color="white"))
    label.rect(bg_color="green", rx=10, ry=10)
    label.text("Comment for\nline")
    label.polygon(
        [label.p("99%", "40%"), label.p("99%", "60%"), t.line_box(4).p(0, "50%")],
        bg_color="green",
    )


@check("styles-highlight")
def test_styles_and_highlight(test_env):
    slide = test_env.slide
    b = slide.box()
    t = b.code(
        "c",
        """#include <stdio.h>
/* Hello world program */

int ~#A{main}() {
    printf("Hello ~emph{world!\\n");}
    return 0;
}""",
        use_styles=True,
    )

    t.inline_box("#A", below=t).rect(bg_color="red")


@check("linenumbers")
def test_line_numbers(test_env):
    slide = test_env.slide

    slide.box().text("Line Highlighting")
    slide.box().code(
        "c",
        """#include <stdio.h>
/* Hello world program */


int main() {
    printf("Hello world!\\n");
    return 0;



}

""",
        line_numbers=True,
    )


@check("highlight-whitespace")
def test_highlight_whitespace(test_env):
    slide = test_env.slide

    box = slide.box().rect(bg_color="red")
    box.box(padding=10).code(
        "rust",
        """
line
second_line // comment""",
    )


@check("highlight-bug-2")
def test_highlight_bug2(test_env):
    text = """strlen("ahoj"); // 4

if (strcmp(str, "hello") == 0) // str equals "hello"

char buffer[80];
strcpy(buffer, "these");    // copy "these" to buffer
strcat(buffer, "strings");     // append "strings" to buffer"""

    slide = test_env.slide
    slide.box().code("c", text)


@check("highlight-bug-3")
def test_highlight_bug3(test_env):
    text = """// b

    """

    slide = test_env.slide
    slide.box().code("c", text, use_styles=True)


@check("highlight-bug-4")
def test_highlight_bug4(test_env):
    text = """int now = (int) time(NULL); // get current time
srand(now); // initialize S with the current time

int num1 = rand(); // from interval [0, RAND_MAX]
int num2 = rand() % 100; // from interval [0, 99]
int num3 = rand() % 100 + 5; // from interval [5, 104]

// from interval [0.0, 1.0]
float num4 = rand() / (float) RAND_MAX;"""

    slide = test_env.slide
    slide.box().code("c", text, use_styles=False)


@check("console")
def test_console(test_env):
    slide = test_env.slide

    slide.set_style("shell", elsie.TextStyle(color="white"), base="code")
    slide.set_style("prompt", elsie.TextStyle(color="#aaaaff"))
    slide.set_style("cmd", elsie.TextStyle(color="yellow"))

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
        "Creating 'example.pdf'........ done\n",
        "shell",
        escape_char="!",
    )


@check("list")
def test_list(test_env):
    slide = test_env.slide

    def list_item(parent):
        b = parent.box(x=0, horizontal=True)
        b.box(width=25, y=0).text("•")
        return b.box(width="fill")

    main = slide.box()
    main.update_style("default", elsie.TextStyle(align="left"))
    list_item(main).text("This is LIST DEMO")
    list_item(main).text("This is multi\nline\nitem")
    list_item(main).text("Last item")


@check("styles")
def test_styles(test_env):
    slide = test_env.slide

    slide.set_style("h1", elsie.TextStyle(size=60))
    slide.set_style("h2", elsie.TextStyle(size=50))
    slide.set_style("h3", elsie.TextStyle(size=40))

    slide.set_style("my_red", elsie.TextStyle(color="red"))
    slide.set_style("my_green", elsie.TextStyle(color="green"))
    slide.set_style("my_blue", elsie.TextStyle(color="blue"))

    slide.box().text("Header 1", "h1")
    slide.box().text("Header 2", "h2")
    slide.box().text("Header 3", "h3")

    # Build in styles
    text = "Normal text | ~tt{Type writer} | ~emph{emphasis} | ~alert{alert}"
    slide.box().text(text)

    slide.box().text("~my_red{red} ~my_green{green} ~my_blue{blue}")

    # Inline style
    slide.box().text(
        "~my_red{red} gray ~my_blue{blue}", elsie.TextStyle(size=7, color="gray")
    )


def test_pygments_single_line_comment():
    test = """
{
    // do something
}
    """.strip()

    c = highlight_code(test, "rust")
    assert number_of_lines(c) == 3


def test_extract_line():
    text = "Hello ~x{world}!"
    tokens = parse_text(text)

    for i in range(3):
        r = extract_line(tokens, i)
        assert tokens == r[0]
        assert r[1] == i

    text = "First ~z{ line\nA ~a{second~w{line}}\nThis} line} ~v{There}\n"
    tokens = parse_text(text)

    assert tokens[7][1] == "w"
    r, p = extract_line(tokens, 7)
    assert r == [
        ("begin", "z"),
        ("text", "A "),
        ("begin", "a"),
        ("text", "second"),
        ("begin", "w"),
        ("text", "line"),
        ("end", None),
        ("end", None),
        ("end", None),
    ]
    assert p == 4


def _test_text_box_slide(slide):
    slide.set_style("my_red", elsie.TextStyle(color="red"))
    slide.set_style("my_green", elsie.TextStyle(color="green"))
    slide.set_style("my_blue", elsie.TextStyle(color="blue"))

    text = (
        "This is a long ~my_red{text}\n\nthat\n~my_green{has} a various\nproperties,"
        " ~my_blue{like a boxes} used in the text."
    )

    b = slide.box().text(text)
    b.inline_box("my_red").rect(color="red")
    b.inline_box("my_green").rect(color="green")
    b.inline_box("my_blue").rect(color="blue")

    slide.box(height=70)

    b = slide.box().text(text, style=elsie.TextStyle(size=40))
    b.inline_box("my_red").rect(color="red")
    b.inline_box("my_green").rect(color="green")
    b.inline_box("my_blue").rect(color="blue")


@check("text-box-left", cairo_threshold=18)
def test_text_box_left(test_env):
    slide = test_env.slide
    slide.update_style("default", elsie.TextStyle(align="left"))
    _test_text_box_slide(slide)


@check("text-box-middle")
def test_text_box_middle(test_env):
    slide = test_env.slide
    slide.update_style("default", elsie.TextStyle(align="middle"))
    _test_text_box_slide(slide)


@check("text-box-right", cairo_threshold=18)
def test_text_box_right(test_env):
    slide = test_env.slide
    slide.update_style("default", elsie.TextStyle(align="right"))
    _test_text_box_slide(slide)


@check("dummy-style")
def test_text_dummy_style(test_env):
    slide = test_env.slide
    b = slide.box().text("~#ABC{This} ~#ABC{is} ~#ABC{a text}.")
    b.inline_box("#ABC", n_th=3).rect(color="black")


@check("dummy-style-code", expect_count=2)
def test_code_dummy_style(test_env):
    slide = test_env.slide
    b = slide.box().code(
        "cpp",
        """
~#access{int v = array[mid];}""",
        use_styles=True,
    )
    b.inline_box("#access", show="next+").rect(bg_color="red")


@check("code-use-styles")
def test_code_dummy_use_style(test_env):
    c1 = """
    async fn binary_search(array: &[u32], needle: u32) -> i32
    {
        let mid = (l + r) / 2;

        // start a memory read and suspend the coroutine
        prefetch(&array[mid]);          """
    c2 = """
            Delay::new(Duration::from_nanos(500)).await;
        }
    }"""
    slide = test_env.slide
    slide.box().code("rust", c1 + c2, use_styles=True)


def test_text_merge2():
    def test(t1, t2):
        p1 = parse_text(t1)
        p2 = parse_text(t2)

        r1 = tokens_merge(p1, p2)
        r2 = tokens_merge(p2, p1)
        assert r1 == r2
        assert r1.count(("begin", "a")) == 1
        assert r1.count(("begin", "b")) == 1
        assert r1.count(("end", None)) == 2
        assert tokens_to_text_without_style(r1) == "Aaa Bbb Ccc"

    t1 = "Aaa ~a{Bbb} Ccc"
    t2 = "~b{Aaa Bbb Ccc}"
    test(t1, t2)

    t1 = "Aaa ~a{Bbb} Ccc"
    t2 = "Aaa ~b{Bbb Ccc}"
    test(t1, t2)

    t1 = "Aaa ~a{Bbb} Ccc"
    t2 = "~b{Aaa Bbb} Ccc"
    test(t1, t2)

    t1 = "~b{Aaa ~a{Bbb} Ccc}"
    t2 = "Aaa Bbb Ccc"
    test(t1, t2)


def test_text_merge_and_destylize():
    t1 = "Hello world!\n  This is nice line   \n\n\nLast line "
    t2 = "Hello ~b{~a{world!}\n  ~c{This} is nice} line   \n\n\n~d{Last line} "
    t3 = "Hello ~x{world!\n  Th}~y{is is nice line }  \n\n\nLast~z{ }line "

    p2 = parse_text(t2)
    p3 = parse_text(t3)

    assert t1 == tokens_to_text_without_style(parse_text(t1))
    assert t1 == tokens_to_text_without_style(p2)
    assert t1 == tokens_to_text_without_style(p3)

    r = tokens_merge(p2, p3)
    assert t1 == tokens_to_text_without_style(r)

    r2 = [
        ("text", "Hello "),
        ("begin", "b"),
        ("begin", "x"),
        ("begin", "a"),
        ("text", "world!"),
        ("end", None),
        ("newline", 1),
        ("text", "  "),
        ("begin", "c"),
        ("text", "Th"),
        ("end", None),
        ("end", None),
        ("begin", "c"),
        ("begin", "y"),
        ("text", "is"),
        ("end", None),
        ("end", None),
        ("begin", "y"),
        ("text", " is nice"),
        ("end", None),
        ("end", None),
        ("begin", "y"),
        ("text", " line "),
        ("end", None),
        ("text", "  "),
        ("newline", 3),
        ("begin", "d"),
        ("text", "Last"),
        ("begin", "z"),
        ("text", " "),
        ("end", None),
        ("text", "line"),
        ("end", None),
        ("text", " "),
    ]
    assert r == r2


@check("text-fit-a", cairo=False)
def test_text_scale_to_fit_a(test_env):
    slide = test_env.slide
    slide.box(x=50, y=50, width=300, height=300).rect(bg_color="#bbffbb").text(
        "This is\ntext"
    )
    slide.box(x=650, y=50, width=300, height=300).rect(bg_color="#bbffbb").text(
        "This is\ntext", scale_to_fit=True
    )

    slide.box(x=50, y=400, width=300, height=300).rect(bg_color="#bbffbb").text(
        "This is\ntext", elsie.TextStyle(size=160)
    )
    slide.box(x=650, y=400, width=300, height=300).rect(bg_color="#bbffbb").text(
        "This is\ntext", elsie.TextStyle(size=160), scale_to_fit=True
    )


@check("text-fit-b", cairo=False)
def test_text_scale_to_fit_b(test_env):
    slide = test_env.slide
    slide.box(x=50, y=50, width=300, height=300).fbox().rect(bg_color="#bbffbb").text(
        "This is\ntext"
    )
    slide.box(x=650, y=50, width=300, height=300).fbox().rect(bg_color="#bbffbb").text(
        "This is\ntext", scale_to_fit=True
    )

    slide.box(x=50, y=400, width=300, height=300).fbox().rect(bg_color="#bbffbb").text(
        "This is\ntext", elsie.TextStyle(size=160)
    )
    slide.box(x=650, y=400, width=300, height=300).fbox().rect(bg_color="#bbffbb").text(
        "This is\ntext", elsie.TextStyle(size=160), scale_to_fit=True
    )


@check("text-fit-pointers1", cairo=False)
def test_text_scale_to_fit_pointers1(test_env):
    slide = test_env.slide
    t = slide.text("This is ~#A{full}\nslide\ntext!", scale_to_fit=True)
    t.line_box(2, z_level=-1).rect(bg_color="red")
    t.inline_box("#A", z_level=-1).rect(bg_color="blue")


@check("text-fit-pointers2", cairo=False)
def test_text_scale_to_fit_pointers2(test_env):
    slide = test_env.slide
    t = slide.text(
        "This is full\nslide\ntext!\nvery long ~#A{long} long long long line",
        scale_to_fit=True,
    )
    t.line_box(2, z_level=-1).rect(bg_color="red")
    t.inline_box("#A", z_level=-1).rect(bg_color="blue")


@check("text-fit-code", cairo=False)
def test_text_scale_to_fit_code(test_env):
    slide = test_env.slide
    slide.code(
        "c",
        """
#include <stdio.h>

int main() {
    return 0;
}""",
        scale_to_fit=True,
    )


@check("text-fit-fill")
def test_text_scale_to_fit_fill(test_env):
    slide = test_env.slide
    box = slide.box(width="100%", height="30%").rect(bg_color="green")
    box2 = box.box(height="fill").rect(bg_color="blue")
    box2.code(
        "c",
        """
#include <stdio.h>

int main() {
    return 0;
}""",
        scale_to_fit=True,
    )

    box = slide.box(width="30%", height="60%").rect(bg_color="green")
    box2 = box.box(width="fill").rect(bg_color="blue")
    box2.code(
        "c",
        """
    #include <stdio.h>

    int main() {
        return 0;
    }""",
        scale_to_fit=True,
    )


@check("text-fit-empty")
def test_text_scale_to_fit_empty(test_env):
    slide = test_env.slide
    slide.box().text("", scale_to_fit=True)


@check("text-above-below")
def test_text_above_below(test_env):
    slide = test_env.slide
    t = slide.text("Hello ~tt{world!}\nSecond line")
    t.line_box(0, below=t).rect(bg_color="green")
    t.inline_box("tt", below=t).rect(bg_color="orange")
    t.inline_box("tt").rect(color="red", stroke_width=3)
    t.line_box(0, above=t).rect(color="blue", stroke_width=6)


def test_text_style_create():
    style = elsie.TextStyle()
    assert style.size is None
    assert style.font is None

    style = elsie.TextStyle(
        font="X",
        size=10,
        align="left",
        line_spacing=1.2,
        color="black",
        bold=True,
        italic=False,
    )
    assert style.size == 10
    assert style.font == "X"
    assert style.bold is True
    assert style.italic is False
    assert style.color == "black"
    assert style.line_spacing == 1.2
    assert style.align == "left"

    with pytest.raises(Exception, match="font"):
        elsie.TextStyle(font=12)
    with pytest.raises(Exception, match="size"):
        elsie.TextStyle(size="zzz")
    with pytest.raises(Exception, match="line_spacing"):
        elsie.TextStyle(line_spacing="zzz")
    with pytest.raises(Exception, match="color"):
        elsie.TextStyle(color=123)
    with pytest.raises(Exception, match="bold"):
        elsie.TextStyle(bold=10)
    with pytest.raises(Exception, match="italic"):
        elsie.TextStyle(italic="a")
    with pytest.raises(Exception, match="no attribute"):
        style.unknown = 10


def test_text_style_update():

    style = elsie.TextStyle(font="Y", size=10)
    style2 = elsie.TextStyle(size=20, align="left")
    style.update(style2)

    assert style2.font is None
    assert style2.size == 20
    assert style2.align == "left"
    assert style.font == "Y"
    assert style.size == 20
    assert style.align == "left"


def test_text_style_compose():

    style = elsie.TextStyle(font="Y", size=10)
    style2 = style.compose(elsie.TextStyle(size=20, align="left"))

    assert style2.font == "Y"
    assert style2.size == 20
    assert style2.align == "left"
    assert style.font == "Y"
    assert style.size == 10
    assert style.align is None


@check("text-rotated")
def test_rotated_text(test_env):
    slide = test_env.slide

    slide.box(x=100, y=100).text("Hello world!", rotation=90)
    slide.box(x=100, y=300).text("Hello world!", rotation=180)
    slide.box(x=100, y=500).code("Python", "a = 5", rotation=45)
