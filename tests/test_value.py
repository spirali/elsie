from elsie.value import SizeValue, PosValue
from elsie.lazy import LazyValue
from elsie.show import ShowInfo

import pytest


def test_size_parse_value():

    a = SizeValue.parse(100)
    assert a.min_size == 100.0
    assert a.fill == 0
    assert a.ratio is None

    a = SizeValue.parse("100")
    assert a.min_size == 100.0
    assert a.fill == 0
    assert a.ratio is None

    a = SizeValue.parse("90%")
    assert a.ratio == 0.9
    assert a.min_size == 0
    assert a.fill == 0

    a = SizeValue.parse("fill")
    assert a.fill == 1
    assert a.min_size == 0
    assert a.ratio is None

    a = SizeValue.parse("fill(23)")
    assert a.fill == 23
    assert a.min_size == 0
    assert a.ratio is None

    a = SizeValue.parse(LazyValue(lambda: 10))
    assert a.fill == 0
    assert a.min_size == 0
    assert a.ratio is None
    assert a.lazy_value is not None

    with pytest.raises(Exception):
        SizeValue.parse("abc")


def test_pos_parse_value():

    a = PosValue.parse(100)
    assert a.fix_pos == 100.0
    assert a.ratio is None
    assert a.align is None

    a = PosValue.parse("100")
    assert a.fix_pos == 100.0
    assert a.ratio is None
    assert a.align is None

    a = PosValue.parse("90%")
    assert a.fix_pos is None
    assert a.ratio == 0.9
    assert a.align is None

    a = PosValue.parse("[90%]")
    assert a.fix_pos is None
    assert a.align == 0.9
    assert a.ratio is None

    a = PosValue.parse(LazyValue(lambda: 10))
    assert a.fix_pos is None
    assert a.ratio is None
    assert a.align is None
    assert a.lazy_value is not None

    with pytest.raises(Exception):
        PosValue.parse("abc")


def test_parse_show_info():
    s = ShowInfo.parse(2)
    assert s.steps == (2,)
    assert not s.open_step
    assert s._min_steps == 2

    s = ShowInfo.parse("5")
    assert s.steps == (5,)
    assert not s.open_step
    assert s._min_steps == 5

    a = ShowInfo.parse("2-123")
    assert a.steps == tuple(range(2, 124))
    assert not a.open_step
    assert a.min_steps() == 123

    s = ShowInfo.parse("5-8, 1-6, 9")
    assert s.steps == (1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert not s.open_step
    assert s._min_steps == 9

    s = ShowInfo.parse("5+")
    assert s.steps == ()
    assert s.open_step == 5
    assert s._min_steps == 5

    s = ShowInfo.parse("1,3-5,8+,4-6")
    assert s.steps == (1, 3, 4, 5, 6)
    assert s.open_step == 8
    assert s._min_steps == 8

    s = ShowInfo.parse(None)
    assert s.open_step == 1
    assert not s.steps

    with pytest.raises(Exception):
        ShowInfo.parse("")

    with pytest.raises(Exception):
        ShowInfo.parse("5+,6+")

    s = ShowInfo.parse("5", 1)
    assert s.steps == (5, )

    s = ShowInfo.parse("next", 0)
    assert s.steps == (1,)

    s = ShowInfo.parse("next", 2)
    assert s.steps == (3,)

    s = ShowInfo.parse("next+", 2)
    assert s.steps == ()
    assert s.open_step == 3

    with pytest.raises(Exception):
        ShowInfo.parse("next")


def test_show_max_step():
    assert ShowInfo((1, 2, 3)).max_step() == 3
    assert ShowInfo((1, 2, 3), open_step=4).max_step() == 4
    assert ShowInfo(None, open_step=4).max_step() == 4


def test_show_is_visible():
    s = ShowInfo.parse("1,3-5,8+,4-6")
    assert s.is_visible(1)
    assert not s.is_visible(2)
    assert s.is_visible(3)
    assert s.is_visible(4)
    assert s.is_visible(5)
    assert s.is_visible(8)
    assert s.is_visible(10)
