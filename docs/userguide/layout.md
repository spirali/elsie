# Layout
The most prominent objects in Elsie are boxes. They serve as a layout mechanism
and the way how to put a content into a slide.

### Creating boxes

Let us create the following example, where 3 boxes are created from the
top-level box. The new box is created by calling `.box(...)` on an existing box.
The parameter ``slide`` passed into the slide function is also a box.

```python
@elsie.slide()
def boxdemo1(slide):
    slide.box().text("Box 1")
    slide.box().text("Box 2")
    slide.box().text("Box 3")
```

The code will create the following slide:

<img width="512px" height="384px" src="slide_imgs/boxdemo0.png">

Boxes do not produce any visible content but it influence positions of other
elements. To see where the boxes are, we can switch on the box debug mode:

```python
@elsie.slide(debug_boxes=True)
def boxdemo1(slide):
    slide.box().text("Box 1")
    slide.box().text("Box 2")
    slide.box().text("Box 3")
```

<img width="512px" height="384px" src="slide_imgs/boxdemo1.png">

Here we see the four boxes, the top-level box representing the whole slide and
three inner boxes.

Newly created boxes have the following behavior as default:
- It occupies as less space as possible (in our case is only as big as it could
  contain the text)
- Boxes are put verticaly in the order as they were defined
- They are centered vertically and horizontally.

In the text below, we will see how these default positioning and sizes can be changed.

Boxes can be hierarchically composed (parameter ``padding`` creates a padding in
all directions, it will be explained later).

```python
slide.box(padding=40).box(padding=40).box(padding=40).text("Box 1")
```

<img width="512px" height="384px" src="slide_imgs/composition.png">


### Tree of boxes

Boxes creates a tree of *boxes* and *box items*. Boxes creates layout and box items
represents paitable contant as text, pictures, etc.
Box items are always leaves of the tree and does not contain child boxes.

When a slide is rendered, the box tree is traversed in depth-first way and each child is visited in the order in which it was defined.

