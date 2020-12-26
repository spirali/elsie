from copy import deepcopy

import lxml.etree as et

from ..slides.show import ShowInfo


def parse_show_info_from_label(element):
    label = element.get("{http://www.inkscape.org/namespaces/inkscape}label")
    return ShowInfo.from_label(label)


def get_image_steps(root):
    steps = 1
    for element in root.iter():
        show_info = parse_show_info_from_label(element)
        if show_info is not None:
            steps = max(steps, show_info.min_steps())
    return steps


def create_image_data(root, step):
    hidden = []

    def find_hidden_elements(element):
        for child in element:
            show_info = parse_show_info_from_label(child)
            if show_info is not None and not show_info.is_visible(step):
                hidden.append((element, child))
                continue
            find_hidden_elements(child)

    root = deepcopy(root)
    find_hidden_elements(root)
    for element, child in hidden:
        element.remove(child)
    return et.tostring(root).decode()
