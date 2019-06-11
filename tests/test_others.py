

def test_next(test_env):
    slide = test_env.slide
    slide.box().text("X")
    slide.box(show=2).box(show=2).text("A")
    slide.box().box(show="next").text("B")
    slide.box().box(show="next+").text("C")
    slide.box().box(show="6+").text("D")
    slide.box().box(show="next").text("E")
    slide.box().box(show="next").text("F")
    test_env.check("test_next", 8)



