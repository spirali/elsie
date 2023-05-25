<p align="center">
<img width="300" src="docs/logo.jpeg">
</p>

# Elsie
Elsie is a framework for **creating slides programmatically** using Python.

**Quick links**
- [**Documentation**](https://spirali.github.io/elsie)
- Demonstration of features ([PDF](examples/bigdemo/bigdemo.pdf), [source code](examples/bigdemo/bigdemo.py))
- [Gallery of Elsie presentations](https://spirali.github.io/elsie/gallery)
- [API reference](https://spirali.github.io/elsie/apidoc)

## Hello world
```python
import elsie

slides = elsie.SlideDeck()

@slides.slide()
def hello(slide):
    slide.text("Hello world!")

slides.render("slides.pdf")
```

## Installation
### Requirements
- Python 3.6+
- Inkscape 1.0+ (required only for Inkscape backend)
    - You can find installation instructions [here](https://wiki.inkscape.org/wiki/index.php/Installing_Inkscape)
    - Versions under 1.0 and above 0.92 might also work, but they are not primarily supported
    - Elsie uses Inkscape in the background, you do not have to know how to use it
- `pdflatex`, `pdf2svg` (required only for `LaTeX` support)

### Installation using pip
```bash
$ pip3 install elsie
```

If you want to use the [`Cairo`](https://spirali.github.io/elsie/userguide/basics/#backends) backend,
install `Elsie` with the `cairo` extra package:
```bash
$ pip3 install elsie[cairo]
```

### Installation using Docker
```bash
$ docker build -t elsie .
```
