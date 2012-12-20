"""
Unit tests for the songprint.album module.
"""

import unittest

from songprint.album import Album


class TestEquality(unittest.TestCase):
    """Tests for album equality."""

    def test_exact(self):
        """Verify exact album name matches are equal."""
        self.assertEqual(Album("Album Name"), Album("Album Name"))

    def test_years(self):
        """Verify albums with the same name, but different years are equal."""
        self.assertEqual(Album("Album A", 1997), Album("Album A", 1998))


class TestInequality(unittest.TestCase):
    """Tests for album inequality."""

    def test_different(self):
        """Verify different album names are not equal."""
        self.assertNotEqual(Album("Album A"), Album("Album B"))

    def test_years(self):
        """Verify albums with different names, but the same year are not equal."""
        self.assertNotEqual(Album("Album A", 1997), Album("Album B", 1997))


if __name__ == '__main__':
    unittest.main()
