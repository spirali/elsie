# Getting started
This is a short tutorial that explains the basic of using *Elsie* and links to the user guide,
which explains individual concepts in more detail.

## Creating a slide deck
To build a presentation with *Elsie*, you first have to import it and create an instance of a
[`SlideDeck`](elsie.slides.slidedeck.SlideDeck):
```python
import elsie
slides = elsie.SlideDeck()
```
`SlideDeck` is used to add slides to your presentation and also to render the slides to PDF at the
end. You can find more about if [here](userguide/basics.md).

## Adding slides
The easiest way of adding slides to the slide deck is to create a function for each slide and
mark it with the [`slide`](elsie.slides.slidedeck.SlideDeck.slide) decorator:
```python
@slides.slide()
def slide1(slide):
    # ...
```
Each decorated function will receive a slide as its parameter. It should then fill the slide with
the desired content.

## Adding slide content
You can add various things to slides, like [text](userguide/text.md),
[images](userguide/images.md), [source code](userguide/syntax_highlighting.md),
[shapes](userguide/shapes.md), etc. Each item added to a slide needs to be inside a
[Box](userguide/layout.md) which will decide its layout.

You can create a new box by calling the `box` method on a slide. Inside a box you can then e.g.
write some text and apply a style to it:
```python
@slides.slide()
def slide1(slide):
    slide.box().text("Hello world")
    slide.box().text("This slide was created by Elsie", style=elsie.TextStyle(bold=True))
```
By default, multiple boxes will be stacked below one another and horizontally centered. You can
change these properties by modifying the
[box properties](userguide/layout.md#default-box-layout-properties).

*Elsie* has built-in support for fragments, which means that you can easily reveal individual boxes
gradually, using the `show` parameter:
```python
@slides.slide()
def slide2(slide):
    slide.box(show="1-2").text("I am shown in fragments 1 and 2")
    slide.box(show="2+").text("I am shown in fragment 2 and 3")
    slide.box(show="3").text("I am shown in fragment 3")
```
You can find more about revealing [here](userguide/revealing.md).

## Rendering slides
After you build all slides of your presentation, call the
[`render`](elsie.slides.slidedeck.SlideDeck.render) method to build the resulting PDF file:
```python
slides.render("slides.pdf")
```
You can also e.g. return a list of slides in raw SVG form or postprocess all slides. See more
details about rendering slides [here](userguide/basics.md#rendering-slides).

You can check the user guide or the cookbook to find more detailed guides about individual concepts
present in *Elsie*.

For completeness, here is the full code that was shown in this tutorial:
```python
import elsie
slides = elsie.SlideDeck()

@slides.slide()
def slide1(slide):
    slide.box().text("Hello world")
    slide.box().text("This slide was created by Elsie", style=elsie.TextStyle(bold=True))

    
@slides.slide()
def slide2(slide):
    slide.box(show="1-2").text("I am shown in fragments 1 and 2")
    slide.box(show="2+").text("I am shown in fragment 2 and 3")
    slide.box(show="3").text("I am shown in fragment 3")

slides.render("slides.pdf")
```
