# Images
Images can be inserted into a slide by calling the [`image`](elsie.boxmixin.BoxMixin.image) method
on a box. The first parameter is the path to the image.

```elsie,height=120,border=no
slide.image("imgs/python.png")
```

By default, the image tries to maximally fit into its containing box without changing the aspect
ratio. Image scale can be set explicitly with the `scale` parameter.

```elsie,height=120,border=no
slide.image("imgs/python.png", scale=0.2)
```

You can also rotate images using the `rotation` parameter. Pass it an angle in degrees to rotate
the image clockwise around its center.

```elsie,height=120,border=no
slide.image("imgs/python.png", rotation=180)
```

`Elsie` supports the following image formats: SVG, PNG, JPEG, and ORA (Open Raster Format).

## Embedding fragments in images
Sometimes you may want to create slides manually in e.g. Inkscape, for example if the slide is
drawn by hand or if it contains many finely-tuned objects. Using these manually created slides in
*Elsie* is easy, you can just export them from Inkscape and include them in a box using the `image`
method.

However, if you want to create animations using this manual approach, it gets quickly pretty
tedious to export all the fragments of the animation one by one and then include them in *Elsie*,
especially if you are modifying the animation interactively. For that reason *Elsie* allows you to
create an animation from a single SVG or ORA file.

If you name a layer (SVG/ORA) or a label of an element (SVG only) in the following way:
`<name>**<annotation>`, the `annotation` part will be interpreted by *Elsie* as a value for the
`show` parameter of a box. Using this convention, you can assign [fragments](revealing.md) to
individual elements inside a single SVG or ORA image and thus create an animation from a single
file. Note that fragment [placeholders](revealing.md#fragment-placeholders) are not allowed in this
context.

Here are some examples of how it works:

- SVG layer/element named `Foo **2+` will only be shown in fragments `2` and further.
- SVG layer/element named `Bar **3-5` will only be shown in fragments `3`, `4` and `5`.

All elements that do not use the `**`-suffixed name will be interpreted as having `show="1+"`.

You can further control how fragments of an image will be displayed using the following parameters
of the [`image`](elsie.boxmixin.BoxMixin.image) method:

- `fragments=False`: Fragment annotations will be ignored.
- `show_begin=<x>`: Shifts all fragments in the image forward so that `x` will be the first fragment
from the perspective of the image. This will cause the image to appear at fragment `x`, a layer
named `Foo**2` would appear at fragment `x + 1`, etc.
- `select_fragments=<list>` (each element of the list is either an integer or `None`): This
parameter allows you to completely rearrange the fragments of the image. For example,
`[3, 7, None, 3]` would show:
    - In the 1st slide fragment: the 3rd image fragment
    - In the 2nd slide fragment: the 7th image fragment
    - In the 3rd slide fragment: no image fragment
    - In the 4rd slide fragment: again the 3rd image fragment
