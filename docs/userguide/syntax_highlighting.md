# Syntax highlighting
*Elsie* uses `Pygments` to provide syntax highlighting. You can use any supported language from
this [list](https://pygments.org/languages).

You can use the [`code`](elsie.boxtree.boxmixin.BoxMixin.code) function on a
box to render text with syntax highlighting. The first parameter of the function is the language
syntax that should be highlighted.
```elsie,height=150
slide.box().code("python", """
name = "Elsie"
print("Hello", name)
""")
```

### Differences to `text`
The `code` method behaves similarly as the `text` method, with two exceptions:

- The `code` method uses the text style `"code"` as a base style (instead of `"default"`).
- If you want to use inline styles, you have to explicitly enable them by passing `use_styles=True`.

## Line numbering
You can render line numbers using the parameter `line_numbers`. The style of line numbers can be
modified by changing the `code_lineno` style.
```elsie
style = slide.get_style(
    "code_lineno",
    full_style=False
).compose(elsie.TextStyle(color="red"))
slide.set_style("code_lineno", style)

slide.box().code("python", """
a = 1
b = 2
c = 3
""", line_numbers=True)
```

## Line and inline boxes
The [`text`](elsie.boxtree.boxmixin.BoxMixin.text) and [`code`](elsie.boxtree.boxmixin.BoxMixin.code) methods
return a special [`TextBoxItem`](elsie.text.textboxitem.TextBoxItem) item that offers the following two
methods:

- [`line_box`](elsie.text.textboxitem.TextBoxItem.line_box) creates a box around a specified line (line
numbers are counted from 0). Other arguments are forwarded to the box. You can use this to create
e.g. colored boxes around selected code lines.

```elsie,height=150
box = slide.box().code("python", """
name = "Elsie"
print("Hello", name)
""")

box.line_box(1, z_level=-1).rect(bg_color="orange")
```

- [`inline_box`](elsie.text.textboxitem.TextBoxItem.inline_box) creates a box around text which is
wrapped with the given style. If there are multiple occurrences of the specified inline style, you
can specify which one do you want by the `nth` argument. `style_name` can be any existing style
name or a dummy style that starts with the `"#"` character. Dummy styles do not have to be defined
and they do not have any visual effect. They serve purely for defining inline boxes.

```elsie
text_item = slide.box().text("""This is a long
text ~#A{that} takes
3 lines.
""")

text_item.inline_box("#A", z_level=-1).rect(bg_color="green")
```

Note that boxes created by `line_box` and `inline_box` are always created after the box containing
the text. Therefore, to render them below the text, you have to use the `z_level` or `below`
parameters (see [Modifying render order](layout.md#modifying-render-order)).
