import elsie

slides = elsie.SlideDeck()


@slides.slide()
def slide1(slide):
    slide.text("Page numbering demo")


@slides.slide()
def slide2(slide):
    slide.box().text("Hello world!")
    slide.box(show="next+").text("Hello world!")
    slide.box(show="next+").text("Hello world!")


@slides.slide()
def slide3(slide):
    slide.box().text("Last slide")


def page_numbering(slides):
    for i, slide in enumerate(slides):
        slide.box(x="90%", y="90%", width=70, height=45).rect(
            bg_color="orange", rx=5, ry=5
        ).text(f"{i + 1}/{len(slides)}")


slides.render("page_numbers.pdf", slide_postprocessing=page_numbering)
