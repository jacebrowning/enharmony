#!/usr/bin/env python

"""
Unit tests for the enharmony.base module.
"""

import unittest
import logging


from comparable.test import TestCase

from enharmony.base import TextTitle, TextList
from enharmony import settings


@unittest.skip("not implemented")
class TestTextTitle(TestCase):  # pylint: disable=R0904
    """Tests for the TextTitle class."""

    def test_parse_title(self):
        """Verify a text title is parsed."""
        title = TextTitle("The Song Name ")
        self.assertEqual("", str(title.prefix))
        self.assertEqual("The Song Name", str(title.title))
        self.assertEqual("", str(title.suffix))
        self.assertEqual("The Song Name", str(title))

    def test_parse_title_suffix(self):
        """Verify a text title with a suffix is parsed."""
        title = TextTitle("The Song Name  (Original)")
        self.assertEqual("", str(title.prefix))
        self.assertEqual("The Song Name", str(title.title))
        self.assertEqual("Original", str(title.suffix))
        self.assertEqual("The Song Name (Original)", str(title))

    def test_parse_prefix_title(self):
        """Verify a text title with a prefix is parsed."""
        title = TextTitle("  (The Song) Name")
        self.assertEqual("The Song", str(title.prefix))
        self.assertEqual("Name", str(title.title))
        self.assertEqual("", str(title.suffix))
        self.assertEqual("(The Song) Name", str(title))

    def test_parse_prefix_title_suffix(self):
        """Verify a text title with a prefix and suffix is parsed."""
        title = TextTitle("(The Song) Name  (Original)")
        self.assertEqual("The Song", str(title.prefix))
        self.assertEqual("Name", str(title.title))
        self.assertEqual("Original", str(title.suffix))
        self.assertEqual("(The Song) Name (Original)", str(title))

    def test_similar_unequal(self):
        """Verify two different text titles are not similar."""
        similarity = TextTitle("The Song Name") % TextTitle("A Different Song Name")
        self.assertFalse(similarity)
        self.assertGreater(0.72, similarity)

    def test_similar_equal(self):
        """Verify two equal text titles are similar."""
        similarity = TextName("The Song Name") % TextName("The Song Name")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_close(self):
        """Verify two close text titles are similar."""
        similarity = TextName("This is the song name") % TextName("(this) is the song name.")
        self.assertTrue(similarity)
        self.assertLess(0.93, similarity)


@unittest.skip("not implemented")
class TestTextList(TestCase):  # pylint: disable=R0904
    """Tests for the TextList class."""

    def test_parse_list_with_and(self):
        """Verify a 3-item text list is parsed."""
        lst = TextList("This, That, and  the Other ")
        self.assertEqual((TextName("This"), TextName("That"), TextName("the Other")), lst.items)
        self.assertEqual("This, That, the Other", str(lst))

    def test_parse_pair(self):
        """Verify a 2-item text list is parsed."""
        lst = TextList(" Something &  This Thing")
        self.assertEqual((TextName("Something"), TextName("This Thing")), lst.items)
        self.assertEqual("Something, This Thing", str(lst))

    def test_similar_unequal(self):
        """Verify two different text lists are not similar."""
        similarity = TextList("This, That, and  the Other ") % TextList("This Other Thing & One")
        self.assertFalse(similarity)
        self.assertGreater(0.31, similarity)

    def test_similar_equal(self):
        """Verify two equal text lists are similar."""
        similarity = TextList("This + That") % TextList("This + That")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_close(self):
        """Verify two close text lists are similar."""
        similarity = TextList("This, That, and  the Other ") % TextList("That, This &  the Other ")
        self.assertTrue(similarity)
        self.assertLess(0.99, similarity)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
