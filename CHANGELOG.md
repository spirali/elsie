
# v2.0

## BREAKING CHANGE

### TextStyles

Text styles are not dictionaries any more but instances of `elsie.TextStyle`.

New methods for working with styles:

```
box.set_style("new-style", elsie.TextStyle(size=10))
box.update_style("new-style", elsie.TextStyle(bold=True))
```

Methods: `new_style` and `derive_style` were removed.

### Line box and Inline box

`line_box` and `inline_box` (previously `text_box`) has to be now called on
object returned by .text(...)

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

Argument `lines` in `line_box` is now renamed to `n_lines`


## NEW

Arguments `above` and `below` in `.box(..)` method.

```python
r = b.rect(...)
b.box(..,  below=r)  # The new box is drawn before rectangle 
```
