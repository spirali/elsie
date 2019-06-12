
def test_line_highlight_fragments(test_env):
    slide = test_env.slide

    img = test_env.assets_path("testimage.svg")
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

    img = test_env.assets_path("testimage.svg")
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
    slide.image(test_env.assets_path("testimage2.svg"))
    test_env.check("imageshowx", 3)


def test_image_no_fragments_show_begin(test_env):
    slide = test_env.slide
    img = test_env.assets_path("testimage.svg")
    slide.image(img, fragments=False, show_begin=3)
    test_env.check("nofrag_showbegin", 3)


def test_image_scale_width(test_env):
    test_env.slide.box(width=300).image(test_env.assets_path("scale.svg"))
    test_env.check("scale-width")


def test_image_scale_height(test_env):
    test_env.slide.box(height=100).image(test_env.assets_path("scale.svg"))
    test_env.check("scale-height")


def test_image_scale_width_height(test_env):
    test_env.slide.box(width=300, height=100).image(test_env.assets_path("scale.svg"))
    test_env.check("scale-width-height")


def test_image_scale_no_dimensions(test_env):
    test_env.slide.box().image(test_env.assets_path("scale.svg"))
    test_env.check("scale-no-dimensions")

def test_image_bitmap(test_env):
    slide = test_env.slide
    img_png = test_env.assets_path("test.png")
    img_jpg = test_env.assets_path("test.jpeg")

    b = slide.fbox(height=140)
    b.rect(bg_color="green")
    b.image(img_png)

    b = slide.fbox(height=300)
    b.rect(bg_color="blue")
    b.image(img_png)

    b = slide.fbox(height=300)
    b.rect(bg_color="green")
    b.image(img_jpg)

    test_env.check("image-bitmap", 1)
