# Installation
## Requirements
- Python 3.6+
- Inkscape 0.92+ (1.0+ recommended)
- (Required only LaTeX support): pdflatex, pdf2svg

## Native installation
You can install *Elsie* using **PyPi**:
```bash
$ pip3 install elsie
```

You will also need **Inkscape** installed, preferably version 1.0+. You can find how to install
Inkscape [here](https://wiki.inkscape.org/wiki/index.php/Installing_Inkscape). On Ubuntu you can
simply execute
```bash
$ apt-get install inkscape
```

## Docker installation
We also provide a [Docker image](https://github.com/spirali/elsie/blob/master/Dockerfile) that has
Inkscape and all required Python dependencies installed.

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
