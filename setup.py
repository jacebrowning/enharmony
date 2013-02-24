#!/usr/bin/env python

"""
Installer for setuptools.
"""

from setuptools import setup, find_packages

from songprint.settings import __version__ as VERSION

setup(
name='songprint',
author="Jace Browning",
author_email="jace.browning@gmail.com",
version=VERSION,
description=("Textual comparison of song tags."),
packages=find_packages(),
)
