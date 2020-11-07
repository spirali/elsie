import os
import sys

import pytest

PYTEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(PYTEST_DIR)
# WORK_DIR = os.path.join(PYTEST_DIR, "work")
DATA_DIR = os.path.join(PYTEST_DIR, "data")

sys.path.insert(0, ROOT_DIR)

import elsie  # noqa
import test_utils  # noqa


class SlideTester:
    def __init__(self):
        self.slides = elsie.Slides(name_policy="ignore")
        self._slide = None

    @property
    def slide(self):
        if self._slide is None:
            self._slide = self.slides.new_slide()
        return self._slide

    def data_path(self, subpath):
        return os.path.join(DATA_DIR, subpath)

    def assets_path(self, subpath):
        return os.path.join(DATA_DIR, "assets", subpath)

    def check(self, expected, expect_count=1, render_args=None):
        if render_args is None:
            render_args = {}
        done = False
        svgs = self.slides.render(output=None, return_svg=True, **render_args)
        try:
            assert len(svgs) == expect_count
            for i, (_slide, _step, result) in enumerate(svgs):
                filename = self.data_path(
                    os.path.join("checks", "{}-{}.svg".format(expected, i))
                )
                with open(filename) as f:
                    expected_content = f.read()
                print("Slide", i)
                if expected_content != result:
                    test_utils.svg_check(expected_content, result)
            done = True
        finally:
            if not done:
                for i, (_slide, _step, svg) in enumerate(svgs):
                    with open("{}-{}.svg".format(expected, i), "w") as f:
                        f.write(svg)


@pytest.yield_fixture(autouse=True, scope="function")
def test_env(tmp_path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    tester = SlideTester()
    try:
        yield tester
    finally:
        os.chdir(cwd)
