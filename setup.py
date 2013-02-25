#!/usr/bin/env python

"""
Setup script for SongPrint.
"""

from distutils.core import setup

from songprint.settings import __version__ as VERSION

setup(
    name='SongPrint',
    version=VERSION,
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',
    packages=['songprint', 'songprint.test'],
    scripts=["bin/demo_lastfm.py"],
    url='http://pypi.python.org/pypi/SongPrint/',
    license='LICENSE.txt',
    description="Song matching based on textual comparison of attributes.",
    long_description=open('README.rst').read(),
)
