import os
import sys

import pytest

PYTEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(PYTEST_DIR)
DATA_DIR = os.path.join(PYTEST_DIR, "data")

sys.path.insert(0, ROOT_DIR)

import test_utils  # noqa

import elsie  # noqa
from elsie.render.backends.svg.backend import InkscapeBackend  # noqa
from elsie.render.inkscape import InkscapeShell  # noqa


class SlideTester:
    def __init__(self, inkscape_shell=None):
        self.slides = elsie.SlideDeck(
            name_policy="ignore", backend=InkscapeBackend(inkscape=inkscape_shell)
        )
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

    def check(self, expected, expect_count=1, render_args=None, bless=False):
        if render_args is None:
            render_args = {}
        done = False
        units = self.slides.render(output=None, return_units=True, **render_args)
        try:
            assert len(units) == expect_count
            for i, unit in enumerate(units):
                result = unit.get_svg()
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
                for i, unit in enumerate(units):
                    with open("{}-{}.svg".format(expected, i), "w") as f:
                        f.write(unit.get_svg())
                print(f"Units written to {os.getcwd()}", file=sys.stderr)
            if bless:
                for i, unit in enumerate(units):
                    path = self.data_path(
                        os.path.join("checks", "{}-{}.svg".format(expected, i))
                    )
                    with open(path, "w") as f:
                        f.write(unit.get_svg())


@pytest.fixture(autouse=True, scope="session")
def inkscape_shell():
    inkscape_bin = os.environ.get("ELSIE_INKSCAPE") or "/usr/bin/inkscape"
    shell = InkscapeShell(inkscape_bin)
    yield shell
    shell.close()


@pytest.fixture(autouse=True, scope="function")
def test_env(tmp_path, inkscape_shell):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    tester = SlideTester(inkscape_shell)
    try:
        yield tester
    finally:
        os.chdir(cwd)
