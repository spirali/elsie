# Markdown
Since *Elsie* is a rather low-level tool, in certain situations it might feel too verbose.
For some slides, you may just want to display some text with basic formatting, and you don't want
to think about the layout too much.

For such scenarios we provide basic integration with [Markdown](https://commonmark.org/), located
in the [`elsie.ext`](elsie.ext) extension module, which contains opinionated extensions on top of
the *Elsie* core. Markdown support is provided on a best-effort basis, as it intentionally does
not support all Markdown [use cases](#supported-markdown-subset) in order to stay simple.

## Rendering Markdown markup
You can pass a snippet of Markdown markup to the [`markdown`](elsie.ext.markdown.markdown)
function, which will transform it into *Elsie* elements and render it into the given parent box:
```elsie,width=600
from elsie.ext import markdown

markdown(slide.box(), """
# Hello
This text was rendered using **Markdown**
""")
```

You have to use the [CommonMark](https://commonmark.org/) Markdown syntax.

## Supported Markdown subset
*Elsie* supports only a subset of Markdown elements. Here is a list of supported elements:

### Formatted text
You can use headings, paragraphs, blockquotes and text formatting (bold/italic). Line breaks in the
markup will be respected.
```elsie,width=400
from elsie.ext import markdown

markdown(slide.box(), """
# Heading 1
## Heading 2
**bold text**
*italic text*
**bold *and italic* text**
""")
```
You can use [inline styles](text.md#inline-text-styles) inside text to format parts of the text
differently. The default escape character is `~`, but you can change it with the `escape_char`
parameter of the `markdown` function.
```elsie,width=400
from elsie.ext import markdown

markdown(slide.box(), """
This text is in ~tt{monospace}.
""")
```

You can also [override](#overriding-styles) the default style used to render headings, bold text
etc.

### Fenced code
Fenced code blocks will be rendered with syntax-highlighting. Pass the desired language to be
highlighted after the initial three backticks, for example:

~~~elsie
from elsie.ext import markdown

markdown(slide.box(), """
This is Python code:

```python
def say_hello():
    print("Hello world")
```
""")
~~~

### Lists
You can use both unordered lists and ordered lists and also nest them. Unordered lists support two
types of bullet points (`-` or `*`), ordered lists support the format `<number>.`:
```elsie
from elsie.ext import markdown

markdown(slide.box(), """
- Item A
    1. Item B
    1. Item C
- Item D
    * Item E
    * Item F
""")
```

### Links
You can also use Markdown links inside the markup, but this will only affect the formatting of the
text. It will not cause the link to be clickable in the resulting PDF, nor will it render an
underline. This is a limitation of Inkscape and it might be resolved in the future.
```elsie
from elsie.ext import markdown

markdown(slide.box(), """
I am a [link](unused).
""")
```

Horizontal rules, tables, inline code, images, footnotes and indented code blocks are currently
not supported.

## Overriding styles
The [`markdown`](elsie.ext.markdown.markdown) function uses a set of predefined styles for
formatting bold/italic text, individual levels of headings etc. If the parent box into which you
render Markdown already has some of these styles defined, the default style will be overridden by
them. Using this overriding you can change the default appearance of the rendered Markdown
elements:
```elsie,width=400
from elsie import TextStyle
from elsie.ext import markdown
from elsie.ext.markdown import MD_PARAGRAPH_STYLE

slide.set_style(MD_PARAGRAPH_STYLE, TextStyle(color="red"))

markdown(slide.box(), "This is a red paragraph.")
```

Here is a list of the Markdown styles that you can override:

| Style name | Used for | Variable name in `elsie.ext.markdown` |
|:----------:|:-------------:|:------:|
| `"md-paragraph"` | Paragraphs | `MD_PARAGRAPH_STYLE` |
| `"md-bold"` | Bold text | `MD_BOLD_STYLE` |
| `"md-italic"` | Italic text | `MD_ITALIC_STYLE` |
| `"md-link"` | Links | `MD_LINK_STYLE` |
| `"md-blockquote"` | Blockquotes | `MD_BLOCKQUOTE_STYLE`|
| `"md-heading-<level>"` | Headings of the given `level` (`1-6`) | `MD_HEADING_<level>_STYLE` |

You can either use the names directly or import them from the `elsie.ext.markdown` module.

Fenced code blocks use the [standard](syntax_highlighting.md#differences-to-text) `code` style,
so you can override that if you want to alter the appearance of code snippets rendered with
Markdown.
