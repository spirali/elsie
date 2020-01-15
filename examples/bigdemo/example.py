import elsie

# Let us create primary colors used in slides
COLOR1 = "#328cc1"
COLOR2 = "#d9b310"

# Modyfy global text styles
# You can instantiate separate instances of slides,
# and work with them separately, but usually it is convenient
# just to use global instance of slides
elsie.update_style("default", color=COLOR1)  # Default font
elsie.update_style("emph", color=COLOR2)  # Emphasis


# First slide #############################################

@elsie.slide()
def first_slide(slide):
    # Create text styles that are local for this slide
    # Actually, any Box can have own styles that are inherited
    # to any sub-boxes.
    slide.new_style("header", size=35, color="white")
    slide.new_style("header2", size=25, color=COLOR1)

    # Create a box that fill the whole slide horizontaly
    title_box1 = slide.box(width="fill", height=120)
    title_box1.rect(bg_color=COLOR2)  # Draw a filled rectangle

    # Create a sub-box in title_box1.
    # "fbox" is shortcut for box(width="fill", height="fill")
    # p_y is vertical padding (other options are:
    # p_left, p_right, p_top, p_bootom, p_x, padding)
    title_box2 = title_box1.fbox(p_y=10)
    title_box2.rect(bg_color=COLOR1)

    # Put text into a box with style "header"
    title_box2.text("Elsie: Slides in Python in Programmable Way", "header")

    # Create a box that just serves as space filler
    slide.box(height=30)

    # Subtitle box
    subtitle = slide.box()
    subtitle.text("Stanislav Böhm\n~tt{https://github.com/spirali/elsie}",
                  "header2")


# Slide with brief description ############################

@elsie.slide()
def brief_description(slide):
    # Usage of inline styles; Syntax is ~ABC{Text}, it applies style ABC on Text.
    slide.text("~emph{Elsie} is a slide framework based on ~emph{Python}\n")


# Hello world example #####################################

@elsie.slide()
def hello_world(slide):
    slide.box().text("~emph{Hello World} example:")

    slide.box(height=20)  # Space reserving box

    b = slide.box(width="100%")  # Box for code
    b.rect(bg_color="#EEE")  # Background for code

    # Method .code works as .text but it calls pygments for syntax highlight.
    # The first argument is the used language
    # We create another box just for applying small padding
    b.box(p_x=20, p_y=10).code("python", """
    import elsie

    @elsie.slide()
    def hello(slide):
        slide.text("Hello world!")

    elsie.render()""")


# Text fragments ##########################################

@elsie.slide()
def fragments(slide):
    slide.box().text("Elsie supports ...")

    # One slide may generate more pages in resulting pdf
    # Argument 'show' controls on which pages of the slides is the box shown.
    # Possible values:
    # "2" - Show only on the second page
    # "2+" - Show from the second page to the last page
    # "2-5" - Show on second page to 5th page
    # "2,3,4" - Show on pages 2, 3, and 4
    # "next" - Create a new step after so far last step
    # "last" - Index of so far last step
    slide.box(show="2+").text("... fragment ...")
    slide.box(show="3+").text("... revealing.")


# SVG image demo ##########################################

@elsie.slide()
def svg_demo(slide):
    # Include SVG image into slide, it automatically fills the box.
    slide.image("testimage.svg")

    # Now we are creating the window with another picture
    # x="[90%]" is alignment of box ([0%] means left-aligning,
    # [100%] right-aligning).
    window = slide.box(x="[90%]", y="30%", width="30%", height="30%", show="4+")
    window.rect("black", bg_color="white")

    # Title of the window
    title = window.box(width="fill")
    title.update_style("default", size=15, color="white")
    title.rect(bg_color="black")
    title.box(padding=10).text("Scaling and placing images")

    # Placing a image into window. Note that we are using fbox
    # (i.e. width="fill", height="fill")
    # ('image' method does not enforce a size, so if you create a box
    # containing only image without any width/height, then you will see
    # nothing as the image fills box of the zero size).
    window.fbox().image("testimage.svg", fragments=False)


# Header/Footer demo ##########################################

