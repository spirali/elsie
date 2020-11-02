import elsie
import subprocess

@elsie.slide()
def hello(slide):
    slide.text("Hello world!")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def boxdemo0(slide):
    slide.box().text("Box 1")
    slide.box().text("Box 2")
    slide.box().text("Box 3")
    slide.rect(color="black", stroke_width=4)


@elsie.slide(debug_boxes=True)
def boxdemo1(slide):
    slide.box().text("Box 1")
    slide.box().text("Box 2")
    slide.box().text("Box 3")


@elsie.slide(debug_boxes=True)
def sizedemo1(slide):
    slide.box().text("Box 1")
    slide.box(width=300, height=100).text("Box 2")
    slide.box(width="100%").text("Box 3")


@elsie.slide(debug_boxes=True)
def composition(slide):
    slide.box(padding=40).box(padding=40).box(padding=40).text("Box 1")


@elsie.slide(debug_boxes=True)
def filldemo1(slide):
    slide.box().text("Box 1")
    slide.box(width=300, height=100).text("Box 2")
    slide.box(height="fill").text("Box 3")


@elsie.slide(debug_boxes=True)
def padding_demo(slide):
    slide.box(width=200, height=200, p_left=100, name="Top box")
    slide.box(width=200, height="fill", p_y=100, name="Bottom box")


@elsie.slide(debug_boxes=True)
def horizontal(slide):
    parent = slide.box(width="100%", height="100%", horizontal=True)
    parent.box().text("Box 1")
    parent.box().text("Box 2")
    parent.box().text("Box 3")


@elsie.slide(debug_boxes=True)
def xy(slide):
    b = slide.box(width=100, height=100, name="First")
    slide.box(x=b.x("50%"), y=b.y("50%"), width=100, height=100, name="Second")
    slide.box(x=0, y=b.y("100%"), width="100%", height=200, name="Third")


@elsie.slide()
def paiting1(slide):
    slide.box(x="[40%]", y="[40%]", width=300, height=300).rect(bg_color="red")
    slide.box(x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def paiting2(slide):
    red = slide.box(x="[40%]", y="[40%]", width=300, height=300)
    red.rect(bg_color="red")
    slide.box(x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(below=red, x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def paiting3(slide):
    slide.box(x="[40%]", y="[40%]", width=300, height=300).rect(bg_color="red")
    slide.box(z_level=1, x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def steps(slide):
    slide.box().text("Box 1")
    slide.box(show="2+").text("Box 2")
    slide.box(show="3+").text("Box 3")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def text1(slide):
    slide.text("Hello world!", elsie.TextStyle(size=70, color="red"))
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def text2(slide):
    default_style = slide.get_style("default")
    default_style.color = "orange"
    slide.set_style("default", default_style)
    slide.text("Hello world!")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def inline_styles(slide):
    slide.set_style("red", elsie.TextStyle(color="red"))
    slide.text("Normal text ~red{red text} ~tt{Typewriter text}")
    slide.rect(color="black", stroke_width=4)


@elsie.slide(debug_boxes=True)
def scale_to_fit(slide):
    slide.box(width=300, height=80).text("Hello world!", scale_to_fit=True)
    slide.box(width=80, height=300).text("Hello world!", scale_to_fit=True)


@elsie.slide()
def code(slide):
    slide.box().code("python", """
        x = "Elsie"
        print("Hello", x)
    """)
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def textboxes(slide):
    text_item = slide.box().text("""This is a long
    text ~#A{that} takes
    3 lines.
    """)

    text_item.line_box(2, z_level=-1).rect(bg_color="red")
    text_item.inline_box("#A", z_level=-1).rect(bg_color="green")
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def rectangle(slide):
    box = slide.box(x="[50%]", y="[50%]", width="80%", height=300)
    box.rect(bg_color="green", color="red", stroke_width=10, stroke_dasharray="10 4", rx=20, ry=20)
    slide.rect(color="black", stroke_width=4)


@elsie.slide()
def textrect(slide):
    slide.box().rect(bg_color="#aaf").text("Hello!")
    slide.rect(color="black", stroke_width=4)


svgs = elsie.render(return_svg=True)  # Creates file 'slides.pdf'
#svgs = elsie.render(return_svg=False)  # Creates file 'slides.pdf'

slides = elsie.get_global_slides()

for slide, step, out in svgs:
    name = slide._box.name
    if step == 1:
        filename = "imgs/{}.svg".format(name)
    else:
        filename = "imgs/{}-{}.svg".format(name, step)
    print(name)
    with open(filename, "w") as f:
        f.write(out)
    subprocess.check_call(["inkscape", "-b", "#ffffff", "--export-type", "png", filename])