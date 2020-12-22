# Elsie
**Elsie** allows you to **create slides programmatically** using Python.

*Elsie* is a Python library that lets you build
[SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) slides in a
composable way and then render them to PDF. There is no DSL or GUI –
presentations created with *Elsie* are fully programmed with Python.

## Hello world
```elsie,skip=3:-1
import elsie
slides = elsie.Slides()

@slides.slide()
def hello_world(slide):
    import datetime
    slide.box().text(f"Hello from")

    year = str(datetime.datetime.now().year)
    row = slide.box(horizontal=True, p_top=20)
    for i in range(4):
        row.box(width=40, height=40).rect(
          color="black",
          bg_color="black" if i % 2 == 0 else "white"
        ).text(year[i], elsie.TextStyle(color="red"))

slides.render("slides.pdf")
```

## Features
- **Automatic layout** *Elsie* provides a simple, yet powerful layout model. Need rows? Columns?
Padding? Aligned text? Relative/absolute positioning? Automatic scaling? We got you covered.

- **Animations and fragments** Reveal your slides gradually using fragments or create custom
step-by-step animations using Python code. Or draw a fine-tuned SVG image by hand in `Inkscape` and
let *Elsie* turn it into an animation using a handy
[layer-naming convention](userguide/images.md#embedding-fragments-in-images).

- **Source code highlighting** Enjoy beautiful code snippets thanks to built-in
[source code highlighting](userguide/syntax_highlighting.md). Create code walkthroughs using
individual [line highlighting](userguide/syntax_highlighting.md#line-and-inline-boxes) or
[arrows](userguide/shapes.md#arrow-head) pointing to specific code elements.

- **Batteries included** Leverage familiar SVG features - fonts, colors, dashed line borders.
Include `PNG/JPG/SVG/ORA` images directly into your slides. Render [LaTeX](userguide/layout.md)
into your slides. Debug your slides interactively in [Jupyter notebooks](userguide/jupyter.md).

- **Familiarity** At its heart, *Elsie* is a streamlined API for creating SVG images, optimized for
making presentations. If you know the basics of Python and SVG, you'll be right at home.

*Every tool has its disadvantages though.*

- *Elsie* provides a rather low-level API. While that means that you can create a slide in almost
any way you like, you will sometimes have to roll up your sleeves to achieve your desired goal.
But once you implement it, you can just put it inside a function and reuse it the next time!
- *Elsie* produces PDF slides, so it can only create animations with a single frame per page.
If you need 60 FPS animations or GIFs in your presentations, this tool is not for you.
- *Elsie* currently renders SVG slides to PDF using `Inkscape`. Therefore, you must have it
installed on your system for it to work. We provide a
[Docker image](installation.md#docker-installation) with `Inkscape` for convenience.
- *Elsie* is tested only on Linux. If you find a problem on a different platform, do not hesitate
to open a [GitHub issue](https://github.com/spirali/elsie/issues/new).

## Comparison to other tools
- Reveal.js
TODO
- Google slides/PowerPoint
TODO
- Beamer
TODO

## FAQ
- Why do you use `Inkscape` instead of e.g. `Cairo`?
We are experimenting with a `Cairo` backend. It would be probably difficult to fully support
embedding SVG images into slides with Cairo, but it is possible that *Elsie* will not require
Inkscape in the future.
- Why don't you use a known layout model, e.g. `flexbox`?
TODO: ???
Also, we haven't found a usable binding of any layout model in Python. If you know of any, please
let us know.
- Why is there no support for lists in `Elsie`?
Even though a list might sound like a simple feature, it would be difficult to create an abstraction
that would match everyone's needs. We instead provide an [example function](cookbook/lists.md) for
creating a list which you can copy and modify for your use case.

## License
[MIT](https://github.com/spirali/elsie/blob/master/LICENSE).

Created by [Stanislav Böhm](https://github.com/spirali) and
[Jakub Beránek](https://github.com/kobzol).
