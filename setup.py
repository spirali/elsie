#!/usr/bin/env python

import sys
from collections import defaultdict

from setuptools import setup, find_packages

if sys.version_info.major < 3 or (
    sys.version_info.major == 3 and sys.version_info.minor < 6
):
    sys.exit("Python 3.6 or newer is required")

VERSION = None
with open("elsie/version.py") as f:
    exec(f.read())
if VERSION is None:
    raise Exception("version.py executed but VERSION was not set")

extras = defaultdict(list)
dependencies = []
with open("requirements.txt") as f:
    for line in f:
        line = line.strip()
        extra = line.rfind("#")
        if extra == -1:
            dependencies.append(line)
        else:
            extras[line[extra:].lstrip("# ")].append(line[:extra].strip())

setup(
    name="elsie",
    version=VERSION,
    description="Framework for making slides",
    long_description="""
Elsie is a Framework for making slides in Python,
Check out its documentation at https://spirali.github.io/elsie.
      """,
    author="Stanislav Böhm",
    author_email="spirali@kreatrix.org",
    url="https://github.com/spirali/elsie",
    packages=find_packages(),
    install_requires=dependencies,
    extras_require=extras,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
