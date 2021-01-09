import pytest

from elsie import SlideDeck


@pytest.mark.parametrize("policy", ["unique"])
def test_name_policy_unique(policy):
    slides = SlideDeck(name_policy=policy)
    slides.new_slide()
    slides.new_slide()
    slides.new_slide(name="xxx")
    with pytest.raises(Exception, match="already exists"):
        slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    with pytest.raises(Exception, match="has to be a string"):
        slides.new_slide(name=123)
    assert len(slides._slides) == 4


def test_invalid_name_policy():
    with pytest.raises(Exception, match="Invalid"):
        SlideDeck(name_policy="xxx")


@pytest.mark.parametrize("policy", ["ignore", "auto"])
def test_name_policy_ignore(policy):
    slides = SlideDeck(name_policy=policy)
    slides.new_slide(name="xxx")
    slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    assert len(slides._slides) == 3


def test_name_policy_replace():
    slides = SlideDeck(name_policy="replace")
    slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    b2 = slides.new_slide(name="xxx")

    s = slides._slides
    assert len(s) == 2
    assert s[0].name == "yyy"
    assert s[1].name == "xxx"
    assert s[1].box() is b2
