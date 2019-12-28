# Elsie

Elsie is a framework for making slides in Python.

Full demonstration:
  * Result: [example.pdf](examples/bigdemo/example.pdf)
  * Source code: [example.py](examples/bigdemo/example.py)

Minimal example:

```python
import elsie

@elsie.slide()
def hello(slide):
    slide.text("Hello world!")

elsie.render()  # Creates file 'slides.pdf'
```

## Requirements

* Python 3.4 or newer
* Inkscape (Elsie uses Inkscape in the background, you do not have to know how to use it.)
* (Optional for LaTeX support): pdflatex, pdf2svg


## PIP Installation

    pip3 install elsie

Note: This does not install Inkscape, you have to do it manually.

## Manual Installation

    python setup.py build
    python setup.py install
