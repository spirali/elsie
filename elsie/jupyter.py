import uuid

from .slidecls import Slide


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


def render_slide(slide: Slide) -> str:
    units = slide.slides.render(None, return_units=True, select_slides=[slide])
    svgs = filter(None, (unit.get_svg() for unit in units))
    fragments = tuple(
        f"<div class='elsie-step step-{index + 1}'>{svg}</div>"
        for (index, svg) in enumerate(svgs)
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
