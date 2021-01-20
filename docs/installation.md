# Installation
## Requirements
- Python 3.6+
- Inkscape 1.0+ (required only for Inkscape backend)
    - You can find installation instructions [here](https://wiki.inkscape.org/wiki/index.php/Installing_Inkscape)
    - Versions under 1.0 and above 0.92 might also work, but they are not primarily supported
- `pdflatex`, `pdf2svg` (required only for `LaTeX` support)

## Native installation
### Inkscape backend (recommended)
If you want to use Inkscape for rendering slides to PDF, make sure that you have it installed,
preferably with version 1.0+. You can find how to install Inkscape
[here](https://wiki.inkscape.org/wiki/index.php/Installing_Inkscape). On Ubuntu you can simply execute
```bash
$ apt-get install inkscape
```

Then simply install *Elsie* using **PyPi**:
```bash
$ pip3 install elsie
```

### Cairo backend
Install *Elsie* with the `cairo` extra package:
```bash
$ pip3 install elsie[cairo]
```

## Docker installation
We also provide a [Docker image](https://github.com/spirali/elsie/blob/master/Dockerfile) that has
Inkscape and all the required Python dependencies installed.

First build the image:
```bash
$ docker build -t elsie .
```
After that you can use it to render your slides. Let's assume that you have a file called `slides.py`
in the current directory and you want to render it into PDF. You can do that with the following command:
```bash
$ docker run --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    -v${PWD}:/slides \
    elsie python3 /slides/slides.py
```
The slides should then appear in your current directory (by default in `slides.pdf`).
