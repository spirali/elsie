import glob
import os

from elsie import Slides


def test_cache(test_env):
    cache_dir = "elsie-cache"
    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    assert not glob.glob("{}/*".format(cache_dir))
    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "7cdc642e30c1a38b89bf9bb00bcc0f60fc9617bf.pdf",
        "748bb89d5eb54a97933e39f406b1e6ed25d0b219.pdf",
        "f3362fd290216e782a7ced435ca2ceff011776d1.pdf",
        "queries3.cache"
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("3")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "7cdc642e30c1a38b89bf9bb00bcc0f60fc9617bf.pdf",
        "748bb89d5eb54a97933e39f406b1e6ed25d0b219.pdf",
        "f3362fd290216e782a7ced435ca2ceff011776d1.pdf",
        "queries3.cache"
    }

    slides = Slides()

    slide = slides.new_slide()
    slide.box(show="1+").text("1")
    slide.box(show="next+").text("2")
    slide.box(show="next+").text("4")

    slides.render(output="test.pdf", cache_dir=cache_dir)

    assert set(os.path.basename(p) for p in glob.glob("{}/*".format(cache_dir))) == {
        "7cdc642e30c1a38b89bf9bb00bcc0f60fc9617bf.pdf",
        "4e9e0eb2550172bf1c96e0485333d31cb9026c3c.pdf",
        "f3362fd290216e782a7ced435ca2ceff011776d1.pdf",
        "queries3.cache"
    }
