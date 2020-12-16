# Getting started
Want to reuse some slide multiple times, with slight variants? Create a function and parametrize it.
Need to use the same font or color at multiple places, but you're not sure about its final value?
Just create a variable and change it at any time!

Elsie is a framework for making slides using Python.
Its API allows you to build SVG slides programmatically.
Inkscape is then used in the background to render SVG into PDF slides.

Full demonstration:
  * Result: [example.pdf](../examples/bigdemo/example.pdf)
  * Source code: [example.py](../examples/bigdemo/example.py)

## About this text
The main purpose of this text is to create a complete reference for Elsie, where
you can find all the various features that Elsie offers. While this text prioritizes
completeness, it tries to be accessible as much as possible. If you find
something that you do not understand, please let me know.

If you are looking for a more tutorial-like material, try to look at the example
above.

## Creating slides
By default, slides are created with ratio 4:3. More precisly, canvas 1024x768px
canvas is used as the default. However, as long everything is processed as
vector graphics, the exact numbers only influences numeric values of
coordinates, not the resulting resolution.

Another usefull argument is ``Slides`` is ``bg_color`` that allows to change default
background of the slides. The default color is white.

You can change this by the following code:

```python
# Setup slide size as 192x1035, i.e. 16:9

import elsie

slides = elsie.Slides(width=1920, height=1035)
elsie.set_global_slides(slides)
```

Slides are created in Elsie by creating a function and decorating it by
decorator ``@elsie.slide()``. It will create a slides in the same order as the
functions were defined. The decorated function should take a single parameter
that is the root box (see below) that represents the whole are of the slide.


```python
import elsie

@elsie.slide()
def slide1(slide):
    slide.text("First slide")

@elsie.slide()
def slide2(slide):
    slide.text("Second slide")

elsie.render()  # Creates two slide presentation.
```
