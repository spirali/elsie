from conftest import check

from elsie import TextStyle


def test_postprocessing(test_env):
    called = [False]

    def fn(slides):
        called[0] = True
        assert len(slides) == 3
        for i, s in enumerate(slides):
            s.box(x=100, y=100).text("{}/{}".format(i, len(slides)))

    test_env.slides.new_slide()
    test_env.slides.new_slide().box().text("Slide1")
    test_env.slides.new_slide().box().text("Slide2")
    test_env.check_svg(
        "preprocessor", expect_count=3, render_args=dict(slide_postprocessing=fn)
    )
    assert called[0]


@check("debug_boxes", cairo=False)
def test_debug_boxes(test_env):
    COLOR1 = "black"
    COLOR2 = "gray"

    slide = test_env.slides.new_slide(debug_boxes=True)

    slide.set_style("header", TextStyle(size=35, color="white"))
    slide.set_style("header2", TextStyle(size=25, color=COLOR1))

    title_box1 = slide.box(width="fill", height=120)
    title_box1.rect(bg_color=COLOR2)

    title_box2 = title_box1.fbox(p_y=10, name="header")
    title_box2.rect(bg_color=COLOR1)

    title_box2.text("Elsie: SlideDeck in Python in Programmable Way", "header")

    slide.box(height=30, name="filler")

    # Subtitle box
    subtitle = slide.box(name="name")
    subtitle.text("Stanislav Böhm\n~tt{https://github.com/spirali/elsie}", "header2")


@check("leaf_chaining")
def test_leaf_chaining(test_env):
    slide = test_env.slides.new_slide()
    slide.rect(bg_color="black").rect(color="white").text("Hello!").rect(color="green")
    box = slide.box(width="50%", height="50%")
    box.rect(bg_color="black").rect(color="white").text("Hello!").rect(color="green")


@check(
    "per_page_groupping",
    expect_count=2,
    render_args={"slides_per_page": (3, 2)},
    cairo=False,
)
def test_per_page_groupping1(test_env):
    colors = ["red", "green", "blue", "orange"]
    for i in range(10):
        slide = test_env.slides.new_slide()
        slide.rect(bg_color=colors[i % len(colors)])
        slide.text(f"SLIDE {i}", TextStyle(color="white"))


@check("per_page_groupping2", render_args={"slides_per_page": (1, 3)}, cairo=False)
def test_per_page_groupping2(test_env):
    colors = ["red", "green", "blue"]
    for i in range(3):
        slide = test_env.slides.new_slide()
        slide.rect(bg_color=colors[i % len(colors)])
        slide.text(f"SLIDE {i}", TextStyle(color="white"))
