
from elsie import Slides, Arrow

# Let us our primary colors used in slides
COLOR1 = "#328cc1"
COLOR2 = "#d9b310"

# Top-level slide instances
slides = Slides()

# Modyfy global text styles
slides.update_style("default", color=COLOR1)  # Default font
slides.update_style("emph", color=COLOR2)     # Emphasis


# First slide #############################################

# Create a new slide, it actually returns instance of Box.
# We are going to create a lots of boxes
slide = slides.new_slide()

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

slide = slides.new_slide()

# Usage of inline styles; Syntax is ~ABC{Text}, it applies style ABC on Text.
slide.text("~emph{Elsie} is a slide framework based on ~emph{Python}\n")


# Hello world example #####################################

slide = slides.new_slide()

slide.box().text("~emph{Hello World} example:")

slide.box(height=20)  # Space reserving box

b = slide.box(width="100%")  # Box for code
b.rect(bg_color="#EEE")  # Background for code

# Method .code works as .text but it calls pygments for syntax highlight.
# The first argument is the used language
# We create another box just for applying small padding
b.box(p_x=20, p_y=10).code("python", """
from elsie import Slides

slides = Slides()
slide = slides.new_slide()
slide.text("Hello world!")

slides.render("output.pdf")
""")


# Text fragments ##########################################

slide = slides.new_slide()
slide.box().text("Elsie supports ...")

# One slide may generate more pages in resulting pdf
# Argument 'show' controls on which pages of the slides is the box shown.
# Possible values:
# "2" - Show only on the second page
# "2+" - Show from the second page to the last page
# "2-5" - Show on second page to 5th page
slide.box(show="2+").text("... fragments ...")
slide.box(show="3+").text("... revealing.")


# SVG image demo ##########################################

slide = slides.new_slide()

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

slide = slides.new_slide()
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

slide = slides.new_slide()
slide.box().text("Syntax Highlighting")
slide.box(height=30)
slide.box().code("c", """#include <stdio.h>

/* Hello world program */

int main() {
    printf("Hello world!\\n");
    return 0;
}""")


# Line highlighting #######################################

slide = slides.new_slide()
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
arrow = Arrow(10)
p1 = code_box.line_box(0).p("100%", "50%")
p2 = code_box.line_box(5).p("100%", "50%")
slide.box(show="6").line([p1, p1.add(40, 0),
                          p2.add(40, 0), p2],
                         stroke_width=3, color="orange", end_arrow=arrow)


# Console demo ############################################

slide = slides.new_slide()

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


# Text demo ###############################################

slide = slides.new_slide()

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

slide = slides.new_slide()


# A helper function for creating a bullet point and a box for content
def list_item(parent):
    b = parent.box(x=0, horizontal=True)
    b.box(width=25, y=0).text("•")  # A bullet point
    return b.box(width="fill")


main = slide.box()
main.update_style("default", align="left")

list_item(main).text("This is LIST DEMO")
list_item(main).text("This is\nmulti-line\nitem")
list_item(main).text("Last item")


# Columns demo ############################################

slide = slides.new_slide()
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

slide = slides.new_slide()
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


# Chess board ##############################################

slide = slides.new_slide()

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

arrow = Arrow(30)
slide.box(show="1-3").line(
    points, color="white", stroke_width=15, end_arrow=arrow)

tiles[(3, 4)].box(show="1").text("♞", "black")
tiles[(3, 3)].box(show="2").text("♞", "black")
tiles[(3, 2)].box(show="3").text("♞", "black")
tiles[(4, 2)].box(show="4").text("♞", "black")


# Size & Positioning demo #################################

slide = slides.new_slide()

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

bb = b.box(width="fill(2)", height="fill")
bb.rect(color=COLOR1, bg_color=COLOR2)
bb.text("Fill (width='fill(2)')", "inner")

bb = b.box(width="fill(3)", height="fill")
bb.rect(color=COLOR1, bg_color=COLOR2)
bb.text("Fill (width='fill(3)')", "inner")


# The final slide #################################

slide = slides.new_slide()
slide.update_style("default", size=60)
slide.text("Have a nice day!")

# RENDER THE SLIDES NOW!

slides.render("example.pdf")
