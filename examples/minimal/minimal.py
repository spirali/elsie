import elsie


@elsie.slide()
def hello(slide):
    slide.text("Hello world!")


elsie.render()
