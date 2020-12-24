# Text
You can render text by calling the [`text`](elsie.boxmixin.BoxMixin.text) method on a box.
By default, it will create a box item that will draw the specified text in the middle of the box:
```elsie,width=200,height=200
slide.box().text("Hello world!")
```

## Text style
*Elsie* draws text using SVG, so you can use common SVG attributes (such as size, color, font) to
modify the appearance of the rendered text. The style of a text is defined by a
[`TextStyle`](elsie.textstyle.TextStyle) object. Its constructor takes the following parameters:

- `font`: Name of the used font.
- `size`: Size of the used font.
- `align`: Alignment of the text. Allowed values are `"left"`, `"middle"` or `"right"`.
- `line_spacing`: Spacing between lines. The value is relative to the `size` value.
- `color`: Color of the text.
- `bold`: Make the text bold.
- `itelic`: Make the text italic.
- `variant_numeric`: Specifies the style of rendering numbers. Allowed values are `"normal"`,
        `"ordinal"`,
        `"slashed-zero"`,
        `"lining-nums"`,
        `"oldstyle-nums"`,
        `"proportinal-nums"`,
        `"tabular-nums"`,
        `"diagonal-fractions"` or
        `"stacked-fractions"`.
See [SVG documentation](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-variant)
for its meaning.

Each parameter may also be `None` (the default value). This means that the value will be inherited
from its parent style (see below).

If you want to use font or text properties that are not available in `TextStyle`, please
[let us know](https://github.com/spirali/elsie/issues/new).

You can pass a text style as a second argument to the `text` method:
```elsie,width=450,height=150
slide.text("Hello world!", elsie.TextStyle(size=70, color="red"))
```

*Tip*: to avoid repeating the `TextStyle` class name, you can import it via some short alias:
```python
from elsie import TextStyle as s
...
slide.box().text("Hello world!", s(color="red"))
```

### Text style inheritance
Each box also inherits a list of named styles from its parent. If you use a string instead of a
`TextStyle`, *Elsie* will try to find a style with the given name. The two following examples
produce the same slide as the example above:
```elsie,width=450,height=150
# Setting a style globally for all slides
slides.set_style("big_red", elsie.TextStyle(size=70, color="red"))
slide = slides.new_slide(name="slide1")
slide.text("Hello world!", "big_red")
```

```elsie,width=450,height=150
box = slide.box()

# Setting style locally for a box
box.set_style("big_red", elsie.TextStyle(size=70, color="red"))
box.text("Hello world!", "big_red")
```

### Predefined text styles
There are several predefined global styles available by default. You can use them by their name:

- *"default"* - `TextStyle(font="sans-serif", color="black", size=28, line_spacing=1.20, align="middle", variant_numeric="lining-nums")`
- *"tt"* - `TextStyle(font="monospace")`
- *"emph"* - `TextStyle(italic=True)`
- *"alert"* - `TextStyle(bold=True, color="red")`
- *"code"* - `TextStyle(font="monospace", align="left", color="#222" line_spacing=1.20, size=20)`
- *"code_lineno"* - `TextStyle(color="gray")`

The `default` style is special, because it serves as a base text style for all text operations.
In other words, if a property is not specified in the current text style nor in any of its parent
styles, it is inherited from the `default` text style. Therefore, you can modify the `default`
style to change the default style of all text items in your presentation.

For example, the default color of text can be changed globally like this:
```elsie
default_style = slides.get_style("default")
default_style.color = "orange"
slides.set_style("default", default_style)

slide = slides.new_slide("slide")
slide.text("Hello world!")
```

### Updating text style
Getting some text style by name and updating it is a common pattern. Therefore, *Elsie* provides
a shortcut method for this: [`update_style`](elsie.box.Box.update_style):
```python
slides.update_style("default", elsie.TextStyle(color="orange"))
# ^ the same as v
default_style = slides.get_style("default")
default_style.color = "orange"
slides.set_style("default", default_style)
```
If you work with individual `TextStyle` instances, you can compose them together using the
[`compose`](elsie.textstyle.TextStyle.compose) method:
```python
style_a = elsie.TextStyle(color="red")
style_b = style_a.compose(elsie.TestStyle(size=20))
# style_b has color="red" and size=20
```

## Inline text styles
You can also change the style of individual sections of text inside a single string passed to
the `text` method. To do this, wrap a section of text that you want to be styled differently with
`~<style>{<text>}` where `style` is a name of a style and `text` is some section of text.

```elsie,width=600,height=200
slide.set_style("red", elsie.TextStyle(color="red"))
slide.text("Normal text ~red{red text} ~tt{Typewriter text}")
```

Inline styles can also be nested arbitrarily:
```elsie,width=300,height=200
slide.set_style("red", elsie.TextStyle(color="red"))
slide.text("~red{text1 ~tt{text2}}")
```

You can escape the inline style character (by default `~`) by repeating it (e.g. `"~~"`).
If you need to use the `~` character a lot in your text, you can change it to a different
character using the `escape_character` parameter of the
[`text`](elsie.boxmixin.BoxMixin.text) method.

## Text scaling
By default, the size of text is determined by the size defined in its text style. This can be
changed by the parameter `scale_to_fit`, which will scale the text to fit the size of its parent
box.
```elsie,debug
slide.box(width=200, height=80).text("Hello world!", scale_to_fit=True)
slide.box(width=80, height=200).text("Hello world!", scale_to_fit=True)
```

## Text rotation
You can use the `rotation` parameter to rotate the text by the given angle (in degrees) clockwise
around its center.
```elsie
slide.box().text("Hello world!", rotation=45)
```

## Colors
You can define the color of text, [shapes](shapes.md) and other things using a string that is
compatible with SVG. You can be one of the following variants of color definitions:

- Color name: e.g. `green`, `blue`. See list of
[recognized](https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg)
SVG color names.
- Hex color value: e.g. `#fff`, `#a0a0a0`.
- RGB values: e.g. `rgb(34, 12, 64, 0.6)`.
- HSL values: e.g. `hsl(30, 100%, 50%, 0.6)`.
