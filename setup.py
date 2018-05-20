#!/usr/bin/env python

from distutils.core import setup

import sys

if sys.version_info.major < 3 or \
       (sys.version_info.major == 3 and sys.version_info.minor < 2):
    sys.exit("Python 3.2 or newer is required")

setup(name='elsie',
      version='1.0',
      description='Framework for making slides',
      author='Stanislav Bohm',
      url='http://github.com/spirali/elsie',
      packages=['elsie'])
