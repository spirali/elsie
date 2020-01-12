import elsie


@elsie.slide()
def slide1(slide):
    slide.text("Page numbering demo")


@elsie.slide()
def slide2(slide):
    slide.box().text("Hello world!")
    slide.box(show="next+").text("Hello world!")
    slide.box(show="next+").text("Hello world!")

@elsie.slide(include_to_postprocessing=False)
def slide3(slide):
    slide.box().text("Not numbered slide")


@elsie.slide()
def slide4(slide):
    slide.box().text("Last slide")


def page_numbering(slides):
    numbered_slides = list(filter(lambda slide: slide.postprocess, slides))
    for i, slide in enumerate(numbered_slides):
        slide.box(x="90%", y="90%", width=70, height=45).rect(bg_color="orange", rx=5, ry=5).text(
            "{}/{}".format(i + 1, len(numbered_slides)))


elsie.render(slide_postprocessing=page_numbering)
