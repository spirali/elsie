import elsie

slides = elsie.Slides()


@slides.slide()
def hello(slide):
    slide.text("Hello world!")


slides.render("minimal.pdf")