@elsie.slide()
def header_footer(slide):
    slide.new_style("header", color="white", align="right")
    slide.new_style("footer", color="white", size=15)

    header = slide.box(width="fill", height="10%")
    header.rect(bg_color="#5F8DD3")
    header.box(width="fill", p_right=20).text("Demo of Header & Footer", "header")

    slide.box(width="fill", height="10").rect(bg_color="#DDD")

    content = slide.box(height="fill")
    content.text("Content")

    footer = slide.box(width="fill", height="5%", horizontal=True)
    f1 = footer.box(width="fill", height="fill")
    f1.rect(bg_color="#5F8DD3")
    f1.text("Hello!", "footer")
    f2 = footer.box(width="fill", height="fill")
    f2.rect(bg_color="#0F2DD3")
    f2.text("Footer!", "footer")
    f3 = footer.box(width="fill", height="fill")
    f3.rect(bg_color="#5F8DD3")
    f3.text("Hello!", "footer")


# Syntax highlighting ##########################################

@elsie.slide()
def syntax_highlighting(slide):
    slide.box().text("Syntax Highlighting")
    slide.box(height=30)
    slide.box().code("c", """#include <stdio.h>

/* Hello world program */

int main() {
    printf("Hello world!\\n");
    return 0;
}""")


# Line highlighting #######################################

@elsie.slide()
def line_highlighting(slide):
    slide.box().text("Line Highlighting")
    slide.box(height=30)

    code_box = slide.box()
    code_box.code("c", """#include <stdio.h>

/* Hello world program */

int main() {
    printf("Hello world!\\n");
    return 0;
}""")

    # 'line_box' creates box around a specified line of a text (the 1st argument)
    # Lines are counter from 0
    # We are using z_level to put highlights behind the text
    code_box.line_box(4, show="1-3", z_level=-1).rect(bg_color="#D0D0FF")
    code_box.line_box(5, show="2-3", z_level=-1).rect(bg_color="#D0D0FF")
    code_box.line_box(6, show="3", z_level=-1).rect(bg_color="#D0D0FF")

    # The same as previous three, but we are stroking border and
    # not filling the rectangle
    code_box.line_box(4, lines=4, show="4").rect(color="blue")

    # Creating a "commenting label"
    label = slide.box(100, 400, 200, 130, show="5")
    label.update_style("default", color="white")
    label.rect(bg_color="green", rx=10, ry=10)
    label.text("Comment for\na line")

    # Here we creates the triangle heading to a line,
    # method 'p' returns a position relatively to the box
    label.polygon([label.p("99%", "40%"),
                   label.p("99%", "60%"),
                   code_box.line_box(4).p(0, "50%")], bg_color="green")

    # Now we are creating an arrow head for the orange line
    arrow = elsie.Arrow(10)
    p1 = code_box.line_box(0).p("100%", "50%")
    p2 = code_box.line_box(5).p("100%", "50%")
    slide.box(show="6").line([p1, p1.add(40, 0),
                              p2.add(40, 0), p2],
                             stroke_width=3, color="orange", end_arrow=arrow)


# Scaling into box #######################################

@elsie.slide()
def text_scaling(slide):
    slide.box().text("Scaling text into a box")
    slide.box(height=120)

    code_box = slide.box(width=450, height=400)
    code_box.rect(bg_color="#ddd", color="#888")
    code_box.code("c", """#include <stdio.h>

/* Hello world program */

int main() {
    printf("Hello world!\\n");
    return 0;
}""", scale_to_fit=True)
#     ^^^^^^^^^^^^<<<<<<<< this is important



# Text box demo ###############################################

@elsie.slide()
def text_box_demo(slide):
    b = slide.box().text("~#A{Demo} for ~#B{highlighting} a part of a line")

    # Now we select part of text accoring style
    # You can select any style (e.g. "emph")
    # But you can also use "dummy style" that starts with "#"
    # Such style does not have to be declared and it serves
    # only purpose of selecting part of the text
    b.text_box("#A", z_level=-1, show="2").rect(bg_color=COLOR2)

    b2 = b.text_box("#B", z_level=-1, show="3", padding=-3).rect(color=COLOR2)
    arrow = elsie.Arrow(10)
    b2.line([b2.p("50%", "160%"), b2.p("50%", "100%")],
            stroke_width=3, color=COLOR2, end_arrow=arrow)


