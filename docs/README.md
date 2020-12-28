# Elsie
**Elsie** allows you to **create slides programmatically** using Python. It is a Python library
that lets you build [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) slides in a
composable way and then render them to PDF. There is no DSL or GUI – presentations created with
*Elsie* are fully programmed with Python.

It was created out of frustration of having to deal with
[existing tools](#comparison-to-other-tools) for creating presentations. We believe that creating
presentations should be automated and programmable as much as possible.

**Quick links**

- [Installation](installation.md)
- [Getting started](getting_started.md)
- [User guide](userguide/basics.md)
- [Gallery](gallery.md)
- [API Reference](apidoc)

## Elsie example
```elsie,skip=3:-1
import elsie
slides = elsie.SlideDeck()

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
- **Layout model** *Elsie* provides a simple, yet powerful layout model. Need rows? Columns?
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
- **Google slides/PowerPoint**
These tools are fine if you need to make a bunch of very simple slides quickly, but using them
gets very annoying if you need anything more complex. You need to place all items manually,
alignment is usually a mess, fragments (animations) are not supported very well. If you need to
change some small detail (placement, style, color) of a thing that is repeated on many slides, you
pretty much have to go through all the slides and modify them by hand, one by one. Displaying source
code with syntax highlighting is notoriously badly supported, so often you have to resort to
exporting the highlighted code from [carbon.sh](https://carbon.sh) or screenshotting it from your
IDE, both of which are far from ideal. Also, you can't really use source control (e.g. `git`) to
version your presentation, which is a shame.

    However, PowerPoint does allow you to create continuous animations (if you do not export to PDF
    of course), so if you need that, it might be a good choice.

- **LaTeX/Beamer**
LaTeX (Beamer) produces fine-looking presentations, has good support for syntax highlighting and
can be versioned easily. However, in our experience it is not that easy to create custom diagrams
and animations using LaTeX, mainly because of its declarative nature. If you can speak in
[TikZ](https://www.overleaf.com/learn/latex/TikZ_package) and you understand the error messages of
`pdflatex`, you are probably fine. If not, creating slides with complex animations, diagrams and
source code snippets might be easier for you in Python.

    While *Elsie* also has basic support for rendering [LaTeX](userguide/latex.md), if your
    presentation is mostly composed of math formulas, it might be easier to create it in LaTeX
    directly.

- **Reveal.js**
[reveal.js](https://revealjs.com) is a great tool for making HTML presentations. It supports syntax
highlighting, has good-looking animations and can be versioned. However, it shares some disadvantages
of LaTeX/Beamer, which stems from the fact that it is also declarative. Creating an animation that
would walk line-by-line through a source code snippet or that would repeatedly display and hide
objects in custom fragments is difficult. You can actually use JavaScript to create more complex
animations, but it's not integrated very well, and the library itself does not offer you any API
to make it easier.

    That being said, if you are fine with declarative description of slides, and you prefer
    HTML/CSS to Python/SVG, I would recommend you to use `reveal.js`.

- **Prezi**
If you want presentations with three or more dimensions, it's a good choice. Otherwise, the
disadvantages of PowerPoint also apply here.

None of the above solutions allow you to build slides using (an imperative) programming language,
which gives you a number of useful powers. You can split a large presentation into several
modules/files, parametrize animations or objects that appear often using functions, create
arbitrarily complex slides and animations or interactively modify the font, aspect ratio or text
color/size of your whole presentation by changing a single line of code. This is the ultimate
feature of *Elsie* that is not available in the other tools.

## FAQ
- **Why do you use `Inkscape` instead of e.g. `Cairo` for rendering slides?**
We are experimenting with a `Cairo` backend, but it would be probably difficult to fully support
embedding SVG images into slides with Cairo, which is something that we use a lot. But it is
possible that *Elsie* will not require `Inkscape` sometime in the future.
- **Why don't you use an existing layout model, e.g. `flexbox`?**
We made the [layout model](userguide/layout.md) tailored for presentations, which might not be
so easy with a general layout model. And honestly, we couldn't find any usable binding of
a standalone and sane layout model in Python. If you know of any, please
[let us know](https://github.com/spirali/elsie/issues).

## License
[MIT](https://github.com/spirali/elsie/blob/master/LICENSE).

Created by [Stanislav Böhm](https://github.com/spirali) and
[Jakub Beránek](https://github.com/kobzol).
