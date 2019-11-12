import glob
import os

from elsie import Slides


def test_cache(test_env):
    cache_dir = "elsie-cache"
    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    assert not glob.glob("{}/*".format(cache_dir))
    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "1b4b2f663298abc291a730021e0cea8aef08d4e2.pdf",
        "266c6ab63434f5975a5c55583d5745105991b2a8.pdf",
        "d44aa3abda66c75b9749cd0d6b5064303d0f7be3.pdf",
        "queries3.cache"
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "1b4b2f663298abc291a730021e0cea8aef08d4e2.pdf",
        "266c6ab63434f5975a5c55583d5745105991b2a8.pdf",
        "d44aa3abda66c75b9749cd0d6b5064303d0f7be3.pdf",
        "queries3.cache"
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("4")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "0b85d0f51458a11b8d86f7956847e8783dc7d3e3.pdf",
        "266c6ab63434f5975a5c55583d5745105991b2a8.pdf",
        "d44aa3abda66c75b9749cd0d6b5064303d0f7be3.pdf",
        "queries3.cache"
    }
