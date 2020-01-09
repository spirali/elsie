def test_drop_same_consecutive_slides(test_env):
    slide = test_env.slide
    slide.box().text("Drop")
    test_env.slides.new_slide().box().text("Drop")
    test_env.check("drop", render_args=dict(drop_duplicates=True))


def test_keep_same_nonconsecutive_slides(test_env):
    slide = test_env.slide
    slide.box().text("Drop")
    test_env.slides.new_slide().box().text("Interlude")
    test_env.slides.new_slide().box().text("Drop")
    test_env.check("drop-interlude", expect_count=3, render_args=dict(drop_duplicates=True))


def test_preprocessor(test_env):
    called = [False]

    def fn(slides):
        called[0] = True
        assert len(slides) == 3
        for i, s in enumerate(slides):
            s.box(x=100, y=100).text("{}/{}".format(i, len(slides)))

    test_env.slides.new_slide().box().text("Slide1")
    test_env.slides.new_slide().box().text("Slide2")
    test_env.check("preprocessor", expect_count=3, render_args=dict(slide_preprocessor=fn))
    assert called[0]
