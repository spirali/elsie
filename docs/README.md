# Elsie
**Elsie** allows you to **create slides programmatically** using Python.

Elsie is a Python library that lets you build
[SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) slides in a composable way and
then render them to PDF. There is no DSL or GUI – presentations created with *elsie*
are fully programmed with Python!

## Hello world
```python
import elsie, getpass

@elsie.slide()
def hello_world(slide):
    slide.text(f"Hello world from {getpass.getuser()}!")

elsie.render("slides.pdf")
```
<img width="512px" height="384px" src="slide_imgs/hello.png">

## Features
- **Fully programmable presentations!** No more annoying clicking or manually going through hundreds
of slides just to change the font – change a single line of code and regenerate your whole presentation
with a single command. Noticed a typo that spans all slides a moment before your big talk begins?
Just fix it and recreate the whole presentation within seconds! Experience the power of Turing-complete
presentations.
- **Automatic layout** *Elsie* provides a simple yet powerful layout model that can automatically
layout anything. Need rows? Columns? Grids? Padding? Aligned text? Relative positioning? Automatic
scaling? We got you covered. Oh, you want to draw a `64x32` image at the coordinates `(x=105, y=42)`?
You can do that too!
- **Animations and fragments** Reveal your slides gradually using fragments or create custom
step-by-step animations using Python code. Or draw a fine-tuned SVG image by hand in `Inkscape`
and let *Elsie* turn it into an animation using a handy [layer-naming convention](TODO).
- **Source code highlighting** Enjoy automatic [source code highlighting](TODO). Create code walkthroughs
using individual line highlighting or arrows pointing to specific code elements.
- **Batteries included** Leverage familiar SVG features - fonts, colors, dashed line borders,
you name it. Include `PNG/JPG/SVG` images directly into your slides. Render [LaTex](TODO) into your
slides. Debug your slides interactively in [Jupyter notebooks](TODO).
- **Familiarity** At its heart, *Elsie* is an API for creating SVG images, optimized for making slides.
If you know basics of Python and SVG, you'll be right at home.

Every tool has its disadvantages though.

- *Elsie* provides a rather low level API. While that means that you can create a slide in any way
you like, on the other hand you also sometimes have to do some extra work to achieve results that
are trivial in e.g. Powerpoint. TODO: lists
- *Elsie* produces PDF slides, so it can only create animations with a single frame per slide. If you
need 60 FPS animations or GIFs, you will be better off with e.g. PowerPoint.
- Currently, *Elsie* renders SVG slides to PDF using `Inkscape`. Therefore you must have it installed
on your system for it to work. We provide a [Docker image](installation.md#docker-installation) with
`Inkscape` for convenience.
- It will probably only work on Linux.

## How does it work?
TOOD: Inkscape, queries, pillow, etc.
