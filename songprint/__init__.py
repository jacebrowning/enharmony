"""
Package for the songprint package.

The functions provided can be used on L{Song}, L{Title}, L{Artist}, and L{Album} objects.
"""

from songprint.song import Song
from songprint.title import Title
from songprint.artist import Artist
from songprint.album import Album


def find(item, items):
    """Return the best matching item from given list of items.

    @param song: base item to locate best match
    @param songs: list of items for comparison
    @return: item or None if no match exists
    """
    return None


def match(item, items):
    """Return all matching items from the given list of items.

    @param song: base item to locate matches
    @param songs: list of items for comparison
    @return: list of matching items
    """
    return []


def sort(item, items):
    """Return a sorted list of items ranked in descending similarity.

    @param song: base item to perform comparison against
    @param songs: list of items to compare to the base
    @return: list of items sorted by similarity to the base
    """
    return []
