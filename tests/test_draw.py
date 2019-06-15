from elsie import Arrow


def test_line_highlight_no_fragments(test_env):
    slide = test_env.slide

    slide.box(100, 100, 200, 200).rect(color="green")
    slide.box(120, 120, 160, 160).rect(bg_color="green")

    slide.box(320, 100, 200, 200).rect(color="blue", rx=20, ry=20)
    slide.box(340, 120, 160, 160).rect(bg_color="blue", rx=20, ry=20)

    slide.polygon([(540, 300), (740, 300), (640, 100)], color="red")
    slide.polygon([(570, 280), (710, 280), (640, 140)], bg_color="red")

    slide.line(
        [(760, 100), (940, 100), (760, 300), (960, 300)],
        color="orange", stroke_width=5)

    slide.line([(100, 500), (200, 500)], color="black", stroke_width=1)
    slide.line([(100, 550), (200, 550)], color="black", stroke_width=5)
    slide.line([(100, 600), (200, 600)], color="black", stroke_width=10)

    arrow1 = Arrow(10, stroke_width=1)
    slide.line([(300, 500), (400, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = Arrow(20, stroke_width=5)
    slide.line([(300, 550), (400, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = Arrow(30, stroke_width=10)
    slide.line([(300, 600), (400, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = Arrow(10)
    slide.line([(500, 500), (600, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = Arrow(20)
    slide.line([(500, 550), (600, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = Arrow(30)
    slide.line([(500, 600), (600, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = Arrow(10, inner=0.5)
    slide.line([(700, 500), (800, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = Arrow(20, inner=0.5)
    slide.line([(700, 550), (800, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = Arrow(30, inner=0.5)
    slide.line([(700, 600), (800, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = Arrow(10, inner=2.0)
    slide.line([(900, 500), (1000, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = Arrow(20, inner=2.0)
    slide.line([(900, 550), (1000, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = Arrow(30, inner=2.0)
    slide.line([(900, 600), (1000, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    # Dashes

    # dash(10) space(10) ...
    slide.line([(100, 350), (500, 350)], stroke_width=10, stroke_dasharray="10")

    # dash(10) space(20) ...
    slide.line([(100, 380), (500, 380)], stroke_width=10, stroke_dasharray="10 20")

    # dash(20) space(10) dash(2) space(10) ...
    slide.line([(100, 410), (500, 410)], stroke_width=10, stroke_dasharray="20 10 2 10")

    # dashed rectangle
    slide.box(550, 350, 50, 50).rect(stroke_width=5,
                                     stroke_dasharray="2",
                                     color="black",
                                     rx=5,
                                     ry=5)

    test_env.check("shapes")
