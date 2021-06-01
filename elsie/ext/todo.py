def todo_placeholder(box, name=None):
    if name is None:
        name = box.name
    todo_box = box.fbox(padding=3)
    todo_box.rect(bg_color="#ee9", color="black", stroke_width=6)
    if name:
        text = f"TODO\n{name}"
    else:
        text = "TODO"
    inner_box = todo_box.fbox(padding=20)
    inner_box.rect(bg_color="#ee9", color="black", stroke_width=6)
    inner_box.text(text)
    return todo_box
