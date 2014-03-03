Enharmony
=========

[![Build Status](https://travis-ci.org/jacebrowning/enharmony.png?branch=master)](https://travis-ci.org/jacebrowning/enharmony)
[![Coverage Status](https://coveralls.io/repos/jacebrowning/enharmony/badge.png?branch=master)](https://coveralls.io/r/jacebrowning/enharmony?branch=master)
[![PyPI Version](https://badge.fury.io/py/Enharmony.png)](http://badge.fury.io/py/Enharmony)

Enharmony is a library that provides functions to locate duplicate songs
by performing a textual comparison of the songs' attributes.



Getting Started
===============

Requirements
------------

* Python 3.3: http://www.python.org/download/releases/3.3.4/#download


Installation
------------

Enharmony can be installed with 'pip':

    pip install Enharmony

Or directly from the source code:

    git clone https://github.com/jacebrowning/enharmony.git
    cd enharmony
    python setup.py install



Basic Usage
===========

A sample script might look like this:

    #!/usr/bin/env python

    from enharmony import match, Song

    items = [Song("The Beatles", "Rock and Roll Music"),
             Song("Beatles", "rock & roll music"),
             Song("The beetles", "Rock & Roll Music", duration=150),
             Song("The Beatles", Rocky Raccoon")]

    base = Song('beatles', 'rock and roll music', duration=150)

    for item in match(base, items):
        print(item)



For Contributors
================

Requirements
------------

* GNU Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html


Installation
------------

Create a virtualenv:

    make env

Run the tests:

    make test
    make tests  # includes integration tests

Build the documentation:

    make doc

Run static analysis:

    make pep8
    make pylint
    make check  # pep8 and pylint

Prepare a release:

    make dist  # dry run
    make upload
