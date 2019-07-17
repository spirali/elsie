from elsie.highlight import highlight_code
from elsie.textparser import (number_of_lines, parse_text, extract_line,
                              tokens_to_text_without_style,
                              tokens_merge)


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


def test_styles_and_highlight(test_env):
    slide = test_env.slide
    b = slide.box()
    b.code("c", """#include <stdio.h>
/* Hello world program */

int ~#A{main}() {
    printf("Hello ~emph{world!\\n");}
    return 0;
}""", use_styles=True)

    b.text_box("#A", z_level=-1).rect(bg_color="red")
    test_env.check("styles-highlight")


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


def test_highlight_whitespace(test_env):
    slide = test_env.slide

    box = slide.box().rect(bg_color="red")
    box.box(padding=10).code("rust", """
line
second_line // comment""")

    test_env.check("highlight-whitespace", 1)


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
        ('begin', 'z'), ('text', 'A '), ('begin', 'a'), ('text', 'second'),
        ('begin', 'w'), ('text', 'line'), ('end', None), ('end', None), ('end', None)]
    assert p == 4


def _test_text_box_slide(slide):
    slide.new_style("my_red", color="red")
    slide.new_style("my_green", color="green")
    slide.new_style("my_blue", color="blue")

    text = "This is a long ~my_red{text}\n\nthat\n~my_green{has} a various\nproperties," \
           " ~my_blue{like a boxes} used in the text."

    b = slide.box().text(text)
    b.text_box("my_red").rect(color="red")
    b.text_box("my_green").rect(color="green")
    b.text_box("my_blue").rect(color="blue")

    slide.box(height=70)

    b = slide.box().text(text, style={"size": 40})
    b.text_box("my_red").rect(color="red")
    b.text_box("my_green").rect(color="green")
    b.text_box("my_blue").rect(color="blue")


def test_text_box_left(test_env):
    slide = test_env.slide
    slide.update_style("default", align="left")
    _test_text_box_slide(slide)
    test_env.check("text-box-left")


def test_text_box_middle(test_env):
    slide = test_env.slide
    slide.update_style("default", align="middle")
    _test_text_box_slide(slide)
    test_env.check("text-box-middle")


def test_text_box_right(test_env):
    slide = test_env.slide
    slide.update_style("default", align="right")
    _test_text_box_slide(slide)
    test_env.check("text-box-right")


def test_text_dummy_style(test_env):
    slide = test_env.slide
    b = slide.box().text("~#ABC{This} ~#ABC{is} ~#ABC{a text}.")
    b.text_box("#ABC", n_th=3).rect(color="black")
    test_env.check("dummy-style")


def test_code_dummy_style(test_env):
    slide = test_env.slide
    b = slide.box().code("cpp", """
    ~#access{int v = array[mid];}
""", use_styles=True)
    b.text_box("#access", show="next+").rect(bg_color="red")
    test_env.check("dummy-style-code")


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

    r2 = [('text', 'Hello '), ('begin', 'b'), ('begin', 'x'), ('begin', 'a'),
          ('text', 'world!'), ('end', None), ('newline', 1),
          ('text', '  '), ('begin', 'c'), ('text', 'Th'), ('end', None), ('end', None),
          ('begin', 'c'), ('begin', 'y'), ('text', 'is'), ('end', None), ('end', None),
          ('begin', 'y'), ('text', ' is nice'), ('end', None), ('end', None), ('begin', 'y'),
          ('text', ' line '), ('end', None), ('text', '  '), ('newline', 3), ('begin', 'd'),
          ('text', 'Last'), ('begin', 'z'), ('text', ' '), ('end', None),
          ('text', 'line'), ('end', None), ('text', ' ')]
    assert r == r2


