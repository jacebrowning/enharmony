#!/usr/bin/env python

"""
Setup script for SongPrint.
"""

from setuptools import setup, Command


class TestCommand(Command):  # pylint: disable=R0904
    """Runs the unit tests."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        raise SystemExit(subprocess.call([sys.executable, '-m', 'unittest', 'discover']))

setup(
    name='SongPrint',
    version='0.0.x',

    description="Song matching based on textual comparison of attributes.",
    url='http://pypi.python.org/pypi/SongPrint/',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=['songprint', 'songprint.test'],
    scripts=["bin/demo_lastfm.py"],

    cmdclass={'test': TestCommand},
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
)