@elsie.slide()
def text_box_in_code_demo(slide):
    slide.derive_style("default", "small", size=10)
    b = slide.box().text("Words inside code block")
    slide.box(height=80)

    c = slide.box().code("c", """#include <stdio.h>

/* Hello world program */

    int ~#MAIN{main}() {
    printf(~small{"Hello world!\\n"});
    return ~#RETURN_VALUE{0};
}""", use_styles=True)  # <--- use_styles=True is important to enable styling in code block

    p2 = c.text_box("#RETURN_VALUE").p("50%", "100%")

    c.text_box("#MAIN", z_level=-1, p_x=-2).rect(bg_color="#FBB", color="black")

    arrow = elsie.Arrow(10)
    slide.line([p2.add(0, 40), p2],
               end_arrow=arrow, stroke_width=3)

    c.line_box(4).box(x="100%", height="100%").text("← Inline highlight", "small")
    c.line_box(5).box(x="100%", height="100%").text("← Font style changed", "small")
    c.line_box(6).box(x="100%", height="100%").text("← Pointing to a word", "small")


# Console demo ############################################

@elsie.slide()
def console_demo(slide):
    slide.derive_style("code", "shell", color="white")
    slide.new_style("prompt", color="#aaaaff")
    slide.new_style("cmd", color="yellow")

    slide.box().text("Console demo")
    slide.box(height=30)

    # The 'console' is just text with a few styles
    # As we want to use "~" character in the text,
    # we are changing escape_char for styles from "~" to "!"
    console = slide.box()
    console.rect(bg_color="black")
    console.box(p_x=10, p_y=5).text(
        "!prompt{~/path/to/elsie/example$} !cmd{ls}\n"
        "example.py\n\n"
        "!prompt{~/path/to/elsie/example$} !cmd{python3 example.py}\n"
        "Preprocessing................. done\n"
        "Building...................... done\n"
        "Creating 'example.pdf'........ done\n", "shell", escape_char="!")


# LaTeX demo ##############################################

@elsie.slide()
def latex_demo(slide):
    slide.box().latex("\TeX{} demo", scale=5.0)
    slide.box(height="50")
    slide.box().latex("""
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
    """, scale=3.0)


# Text demo ###############################################

@elsie.slide()
def text_demo(slide):
    # New created styles
    slide.new_style("h1", size=60)
    slide.new_style("h2", size=50)
    slide.new_style("h3", size=40)

    slide.new_style("my_red", color="red")
    slide.new_style("my_green", color="green")
    slide.new_style("my_blue", color="blue")

    slide.box().text("Header 1", "h1")
    slide.box().text("Header 2", "h2")
    slide.box().text("Header 3", "h3")

    # Build in styles
    text = "Normal text | ~tt{Type writer} | ~emph{emphasis} | ~alert{alert}"
    slide.box().text(text)
    slide.box().text("~my_red{red} ~my_green{green} ~my_blue{blue}")


# List demo ###############################################

# A helper function for creating a bullet point and a box for content
def list_item(parent):
    b = parent.box(x=0, horizontal=True)
    b.box(width=25, y=0).text("•")  # A bullet point
    return b.box(width="fill")


@elsie.slide()
def list_demo(slide):
    main = slide.box()
    main.update_style("default", align="left")

    list_item(main).text("This is LIST DEMO")
    list_item(main).text("This is\nmulti-line\nitem")
    list_item(main).text("Last item")


# Columns demo ############################################

@elsie.slide()
def columns_demo(slide):
    slide.box(padding=40).text("Columns demo")
    columns = slide.box(width="80%", horizontal=True)

    column1 = columns.box(width="30%")
    column1.text("This is some text\nin the first\ncolumn")

    column2 = columns.box(width="30%", height="100%")
    column2.rect(bg_color="#EEE")
    column2.box(padding=10).code("python", "print 'Hello world!'")

    column1 = columns.box(width="30%")
    column1.text("Some text again\nin the third\ncolumn")


# Shape demo ##############################################

