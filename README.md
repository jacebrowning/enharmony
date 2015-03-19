Enharmony
=========

[![Build Status](http://img.shields.io/travis/jacebrowning/enharmony/master.svg)](https://travis-ci.org/jacebrowning/enharmony)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/enharmony/master.svg)](https://coveralls.io/r/jacebrowning/enharmony)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/enharmony.svg)](https://scrutinizer-ci.com/g/jacebrowning/enharmony/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/Enharmony.svg)](https://pypi.python.org/pypi/Enharmony)
[![PyPI Downloads](http://img.shields.io/pypi/dm/Enharmony.svg)](https://pypi.python.org/pypi/Enharmony)

Enharmony is a library that provides functions to locate duplicate songs
by performing a textual comparison of the songs' attributes.

Getting Started
===============

Requirements
------------

* Python 3.3+

Installation
------------

Enharmony can be installed with pip:

```
$ pip install enharmony
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/enharmony.git
$ cd enharmony
$ python setup.py install
```

Basic Usage
===========

A sample script might look like this:

```python
from enharmony import match, Song

items = [Song("The Beatles", "Rock and Roll Music"),
         Song("Beatles", "rock & roll music"),
         Song("The beetles", "Rock & Roll Music", duration=150),
         Song("The Beatles", Rocky Raccoon")]

base = Song('beatles', 'rock and roll music', duration=150)

for item in match(base, items):
    print(item)
```

For Contributors
================

Requirements
------------

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

Installation
------------

Create a virtualenv:

```
$ make env
```

Run the tests:

```
$ make test
$ make tests  # includes integration tests
```

Build the documentation:

```
$ make doc
```

Run static analysis:

```
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

Prepare a release:

```
$ make dist  # dry run
$ make upload
```
