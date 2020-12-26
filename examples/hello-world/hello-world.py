import elsie

slides = elsie.SlideDeck()


@slides.slide()
def hello(slide):
    slide.text("Hello world!")


slides.render("minimal.pdf")
