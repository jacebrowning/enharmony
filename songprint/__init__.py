"""
Package for the songprint package.
"""

from songprint.song import Song


def match(song, songs):
    """Return the best matching L{Song} object from given list of songs.

    @param song: base song to locate best match
    @param songs: list of songs for comparison
    @return: L{Song} object or None if no match exists
    """
    return None


def find(song, songs):
    """Return all matching L{Song} objects from the given list of songs.

    @param song: base song to locate matches
    @param songs: list of songs for comparison
    @return: list of matching songs
    """
    return []
