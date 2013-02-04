#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import logging

from songprint.base import FuzzyBool
import songprint.settings as settings


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

    def test_representation(self):
        """Verify FuzzyBool objects can be represented as strings."""
        self.assertEqual("100.0% equal", str(FuzzyBool(1.0)))
        self.assertEqual("99.0% equal", str(FuzzyBool(0.99)))
        self.assertEqual("0.0% equal", str(FuzzyBool(0.0)))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
