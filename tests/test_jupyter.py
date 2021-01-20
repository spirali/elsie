import pytest

from elsie.render.jupyter import render_slide_html


@pytest.mark.parametrize("format", ("svg", "png"))
def test_jupyter_render(test_env, format):
    slide = test_env.slide
    slide.box().text("Hello")

    assert render_slide_html(slide.slide, format)


def test_no_js_with_single_step(test_env):
    slide = test_env.slide
    slide.box().text("Hello")

    assert "<script" not in slide._repr_html_()


def test_has_js_with_multiple_steps(test_env):
    slide = test_env.slide
    slide.box().text("Hello")
    slide.box(show="next+").text("World")

    assert "<script" in slide._repr_html_()
