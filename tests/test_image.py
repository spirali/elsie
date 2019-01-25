
def test_line_highlight_fragments(test_env):
    slide = test_env.slide

    img = test_env.data_path("testimage.svg")
    slide.image(img)

    b = slide.box(x="[90%]", y="[30%]", width="30%", height="30%", show="4+")
    b.rect("black", bg_color="white")
    b2 = b.box(width="fill")
    b2.update_style("default", size=15, color="white")
    b2.rect(bg_color="black")
    b2.box(padding=10).text("Scaling and placing images")
    b.fbox().image(img, show_begin=4)

    test_env.check("imagefrag", 6)


def test_line_highlight_no_fragments(test_env):
    slide = test_env.slide

    img = test_env.data_path("testimage.svg")
    slide.image(img, fragments=False)

    b = slide.box(x="[90%]", y="[30%]", width="30%", height="30%")
    b.rect("black", bg_color="white")
    b2 = b.box(width="fill")
    b2.update_style("default", size=15, color="white")
    b2.rect(bg_color="black")
    b2.box(padding=10).text("Scaling and placing images")
    b.fbox().image(img, fragments=False)

    test_env.check("imagenofrag")


def test_image_show(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(test_env.data_path("testimage2.svg"))
    test_env.check("imageshowx", 3)