#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import logging

from songprint.base import Base, FuzzyBool
import songprint.settings as settings


split_text_title = Base._split_text_title  # pylint: disable=W0212,C0103
split_text_list = Base._split_text_list  # pylint: disable=W0212,C0103
compare_text = Base._compare_text  # pylint: disable=W0212,C0103
compare_text_titles = Base._compare_text_titles  # pylint: disable=W0212,C0103
compare_text_lists = Base._compare_text_lists  # pylint: disable=W0212,C0103


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
        """Verify title comparison ignores case and whitespace."""
        self.assertEqual(1.0, compare_text_titles("The Title",
                                                  "the TITLE "))

    def test_compare_title_prefix_1(self):
        """Verify prefixed titles are considered equal."""
        self.assertEqual(1.0, compare_text_titles("(What's the story) Morning Glory",
                                                  "What's the story morning glory"))

    def test_compare_title_prefix_2(self):
        """Verify a title's prefix does not matter for equality."""
        self.assertEqual(1.0, compare_text_titles("(What's the story) Morning Glory",
                                                  "Morning Glory"))

    def test_compare_title_suffix_1(self):
        """Verify suffixed titles are considered equal."""
        self.assertEqual(1.0, compare_text_titles("Album Title (Bonus Version)",
                                                  "Album Title"))

    def test_compare_title_suffix_2(self):
        """Verify differing title suffixes are not considered equal."""
        self.assertGreater(1.0, compare_text_titles("Children (Original Version)",
                                                    "Children (Dream Version"))


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
