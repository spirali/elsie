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

    print(glob.glob("{}/*".format(cache_dir)))

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "2800c8e52864d0c62c981a4f81c871267a30fa66.pdf",
        "05bf89d40d73eb84d537be6de6cb5ddd1dc0d82a.pdf",
        "b687b113b3353a349b33df8767a2becd47a424d1.pdf",
        "queries3.cache",
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "2800c8e52864d0c62c981a4f81c871267a30fa66.pdf",
        "05bf89d40d73eb84d537be6de6cb5ddd1dc0d82a.pdf",
        "b687b113b3353a349b33df8767a2becd47a424d1.pdf",
        "queries3.cache",
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("4")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "a002ab322e755851724c9a70b0afbae0f651b709.pdf",
        "05bf89d40d73eb84d537be6de6cb5ddd1dc0d82a.pdf",
        "b687b113b3353a349b33df8767a2becd47a424d1.pdf",
        "queries3.cache",
    }


def test_viewbox(test_env):
    slide = test_env.slides.new_slide(view_box=(100, 250, 200, 300))
    slide.box(x=100, y=200, width=200, height=300).rect("green").text("Hello!")
    test_env.check("viewbox", 1)
