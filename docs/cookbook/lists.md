# Lists
It is very common to use lists of items in presentations. Although there is no direct
support in *Elsie* for creating lists, it is easy to create your own function for it
and customize it for your use case.

For example, here is a simple function that will create a new list item in the given
parent [box](../userguide/layout.md). The `level` parameter selects the nesting level of the list
item.

```elsie,type=lib
def list_item(parent: Box, level=0, show="last+", **box_args) -> Box:
    b = parent.box(x=level * 25, horizontal=True, show=show, **box_args)
    b.box(width=25, y=0).text("•")  # A bullet point
    return b.box(width="fill")
```

With a function like this, it becomes easy to create lists:
```elsie,width=400,height=200
l = slide.box()
list_item(l).text("Item 1")
list_item(l).text("Item 2")
list_item(l, level=1).text("(nested) Item 3")
list_item(l).text("Item 4")
```

Using [revealing](../userguide/revealing.md), you can then easily create a list of items that will
be revealed gradually:
```elsie,width=500,height=200
l = slide.box()
list_item(l).text("Appears in step 1")
list_item(l, show="next+").text("Appears in step 2")
list_item(l, level=1).text("(nested) Appears in step 2")
list_item(l, show="next+").text("Appears in step 3")
```

If that's still too unwieldy, you can for example put your individual lines into a Python `list`
and write a function that will render it as a set of lines with bullet points using the `list_item`
function.
