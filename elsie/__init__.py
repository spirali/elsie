"""
Elsie allows you to build slides programmatically.

Most important classes are:
- `Slides`: Used for creating a presentation.
- `BoxMixin`: Class which provides methods used to create content inside of slides.
- `TextStyle`: Used to style text.

Hello world example:
```python
import elsie

slides = elsie.Slides()

@slides.slide()
def slide1(slide):
    slide.text("Hello world")

slides.render("slides.pdf")
```

Note: Undocumented functions and classes are not part of the public API.
"""

from .arrow import Arrow  # noqa
from .slides import Slides  # noqa
from .textstyle import TextStyle  # noqa
