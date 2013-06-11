#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import logging

from songprint.base import Similarity, BaseComparable, Comparable
from songprint.base import Number, Text, TextTitle, TextList


class TestSimilarity(unittest.TestCase):  # pylint: disable=R0904
    """Tests for the Similarity class."""

    def test_str(self):
        """Verify similarity objects can be represented as strings."""
        self.assertEqual("100.0% equal", str(Similarity(1.0)))
        self.assertEqual("99.0% equal", str(Similarity(0.99)))
        self.assertEqual("0.0% equal", str(Similarity(0.0)))

    def test_repr(self):
        """Verify object representation works for similarity objects."""
        sim = Similarity(0.89, threshold=0.87)
        self.assertEqual(sim, eval(repr(sim)))

    def test_bool_true(self):
        """Verify a similarity of 1.0 is True."""
        self.assertTrue(Similarity(1.0))

    def test_bool_false(self):
        """Verify a similarity of <1.0 if False."""
        self.assertFalse(Similarity(0.99))

    def test_bool_true_with_threshold(self):
        """Verify a similarity of <1.0 is True with a threshold."""
        self.assertTrue(Similarity(0.89, threshold=0.88))

    def test_bool_false_with_threshold(self):
        """Verify a similarity is False if under the threshold."""
        self.assertFalse(Similarity(0.89, threshold=0.90))

    def test_float_equal(self):
        """Verify similarities and floats can be compared for equality."""
        self.assertEqual(Similarity(0.42), 0.42)

    def test_float_not_equal(self):
        """Verify similarities and floats can be compared for inequality."""
        self.assertNotEqual(0.12, Similarity(0.13))


class TestBaseComparable(unittest.TestCase):  # pylint: disable=R0904
    """Tests for the BaseComparable class."""

    def test_str(self):
        """Verify base comparable objects can be represented as strings."""
        self.assertEqual("abc", str(BaseComparable("abc")))

    def test_repr(self):
        """Verify object representation works for base comparable objects."""
        obj = BaseComparable(42)
        self.assertEqual(obj, eval(repr(obj)))

    def test_eq_true(self):
        """Verify base comparable objects can be compared for equality."""
        self.assertEqual(BaseComparable("hello world"), BaseComparable("hello world"))

    def test_eq_false(self):
        """Verify base comparable objects can be compared for inequality."""
        self.assertNotEqual(BaseComparable("hello world"), BaseComparable("hello world!"))






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
        self.assertEqual(1.0, compare_text("A quick brown fox jumped over the lazy dog.",
                                           "A quick brown fox jumped over the lazy dog."))

    def test_compare_text_similar(self):
        """Verify similar text is almost equal."""
        self.assertLess(0.98, compare_text("A quick brown fox jumped over the lazy dog.",
                                           "A quick brown fox jumped over the lazy dogs."))

    def test_compare_text_different(self):
        """Verify different text is not equal."""
        self.assertEqual(0.0, compare_text("cat",
                                           "123"))

    @unittest.expectedFailure  # TODO: support replacements during text comparison
    def test_compare_with_replacement(self):
        """Verify replaceable words are handled for comparison."""
        self.assertEqual(1.0, compare_text("Rock and roll music",
                                           "Rock & Roll Music"))


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


class TestAverageSimilarity(unittest.TestCase):  # pylint: disable=R0904
    """Tests for calculating weighted similarity averages."""

    def test_single_basic(self):
        """Verify a single basic type similarity can be averaged."""
        self.assertEqual(1.0, average_similarity([(42, 42, 1.0, None)]))
        self.assertEqual(1.0, average_similarity([(42, 42, 0.3, None)]))
        self.assertEqual(0.0, average_similarity([(42, 0, 0.3, None)]))

    def test_mulitple_basic(self):
        """Verify multiple basic type similarities can be averaged."""
        self.assertEqual(0.5, average_similarity([(42, 42, 0.5, None),
                                                  (42, 0, 0.5, None)]))
        self.assertEqual(0.75, average_similarity([(42, 42, 0.3, None),
                                                  (42, 0, 0.1, None)]))

    def test_base(self):
        """Verify a base objects similarity can be averaged."""
        item1 = Base()
        item1.value = 42
        item2 = Base()
        item2.value = 0
        self.assertEqual(1.0, average_similarity([(item1, item1, 1.0, None)]))
        self.assertEqual(0.0, average_similarity([(item1, item2, 0.3, None)]))
        self.assertEqual(0.2, average_similarity([(item1, item1, 0.2, None),
                                                  (item1, item2, 0.8, None)]))





if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
