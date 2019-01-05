#!/usr/bin/env python

from setuptools import setup
import sys

if sys.version_info.major < 3 or \
       (sys.version_info.major == 3 and sys.version_info.minor < 4):
    sys.exit("Python 3.4 or newer is required")


VERSION = None
with open("elsie/version.py") as f:
     exec(f.read())
if VERSION is None:
    raise Exception("version.py executed but VERSION was not set")

setup(name='elsie',
      version=VERSION,
      description='Framework for making slides',
      long_description="""
Elsie is a Framework for making slides in Python,
see http://github.com/spirali/elsie for an example.
      """,
      author='Stanislav Bohm',
      url='http://github.com/spirali/elsie',
      packages=['elsie'],
      install_requires=["pypdf2", "pygments", "lxml"],
      classifiers=("Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"))
