import elsie
from elsie.ext.latex import latex

slides = elsie.SlideDeck()


@slides.slide()
def latex_demo(slide):
    latex(slide.box(), "\TeX{} demo", scale=5.0)
    slide.box(height="50")
    latex(slide.box(),
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


slides.render("latex.pdf")
