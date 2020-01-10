import elsie


@elsie.slide()
def slide1(slide):
    slide.text("Page numbering demo")


@elsie.slide()
def slide2(slide):
    slide.box().text("Hello world!")
    slide.box(show="next+").text("Hello world!")
    slide.box(show="next+").text("Hello world!")


@elsie.slide()
def slide3(slide):
    slide.box().text("Last slide")


def page_numbering(slides):
    for i, slide in enumerate(slides):
        slide.box(x="90%", y="90%", width=70, height=45).rect(bg_color="orange", rx=5, ry=5).text(
            "{}/{}".format(i + 1, len(slides)))


elsie.render(slide_preprocessor=page_numbering)
