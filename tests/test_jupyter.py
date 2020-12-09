def test_no_js_with_single_step(test_env):
    slide = test_env.slide
    slide.box().text("Hello")

    assert "<script" not in slide._repr_html_()


def test_has_js_with_multiple_steps(test_env):
    slide = test_env.slide
    slide.box().text("Hello")
    slide.box(show="next+").text("World")

    assert "<script" in slide._repr_html_()
