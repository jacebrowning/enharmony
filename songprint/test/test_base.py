#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import logging

from songprint.base import Base
import songprint.settings as settings


class TestCompareText(unittest.TestCase):  # pylint: disable=R0904
    """Tests for comparing text."""

    def test_compare_text_exact(self):
        """Verify exact text comparison works."""
        text1 = "A quick brown fox jumped over the lazy dog."
        text2 = "A quick brown fox jumped over the lazy dog."
        self.assertEqual(1.0, Base._compare_text(text1, text2))

    def test_compare_text_similar(self):
        """Verify similar text is almost equal."""
        text1 = "A quick brown fox jumped over the lazy dog."
        text2 = "A quick brown fox jumped over the lazy dogs."
        self.assertLess(0.98, Base._compare_text(text1, text2))

    def test_compare_text_different(self):
        """Verify different text is not equal."""
        text1 = "cat"
        text2 = "123"
        self.assertEqual(0.0, Base._compare_text(text1, text2))


class TestCompareList(unittest.TestCase):  # pylint: disable=R0904
    """Tests for comparing textual lists."""

    def test_compare_list_equal(self):
        """Verify the same list is considered equal."""
        text1 = "Milk, flour, and eggs"
        text2 = "milk, flour and Eggs"
        self.assertEqual(1.0, Base._compare_text_list(text1, text2))

    def test_compare_list_order(self):
        """Verify differently ordered lists are equal."""
        text1 = "Milk, flour, and eggs"
        text2 = "flour, Eggs, MILK"
        self.assertEqual(1.0, Base._compare_text_list(text1, text2))

    def test_compare_list_missing(self):
        """Verify a list with a missing item is still somewhat equal."""
        text1 = "Milk and flour"
        text2 = "flour, Eggs, MILK"
        self.assertLess(0.5, Base._compare_text_list(text1, text2))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
