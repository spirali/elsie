<p align="center">
<img width="300" src="docs/logo.jpeg">
</p>

# Elsie
Elsie is a framework for **creating slides programmatically** using Python.

**Quick links**
- [Documentation](https://spirali.github.io/elsie)
- Demonstration of features:
   * [PDF](examples/bigdemo/bigdemo.pdf)
   * [source code](examples/bigdemo/bigdemo.py)
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
- Inkscape 1.0+ installed
    - You can find installation instructions [here](https://wiki.inkscape.org/wiki/index.php/Installing_Inkscape).
    - Elsie uses Inkscape in the background, you do not have to know how to use it.
- (Optional for LaTeX support): `pdflatex` and `pdf2svg`

### Installation using pip
```bash
$ pip3 install elsie
```

### Installation using Docker
```bash
$ docker build -t elsie .
```
