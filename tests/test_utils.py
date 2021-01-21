import os
import re
import sys
from typing import List

import lxml.etree as et
import pytest
from PIL import Image, ImageChops, ImageStat

from elsie.render.backends import CairoBackend, InkscapeBackend

numbers_split = re.compile(r"(-?[\d.]+)")


VALUE_TOLERANCE = 0.85
if os.environ.get("CI"):
    VALUE_TOLERANCE *= 2


def string_check(s1, s2, name, tolerance):
    lst1 = numbers_split.split(s1)
    lst2 = numbers_split.split(s2)
    assert len(lst1) == len(lst2)
    for a1, a2 in zip(lst1, lst2):
        a1 = a1.strip()
        a2 = a2.strip()
        if a1 == a2:
            continue
        try:
            tmp1 = float(a1)
            tmp2 = float(a2)
            assert abs(tmp1 - tmp2) < tolerance, name
        except ValueError:
            print(s1)
            print(s2)
            # To show pytest error message
            assert a1 == a2


def element_check(e1, e2, tolerance):
    if e1.tag != e2.tag:
        raise Exception("Different tags: {} vs {}".format(e1.tag, e2.tag))

    c1 = list(e1)
    c2 = list(e2)

    if e1.text != e2.text:
        string_check(e1.text, e2.text, "element's text", tolerance)

    if frozenset(e1.keys()) != frozenset(e2.keys()):
        print(e1.items())
        print(e2.items())
        print(e1.text)
        print(e1, e2)
        # To show pytest error message
        assert frozenset(e1.keys()) == frozenset(e2.keys())

    for (name, v1) in e1.items():
        v2 = e2.get(name)
        if v1 != v2:
            string_check(v1, v2, "{}/{}".format(e1.tag, name), tolerance)

    if len(c1) != len(c2):
        raise Exception("Different number of children for: {} {}".format(e1, e2))

    for child1, child2 in zip(c1, c2):
        element_check(child1, child2, tolerance)


def svg_check(svg1, svg2, tolerance=VALUE_TOLERANCE):
    root1 = et.fromstring(svg1)
    root2 = et.fromstring(svg2)
    element_check(root1, root2, tolerance)


def test_svg_compare():
    tolerance = 0.85

    svg_check("<x/>", "<x/>")
    with pytest.raises(Exception, match="number of"):
        svg_check("<x></x>", "<x><y/></x>")
    svg_check("<x><y a='1' b='1'/></x>", "<x><y b='1' a='1'/></x>")
    with pytest.raises(AssertionError):
        svg_check(
            "<x><y a='1' b='1'/></x>", "<x><y b='1' a='2'/></x>", tolerance=tolerance
        )
    with pytest.raises(AssertionError):
        svg_check("<x><y a='a'/></x>", "<x><y/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='a'/></x>", "<x><y a='0'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='1' b='1'/></x>", "<x><y b='1'/></x>")

    svg_check("<x><y a='0.0001'/></x>", "<x><y a='0'/></x>", tolerance=tolerance)
    with pytest.raises(AssertionError):
        svg_check("<x><y a='0.99'/></x>", "<x><y a='0'/></x>", tolerance=tolerance)

    svg_check(
        "<x><y a='1.0001, 3.02'/></x>",
        "<x><y a='0.999, 3.01'/></x>",
        tolerance=tolerance,
    )
    with pytest.raises(AssertionError):
        svg_check(
            "<x><y a='1.0001, 3.02'/></x>",
            "<x><y a='0.001, 3.01'/></x>",
            tolerance=tolerance,
        )

    svg_check(
        "<x><y a='scale(10.1)'/></x>",
        "<x><y a='scale(10.2)'/></x>",
        tolerance=tolerance,
    )
    with pytest.raises(AssertionError):
        svg_check(
            "<x><y a='scale(11.1)'/></x>",
            "<x><y a='scale(10.0)'/></x>",
            tolerance=tolerance,
        )
    with pytest.raises(AssertionError):
        svg_check(
            "<x><y a='scale(11.1)'/></x>",
            "<x><y a='scalex(10.0)'/></x>",
            tolerance=tolerance,
        )


def compare_images(
    png_inkscape: List[str], png_cairo: List[str], diff_threshold: float
):
    def concat_images(im1, im2):
        dst = Image.new("RGB", (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    assert len(png_inkscape) == len(png_cairo)
    for (inkscape, cairo) in zip(png_inkscape, png_cairo):
        inkscape_img = Image.open(inkscape)
        cairo_img = Image.open(cairo)
        difference = ImageChops.difference(inkscape_img, cairo_img)
        stat = ImageStat.Stat(difference)
        diff = sum(stat.mean)
        if diff > diff_threshold:
            combined = concat_images(inkscape_img, cairo_img)
            path = os.path.abspath("combined.png")
            combined.save(path)
            raise Exception(
                f"Cairo and Inkscape images differ by {diff} pixels, images written to {path}"
            )
        else:
            print("Difference:", diff, file=sys.stderr)


def check_svg(svg: str, inkscape_shell, wrapped, check_kwargs, *args, **kwargs):
    from conftest import SlideTester

    test_env = SlideTester(InkscapeBackend(inkscape=inkscape_shell))
    wrapped(test_env=test_env, *args, **kwargs)
    test_env.check_svg(svg, **check_kwargs)


def check_cairo(wrapped, inkscape_shell, diff_threshold, *args, **kwargs):
    from conftest import SlideTester

    t_inkscape = SlideTester(InkscapeBackend(inkscape=inkscape_shell))
    wrapped(test_env=t_inkscape, *args, **kwargs)
    png_inkscape = t_inkscape.slides.render(
        output=None, export_type="png", prune_cache=False
    )

    t_cairo = SlideTester(CairoBackend())
    wrapped(test_env=t_cairo, *args, **kwargs)
    png_cairo = t_cairo.slides.render(output=None, export_type="png", prune_cache=False)
    compare_images(png_inkscape, png_cairo, diff_threshold)
