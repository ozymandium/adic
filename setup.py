#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
  name = 'adic',
  version = '0.1',
  packages = find_packages(exclude="scripts"),
  scripts = [
    'scripts/abbreviate-file',
  ],
  entry_points = {
    'console_scripts': [
      'adic-adev = adic.adev:main',
      'adic-char = adic.characterize:main',
    ],
  },
)