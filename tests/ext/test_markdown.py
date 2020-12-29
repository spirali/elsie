from elsie import TextStyle
from elsie.ext.markdown import (
    MD_BOLD_STYLE,
    MD_PARAGRAPH_STYLE,
    markdown,
    md_heading_style_name,
)


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
    test_env.check("md-basic")


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
    test_env.check("md-text-formatting")


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
    test_env.check("md-blank-line-between-paragraphs")


def test_md_inline_style(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    ~tt{monospace font} normal font
    """,
    )
    test_env.check("md-inline-style")


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
    test_env.check("md-override-style")


def test_md_skip_invalid_elements(test_env):
    slide = test_env.slide

    markdown(
        slide,
        """
    ![](image.png)

        code block

    [link](todo)
    """,
    )
    test_env.check("md-skip-invalid-elements")


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
    test_env.check("md-fenced-code")


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
    test_env.check("md-list-simple")


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
    test_env.check("md-ul-bullet-point")
