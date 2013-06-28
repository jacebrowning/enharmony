Introduction
============

SongPrint is a library that provides functions to locate duplicate songs by
performing a textual comparison of the songs' attributes.



Getting Started
===============

Requirements
------------

* Python 2.7


Installation
------------

SongPrint can be installed with ``pip`` or ``easy_install``::

    pip install SongPrint
    
After installation, the package is available under the name ``songprint``::

    python
    >>> import songprint
    


Sample Usage
============

A sample script might look like this::

    #!/usr/bin/env python

    from songprint import match, Song
    
    items = [Song("The Beatles", "Rock and Roll Music"),
             Song("Beatles", "rock & roll music"),
             Song("The beetles", "Rock & Roll Music", duration=150),
             Song("The Beatles", Rocky Raccoon")]
    
    base = Song('beatles', 'rock and roll music', duration=150)
    
    for item in match(base, items):
        print(item)
        
        
Testing
=======

The ``sonprint`` package contains unit tests which can be run from source::

    python setup.py test