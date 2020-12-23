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
