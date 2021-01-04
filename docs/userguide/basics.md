# Basics
A presentation (set of slides) is represented in *Elsie* with the
[`SlideDeck`](elsie.slides.slidedeck.SlideDeck) class. The most important parameters of the
presentation is the width and height of the resulting PDF pages, which also affects the resulting
aspect ratio. The default size if `1024x768`, which corresponds to aspect ratio `4:3`.

Here is an example of creating a new presentation:
```python
import elsie
slides = elsie.SlideDeck(width=1024, height=768)
```
Once you have a `SlideDeck` object, you can create new slides from it.

## Creating slides
You can create new slides in two ways, either using the [`new_slide`](elsie.slides.slidedeck.SlideDeck.new_slide)
method or via a [decorator](#decorator). The `new_slide` method will create a new slide, but for
convenience, it will not return the slide itself, but its [root box](layout.md), so that you can
use the returned object immediately for adding things to the slide. Except for some advanced usage,
you shouldn't ever need to deal with the [`Slide`](elsie.slides.slide.Slide) instance itself.

```python
slide = slides.new_slide(bg_color="blue")
```

Once you have a slide, you can add content to it, for example [text](text.md), [images](images.md),
[shapes](shapes.md) or [source code](syntax_highlighting.md).

### Decorator
A more convenient way of creating a slide is using the [`slide`](elsie.slides.slidedeck.SlideDeck.slide)
decorator. If you apply it to a function, it will create a new slide and pass its root box as a
parameter to the function. It will also set the name of the slide according to the name of the
decorated function.

```python
@slides.slide()
def slide1(slide: elsie.Box):
    slide.box().text("Hello")
```

With this approach, the slide will be added to the slide deck immediately when you use the
decorator. Therefore, you should not call the decorated function manually. The order of the slides
will be the same as in the source code:

```python
@slides.slide()
def slide1(slide):
    slide.text("Slide 1")

@slides.slide()
def slide2(slide):
    slide.text("Slide 2")
```
You can also combine the decorator and `new_slide`, although this is mostly discouraged, as it get
be confusing to follow the order of the slides.

Both `slide` and `new_slide` have parameters that allow you to change the background color and SVG
viewbox of the slide (see example usage [here](../cookbook/zoom.md)). You can also choose
its name (see [below](#name-policy)) or enable [debug draw mode](layout.md#debug-draw-mode).

## Rendering slides
After you have created all of your desired slides and filled them with content, you can render your
presentation using the [`render`](elsie.slides.slidedeck.SlideDeck.render) method. There are several useful
parameters of this method:

- `output`: Change the output filename of the rendered PDF (default is `slides.pdf`).
- `slide_postprocessing`: Apply some postprocessing function to all slides. See an example
[here](../cookbook/postprocessing.md).
- `select_slides`: Render only a selected subset of slides.
- `return_units`: Return a list of SVG slides without rendering them. This can be useful if you
just want to build your slides using *Elsie*, but render them in a another way.
- `slider_per_page(x, y)`: Group several slides into a single page. Each page will contain a grid
of slides with `x` rows and `y` columns. This can be useful e.g. for creating presentation
previews.

*Elsie* uses caching to speed-up the rendering. The cache will be created in a directory named
`elsie-cache`.

## Name policy
If you create slides in an interactive Python session (for example in `IPython` or
[Jupyter](jupyter.md)), you might inadvertedly create new slides after modifying and re-executing
a piece of code.

For example, if this code was inside a Jupyter notebook cell:
```
@slides.slide()
def slide1(slide):
    slide.box().text("Hello")
```
Each time you would execute the cell, a new slide would be added to the presentation, which is
probably not what you want.

To solve this issue, *Elsie* contains a so-called *name policy*, which decides how to react to the
situation where the same slide is created repeatedly. SlideDeck are identified by their name, which you
either pass to `new_slide` or it is determined automatically if the [decorator](#decorator) is used.

The `SlideDeck` instance has one of the following name policies, which decides what to do when a new
slide is created:

- `unique`: Creating two slides with the same name will result in an error. This is to stop you from
creating multiple instances of the same slide inadvertedly. Note that when a name of a slide is
unset (it is `None`), the slide will be allowed to be created.
- `replace`: When a slide with the same name already exists, the previous slide will be removed, and
the new slide will be placed at the end of the slide list.
- `ignore`: The name of slides will not be checked, essentially turns off name policy.
- `auto` (the default): Uses `replace` when running inside Jupyter, otherwise uses `unique`.

Since Jupyter automatically sets a name policy which is most probably the one that you want in an
interactive environment (`replace`), you will not have to deal with name policy most of the time.
