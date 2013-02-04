"""
Package for the songprint package.

The functions provided can be used on L{Song}, L{Title}, L{Artist}, and L{Album} objects.
"""

from songprint.song import Song
from songprint.title import Title
from songprint.artist import Artist
from songprint.album import Album


def find(base, items):
    """Return the best matching item from given list of items.

    @param base: base item to locate best match
    @param items: list of items for comparison
    @return: item or None if no match exists
    """
    best_similarity = 0
    best_item = None
    for item in items:
        similarity = base.similarity(item)
        if similarity > best_similarity:
            best_similarity = similarity
            best_item = item
    return best_item


def match(base, items):
    """Return all matching items from the given list of items.

    @param base: base item to locate matches
    @param items: list of items for comparison
    @return: list of matching items
    """
    return [item for item in items if (item == base)]


def sort(base, items):
    """Return a sorted list of items ranked in descending similarity.

    @param base: base item to perform comparison against
    @param items: list of items to compare to the base
    @return: list of items sorted by similarity to the base
    """
    return sorted(items, key=base.similarity, reverse=True)