@elsie.slide()
def shape_demo(slide):
    slide.box(100, 100, 200, 200).rect(color="green")
    slide.box(120, 120, 160, 160).rect(bg_color="green")

    slide.box(320, 100, 200, 200).rect(color="blue", rx=20, ry=20)
    slide.box(340, 120, 160, 160).rect(bg_color="blue", rx=20, ry=20)

    slide.polygon([(540, 300), (740, 300), (640, 100)], color="red")
    slide.polygon([(570, 280), (710, 280), (640, 140)], bg_color="red")

    slide.line([(760, 100), (940, 100), (760, 300), (960, 300)],
               color="orange", stroke_width=5)

    slide.line([(100, 500), (200, 500)], color="black", stroke_width=1)
    slide.line([(100, 550), (200, 550)], color="black", stroke_width=5)
    slide.line([(100, 600), (200, 600)], color="black", stroke_width=10)

    arrow1 = elsie.Arrow(10, stroke_width=1)
    slide.line([(300, 500), (400, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = elsie.Arrow(20, stroke_width=5)
    slide.line([(300, 550), (400, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = elsie.Arrow(30, stroke_width=10)
    slide.line([(300, 600), (400, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = elsie.Arrow(10)
    slide.line([(500, 500), (600, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = elsie.Arrow(20)
    slide.line([(500, 550), (600, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = elsie.Arrow(30)
    slide.line([(500, 600), (600, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = elsie.Arrow(10, inner=0.5)
    slide.line([(700, 500), (800, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = elsie.Arrow(20, inner=0.5)
    slide.line([(700, 550), (800, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = elsie.Arrow(30, inner=0.5)
    slide.line([(700, 600), (800, 600)], color="black", stroke_width=10,
               start_arrow=arrow3, end_arrow=arrow3)

    arrow1 = elsie.Arrow(10, inner=2.0)
    slide.line([(900, 500), (1000, 500)], color="black", stroke_width=1,
               start_arrow=arrow1, end_arrow=arrow1)
    arrow2 = elsie.Arrow(20, inner=2.0)
    slide.line([(900, 550), (1000, 550)], color="black", stroke_width=5,
               start_arrow=arrow2, end_arrow=arrow2)
    arrow3 = elsie.Arrow(30, inner=2.0)
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
    slide.box(550, 350, 50, 50).rect(
        stroke_width=5, stroke_dasharray="2", color="black", rx=5, ry=5)


# Path demo ##############################################

@elsie.slide()
def path_demo(slide):
    slide.box(x=150, y=150).text("Path demo")

    root = slide.box(x=250, y="[50%]", width=100, height=50).rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5).text(
        "Root")
    child1 = slide.box(x=650, y="[20%]", width=100, height=50).rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5).text(
        "Child1")
    child2 = slide.box(x=650, y="[80%]", width=100, height=50).rect(color=COLOR1, bg_color="#EEE", rx=5, ry=5).text(
        "Child2")

    arrow = elsie.Arrow(10)

    # Path root -> child1
    r1 = root.p("100%", "50%")
    c1 = child1.p("0%", "50%")

    # See SVG <path> documentation for commands explanation
    # In short: M = move to, L = line to, C/S = bezier curve, Q/T = quadratic
    slide.path([("M", r1), ("C", r1.add(300, 0), c1.add(-300, 0), c1)], end_arrow=arrow, stroke_width=2, color=COLOR1)

    # Path root -> child2
    c2 = child2.p("0%", "50%")
    slide.path([("M", r1), ("Q", c2.add(-100, 0), c2)], end_arrow=arrow, stroke_width=2, color=COLOR1,
               stroke_dasharray="10")

    # Path chiled1 -> child1
    c1t = child1.p("50%", "0%")
    c1r = child1.p("100%", "50%")
    slide.path([("M", c1t), ("C", c1t.add(0, -100), c1r.add(100, 0), c1r)], end_arrow=arrow, stroke_width=2,
               color=COLOR1)

    # c3 = child2.p("50%", "50%")
    # slide.path([("M", c3.add(0, -100)),
    #            ("C", c3.add(100, -100), c3.add(100, -0), c3.add(0, 100)),
    #            ("C", c3.add(-150, -100), c3.add(-100, -10), c3.add(0, -100))], bg_color="#909090", color=None)#

    slide.path([("M", (650, 350)), ("L", (750, 350))], stroke_width=4, color="green")
    slide.path([("M", (600, 450)), ("L", (700, 250)), ("L", (800, 450))], stroke_width=4, color="red")
    slide.path([("M", (600, 450)), ("Q", (700, 250), (800, 450))], bg_color="blue", color=None)


# Chess board ##############################################

@elsie.slide()
def chessboard_demo(slide):
    # Create a chess board

    board = slide.box(width=500, height=500)
    board.new_style("black", color="black", size=50)

    colors = [COLOR1, COLOR2]
    tiles = {}
    for i in range(8):
        row = board.box(height="fill", width="100%", horizontal=True)
        for j in range(8):
            b = row.box(width="fill", height="100%")
            b.rect(bg_color=colors[(i + j) % 2])
            tiles[(j, i)] = b.overlay(z_level=1)
    board.rect(color=COLOR1, stroke_width=3)

    # Create the arrow
    points = [
        tiles[(3, 4)].mid_point(),
        tiles[(3, 2)].mid_point(),
        tiles[(4, 2)].mid_point()
    ]

    arrow = elsie.Arrow(30)
    slide.box(show="1-3").line(
        points, color="white", stroke_width=15, end_arrow=arrow)

    tiles[(3, 4)].box(show="1").text("♞", "black")
    tiles[(3, 3)].box(show="2").text("♞", "black")
    tiles[(3, 2)].box(show="3").text("♞", "black")
    tiles[(4, 2)].box(show="4").text("♞", "black")


# Size & Positioning demo #################################

@elsie.slide()
def position_demo(slide):
    slide.box().text("Position demo")
    slide.box(height=15)

    slide.new_style("inner", color="white", size=15)

    b = slide.box(width="70%", height=40)
    b.rect(color=COLOR1)
    bb = b.box(200, width="30%", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fixed position (x=200)", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color=COLOR1)
    bb = b.box("50%", width="30%", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Ratio (x='50%')", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color=COLOR1)
    bb = b.box("[50%]", width="30%", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Align (x='[50%]')", "inner")
    slide.box(height=30)

    slide.box().text("Size demo")
    slide.box(height=15)

    b = slide.box(width="70%", height=40)
    b.rect(color=COLOR1)
    bb = b.box(0, width="200", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fixed size (width=200)", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color=COLOR1)
    bb = b.box(0, width="50%", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Ratio (width='50%')", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40, horizontal=True)
    b.rect(color=COLOR1)
    bb = b.box(width="fill", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fill (width='fill')", "inner")

    slide.box(height=10)

    b = slide.box(width="70%", height=40, horizontal=True)
    b.rect(color=COLOR1)

    bb = b.box(width="fill", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fill (width='fill')", "inner")

    bb = b.box(width="fill(3)", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fill (width='fill(3)')", "inner")

    bb = b.box(width="fill(2)", height="fill")
    bb.rect(color=COLOR1, bg_color=COLOR2)
    bb.text("Fill (width='fill(2)')", "inner")


# Zoom to rectanle at position 300, 200 with size 400, 400
@elsie.slide(view_box=(300, 200, 400, 400))
def zoomed_position_demo(slide):
    position_demo(slide)
    slide.box(x=390, y=200).rect(bg_color="black").fbox(padding=10).text("Zooming demo", {"color": "white"})


@elsie.slide(debug_boxes=True)
def debugging_slides(slide):
    slide.new_style("header", size=35, color="white")
    slide.new_style("header2", size=25, color=COLOR1)

    slide.box(p_bottom=120, width=300, height=200, name="debug title").text("Debugging layout")

    title_box1 = slide.box(width="fill", height=120, name="title")
    title_box1.rect(bg_color=COLOR2)

    title_box2 = title_box1.fbox(p_y=10, name="header")
    title_box2.rect(bg_color=COLOR1)


    title_box2.text("Elsie: Slides in Python in Programmable Way", "header")

    slide.box(height=30, name="filler")

    # Subtitle box
    subtitle = slide.box(name="name")
    subtitle.text("Stanislav Böhm\n~tt{https://github.com/spirali/elsie}",
                  "header2")


# The final slide #################################

@elsie.slide()
def final_slide(slide):
    # Demonstration of inline style
    # we do not provide style name, but directly create
    # style in place
    slide.text("Have a nice day!", {"size": 60})


# RENDER THE SLIDES NOW!


elsie.render("example.pdf")
