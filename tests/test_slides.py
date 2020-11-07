from elsie import Slides
import pytest


@pytest.mark.parametrize("policy", ["auto", "unique"])
def test_name_policy_unique(policy):
    slides = Slides(name_policy=policy)
    with pytest.raises(Exception, match="needs an explicit name"):
        slides.new_slide()
    slides.new_slide(name="xxx")
    with pytest.raises(Exception, match="already exists"):
        slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    with pytest.raises(Exception, match="needs an explicit name"):
        slides.new_slide()
    with pytest.raises(Exception, match="has to be a string"):
        slides.new_slide(name=123)
    assert len(slides._slides) == 2


def test_invalid_name_policy():
    with pytest.raises(Exception, match="Invalid"):
        Slides(name_policy="xxx")


def test_name_policy_ignore():
    slides = Slides(name_policy="ignore")
    slides.new_slide(name="xxx")
    slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    assert len(slides._slides) == 3


def test_name_policy_ignore():
    slides = Slides(name_policy="replace")
    slides.new_slide(name="xxx")
    slides.new_slide(name="yyy")
    b2 = slides.new_slide(name="xxx")

    s = slides._slides
    assert len(s) == 2
    assert s[0].name == "yyy"
    assert s[1].name == "xxx"
    assert s[1].box() is b2
