# Grids
The [box](../userguide/layout.md) model of *Elsie* makes it easy to create fixed size rectangular
grids. Simply create a box with a horizontal layout for each row and then fill it with a fixed-size
box for each column. If you need spaces between the grid items, you can put padding on the inner
boxes.

```elsie,width=400
row_count = 2
column_count = 3

for r in range(row_count):
    row = slide.box(horizontal=True, p_bottom=10)
    for c in range(column_count):
        color = "#FF2400" if c % 2 == 0 else "#16A085"
        box = row.box(width=50, height=50, p_right=10)
        box.rect(color="black", bg_color=color)
        box.text(f"({r}, {c})", elsie.TextStyle(color="white"))
```

Using [fragments](../userguide/revealing.md), you can then make the grid items appear gradually:
```elsie,width=400
row_count = 2
column_count = 3

fragment = 1
for r in range(row_count):
    row = slide.box(horizontal=True, p_bottom=10)
    for c in range(column_count):
        box = row.box(width=50, height=50, p_right=10, show=f"{fragment}+")
        box.rect(color="black")
        box.text(f"({r}, {c})")
        fragment += 1
```
