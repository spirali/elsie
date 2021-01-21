import contextlib
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
    def __init__(self, backend):
        self.slides = elsie.SlideDeck(name_policy="ignore", backend=backend)
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

    def check_svg(self, expected, expect_count=1, render_args=None, bless=False):
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


@contextlib.contextmanager
def change_workdir(workdir):
    cwd = os.getcwd()
    try:
        os.chdir(workdir)
        yield
    finally:
        os.chdir(cwd)


@pytest.fixture(autouse=True, scope="session")
def inkscape_shell():
    inkscape_bin = os.environ.get("ELSIE_INKSCAPE") or "/usr/bin/inkscape"
    shell = InkscapeShell(inkscape_bin)
    yield shell
    shell.close()


@pytest.fixture(autouse=True, scope="function")
def test_env(tmp_path, inkscape_shell):
    with change_workdir(tmp_path):
        backend = InkscapeBackend(inkscape=inkscape_shell)
        tester = SlideTester(backend)
        yield tester


CAIRO_DIFF_THRESHOLD = 10


def check(
    svg: str = None, cairo=True, cairo_threshold=CAIRO_DIFF_THRESHOLD, **check_kwargs
):
    assert svg or cairo

    def wrapper(wrapped):
        def fn(tmp_path, inkscape_shell, *args, **kwargs):
            with change_workdir(tmp_path):
                if svg:
                    test_utils.check_svg(
                        svg,
                        inkscape_shell,
                        wrapped,
                        check_kwargs=check_kwargs,
                        *args,
                        **kwargs,
                    )
                if cairo:
                    test_utils.check_cairo(
                        wrapped,
                        inkscape_shell,
                        diff_threshold=cairo_threshold,
                        *args,
                        **kwargs,
                    )

        return fn

    return wrapper
