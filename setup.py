#!/usr/bin/env python

"""
Setup script for Enharmony.
"""

import setuptools

from enharmony import __project__, __version__

import os
if os.path.exists('README.rst'):
    README = open('README.rst').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()


setuptools.setup(
    name=__project__,
    version=__version__,

    description="Song matching based on textual comparison of attributes.",
    url='http://pypi.python.org/pypi/Enharmony',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),
    scripts=["bin/demo_lastfm.py"],

    entry_points={'console_scripts': []},
    long_description=(README + '\n' + CHANGES),
    license='LGPL',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  # pylint: disable=C0301
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=["Comparable >= 0.2"],
)
