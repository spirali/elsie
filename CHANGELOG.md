
= v2.0

== BREAKING CHANGE

=== TextStyles

Text styles are not dictionaries any more but instances of `elsie.TextStyle`.

New methods for working with styles:

```
box.set_style("new-style", elsie.TextStyle(size=10))
box.update_style("new-style", elsie.TextStyle(bold=True))
```

Methods: `new_style` and `derive_style` were removed.

=== Line box and Inline box

`line_box` and `inline_box` (previously `text_box`) has to be now called on
object returned by .text(...)

Before:

```
b = ...box(...)
b.text(...)
b.line_box(...)
b.text_box(...)
```

Now:

```
b = ...box(...)
t = b.text(...)
t.line_box(...)
t.inline_box(...)
```

Argument `lines` in `line_box` is now renamed to `n_lines`