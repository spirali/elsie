import glob
import os

from conftest import check

from elsie import SlideDeck


# test_env has to be there to switch to work directory
def test_cache1(test_env):
    cache_dir = "elsie-cache"
    slides = SlideDeck(name_policy="ignore")

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    assert not glob.glob("{}/*".format(cache_dir))
    slides.render(output="test.pdf")

    print(glob.glob("{}/*".format(cache_dir)))

    fs = set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir)))
    assert "queries3.cache" in fs
    assert len(fs) == 4

    slides = SlideDeck(name_policy="ignore")

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    slides.render(output="test.pdf")

    fs2 = set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir)))
    assert fs2 == fs

    slides = SlideDeck(name_policy="ignore")

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("4")

    slides.render(output="test.pdf")

    print(fs2)
    fs3 = set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir)))
    assert "queries3.cache" in fs3
    assert len(fs3.difference(fs)) == 1


# test_env has to be there to switch to work directory
def test_cache2(test_env):
    cache_dir = "elsie-cache"

    slides = SlideDeck(name_policy="ignore")
    for i in range(10):
        slide = slides.new_slide()
        slide.box(width=100, height=100).rect(bg_color="blue")

    assert not glob.glob("{}/*".format(cache_dir))
    slides.render(output="test.pdf")

    files = set([os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))])
    assert 2 == len(files)

    slides = SlideDeck(name_policy="ignore")
    for i in range(10):
        slide = slides.new_slide()
        slide.box(width=100, height=100).rect(bg_color="green")

    slides.render(output="test.pdf")

    files2 = set([os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))])
    assert 2 == len(files2)
    assert files != files2


@check("viewbox")
def test_viewbox(test_env):
    slide = test_env.slides.new_slide(view_box=(100, 250, 200, 300))
    slide.box(x=100, y=200, width=200, height=300).rect("green").text("Hello!")


def test_add_raw_pdf(test_env):
    slides = test_env.slides
    slides.add_pdf(test_env.assets_path("test.pdf"))
    slides.render("test.pdf")
