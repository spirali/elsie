# Headers and footers
It is quite common to use a unified header and/or footer for all slides of a slide deck. You can
achieve this using *Elsie* e.g. by creating a factory function for each slide:
```elsie,type=lib
def init_slide(slide, header_text: str):
    # Create a header with some background color
    header = slide.box(width="fill", height="10%").rect(bg_color="#23363A")

    # Put some text into the header
    header.box(x=10, padding=10).text(header_text, style=elsie.TextStyle(
        size=30,
        bold=True,
        color="#FFFFFF"
    ))

    # Return the remaining content of the slide 
    return slide.fbox()
```

And then calling this function on each slide to give it a header.

```elsie,width=600
@slides.slide()
def slide1(slide):
    content = init_slide(slide, "Welcome")
    content.text("Welcome to my presentation")
```

```elsie,width=600
@slides.slide()
def slide2(slide):
    content = init_slide(slide, "Outline")
    content.text("Here is the outline of my presentation")
```
