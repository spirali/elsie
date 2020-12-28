from elsie.ext import ListBuilder


def test_list_basic(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box())
    lst.item().text("Item 1")
    lst.item().text("Item 2")
    lst.item().text("Item 3")

    test_env.check("list-basic")


def test_list_override(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box())
    lst.item(bullet="x").text("Item 1")
    lst.item(show="next+", height=200).text("Item 2")
    lst.item().text("Item 3")

    test_env.check("list-override")


def test_list_no_bullet(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box(), bullet=None)
    lst.item().text("Item 1")
    lst.item().text("Item 2")
    lst.item().text("Item 3")

    test_env.check("list-no-bullet", bless=True)


def test_list_indent_explicit(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box())
    lst.item().text("Item 1")
    lst.item(level=1).text("Item 2")
    lst.item(level=1).text("Item 3")
    lst.item(level=2).text("Item 4")
    lst.item(level=3).text("Item 5")
    lst.item(level=1).text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-indent")


def test_list_indent_stateful(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box())
    lst.item().text("Item 1")
    lst.indent()
    lst.item().text("Item 2")
    lst.item().text("Item 3")
    lst.indent()
    lst.item().text("Item 4")
    lst.indent()
    lst.item().text("Item 5")
    lst.dedent(2)
    lst.item().text("Item 6")
    lst.dedent()
    lst.item().text("Item 7")

    test_env.check("list-indent")


def test_list_indent_scope(test_env):
    slide = test_env.slide
    lst = ListBuilder(slide.box())
    lst.item().text("Item 1")
    with lst.indent_scope():
        lst.item().text("Item 2")
        lst.item().text("Item 3")
        with lst.indent_scope():
            lst.item().text("Item 4")
            with lst.indent_scope():
                lst.item().text("Item 5")
        lst.item().text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-indent")
