from conftest import check

from elsie import TextStyle
from elsie.ext.markdown import (
    MD_BOLD_STYLE,
    MD_PARAGRAPH_STYLE,
    markdown,
    md_heading_style_name,
)


@check("md-basic")
def test_md_basic(test_env):
    slide = test_env.slide
    markdown(
        slide,
        """
    # Hello
    How are you doing?

    ## This is another heading
    And this is another paragraph
    """,
    )


@check("md-text-formatting")
def test_md_text_formatting(test_env):
    slide = test_env.slide
    markdown(
        slide,
        """
    *italic* text
    **bold** text
    *italic text interleaved with **bold** text*
    """,
    )


@check("md-blank-line-between-paragraphs")
def test_md_blank_line_between_paragraphs(test_env):
    slide = test_env.slide
    markdown(
        slide,
        """
    Paragraph 1

    Paragraph 2

    Paragraph 3, which has
    multiple lines
    """,
    )


@check("md-inline-style")
def test_md_inline_style(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    ~tt{monospace font} normal font
    """,
    )


@check("md-override-style")
def test_md_override_style(test_env):
    slide = test_env.slide

    wrapper = slide.box()
    wrapper.set_style(MD_PARAGRAPH_STYLE, TextStyle(size=20))
    wrapper.set_style(MD_BOLD_STYLE, TextStyle(italic=True))
    wrapper.set_style(md_heading_style_name(1), TextStyle(size=18))
    wrapper.set_style(md_heading_style_name(2), TextStyle(size=40))

    markdown(
        wrapper,
        """
    I am **bold** (or not?)

    # Small heading
    ## Large heading
    """,
    )


@check("md-skip-invalid-elements")
def test_md_skip_invalid_elements(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    ![](image.png)

        code block
    """,
    )


@check("md-fenced-code")
def test_md_fenced_code(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    This is some Python:
    ```python
    def test(x):
        return x + 1
    ```

    And this is some C:
    ```c
    int main() {
        return 0;
    }
    ```
    """,
    )


@check("md-list-simple")
def test_md_list_simple(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    - Item A
    - Item B
    - Item C

    1. Item 1
    2. Item 2
    3. Item 3
    """,
    )


@check("md-list-ul-nested")
def test_md_list_ul_nested(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    - Item A
        * Subitem A
            - Subitem X
        * Subitem B
    - Item B
        - Subitem A
    - Item C
        - Subitem C
    """,
    )


@check("md-list-ol-nested")
def test_md_list_ol_nested(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    1. Item A
        1. Subitem A
        2. Subitem B
    2. Item B
        1. Subitem A
        2. Subitem B
    """,
    )


@check("md-list-ul-ol-nested")
def test_md_list_ul_ol_nested(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    - Item A
        1. Subitem A
        2. Subitem B
    - Item B
        1. Subitem A
            - Subitem X
        2. Subitem B
    """,
    )


@check("md-list-ol-ul-nested")
def test_md_list_ol_ul_nested(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    1. Item A
        - Subitem A
        - Subitem B
    2. Item B
        - Subitem A
            1. Subitem X
        - Subitem B
    """,
    )


@check("md-list-item-multi-line")
def test_md_list_item_multi_line(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    1. This item
    has multiple lines
    2. This item also has
    multiple lines
    """,
    )


@check("md-ul-bullet-point")
def test_md_ul_bullet_point(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    - Item A
    - Item B
    - Item C

    * Item A
    * Item B
    * Item C
    """,
    )


@check("md-link")
def test_md_link(test_env):
    slide = test_env.slide

    markdown(slide, "Hello [link](https://foo.com).")


@check("md-blockquote")
def test_md_blockquote(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
Normal text
> quoted text
> quoted *text* with **formatting**
""",
    )
