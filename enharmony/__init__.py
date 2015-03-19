"""Package for Enharmony."""

import sys

__project__ = 'Enharmony'
__version__ = '0.0.0'

VERSION = __project__ + '-' + __version__

PYTHON_VERSION = 3, 3

if not sys.version_info >= PYTHON_VERSION:  # pragma: no cover (manual test)
    exit("Python {}.{}+ is required.".format(*PYTHON_VERSION))

try:
    from enharmony.song import Song
    from enharmony.title import Title
    from enharmony.artist import Artist
    from enharmony.album import Album
except ImportError:  # pragma: no cover (manual test)
    pass
