# Fragments
## Fragments

Fragments allow to reveal parts of a slide gradually in several steps. It is
controlled by parameter ``show`` that defines in which steps the box content
should be drawn. Note that ``show`` influences only drawing not the layout, i.e.
space for a box is allocated in every step even the box is not shown in this
step. Steps are counted from 1. Every slide (even empty) generates at least one
step.

The possible values are the following. Value ``last`` returns the current maximal step, ``next`` takes the the current maximal step and adds 1.

* ``None`` (default) - Box is shown in all steps (it is equivalent to value ``"1+"``)
* positive integer / ``"next"`` / ``"last"`` -- Box is shown only in step specified by the value
* ``"XX+"`` where XX is a positive integer or ``next`` or ``last`` - Box is shown in the step specified by the value and in all folllowing steps.
* ``"XX-YY"`` where XX and YY are positive integers or ``next`` or ``last`` -
Box shown only in the range of steps speficified by values.
It is inclusive range from both sides.

```python
@elsie.slide()
def steps(slide):
    slide.box().text("Box 1")
    slide.box(show="2+").text("Box 2")
    slide.box(show="3+").text("Box 3")
```

This creates the following three slides:

<img width="512px" height="384px" src="slide_imgs/steps.png">
<img width="512px" height="384px" src="slide_imgs/steps-2.png">
<img width="512px" height="384px" src="slide_imgs/steps-3.png">

The same result can be also achieved by this code:

```python
@elsie.slide()
def steps(slide):
    slide.box().text("Box 1")
    slide.box(show="next+").text("Box 2")
    slide.box(show="next+").text("Box 3")
```
