# Shapes
### Rectangles

The simplest box items are rectangles, they are created by calling ``.rect(..)``
method on a box. The position and size of a rectangle is taken from the box. A
``rectangle`` method takes the following parameters:

* ``color`` (``str`` or ``None``) -- Defines a color that is used to draw a rectangle. If ``None`` no rectangle is drawn. (Default ``None``)
* ``stroke_width`` (a number) -- Defines thickness of the drawn rectangle
* ``stroke_dasharray`` (``str`` or ``None``) -- Defines pattern of dashes and gaps to paint a rectangle. More information: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
* ``bg_color`` (``str`` or ``None``) -- Defines a color that is used to fill the rectangle.
* ``rx`` and ``ry`` -- Defines a radius of round corners of the rectangle. See https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect.

```python
@elsie.slide()
def rectangle(slide):
    box = slide.box(x="[50%]", y="[50%]", width="80%", height=300)
    box.rect(bg_color="green", color="red", stroke_width=10, stroke_dasharray="10 4", rx=20, ry=20)
```

<img width="512px" height="384px" src="slide_imgs/rectangle.png">


## Geometrical shapes

Elsie allows to draw additional shapes: (poly)line, polygon, and a generic path.
On top of that, Elsie offers an abstraction for arrow heads that can be placed
on the ends of a line or a path.

### Line and Polygon

Both polygon and line takes a list of points as the first argument.
A point can be defines as:

* A 2-tuple ``(x_value, y_value)`` where ``x_value`` (resp ``y_value``) that are passed to method ``.x(..)`` (resp ``.y(..)``) of the box holding the line/polygon.
* A dynamic point obtained by calling ``.p(x_value, y_value)`` of any box.

TODO

### Arrow head

An arrow head is be defined by instantiating class ``elsie.Arrow``
that takes the following attributes:

* ``size`` - The size of the arrow head
* ``angle`` - The main angle of arrow head
* ``stroke_width`` - If ``None`` then the arrow head is filled area, otherwise it defines the thickness of the line that is used to draw the arrow head.
* ``inner`` - How the inner point of the arrow is moved. Value 1.0 has no
  effect, value bigger than 1.0 produce a diamond shape, value smaller than 1.0
  produce a more sharp arrow. See the effect in the picture below. The move of
  the point is the proportional to the size of the arrow.

<img src="imgs/arrows.png"/>

Note: That the head defines only the shape, not the color. The color is taken from the line where the arrow head is attached.

## Path

TODO

## Chaining box items

TODO


## Modification of LazyPoints

TODO
