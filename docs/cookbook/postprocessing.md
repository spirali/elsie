# Slide postprocessing
Sometimes you may want to add some global data to your slides, for example a footer, license
information or [slide numbers](#slide-numbering). To make it easier, you can pass a function to
the `slide_postprocessing` parameter of the [`render`](elsie.slides.Slides.render) method. The
function will receive a list of root boxes of each slide in the presentation. You can then go
through the list and modify the slides, for example by adding some text to them.

## Slide numbering
It is quite easy to add numbers to each slide using slide postprocessing. Here is an example:
```python
import elsie
slides = elsie.Slides()

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

slides.render(slide_postprocessing=page_numbering)
```
You can find the rendered PDF with slide numbers
[here](https://github.com/spirali/elsie/raw/master/examples/page_numbers/page_numbers.pdf).

You could also easily create a fragment number for each fragment of each slide by iterating numbers
up to the [`current_slide()`](elsie.slidecls.Slide.current_step) of each slide.
