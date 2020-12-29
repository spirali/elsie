# Lists
Lists of items are very common in presentations, and they come in all sorts of forms and shapes.
That makes it quite difficult to find a general abstraction that could be used to create an
arbitrary list. At the same time, often you just want a quick way to create a simple list, without
bells and whistles.

For that reason, *Elsie* does not provide direct list support in its core, but it provides a set of
helper utilities for creating lists. They are located in the [`elsie.ext`](elsie.ext) module, which
contains opinionated extensions on top of the *Elsie* core. If the helper utilities fit your needs,
feel free to use them. If not, you can just implement your own functions for creating lists in
your presentations.

## Creating lists
To create a list, you can use either the [`unordered_list`](elsie.ext.list.unordered_list)
or the [`ordered_list`](elsie.ext.list.ordered_list) function. Simply pass it a parent box which
will contain the list and then use the returned object to create new list items with the
[`item`](elsie.ext.list.ListBuilder.item) method:

```elsie,width=400,height=200
from elsie.ext import unordered_list

lst = unordered_list(slide.box())
lst.item().text("Item 1")
lst.item().text("Item 2")
lst.item().text("Item 3")
```

You can also pass several useful options to these functions:

- `indent`: Default horizontal gap between individual indentation levels
- `label_padding`: Horizontal padding between the item label and its content
- `label`: Either a string or a function that will be used to render the label of each
item.
- `start` (only for `ordered_list`): The sequence number at which will the ordered list start.
- Any additional keyword arguments passed to these functions will be passed to the box created for
each list item.

The only difference between ordered and unordered lists is the render function of their label. By
default, unordered lists have a constant bullet point used as a label (`•`). The label of an
ordered list is rendered as a sequence of arabic numbers joined with a dot (e.g. `1.3.2`). You
can change the label with the `label` parameter.

## Nesting lists
Both `unordered_list` and `ordered_list` return an object which holds a list of counter values, one
for each nesting level. Each call of the `item` method will create a new item in the list and
increment the value of the last counter in the list.

A top level list is not nested, so it only has a single counter.
You can call the [`ul`](elsie.ext.list.ListBuilder.ul) or [`ol`](elsie.ext.list.ListBuilder.ol)
method to create an unordered, respectively ordered nested (indented) sublist. By default, the
last counter value if the new sublist will start at `1`, but you can override this with the
`start` parameter for ordered lists.

```elsie,width=400,height=200
from elsie.ext import ordered_list

lst = ordered_list(slide.box())
lst.item().text("Item 1")           # Counters of lst = [1]
l2 = lst.ol()                       # Counters of l2 = [1, 1]
l2.item().text("Nested item 1")     # Counters of l2 = [1, 2]
l2.item().text("Nested item 2")
l3 = l2.ol(start=4)                 # Counters of l3 = [1, 2, 4]
l3.item().text("Nested item 3")
lst.item().text("Item 2")           # Counters of lst = [2]
```

If you use a function to render the label of your list items, it will be passed a Box which should
be filled with the label content and also a list of counter values for the specific list item. This
is especially useful for ordered lists:

```elsie,width=400,height=200
from elsie.ext import ordered_list

def render_label(box, counters):
    style = elsie.TextStyle()
    if len(counters) == 1:  # Top-level label
        style.bold = True 
    box.text(".".join(str(c) for c in counters), style=style)

lst = ordered_list(slide.box(), label=render_label)
lst.item().text("Item 1")
l2 = lst.ol(label=render_label)
l2.item().text("Nested item 1")
l2.item().text("Nested item 2")
lst.item().text("Item 2")
```

You can also pass additional parameters to the `ul` and `ol` methods to override the default
properties of the sublist (such as its label). Note that the label is not inherited by the sublist
from the parent. For convenience, you can also use (sub)lists with the `with` keyword to create
visually indented blocks (this is purely visual, it does not change the behaviour of the list in
any way):

```elsie,width=400,height=200
from elsie.ext import unordered_list

lst = unordered_list(slide.box())
lst.item().text("Item 1")
with lst.ul(label="-") as l2:
    l2.item().text("Nested item 1")
    l2.ul().item().text("Nested item 2") # The label here is not inherited
lst.item().text("Item 2")
```

## Revealing
Using [revealing](../userguide/revealing.md), you can easily create a list of items that will
be revealed gradually. If you do not set the `show` key in the default box arguments for a list,
it will use `show="last+"`, which is handy for showing indented items at the same time as their
parent item:
```elsie,width=600,height=200
from elsie.ext import unordered_list

lst = unordered_list(slide.box())
lst.item().text("Appears in fragment 1")
lst.item(show="next+").text("Appears in fragment 2")
lst.ul().item().text("(nested) Appears in fragment 2")
lst.item(show="next+").text("Appears in fragment 3")
```
