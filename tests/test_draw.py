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
        [(760, 100), (940, 100), (760, 300), (960, 300)], color="orange", stroke_width=5
    )

    slide.line([(100, 500), (200, 500)], color="black", stroke_width=1)
    slide.line([(100, 550), (200, 550)], color="black", stroke_width=5)
    slide.line([(100, 600), (200, 600)], color="black", stroke_width=10)

    arrow1 = Arrow(10, stroke_width=1)
    slide.line(
        [(300, 500), (400, 500)],
        color="black",
        stroke_width=1,
        start_arrow=arrow1,
        end_arrow=arrow1,
    )
    arrow2 = Arrow(20, stroke_width=5)
    slide.line(
        [(300, 550), (400, 550)],
        color="black",
        stroke_width=5,
        start_arrow=arrow2,
        end_arrow=arrow2,
    )
    arrow3 = Arrow(30, stroke_width=10)
    slide.line(
        [(300, 600), (400, 600)],
        color="black",
        stroke_width=10,
        start_arrow=arrow3,
        end_arrow=arrow3,
    )

    arrow1 = Arrow(10)
    slide.line(
        [(500, 500), (600, 500)],
        color="black",
        stroke_width=1,
        start_arrow=arrow1,
        end_arrow=arrow1,
    )
    arrow2 = Arrow(20)
    slide.line(
        [(500, 550), (600, 550)],
        color="black",
        stroke_width=5,
        start_arrow=arrow2,
        end_arrow=arrow2,
    )
    arrow3 = Arrow(30)
    slide.line(
        [(500, 600), (600, 600)],
        color="black",
        stroke_width=10,
        start_arrow=arrow3,
        end_arrow=arrow3,
    )

    arrow1 = Arrow(10, inner=0.5)
    slide.line(
        [(700, 500), (800, 500)],
        color="black",
        stroke_width=1,
        start_arrow=arrow1,
        end_arrow=arrow1,
    )
    arrow2 = Arrow(20, inner=0.5)
    slide.line(
        [(700, 550), (800, 550)],
        color="black",
        stroke_width=5,
        start_arrow=arrow2,
        end_arrow=arrow2,
    )
    arrow3 = Arrow(30, inner=0.5)
    slide.line(
        [(700, 600), (800, 600)],
        color="black",
        stroke_width=10,
        start_arrow=arrow3,
        end_arrow=arrow3,
    )

    arrow1 = Arrow(10, inner=2.0)
    slide.line(
        [(900, 500), (1000, 500)],
        color="black",
        stroke_width=1,
        start_arrow=arrow1,
        end_arrow=arrow1,
    )
    arrow2 = Arrow(20, inner=2.0)
    slide.line(
        [(900, 550), (1000, 550)],
        color="black",
        stroke_width=5,
        start_arrow=arrow2,
        end_arrow=arrow2,
    )
    arrow3 = Arrow(30, inner=2.0)
    slide.line(
        [(900, 600), (1000, 600)],
        color="black",
        stroke_width=10,
        start_arrow=arrow3,
        end_arrow=arrow3,
    )

    # Dashes

    # dash(10) space(10) ...
    slide.line([(100, 350), (500, 350)], stroke_width=10, stroke_dasharray="10")

    # dash(10) space(20) ...
    slide.line([(100, 380), (500, 380)], stroke_width=10, stroke_dasharray="10 20")

    # dash(20) space(10) dash(2) space(10) ...
    slide.line([(100, 410), (500, 410)], stroke_width=10, stroke_dasharray="20 10 2 10")

    # dashed rectangle
    slide.box(550, 350, 50, 50).rect(
        stroke_width=5, stroke_dasharray="2", color="black", rx=5, ry=5
    )

    test_env.check("shapes")


def test_path(test_env):
    COLOR1 = "blue"

    slide = test_env.slide
    box = slide.box(height="80%", width="80%").rect(color="black")

    arrow1 = Arrow(10)
    box.path(
        [("M", box.p(0, 0)), ("L", (300, 400)), ("Q", (400, 400), (300, 500))],
        end_arrow=arrow1,
    )

    box.path(
        [
            ("M", box.p(0, 0)),
            ("C", box.p(0, -40), box.p("100%", -40), box.p("100%", 0)),
        ],
        color="red",
        stroke_width=4,
        bg_color="blue",
    )

    root = (
        slide.box(x=250, y="[50%]", width=100, height=50)
        .rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5)
        .text("Root")
    )
    child1 = (
        slide.box(x=650, y="[20%]", width=100, height=50)
        .rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5)
        .text("Child1")
    )
    child2 = (
        slide.box(x=650, y="[80%]", width=100, height=50)
        .rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5)
        .text("Child2")
    )

    arrow = Arrow(10)

    # Path root -> child1
    r1 = root.p("100%", "50%")
    c1 = child1.p("0%", "50%")

    # See SVG <path> documentation for commands explanation
    # In short: M = move to, L = line to, C/S = bezier curve, Q/T = quadratic
    slide.path(
        [("M", r1), ("C", r1.add(300, 0), c1.add(-300, 0), c1)],
        end_arrow=arrow,
        stroke_width=2,
        color=COLOR1,
    )

    # Path root -> child2
    c2 = child2.p("0%", "50%")
    slide.path(
        [("M", r1), ("Q", c2.add(-100, 0), c2)],
        end_arrow=arrow,
        stroke_width=2,
        color=COLOR1,
        stroke_dasharray="10",
    )

    # Path chiled1 -> child1
    c1t = child1.p("50%", "0%")
    c1r = child1.p("100%", "50%")
    slide.path(
        [("M", c1t), ("C", c1t.add(0, -100), c1r.add(100, 0), c1r)],
        end_arrow=arrow,
        stroke_width=2,
        color=COLOR1,
    )

    slide.path([("M", (650, 350)), ("L", (750, 350))], stroke_width=4, color="green")
    slide.path(
        [("M", (600, 450)), ("L", (700, 250)), ("L", (800, 450))],
        stroke_width=4,
        color="red",
    )
    slide.path(
        [("M", (600, 450)), ("Q", (700, 250), (800, 450))], bg_color="blue", color=None
    )

    test_env.check("path")


def test_draw_relative_to_box(test_env):
    slide = test_env.slide

    box = slide.box(x=100, y=200, width=400, height=150).rect(bg_color="#ccc")

    box.polygon([(0, 0), ("100%", "0%"), ("50%", 20)], bg_color="yellow")
    box.line([(0, 50), ("100%", "50%")], color="red")
    box.path([("M", (0, 50)), ("L", ("50%", "100%"))], color="green")

    test_env.check("draw-boxrel")
