Note: This file documents major changes visible to users; see Git history for detailed log.

# v3.2

## Fixes

* Comptability with Inkscape 1.1

## New features

### New modules in extension added:

* Simple export to pptx (slides as PNG pictures)

```python
from elsie.ext.export import export_pptx

export_pptx(slides, "output.pptx")
```

* Todo placeholder

```python
from elsie.ext.todo import todo_placehodler

todo_placeholder(box)
```

# v3.1

## New features

### Add new experimental Cairo backend
You can use the new Cairo backend to render slides without the need to install `Inkscape`.
To use it, install elsie with the `cairo` extra package:
```bash
$ pip install elsie[cairo]
```

And then pass `CairoBackend` to `SlideDeck`:
```python
import elsie
from elsie.render.backends import CairoBackend

slides = elsie.SlideDeck(backend=CairoBackend())
```

# v3.0

## Breaking changes

### Global instance of Slides is removed and Slides are renamed to SlideDeck

Global slides were removed. You can just create instance of Slides (now SlideDeck)
as follows:

Before:
```python
elsie.slide()
def a_function(slide):
    pass
```

Now:
```python
slides = elsie.SlideDeck()

slides.slide()
def a_function(slide):
    pass
```

### Box arguments are now "keyword only"

Before you could write:

```python
slide.box(50, 0, 100, 100)
```

To avoid confusion, positional arguments are disabled and all arguments have to be named:

```python
slide.box(x=50, y=0, width=100, height=100)
```


## New features

* [New documentation](https://spirali.github.io/elsie/)
* Large speedup in slide rendering by using Inkscape shell interface
* `ext` package with support for [lists](https://spirali.github.io/elsie/userguide/lists/) and [markdown](https://spirali.github.io/elsie/userguide/lists/)
* [Jupyter integration](https://spirali.github.io/elsie/userguide/jupyter/)


# v2.1

## New features

* ORA support
* Method TextStyle.compose()

# v2.0
## Breaking changes
### TextStyles
Text styles are no longer dictionaries. From now on, they will be instances of `elsie.TextStyle`.

New methods for working with styles:

```
box.set_style("new-style", elsie.TextStyle(size=10))
box.update_style("new-style", elsie.TextStyle(bold=True))
```

Methods `new_style` and `derive_style` were removed.

### Line box and Inline box
`line_box` and `inline_box` (previously `text_box`) can be now only used on objects returned by
the `text` or `code` methods.

Before:
```python
b = ...box(...)
b.text(...)
b.line_box(...)
b.text_box(...)
```

Now:
```python
b = ...box(...)
t = b.text(...)
t.line_box(...)
t.inline_box(...)
```

Argument `lines` in `line_box` was renamed to `n_lines`.

## New features
Arguments `above` and `below` in `.box(..)` method. See
[documentation](https://spirali.github.io/elsie/userguide/layout/#modifying-render-order)
for their explanation.
```python
r = b.rect(...)
b.box(..,  below=r)  # The new box is drawn before rectangle
```
