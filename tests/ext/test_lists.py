from elsie.ext import ordered_list, unordered_list


def test_list_basic(test_env):
    slide = test_env.slide
    lst = unordered_list(slide.box())
    lst.item().text("Item 1")
    lst.item().text("Item 2")
    lst.item().text("Item 3")

    test_env.check("list-basic")


def test_list_with(test_env):
    slide = test_env.slide
    lst = unordered_list(slide.box())
    with lst.ul() as l:
        with l.ul():
            pass


def test_list_override(test_env):
    slide = test_env.slide
    lst = unordered_list(slide.box(), label_padding=20, indent=50)
    lst.item(label="x", label_padding=10).text("Item 1")
    lst.item(show="next+", height=200).text("Item 2")
    lst.ul().item().text("Item 3")
    lst.ul(indent=5).item().text("Text 4")

    test_env.check("list-override", expect_count=2)


def test_list_no_bullet(test_env):
    slide = test_env.slide
    lst = unordered_list(slide.box(), label_render_fn=lambda _: None)
    lst.item().text("Item 1")
    lst.item().text("Item 2")
    lst.item().text("Item 3")

    test_env.check("list-no-bullet")


def test_list_indent(test_env):
    slide = test_env.slide
    lst = unordered_list(slide.box())
    lst.item().text("Item 1")
    l2 = lst.ul()
    l2.item().text("Item 2")
    l2.item().text("Item 3")
    l3 = l2.ul()
    l3.item().text("Item 4")
    l3.ul().item().text("Item 5")
    l2.item().text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-indent")


def test_ordered_list(test_env):
    slide = test_env.slide
    lst = ordered_list(slide.box())
    lst.item().text("Item 1")
    l2 = lst.ol()
    l2.item().text("Item 2")
    l2.item().text("Item 3")
    l2.ol().item().text("Item X")
    l2.item().text("Item Y")
    lst.item().text("Item 4")
    lst.item().text("Item 5")
    lst.item().text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-ordered-indent")


def test_ordered_list_explicit_level(test_env):
    slide = test_env.slide
    lst = ordered_list(slide.box())
    lst.item().text("Item 1")
    l2 = lst.ol(level=(1, 2))
    l2.item().text("Item 2")
    l2.item().text("Item 3")
    l2.ol().item().text("Item X")
    l2.item().text("Item Y")
    lst.item().text("Item 4")
    l3 = lst.ol(level=())
    l3.item().text("Item 5")
    l3.item().text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-ordered-explicit-level")


def test_combine_ordered_unordered(test_env):
    slide = test_env.slide
    lst = ordered_list(slide.box())
    lst.item().text("Item 1")
    l2 = lst.ol()
    l2.item().text("Item 2")
    l2.item().text("Item 3")
    l2.ul().item().text("Item X")
    l2.item().text("Item Y")
    lst.item().text("Item 4")
    l3 = lst.ul()
    l3.item().text("Item 5")
    l3.ol().item().text("Item 6")
    lst.item().text("Item 7")

    test_env.check("list-combine-ordered-unordered")
