import elsie

slides = elsie.Slides(debug = True)


@slides.slide()
def latex_demo(slide):
    slide.box().latex("\TeX{} demo", scale=5.0)
    slide.box(height="50")
    slide.box().latex(
        """
    $$
        \\begin{bmatrix}
            1 & \sqrt{x} & 0 \\\\
            0 & 1 & -1
        \\end{bmatrix}\\begin{bmatrix}
            1  \\\\
            \\frac{\\alpha}{x}  \\\\
            1
        \\end{bmatrix}
        =\\begin{bmatrix}
            1+\\frac{\\alpha}{\sqrt{x}}  \\\\
            \\frac{\\alpha}{x}-1
        \\end{bmatrix}
    $$
    """,
        scale=3.0,
    )


slides.render("latex_demo.pdf")
