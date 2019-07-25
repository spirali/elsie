def test_next(test_env):
    slide = test_env.slide
    slide.box().text("X")
    slide.box(show=2).box(show=2).text("A")
    slide.box().box(show="next").text("B")
    slide.box().box(show="next+").text("C")
    slide.box().box(show="last+").text("C1")
    slide.box().box(show="last+").text("C2")
    slide.box().box(show="6+").text("D")
    slide.box().box(show="next-8").text("E")
    slide.box().box(show="last").text("E1")
    slide.box().box(show="next-10").text("F")
    test_env.check("next", 10)


def test_last_in_empty_slide(test_env):
    b = test_env.slide.box(show="last").text("1")
    assert b._show_info.steps == (1,)
    assert b._show_info.open_step is None


def test_last_plus_in_empty_slide(test_env):
    b = test_env.slide.box(show="last+").text("1")
    assert b._show_info.steps == ()
    assert b._show_info.open_step == 1


def test_next_in_empty_slide(test_env):
    b = test_env.slide.box(show="next").text("1")
    assert b._show_info.steps == (2,)
    assert b._show_info.open_step is None


def test_next_plus_in_empty_slide(test_env):
    b = test_env.slide.box(show="next+").text("1")
    assert b._show_info.steps == ()
    assert b._show_info.open_step == 2