This can be modified by parameters ``above``, ``below`` and z-level, see [Modifying painting order](#modifying-painting-order).

Allmost all methods on box creates a new boxes (e.g. ``box``) or box items (e.g. ``text`` or ``rect``). Actually all these methods are also provided by box items; however as box items cannot directly contain its own child elements, they are created in the parent box of the box item. Therefore the following two slides creates the equivalent slides:

```python
@elsie.slide()
def textrect_v1(slide):
    box = slide.box()
    box.rect(bg_color="#aaf")
    box.text("Hello!")

@elsie.slide()
def textrect_v2(slide):
    slide.box().rect(bg_color="#aaf").text("Hello!")
```

<img width="512px" height="384px" src="slide_imgs/textrect.png">


### Box naming

Box can be named by calling ``.box(name="Box name")``. It has no impact on
normal rendering of the slide. The name of slide is shown when
argument ``debug_boxes=True`` is used.

The name of the top-level slide is name of the slide function when the decorator
``@elsie.slide()`` is used to create the slide.


### Width and Height

Width and height of a box can be changed by setting ``width`` and ``height`` arguments when calling ``.box(...)`` method.

```python
@elsie.slide(debug_boxes=True)
def sizedemo1(slide):
    slide.box().text("Box 1")
    slide.box(width=300, height=100).text("Box 2")
    slide.box(width="100%").text("Box 3")
```

<img width="512px" height="384px" src="slide_imgs/sizedemo1.png">

These paramters define **minimal** size of the box. This mean that when its
content (child boxes, texts, etc.) request a bigger size, the box will use the
requested size of the content.

The value should be one of the following:

* ``None`` (default): No minimal size request
* ``int``, ``float``, or a string containg only digits: Size defined in pixels
* String in format ``"XX%"`` where XX is a number (e.g. ``"50%"``): Size defined
  in percentage of the parent box size.
* String ``"fill"`` or ``"fill(XX)"`` where XX is a number. The box fills all
  available space of the parent box. If more boxes on the same level use filling
  value then the size is distributed respecting the ratio of parameters. For
  example, when one box has argument ``fill(2)`` and second one ``fill(3)``,
  remaining size will be divided in ratio 2:3. Value ``"fill"`` is shortcut for
  ``"fill(1)"``.

The following code shows example of "fill" usage:

```python
@elsie.slide(debug_boxes=True)
def filldemo1(slide):
    slide.box().text("Box 1")
    slide.box(width=300, height=100).text("Box 2")
    slide.box(height="fill").text("Box 3")
```

<img width="512px" height="384px" src="slide_imgs/filldemo1.png">


### Box aliases

New box can be created also by calling methods ``fbox``, ``sbox``, and ``overlay``.

* Method ``fbox(...)`` (fill-box) is a shortcut for calling ``box(width="fill", height="fill", ...)``.
* Method ``sbox(...)`` (stretch-box) is a shortcut for
calling ``box(width="fill", ...)`` if the parent box is vertical and
``box(width="fill", ...)`` if the parent box is horizontal.
In other words, it fills the box in the unmanaged direction.
* Method ``overlay(..)`` is a shortcut for ``box(x=0, y=0, width="100%", height="100%)``.


### Padding

By default, box gives all its space to its children. This can be controlled by
padding. There are four padding values: left, right, top, and bottom. There are
controlled by parameters ``p_left``, ``p_right``, ``p_top``, and ``p_bottom``.
After the layout of parent box is computed and the final size and position is
given to a box, padding shrinks its size in the specified directions.

Padding can also be set through the following parameters:
* ``p_x`` that sets ``p_left`` and ``p_right``
* ``p_y`` that sets ``p_top`` and ``p_bottom``
* ``padding`` that sets all four paddings.

```python
@elsie.slide(debug_boxes=True)
def padding_demo(slide):
    slide.box(width=200, height=200, p_left=100, name="Top box")
    slide.box(width=200, height="fill", p_y=100, name="Bottom box")
```

<img width="512px" height="384px" src="slide_imgs/padding_demo.png">


### Box Position

Position of box can be set by arguments `x` and `y`. The allowed values are:

* ``None`` (default) -- see below.
* ``int``, ``float``, or string containing only digits -- absolute position of
  in pixels. Coordinates are relative to top-left corner of the parent box.
* string ``"XX%`` where XX is a number -- position in the parent box where 0% is left (for ``x``) or top (for ``y``) edge of the box and 100% is right (for ``x``) or bottom (for ``y``) edge of the box.
* string ``"[XX%]`` where XX is a number -- aligning box in the parent box. ``"[0%]"`` is left (resp. top), ``"[50%]`` is a middle, and ``"[100%]"`` is right (resp. bottom).
* Dynamically defined position -- see below.


### Default position

The default position is influenced by configuration of the parent box.
When the parent box is vertical (default behavior),
the value for x-axis equivalent to ``"[50%]"``, i.e. centering horizontally.

Fox y-axis, the behavior is a more complex. When a box have ``y`` attribtue set
to ``None`` then we call such a box as *managed box*. A box takes its all
children boxes that are managed and stack them one-by-one while centering the
resulting composite object. The behavior can be observed in the ``boxdemo1`` at
the beginning of the user guide.

<img width="512px" height="384px" src="slide_imgs/boxdemo1.png">

The vertical stacking can be switched
to horizontal by ``horizontal=True`` in box construction.
In such case, children boxes are stacked by x-axis and ``"[50%]"`` is default for y-axis.

```python
@elsie.slide(debug_boxes=True)
def horizontal(slide):
    parent = slide.box(width="100%", height="100%", horizontal=True)
    parent.box().text("Box 1")
    parent.box().text("Box 2")
    parent.box().text("Box 3")
```

<img width="512px" height="384px" src="slide_imgs/horizontal.png">


### Dynamic positions

Box position can be defined dynamically with respect to other boxes. Calling
method ``x`` (resp. ``y``) on a box returns a proxy object that returns real
position when the layout is computed. The reference point is the left top corner
of the box.

Arguments can be:

* an integer or float -- the constant added to the reference point
* a string in form ``"XX%"`` where XX is an integer -- the ratio of the size of the box added to the reference point

For example:

* .x("0%") returns the most left coordinate of the box.
* .x("50%") returns "x" coordinate of the middle of the box.
* .x("100%") return the most right coordinate of the box.
* .x(10) returns the most left edge of th box + 10.

Example:

```python
@elsie.slide(debug_boxes=True)
def horizontal(slide):
    b = slide.box(width=100, height=100, name="First")
    slide.box(x=b.x("50%"), y=b.y("50%"), width=100, height=100, name="Second")
    slide.box(x=0, y=b.y("100%"), width="100%", height=200, name="Third")
```

<img width="512px" height="384px" src="slide_imgs/xy.png">

### Modifying painting order

By default, boxes are painted by the depth-first walk through the box tree.
Each child is visited in the order in which it was defined.

In the following example, the blue box is painted over all previous boxes as it is defined the last.

```python
@elsie.slide()
def paiting1(slide):
    slide.box(x="[40%]", y="[40%]", width=300, height=300).rect(bg_color="red")
    slide.box(x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
```

<img width="512px" height="384px" src="slide_imgs/paiting1.png">

The order in inside box can be defined by attributes ``below`` and ``above`` that takes another child in the box (box or box item) and creates new directly below or above given object.


<img width="512px" height="384px" src="slide_imgs/paiting2.png">


```python
@elsie.slide()
def paiting2(slide):
    red = slide.box(x="[40%]", y="[40%]", width=300, height=300)
    red.rect(bg_color="red")
    slide.box(x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(below=red, x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
```

To modify drawing order even across boxes can be modified by ``z_level``. Before
final drawing, all drawing elements is stable sorted by ``z_level``. It causes
that an element with a higher ``z_level`` is drawn *after* an element with a
lower ``z_level``. If ``z_level`` is not specified, it is inherited from a
parent box. The top-level box has ``z_level`` set to 0.


```python
@elsie.slide()
def paiting3(slide):
    slide.box(x="[40%]", y="[40%]", width=300, height=300).rect(bg_color="red")
    slide.box(z_level=1, x="[60%]", y="[50%]", width=300, height=300).rect(bg_color="green")
    slide.box(x="[30%]", y="[60%]", width=300, height=300).rect(bg_color="blue")
```

<img width="512px" height="384px" src="slide_imgs/paiting3.png">
