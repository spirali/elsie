import lxml.etree as et
import pytest
import re

numbers_split = re.compile("(-?[\d\.]+)")


def string_check(s1, s2):
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
            assert abs(tmp1 - tmp2) < 0.4
        except ValueError:
            print(s1)
            print(s2)
            # To show pytest error message
            assert a1 == a2


def element_check(e1, e2):
    if e1.tag != e2.tag:
        raise Exception("Different tags: {} vs {}".format(e1.tag, e2.tag))

    c1 = list(e1)
    c2 = list(e2)

    if e1.text != e2.text:
        string_check(e1.text, e2.text)

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
            string_check(v1, v2)

    if len(c1) != len(c2):
        raise Exception("Different number of children for: {} {}".format(e1, e2))

    for child1, child2 in zip(c1, c2):
        element_check(child1, child2)


def svg_check(svg1, svg2):
    root1 = et.fromstring(svg1)
    root2 = et.fromstring(svg2)
    element_check(root1, root2)


def test_svg_compare():

    svg_check("<x/>", "<x/>")
    with pytest.raises(Exception, match="number of"):
        svg_check("<x></x>", "<x><y/></x>")
    svg_check("<x><y a='1' b='1'/></x>", "<x><y b='1' a='1'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='1' b='1'/></x>", "<x><y b='1' a='2'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='a'/></x>", "<x><y/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='a'/></x>", "<x><y a='0'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='1' b='1'/></x>", "<x><y b='1'/></x>")

    svg_check("<x><y a='0.0001'/></x>", "<x><y a='0'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='0.7'/></x>", "<x><y a='0'/></x>")

    svg_check("<x><y a='1.0001, 3.02'/></x>", "<x><y a='0.999, 3.01'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='1.0001, 3.02'/></x>", "<x><y a='0.001, 3.01'/></x>")

    svg_check("<x><y a='scale(10.1)'/></x>", "<x><y a='scale(10.2)'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='scale(10.1)'/></x>", "<x><y a='scale(10.9)'/></x>")
    with pytest.raises(AssertionError):
        svg_check("<x><y a='scale(10.1)'/></x>", "<x><y a='scalex(10.1)'/></x>")
