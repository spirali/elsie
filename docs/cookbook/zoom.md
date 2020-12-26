# Zooming
SVG defines a [viewbox](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox)
attribute, which allows you to change from which view point is the SVG image rendered. *Elsie* also
supports this attribute via the [`view_box`](elsie.slides.slidedeck.SlideDeck.slide) parameter.

Using a specific viewbox, you can for example create "zoomed" slides. This might be useful if you
first want to show an overview of something and then later zoom-in to show some details.

Let's create a function that will render some content:
```elsie,type=lib
def render_slide(parent):
    parent.box(x=50, y=50, width=100, height=80).rect(bg_color="red")
    return parent.box(x=180, y=50, width=80, height=80).ellipse(bg_color="blue")
```

Now we can use it to create an overview slide:
```elsie,height=200
@slides.slide()
def overview(slide):
    render_slide(slide)
```

And then render the slide content again, this time zoomed-in on a particular spot:
```elsie,height=200
@slides.slide(view_box=(120, 80, 80, 30))
def detail(slide):
    circle = render_slide(slide)

    # Text label
    textbox = slide.box(x=130, y=80, z_level=2)
    textbox.text("Circle edge", elsie.TextStyle(size=6))
    textbox.overlay(z_level=1).rect(bg_color="yellow")

    # Line with arrow
    slide.box().line([
        textbox.p("100%", "50%"),
        circle.p("0%", "50%")
    ], end_arrow=elsie.Arrow(size=6))
```
