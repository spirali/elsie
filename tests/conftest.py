import os
import sys
import pytest
import shutil

PYTEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(PYTEST_DIR)
WORK_DIR = os.path.join(PYTEST_DIR, "work")
DATA_DIR = os.path.join(PYTEST_DIR, "data")

sys.path.insert(0, ROOT_DIR)

import elsie  # noqa


def prepare():
    """Prepare working directory

    If directory exists then it is cleaned;
    If it does not exists then it is created.
    """
    if os.path.isdir(WORK_DIR):
        for root, dirs, files in os.walk(WORK_DIR):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o700)
            for f in files:
                os.chmod(os.path.join(root, f), 0o700)
        for item in os.listdir(WORK_DIR):
            path = os.path.join(WORK_DIR, item)
            if os.path.isfile(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
    else:
        os.makedirs(WORK_DIR)
    os.chdir(WORK_DIR)


class SlideTester:

    def __init__(self):
        self.slides = elsie.Slides()
        self.slide = self.slides.new_slide()

    def data_path(self, subpath):
        return os.path.join(DATA_DIR, subpath)

    def check(self, expected, expect_count=1, render_args=None):
        if render_args is None:
            render_args = {}
        done = False
        svgs = self.slides.render(output=None, return_svg=True, **render_args)
        try:
            assert len(svgs) == expect_count
            for i, result in enumerate(svgs):
                filename = self.data_path("{}-{}.svg".format(expected, i))
                with open(filename) as f:
                    expected_content = f.read()
                print("Slide", i)
                assert expected_content == result
            done = True
        finally:
            if not done:
                for i, svg in enumerate(svgs):
                    with open("{}-{}.svg".format(expected, i), "w") as f:
                        f.write(svg)


@pytest.yield_fixture(autouse=True, scope="function")
def test_env():
    prepare()
    os.chdir(WORK_DIR)
    tester = SlideTester()
    yield tester
