"""
Unit tests for the songprint.song module.
"""

import unittest

from songprint.song import Song


class TestEquality(unittest.TestCase):
    """Tests for song equality."""

    def test_exact(self):
        """Verify exact matches are equal."""
        self.assertEqual(Song("Artist", "Title"), Song("Artist", "Title"))

    def test_case(self):
        """Verify case does not matter."""
        self.assertEqual(Song("Artist", "Title"), Song("artist", "title"))

    def test_remixes(self):
        """Verify similarly labeled remixes are equal."""
        self.assertEqual(Song("Artist", "Title (remix)"), Song("Artist", "Title [Remix]"))

    def test_title_articles(self):
        """Verify song titles with missing articles are matched."""
        self.assertEqual(Song("Artist", "The Song Name"), Song("Artist", "Song Name"))


class TestInequality(unittest.TestCase):
    """Tests for song inequality."""

    def test_live(self):
        """Verify a live song does not match."""
        self.assertNotEqual(Song("Artist", "Title"), Song("Artist", "Title (live)"))


if __name__ == '__main__':
    unittest.main()
