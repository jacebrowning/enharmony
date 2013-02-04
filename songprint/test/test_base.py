#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import random
import logging

from songprint import find, match, sort, Song, Title, Artist, Album
from songprint.base import FuzzyBool
import songprint.settings as settings


class TestFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Tests against the primary package functions."""

    songs = [Song("The Artists", "Song Title"),
             Song("The Artists", "Song Title 2"),
             Song("The Artists", "Song Title 3")]
    titles = [Title("The Song Title"),
              Title("The Song Title [Live]")]
    artists = [Artist("The Artists"),
               Artist("The Artists & Others")]
    albums = [Album("Album Title"),
              Album("Album Title (Bonus Tracks)")]

    def test_find(self):
        """Verify items can be found in lists."""
        for items in (self.songs, self.titles, self.artists, self.albums):
            logging.info("current items list: {0}".format(items))
            for item in items:
                logging.info("finding by item: {0}".format(repr(item)))
                self.assertEqual(item, find(item, items))

    def test_match(self):
        """Verify items can be matched in lists."""
        self.assertEqual(1, len(match(self.songs[0], self.songs)))
        self.assertEqual(1, len(match(self.titles[0], self.titles)))
        self.assertEqual(1, len(match(self.artists[0], self.artists)))
        self.assertEqual(1, len(match(self.albums[0], self.albums)))

    def test_sort_songs(self):
        """Verify a songs lists can be sorted."""
        self.skipTest("TODO: implement song comparison")
        copy = list(self.songs)
        random.shuffle(copy)
        self.assertEqual(self.songs, sort(self.songs[0], copy))

    def test_sort_titles(self):
        """Verify a titles lists can be sorted."""
        copy = list(self.titles)
        random.shuffle(copy)
        self.assertEqual(self.titles, sort(self.titles[0], copy))

    def test_sort_artists(self):
        """Verify an artists lists can be sorted."""
        copy = list(self.artists)
        random.shuffle(copy)
        self.assertEqual(self.artists, sort(self.artists[0], copy))

    def test_sort_albums(self):
        """Verify an albums lists can be sorted."""
        copy = list(self.albums)
        random.shuffle(copy)
        self.assertEqual(self.albums, sort(self.albums[0], copy))


class TestFuzzyBool(unittest.TestCase):  # pylint: disable=R0904
    """Tests for the FuzzyBool class."""

    def test_true(self):
        """Verify a 1.0 fuzzy boolean is True."""
        self.assertTrue(FuzzyBool(1.0))

    def test_false(self):
        """Verify a <1.0 fuzzy boolean is False."""
        self.assertFalse(FuzzyBool(0.99))

    def test_true_with_threshold(self):
        """Verify a <1.0 fuzzy boolean is True with a threshold."""
        self.assertTrue(FuzzyBool(0.89, threshold=0.87))

    def test_false_with_threshold(self):
        """Verify a fuzzy boolean is False when below the threshold."""
        self.assertFalse(FuzzyBool(0.89, threshold=0.90))

    def test_strings(self):
        """Verify FuzzyBool objects can be represented as strings."""
        self.assertEqual("100.0% equal", str(FuzzyBool(1.0)))
        self.assertEqual("99.0% equal", str(FuzzyBool(0.99)))
        self.assertEqual("0.0% equal", str(FuzzyBool(0.0)))

    def test_representation(self):
        """Verify object representation works for FuzzyBool objects."""
        fuzz = FuzzyBool(0.89, threshold=0.87)
        self.assertEqual(fuzz, eval(repr(fuzz)))
        self.assertEqual(fuzz, True)
        self.assertNotEqual(fuzz, 0.89)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
