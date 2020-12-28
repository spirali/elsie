# Lists
Lists of items are very common in presentations, and they come in all sorts of forms and shapes.
That makes it quite difficult to find a general abstraction that could be used to create an
arbitrary list. At the same time, often you just a quick way to create a simple list.

For that reason, *Elsie* does not have list handling support in its core, but it provides a set of
helper utilities for creating lists. They are located in the [`elsie.ext`](elsie.ext) module, which
contains opinionated extensions on top of the *Elsie* core. If the helper utilities fit your needs,
feel free to use them. If not, you can just implement your own functions for creating lists in
your presentations.

```elsie,type=lib
from elsie.ext import ListBuilder
```

## Unordered lists
To create an unordered list, you can use the [`ListBuilder`](elsie.ext.list.ListBuilder) class.
Pass it a parent box which will contain the list and default parameters for each list item. Then
create new items with the [`item`](elsie.ext.list.ListBuilder.item) method:

```elsie,width=400,height=200
from elsie.ext import ListBuilder

lst = ListBuilder(slide.box())
lst.item().text("Item 1")
lst.item().text("Item 2")
lst.item().text("Item 3")
```

### Nesting lists
The `ListBuilder` gives you several options of setting the indentation level of individual list
items. It remembers its current indentation level, which can be changed with the
[`indent`](elsie.ext.list.ListBuilder.indent) and [`dedent`](elsie.ext.list.ListBuilder.dedent)
methods, and it will apply it newly created items. You can also override the indentation level of
an individual item with the `level` parameter of the [`item`](elsie.ext.list.ListBuilder.item)
method or use the [`indent_scope`](elsie.ext.list.ListBuilder.indent_scope) context manager to
change the indentation level of multiple items in the given soure code scope. You can also combine
these methods together if you want, choose the style that fits you.

As a demonstration, the following three code snippets will produce the same list.

- Manual indentation using the level parameter
```python
lst = ListBuilder(slide.box())
lst.item().text("Item 1")
lst.item(level=1).text("Item 2")
lst.item(level=2).text("Item 3")
lst.item().text("Item 4")
```
- Stateful indentation using the `indent` and `dedent` methods
```python
lst = ListBuilder(slide.box())
lst.item().text("Item 1")
lst.indent()
lst.item().text("Item 2")
lst.indent()
lst.item().text("Item 3")
lst.dedent(2)
lst.item().text("Item 4")
```
- Identation using `with` scopes.
```elsie
lst = ListBuilder(slide.box())
lst.item().text("Item 1")
with lst.indent_scope():
    lst.item().text("Item 2")
    with lst.indent_scope():
        lst.item().text("Item 3")
lst.item().text("Item 4")
```

#### Revealing
Using [revealing](../userguide/revealing.md), you can easily create a list of items that will
be revealed gradually. The default fragment selector for list items is `last+`, which is handy for
showing indented items at the same time as their parent item:
```elsie,width=600,height=200
lst = ListBuilder(slide.box())
lst.item().text("Appears in fragment 1")
lst.item(show="next+").text("Appears in fragment 2")
lst.item(level=1).text("(nested) Appears in fragment 2")
lst.item(show="next+").text("Appears in fragment 3")
```
