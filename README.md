# Elsie

Elsie is a framework for making slides in Python

Example:
  * Result: [example.pdf](example/example.pdf)
  * Source code: [example.py](example/example.py)

Elsie is based on experience with my previous project
https://github.com/spirali/elphie/. It is a complete rewrite while making it
more flexible by directly exposing boxes.

# Requirements

* Python 3.4 or newer
* Inkscape
* pypdf2 (or pdfunite; configurable in `render` method)
* pygments
* lxml

# Installation

    python setup.py build
    python setup.py install
