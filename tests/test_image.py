import io

from conftest import check

import elsie


@check("imagefrag", expect_count=6, cairo_threshold=15)
def test_line_highlight_fragments(test_env):
    slide = test_env.slide

    img = test_env.assets_path("testimage.svg")
    slide.image(img)

    b = slide.box(x="[90%]", y="[30%]", width="30%", height="30%", show="4+")
    b.rect("black", bg_color="white")
    b2 = b.box(width="fill")
    b2.update_style("default", elsie.TextStyle(size=15, color="white"))
    b2.rect(bg_color="black")
    b2.box(padding=10).text("Scaling and placing images")
    b.fbox().image(img, show_begin=4)


@check("imagenofrag", cairo_threshold=15)
def test_line_highlight_no_fragments(test_env):
    slide = test_env.slide

    img = test_env.assets_path("testimage.svg")
    slide.image(img, fragments=False)

    b = slide.box(x="[90%]", y="[30%]", width="30%", height="30%")
    b.rect("black", bg_color="white")
    b2 = b.box(width="fill")
    b2.update_style("default", elsie.TextStyle(size=15, color="white"))
    b2.rect(bg_color="black")
    b2.box(padding=10).text("Scaling and placing images")
    b.fbox().image(img, fragments=False)


@check("imageshowx", expect_count=3)
def test_image_show(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(test_env.assets_path("testimage2.svg"))


@check("nofrag_showbegin", expect_count=3, cairo_threshold=10)
def test_image_no_fragments_show_begin(test_env):
    slide = test_env.slide
    img = test_env.assets_path("testimage.svg")
    slide.image(img, fragments=False, show_begin=3)


@check("image-bitmap")
def test_image_bitmap(test_env):
    slide = test_env.slide
    img_png = test_env.assets_path("test.png")
    img_jpg = test_env.assets_path("test.jpeg")

    b = slide.fbox(height=140)
    b.rect(bg_color="green")
    b.image(img_png)

    b = slide.fbox(height=300)
    b.rect(bg_color="blue")
    b.image(img_png)

    b = slide.fbox(height=300)
    b.rect(bg_color="green")
    b.image(img_jpg)


@check("image-svg-no-size")
def test_image_svg_no_size(test_env):
    slide = test_env.slide

    b = slide.box(width="fill", horizontal=True)
    b.box(x="[90%]").image(test_env.assets_path("test100x30.svg"))

    slide.box(y="[90%]").image(test_env.assets_path("test100x30.svg"))


@check("image-bitmap-no-size")
def test_image_bitmap_no_size(test_env):
    slide = test_env.slide

    b = slide.box(width="fill", horizontal=True)
    b.box(x="[90%]").image(test_env.assets_path("test.png"))

    slide.box(y="[90%]").image(test_env.assets_path("test.jpeg"))


@check("image-width")
def test_image_width(test_env):
    test_env.slide.box(width=300).rect(bg_color="green").image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(width=50).image(test_env.assets_path("test100x30.svg"))
    test_env.slide.box(width=300).image(test_env.assets_path("test.png"))
    test_env.slide.box(width=300).image(test_env.assets_path("test100x30.svg"))


@check("image-height")
def test_image_height(test_env):
    test_env.slide.box(height=100).rect(bg_color="green").image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(height=10).image(test_env.assets_path("test100x30.svg"))
    test_env.slide.box(height=100).image(test_env.assets_path("test.png"))
    test_env.slide.box(height=200).image(test_env.assets_path("test100x30.svg"))


@check("image-width-height")
def test_image_width_height(test_env):
    test_env.slide.box(width=300, height=100).image(
        test_env.assets_path("test100x30.svg")
    )
    test_env.slide.box(width=300, height=100).image(test_env.assets_path("test.png"))


@check("image-show-next", expect_count=5)
def test_image_show_next(test_env):
    slide = test_env.slide
    img = test_env.assets_path("testimage.svg")
    slide.box(width=100, height=100).image(img, show_begin=2)
    slide.box(width=30, height=30, show="next").rect(bg_color="black")


@check("ora-nofrag")
def test_ora_no_fragments(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img, fragments=False)


@check("ora-frag", expect_count=4)
def test_ora_fragments_1(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img)


@check("ora-frag-sb", expect_count=6)
def test_ora_fragments_showbegin(test_env):
    slide = test_env.slide
    img = test_env.assets_path("oratest.ora")
    slide.image(img, show_begin=3)


@check("image-substeps1", expect_count=3, cairo_threshold=10)
def test_image_substeps_show1(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(test_env.assets_path("testimage.svg"), select_fragments=[3, None, 1])


@check("image-substeps2", expect_count=3)
def test_image_substeps_show2(test_env):
    """ Regresion test for show attribute when element has no childs """
    slide = test_env.slide
    slide.image(
        test_env.assets_path("testimage.svg"), select_fragments=[2], show_begin=2
    )
    slide.box(width="100", height="100", show="1-3").rect(color="black")


@check("image-source")
def test_image_other_sources(test_env):
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\x00\x00\x00\x90\x91h6\x00\x00\x01\x84iCCPICC profile\x00\x00(\x91}\x91=H\xc3P\x14\x85OS\x8bR*\x0ev\x10q\xc8Pu\xb1 *\xe2\xa8U(B\x85P+\xb4\xea`\xf2\xd2?h\xd2\x90\xa4\xb88\n\xae\x05\x07\x7f\x16\xab\x0e.\xce\xba:\xb8\n\x82\xe0\x0f\x88\x9b\x9b\x93\xa2\x8b\x94x_Rh\x11\xe3\r\x8f|\x9cw\xcf\xe1\xbd\xfb\x00\xa1Qa\x9a\xd55\x0eh\xbam\xa6\x93\t1\x9b[\x15\xbb_\x11@\x08a\xfaFef\x19s\x92\x94\x82o}\xddS7\xd5]\x9cg\xf9\xf7\xfdY\xbdj\xdeb@@$\x9ee\x86i\x13o\x10Oo\xda\x06\xe7}\xe2(+\xc9*\xf19\xf1\x98I\x07$~\xe4\xba\xe2\xf1\x1b\xe7\xa2\xcb\x02\xcf\x8c\x9a\x99\xf4<q\x94X,v\xb0\xd2\xc1\xacdj\xc4S\xc41U\xd3)_\xc8z\xacr\xde\xe2\xacUj\xacuN~\xc3H^_Y\xe6:\xad!$\xb1\x88%H\x10\xa1\xa0\x862*\xb0\x11\xa7\xbfN\x8a\x854\xed\'|\xfc\x83\xae_"\x97B\xae2\x189\x16P\x85\x06\xd9\xf5\x83\xbf\xc1\xef\xd9Z\x85\xc9\t/)\x92\x00B/\x8e\xf31\x0ct\xef\x02\xcd\xba\xe3|\x1f;N\xf3\x04\x08>\x03Wz\xdb_m\x003\x9f\xa4\xd7\xdbZ\xec\x08\xe8\xdb\x06.\xae\xdb\x9a\xb2\x07\\\xee\x00\x03O\x86l\xca\xae\x14\xa4%\x14\n\xc0\xfb\x19=S\x0e\xe8\xbf\x05\xc2k\xde\xdcZ\xfb8}\x0024\xab\xd4\rpp\x08\x8c\x14){\xdd\xe7\xde=\x9ds\xfb\xb7\xa75\xbf\x1f\x0e\xc5r\x7f\xe7\xea4\x97\x00\x00\x00\tpHYs\x00\x00.#\x00\x00.#\x01x\xa5?v\x00\x00\x00\x07tIME\x07\xe5\x01\x05\n\x0f5\\_\xa4)\x00\x00\x00\x19tEXtComment\x00Created with GIMPW\x81\x0e\x17\x00\x00\x01NIDAT(\xcf\x95\x92KO\xc2@\x14\x85\xbf\x99i\x996@\x83\x88\x18\x15T\xa2\x89k\x7f\xa2?\xce\xadk\x8d\xd1\xb0!j\x00\xc3\xab\xe5\xd12\xd7\x05\x8f \x95\x857wq7\xdf\xe4\x9c3G\xf1p\xcc\x7fF\xf3\xcf\xf9\x130\xa0\x0e\x01\xde\xce\xad dY\xc7E\x88\xc3\x1b\xa2G\x90@\x06\x92\x07\x14\x12\xb1\xb8#\xbee\x16!\x1aY\x12\x0e(\xbdQxG\r\xc0\xed\x01\x96\xb4E\xff\x9e^\x93q\x918 \xd3\x142\xaenh>b\x9fP\xe3\xdf\x80+3\xbb\xa4\xdf\xe0\xa3F7d\xa6\x10\x8d\xef\x98_\x13N8\xeb`&+a\x1b\xd3R&\xa9\xd3\xad\xd0\x0f\x88\r\xa9f\tsM\xec3\xa8\x91\xd6\xf7RR\xb8\x90,djY\xe8\xb5\xda\x95OOP\x82\xb3\xdb\xa77\x00`\x16\x84\x0b\xb4\xa0A\x81\x06\xeb\x88f\x84cL\xb2\rj\xe5\xc1\xa1\'\x94>i\x9c\x90i\xbe\x8b\xcc\x15\xbe#J9\x1aQ\xeea\xba\xb9\x94L\x8f\xe0\x95\xf3\x14\x93A\x8ba\x01\xdfQ\x8d9\xed\x10=c\xbe\xf2\xff\x90\xe0\xb71C*U\x82\x0b\xfa\x16\x0f\xec\x9cJ\x1b\xfb\x02\xd3< \x90\xa0ST\x86\x80\x12\x84\xf52\xde\xea\xc9wIP\x19~J\xc1\xa1\x1d\n\xc4\x809\xd4%@0S\x8a1e\x8b\x16\xec\x14\x95"f\xb7\x8a?\x16x~\xc8\xa7l"\x17\x00\x00\x00\x00IEND\xaeB`\x82'  # noqa
    slide = test_env.slide
    slide.box(width=100, height=100).image(data, image_type="png")
    slide.box(width=100, height=100).image(io.BytesIO(data), image_type="png")
