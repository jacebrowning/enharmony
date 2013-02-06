#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import random
import logging

from songprint import find, match, sort, Song, Title, Artist, Album
from songprint.base import Base, FuzzyBool
import songprint.settings as settings


split_text_title = Base._split_text_title  # pylint: disable=W0212,C0103
split_text_list = Base._split_text_list  # pylint: disable=W0212,C0103
compare_text = Base._compare_text  # pylint: disable=W0212,C0103
compare_text_titles = Base._compare_text_titles  # pylint: disable=W0212,C0103
compare_text_lists = Base._compare_text_lists  # pylint: disable=W0212,C0103


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


class TestSplitTitle(unittest.TestCase):  # pylint: disable=R0904
    """Tests for splitting titles with optional text."""

    def test_split_title_nominal(self):
        """Verify a normal title is split."""
        self.assertEqual(['Album Title'], split_text_title("Album Title "))

    def test_split_title_prefix(self):
        """Verify a title with a prefix is split."""
        self.assertEqual(['Some', 'Album Title'], split_text_title("(Some) Album Title "))

    def test_split_title_suffix(self):
        """Verify a title with a suffix is split."""
        self.assertEqual(['Album Title', 'Goes Here'], split_text_title("Album Title  (Goes Here)"))

    def test_split_title_combination(self):
        """Verify a combination title is split."""
        self.assertEqual(['Some', 'Album Title', 'Goes Here'], split_text_title(" (Some) Album Title  (Goes Here)"))


class TestSplitList(unittest.TestCase):  # pylint: disable=R0904
    """Tests for splitting textual lists."""

    def test_split_list_nominal(self):
        """Verify a normal list is split."""
        self.assertEqual(['milk', 'Flour', 'EGGS'], split_text_list("milk, Flour, and EGGS"))

    def test_split_list_not_oxford(self):
        """Verify a list not using the Oxford Comma is split."""
        self.assertEqual(['milk', 'Flour', 'Eggs'], split_text_list("milk, Flour and Eggs"))

    def test_split_list_extra(self):
        """Verify a list is extra spaces is split."""
        self.assertEqual(['milk', 'Flour', 'EGGS'], split_text_list("milk,  Flour, and EGGS"))
        self.assertEqual(['milk', 'Flour', 'EGGS'], split_text_list("milk, ,  Flour, and   EGGS"))
        self.assertEqual(['milk', 'Flour', 'EGGS'], split_text_list("  milk, ,  Flour   and   EGGS  "))


class TestCompareText(unittest.TestCase):  # pylint: disable=R0904
    """Tests for comparing text."""

    def test_compare_text_exact(self):
        """Verify exact text comparison works."""
        text1 = "A quick brown fox jumped over the lazy dog."
        text2 = "A quick brown fox jumped over the lazy dog."
        self.assertEqual(1.0, compare_text(text1, text2))

    def test_compare_text_similar(self):
        """Verify similar text is almost equal."""
        text1 = "A quick brown fox jumped over the lazy dog."
        text2 = "A quick brown fox jumped over the lazy dogs."
        self.assertLess(0.98, compare_text(text1, text2))

    def test_compare_text_different(self):
        """Verify different text is not equal."""
        text1 = "cat"
        text2 = "123"
        self.assertEqual(0.0, compare_text(text1, text2))


class TestCompareTitles(unittest.TestCase):  # pylint: disable=R0904
    """Tests for comparing textual titles with optional parts."""

    def test_compare_title_equal(self):
        """Verify the same list is considered equal."""
        text1 = "The Title"
        text2 = "the TITLE "
        self.assertEqual(1.0, compare_text_titles(text1, text2))

    def test_compare_title_prefix(self):
        """Verify prefixed titles are considered equal."""
        text1 = "(What's the story) Morning Glory"
        text2 = "Morning Glory"
        text3 = "What's the story morning glory"
        self.assertEqual(1.0, compare_text_titles(text1, text2))
        self.assertEqual(1.0, compare_text_titles(text1, text3))

    def test_compare_title_suffix(self):
        """Verify suffixed titles are considered equal."""
        text1 = "Album Title (Bonus Version)"
        text2 = "Album Title"
        self.assertEqual(1.0, compare_text_titles(text1, text2))


class TestCompareLists(unittest.TestCase):  # pylint: disable=R0904
    """Tests for comparing textual lists."""

    def test_compare_list_equal(self):
        """Verify the same list is considered equal."""
        text1 = "Milk, flour, and eggs"
        text2 = "milk, flour and Eggs"
        self.assertEqual(1.0, compare_text_lists(text1, text2))

    def test_compare_list_order(self):
        """Verify differently ordered lists are equal."""
        text1 = "Milk, flour, and eggs"
        text2 = "flour, Eggs, MILK"
        self.assertEqual(1.0, compare_text_lists(text1, text2))

    def test_compare_list_missing(self):
        """Verify a list with a missing item is still somewhat equal."""
        text1 = "Milk and flour"
        text2 = "flour, Eggs, MILK"
        self.assertGreater(1.0, compare_text_lists(text1, text2))


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
