"""Package for Enharmony."""

__project__ = 'Enharmony'
__version__ = '0.0.0'

try:
    from enharmony.song import Song
    from enharmony.title import Title
    from enharmony.artist import Artist
    from enharmony.album import Album
except ImportError:  # pragma: no cover, manual test
    pass
