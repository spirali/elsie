import elsie


def test_line_highlight_fragments(test_env):
    slide = test_env.slide

    img = test_env.assets_path("testimage.svg")
    slide.image(img)

    b = slide.box(x="[90%]", y="[30%]", width="30%", height="30%", show="4+")
    b.rect("black", bg_color="white")
    b2 = b.box(width="fill")
    b2.update_style("default", elsie.TextStyle(size=15, color="white"))
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
    b2.update_style("default", elsie.TextStyle(size=15, color="white"))
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


def test_image_svg_no_size(test_env):
    slide = test_env.slide

    b = slide.box(width="fill", horizontal=True)
    b.box(x="[90%]").image(test_env.assets_path("test100x30.svg"))

    slide.box(y="[90%]").image(test_env.assets_path("test100x30.svg"))
    test_env.check("test-image-svg-no-size")


def test_image_bitmap_no_size(test_env):
    slide = test_env.slide

    b = slide.box(width="fill", horizontal=True)
    b.box(x="[90%]").image(test_env.assets_path("test.png"))

    slide.box(y="[90%]").image(test_env.assets_path("test.jpeg"))
    test_env.check("test-image-bitmap-no-size")


def test_image_width(test_env):
    test_env.slide.box(width=300).rect(bg_color="green").image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(width=50).image(test_env.assets_path("test100x30.svg"))
    test_env.slide.box(width=300).image(test_env.assets_path("test.png"))
    test_env.slide.box(width=300).image(test_env.assets_path("test100x30.svg"))
    test_env.check("image-width")


def test_image_height(test_env):
    test_env.slide.box(height=100).rect(bg_color="green").image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(height=10).image(test_env.assets_path("test100x30.svg"))
    test_env.slide.box(height=100).image(test_env.assets_path("test.png"))
    test_env.slide.box(height=200).image(test_env.assets_path("test100x30.svg"))
    test_env.check("image-height")


def test_image_width_height(test_env):
    test_env.slide.box(width=300, height=100).image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(width=300, height=100).image(test_env.assets_path("test.png"))
    test_env.check("image-width-height")


def test_image_show_next(test_env):
    slide = test_env.slide
    img = test_env.assets_path("testimage.svg")
    slide.box(width=100, height=100).image(img, show_begin=2)
    slide.box(width=30, height=30, show="next").rect(bg_color="black")
    test_env.check("image-show-next", 5)


def test_ora_no_fragments(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img, fragments=False)
    test_env.check("ora-nofrag")


def test_ora_fragments_1(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img)
    test_env.check("ora-frag", 4)


def test_ora_fragments_showbegin(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img, show_begin=3)
    test_env.check("ora-frag-sb", 6)


def test_image_substeps_show1(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(test_env.assets_path("testimage.svg"), select_fragments=[3, None, 1])
    test_env.check("image-substeps1", 3)


def test_image_substeps_show2(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(
        test_env.assets_path("testimage.svg"), select_fragments=[2], show_begin=2
    )
    slide.box(width="100", height="100", show="1-3").rect(color="black")
    test_env.check("image-substeps2", 3)
