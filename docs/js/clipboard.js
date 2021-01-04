$(function () {
    var blocks = document.querySelectorAll("pre > code");
    blocks.forEach((block, index) => {
        const parent = block.parentElement;
        parent.id = `__code_${index}`;
        parent.classList.add("code-block");
        parent.insertBefore(
            createCopyButton(parent.id),
            block
        );
    });

    new ClipboardJS(".md-clipboard");
});

function createCopyButton(id) {
    var button = document.createElement("img");
    button.classList.add("md-clipboard");
    button.title = "Copy to clipboard";
    button.setAttribute("data-clipboard-target", "#" + id + " > code");
    button.src = base_url + "/img/clipboard.svg";
    return button;
}
