# Text
Text can be created by calling ``.text(..)`` method on a box. It creates a box
item that draws a text in the middle of the box.

### Defining text styles

Text styles (size, color, font, ...) are defined by ``TextStyle`` instances. The constructor takes the following parameters:

* ``font`` - name of the font
* ``size`` - size of the font
* ``align`` - align of the text, possible values: ``"left"``, ``"middle"``, ``"right"``.
* ``line_spacing`` - Spacing between lines, specified relatively to ``size`` argument.
* ``color`` - a string defining the color name
* ``bold`` - a boolean value if text is bold
* ``itelic`` - a boolean value if text is italic
* ``variant_numeric`` - allowed values: ``"normal"``,
        ``"ordinal"``,
        ``"slashed-zero"``,
        ``"lining-nums"``,
        ``"oldstyle-nums"``,
        ``"proportinal-nums"``,
        ``"tabular-nums"``,
        ``"diagonal-fractions"``,
        ``"stacked-fractions"``. For meaning see SVG standard.

Each parameter may also be ``None`` (default value) that
means that the value should be inherited from the parent style.

The simplest use cases, is passing style directly as the second argument of ``tex`` method:

```python
@elsie.slide()
def text1(slide):
    slide.text("Hello world!", elsie.TextStyle(size=70, color="red"))
```

<img width="512px" height="384px" src="slide_imgs/text1.png">

Each box also inherits from its parent a list of named styles. A style can be named and then referred by its name. The two following examples produce the same slide as the example above:

```python
# Setting style globally
elsie.set_style("big_red", elsie.TextStyle(size=70, color="red"))

@elsie.slide()
def text1(slide):
    slide.text("Hello world!", "big_red")
```


```python
@elsie.slide()
def text1(slide):
    box = slide.box()

    # Setting style locally for a box
    box.set_style("big_red", elsie.TextStyle(size=70, color="red"))

    box.text("Hello world!", "big_red")
```

There are several predifined global styles.

* *"default"* - ``TextStyle(font="Ubuntu", color="black", size=28, line_spacing=1.20, align="middle", variant_numeric="lining-nums")``
* *"tt"* - ``TextStyle(font="Ubuntu mono")``
* *"emph"* - ``TextStyle(italic=True)``
* *"alert"* - ``TextStyle(bold=True, color="red")``
* *"code"* - ``TextStyle(font="Ubuntu Mono", align="left", color="#222" line_spacing=1.20, size=20)``
* *"code_lineno"* - ``TextStyle(color="gray")``

The "default" style is special and it serves as a base text style for all text operations. In other words, if a property is not specified in the current text style, it is inherited from the "default" text style.
Therefore modification of "default" style to globally change default text style.

For example, color of default text can be globally changed as follows:

```python
default_style = elsie.get_style("default")
default_style.color = "orange"
elsie.set_style("default", default_style)

@elsie.slide()
def text2(slide):
    slide.text("Hello world!")
```

<img width="512px" height="384px" src="slide_imgs/text2.png">

Getting a style and updating it is a common pattern; therefore, there is a shortcut method for this: ``update_style``. It can also called globally (as function in ``elsie`` package) or locally as a method of a box.


```python
elsie.update_style("default", elsie.TextStyl(color="orange"))

@elsie.slide()
def text2(slide):
    slide.text("Hello world!")
```

This produce the same result as the example above.


### Inline text styles

Styles can be changed in the text by the following syntax: ~STYLE{TEXT} where STYLE is a named style and TEXT a text that will be drawn.

```python
@elsie.slide()
def inline_styles(slide):
    slide.set_style("red", elsie.TextStyle(color="red"))
    slide.text("Normal text ~red{red text} ~tt{Typewriter text}")
```

Styles can be applied hierarchically without limitation. The escape charater "~"
can be changed to any other character by parameter ``escape_character`` of
``.text()`` method. To write an escape character in the text, repeat it (i.e.
"~~" for default escape character).

<img width="512px" height="384px" src="slide_imgs/inline_styles.png">


### Scaling to fit the box

By default, the size of text is influenced by the size defined in the text
style. This can be changed by parameter ``scale_to_fit`` that scales the text to size that fits inside its parent box.

```python
@elsie.slide(debug_boxes=True)
def scale_to_fit(slide):
    slide.box(width=300, height=80).text("Hello world!", scale_to_fit=True)
    slide.box(width=80, height=300).text("Hello world!", scale_to_fit=True)
```

<img width="512px" height="384px" src="slide_imgs/scale_to_fit.png">


## Colors

In some places, a color can be defined (e.g. color of a text, or a line color).
In all such places, it is expected a string that contains any valid SVG color definition, i.e.:

* Color name - e.g. ``green``, ``blue``; https://commons.wikimedia.org/wiki/File:SVG_Recognized_color_keyword_names.svg
* Hex color value: e.g. ``#fff``, ``#a0a0a0``
* RGB values: e.g. ``rgb(34, 12, 64, 0.6)``
* HSL values: e.g. ``hsl(30, 100%, 50%, 0.6)``
