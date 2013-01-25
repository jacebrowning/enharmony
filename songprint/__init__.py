"""
Package for the songprint package.
"""

from songprint.song import Song


def find(song, songs):
    """Return the best matching L{Song} object from given list of songs.

    @param song: base L{Song} to locate best match
    @param songs: list of L{Song} objects for comparison
    @return: L{Song} object or None if no match exists
    """
    return None


def match(song, songs):
    """Return all matching L{Song} objects from the given list of songs.

    @param song: base song to locate matches
    @param songs: list of songs for comparison
    @return: list of matching songs
    """
    return []


def sort(song, songs):
    """Return a sorted list of songs ranked in descending similarity.

    @param song: base L{Song} to perform comparison against
    @param songs: list of L{Song} objects to compare to the base
    @return: list of L{Song} sorted by similarity to the base
    """
    return []
