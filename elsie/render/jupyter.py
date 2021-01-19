import base64
import uuid
from typing import List

from ..slides.slide import Slide


def get_javascript(max_step: int, slide_id: str) -> str:
    # Divided into two parts for easier {} interpolation
    p1 = f"""
var active_step = 1;
var max_step = {max_step};
var slide_id = ".{slide_id}";
"""

    p2 = """
function getSelector(selector) {
    return slide_id + " " + selector;
}

function updateState(step) {
    var step_str = step.toString();

    document.querySelector(getSelector(".elsie-next")).disabled = step >= max_step;
    document.querySelector(getSelector(".elsie-previous")).disabled = step <= 1;
    document.querySelector(getSelector(".elsie-current-step")).innerText = "Fragment: " + step_str;

    var items = document.querySelectorAll(getSelector(".elsie-step"));
    for (var i = 0; i < items.length; i++) {
        items[i].style.display = "none";
    }
    document.querySelector(getSelector(".elsie-step.step-" + step_str)).style.display = "block";
}
function moveStep(offset) {
    var new_step = active_step + offset;
    if (new_step >= 1 && new_step <= max_step) {
        active_step = new_step;
    }
    updateState(active_step);
}
document.querySelector(getSelector(".elsie-next")).addEventListener('click', function() {
    moveStep(1);
});
document.querySelector(getSelector(".elsie-previous")).addEventListener('click', function() {
    moveStep(-1);
});
updateState(active_step);
"""

    return "<script type='text/javascript'>(function () {" + p1 + p2 + "})()</script>"


CSS = """
.elsie-wrapper {
    margin-bottom: 20px;
}
.elsie-slide {
    margin-bottom: 10px;
}
.elsie-controls {
    display: flex;
    align-items: center;
}
.elsie-controls * {
    margin: 0 10px;
}
"""


def get_slide_repr_steps(slide: Slide, format: str) -> List[str]:
    if format not in ("svg", "png"):
        raise Exception("Slide can be rendered only to SVG or PNG")

    return_units = format == "svg"
    units = slide.slides.render(
        output=None,
        return_units=return_units,
        select_slides=[slide],
        export_type=format,
        prune_cache=False,
    )
    if format == "svg":
        return [unit.svg for unit in units]
    elif format == "png":
        images = []
        for png in units:
            with open(png, "rb") as f:
                data = base64.encodebytes(f.read())
                images.append(
                    f"""<img src="data:image/png;base64, {data.decode()}" />"""
                )
        return images
    else:
        assert False


def render_slide_html(slide: Slide, format: str = "png") -> str:
    step_items = get_slide_repr_steps(slide, format)
    fragments = tuple(
        f"<div class='elsie-step step-{index + 1}'>{content}</div>"
        for (index, content) in enumerate(step_items)
    )
    fragments_text = "\n".join(fragments)

    slide_id = f"elsie-wrapper-{uuid.uuid4().hex}"
    content = f"""
<div class="elsie-wrapper {slide_id}">
<div class="elsie-slide">
    {fragments_text}
</div>
"""
    if len(fragments) > 1:
        content += f"""
<div class="elsie-controls">
    <button class="elsie-previous"><</button>
    <div class="elsie-current-step">Fragment: 1</div>
    <button class="elsie-next">></button>
</div>
{get_javascript(len(fragments), slide_id)}"""
    content += "</div>"
    return content + f"<style>{CSS}</style>"


# https://stackoverflow.com/a/22424821/1107768
def is_inside_notebook():
    try:
        from IPython import get_ipython

        ipython = get_ipython()
        if not ipython:
            return False
        if "IPKernelApp" not in ipython.config:
            return False
    except ImportError:
        return False
    return True
