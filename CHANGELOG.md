
= v2.0

== BREAKING CHANGE

`line_box` and `inline_box` (previosly `text_box`) has to be now called on
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