"""
Elsie allows you to build slides programmatically.

Most important classes are:
- `SlideDeck`: Used for creating a presentation.
- `BoxMixin`: Class which provides methods used to create content inside of slides.
- `TextStyle`: Used to style text.

Hello world example:
```python
import elsie

slides = elsie.SlideDeck()

@slides.slide()
def slide1(slide):
    slide.text("Hello world")

slides.render("slides.pdf")
```

Note: Undocumented functions and classes are not part of the public API.
"""

from .shapes.arrow import Arrow  # noqa
from .slides.slidedeck import SlideDeck  # noqa
from .text.textstyle import TextStyle  # noqa

# Maintained for backwards compatibility
Slides = SlideDeck
