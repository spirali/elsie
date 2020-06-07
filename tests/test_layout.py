from elsie import Arrow


def test_header(test_env):
    slide = test_env.slide
    slide.new_style("header", color="white", align="right")
    slide.new_style("footer", color="white", size=15)
    header = slide.box(width="fill", height="10%")
    header.rect(bg_color="#5F8DD3")
    header.box(width="fill", p_right=20).text("Demo of Header", "header")
    content = slide.box(height="fill")
    content.text("Content")
    footer = slide.box(width="fill", height="5%", horizontal=True)
    b1 = footer.box(width="fill", height="fill")
    b1.rect(bg_color="#5F8DD3")
    b1.text("Hello!", "footer")
    b2 = footer.box(width="fill", height="fill")
    b2.rect(bg_color="#0F2DD3")
    b2.text("Footer!", "footer")
    b3 = footer.box(width="fill", height="fill")
    b3.rect(bg_color="#5F8DD3")
    b3.text("Hello!", "footer")
    test_env.check("header")


def test_full_box(test_env):
    slide = test_env.slide
    slide.box(width="fill", height="100%").rect(bg_color="green")
    test_env.check("fullbox")


def test_prepend(test_env):
    slide = test_env.slide
    slide.box().text("A")
    slide.box(prepend=True).text("B")
    slide.box(prepend=True).text("C")
    slide.box().text("D")
    test_env.check("prepend")


def test_vbox_nofill(test_env):
    slide = test_env.slide
    slide.box(width=20, height=40).rect(bg_color="green")
    b = slide.box(width="100%", height="40%")
    b.rect(bg_color="red")
    b.box(width="30%", height=20).rect(bg_color="white")
    b.box(width="100%", height="50%").rect(bg_color="orange")
    b.box(width="30%", height=20).rect(bg_color="white")
    slide.box(width="fill", height="10%").rect(bg_color="black")
    slide.box(width="20%", height="15%").rect(bg_color="blue")
    test_env.check("vbox-nofill")


def test_vbox_fill(test_env):
    slide = test_env.slide
    slide.box(width=20, height=40).rect(bg_color="green")
    b = slide.box(width="100%", height="fill")
    b.rect(bg_color="red")
    b.box(width="30%", height="fill").rect(bg_color="white")
    b.sbox(height="fill").rect(bg_color="orange")
    b.box(width="30%", height="fill").rect(bg_color="white")
    slide.box(width=20, height="10%").rect(bg_color="green")
    slide.box(width="fill", height="fill").rect(bg_color="black")
    slide.box(width="20%", height="15%").rect(bg_color="blue")
    test_env.check("vbox-fill")


def test_hbox_nofill(test_env):
    slide = test_env.slide
    box = slide.box(width="70%", height="70%", horizontal=True)
    box.sbox(width=20).rect(bg_color="green")
    box.box(width="10%", height="30%").rect(bg_color="black")
    box.sbox(width="20%").rect(bg_color="red")
    box.sbox(width=20).rect(bg_color="green")
    test_env.check("hbox-nofill")


def test_hbox_fill(test_env):
    slide = test_env.slide
    box = slide.box(width="70%", height="70%", horizontal=True)
    box.sbox(width=20).rect(bg_color="green")
    box.box(width="fill", height="30%").rect(bg_color="black")
    box.sbox(width="fill").rect(bg_color="red")
    box.sbox(width=20).rect(bg_color="green")
    test_env.check("hbox-fill")


def test_columns(test_env):
    slide = test_env.slide
    slide.box(padding=40).text("Columns demo")
    columns = slide.box(width="80%", horizontal=True)
    columns.rect(color="black")

    column1 = columns.box(width="30%")
    column1.text("This is some text\nin the first\ncolumn")

    columns.box(p_x=10).box(width=3).rect(bg_color="black")

    column2 = columns.box(width="30%")
    column2.code("python", "print 'Hello world!'")

    column1 = columns.box(width="30%")
    column1.text("Some text again\nin the third\ncolumn")
    test_env.check("columns")


def test_chess(test_env):
    slide = test_env.slide
    board = slide.box(width=500, height=500)
    board.new_style("black", color="black", size=50)

    colors = ["#e0e0ff", "#A0A0ff"]
    tiles = {}
    for i in range(8):
        row = board.box(height="fill", width="100%", horizontal=True)
        for j in range(8):
            b = row.box(width="fill", height="100%")
            b.rect(bg_color=colors[(i + j) % 2])
            tiles[(j, i)] = b.overlay(z_level=1)
    board.rect(color="black")

    points = [
        tiles[(3, 4)].mid_point(),
        tiles[(3, 2)].mid_point(),
        tiles[(4, 2)].mid_point(),
    ]

    arrow = Arrow(30)
    slide.box(show="1-3").line(points, color="green", stroke_width=15, end_arrow=arrow)

    tiles[(3, 4)].box(show="1").text("♞", "black")
    tiles[(3, 3)].box(show="2").text("♞", "black")
    tiles[(3, 2)].box(show="3").text("♞", "black")
    tiles[(4, 2)].box(show="4").text("♞", "black")
    test_env.check("chess", 4)


def test_size_and_pos(test_env):
    slide = test_env.slide

    slide.box().text("Position demo")
    slide.box(height=30)

    slide.new_style("inner", color="white", size=15)

    b = slide.box(width="70%", height=40)
    b.rect(color="black")
    bb = b.box(200, width="30%", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fixed position (x=200)", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color="black")
    bb = b.box("50%", width="30%", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Ratio (x='50%')", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color="black")
    bb = b.box("[50%]", width="30%", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Align (x='[50%]')", "inner")
    slide.box(height=30)

    slide.box().text("Size demo")
    slide.box(height=30)

    b = slide.box(width="70%", height=40)
    b.rect(color="black")
    bb = b.box(0, width="200", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fixed size (width=200)", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40)
    b.rect(color="black")
    bb = b.box(0, width="50%", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Ratio (width='50%')", "inner")
    slide.box(height=10)

    b = slide.box(width="70%", height=40, horizontal=True)
    b.rect(color="black")
    bb = b.box(width="fill", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fill (width='fill')", "inner")

    slide.box(height=10)

    b = slide.box(width="70%", height=40, horizontal=True)
    b.rect(color="black")

    bb = b.box(width="fill", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fill (width='fill')", "inner")

    bb = b.box(width="fill(2)", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fill (width='fill(2)')", "inner")

    bb = b.box(width="fill(3)", height="fill")
    bb.rect(color="black", bg_color="#5F8CA3")
    bb.text("Fill (width='fill(3)')", "inner")

    test_env.check("sizepos")
