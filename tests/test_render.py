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
