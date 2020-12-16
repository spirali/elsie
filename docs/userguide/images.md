# Images
`Elsie` supports the following image formats: SVG, PNG, JPEG and ORA (Open Raster
Format). Images can be inserted into a slide by calling the `image` method on a box.
The first parameter is the path to the image.

```elsie,height=120,border=no
slide.image("imgs/python.png")
```

By default, the image tries to maximally fit into its containing box without changing the aspect
ratio. Image scale can be set explicitly with the `scale` parameter.

```elsie,height=120,border=no
slide.image("imgs/python.png", scale=0.2)
```

## Fragments in images
TODO: write after fragments
Images in the SVG and ORA formats may contain fragments When a layer (SVG, ORA) or a label of an
element (SVG) is named in a special way, it will be  that *suffix* has format ``**XX`` where XX is a string allowed in ``show`` parameter of a box;
except the special values "next" and "last" are not allowed.

Examples:
* "Layer 1 **2+" specifies show parameter "2+" (from the second slide and later)
* "Something **3-5 specifies show parameter "3-5" (show only in given range)

An element and all of its children with such formated name is then shown only the defined steps.
All elements without "**" suffixed name is visible in all steps.


Fragments can be controlled by the following parameters of ``image`` method:

* ``fragments=False`` - Fragment annotations is ignored
* ``show_begin=X`` - Image is first shown in step ``X`` and all constants in annotations are shifted by ``X``.
* ``select_steps=LIST`` where LIST is a list of integers or ``None``s. This allows to completely rearrange steps. Eg. ``[3, 7, None, 3]`` means that
  * in the 1st slide step: the 3rd image step is shown
  * in the 2nd slide step: the 7th image step is shown
  * in the 3rd slide step: no image step is shown
  * in the 4rd slide step: again the third image step is shown
