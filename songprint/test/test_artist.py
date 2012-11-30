"""
Unit tests for the songprint.artist module.
"""

import unittest

from songprint.artist import Artist


class TestEquality(unittest.TestCase):
    """Tests for artist equality."""

    def test_exact(self):
        """Verify exact artist name matches are equal."""
        self.assertEqual(Artist("Artist Name"), Artist("Artist Name"))

    def test_case(self):
        """Verify artist name case does not matter."""
        self.assertEqual(Artist("Artist Name"), Artist("Artist name"))

    def test_ands(self):
        """Verify artist "and" operators do not matter."""
        self.assertEqual(Artist("Artist and Others"), Artist("Artist & others"))
        self.assertEqual(Artist("Artist + Others"), Artist("Others & Artist"))


class TestInequality(unittest.TestCase):
    """Tests for artist inequality."""

    def test_different(self):
        """Verify different artist names are not equal."""
        self.assertNotEqual(Artist("Artist A"), Artist("Artist B"))


if __name__ == '__main__':
    unittest.main()
