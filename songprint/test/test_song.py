"""
Unit tests for the song.py module.
"""

import unittest

from songprint import Song


class TestEquality(unittest.TestCase):
    """Tests for Song equality."""

    def test_exact(self):
        """Verify exact matches are equal."""
        self.assertEqual(Song(), Song())
        self.assertEqual(Song("Artist", "Title"), Song("Artist", "Title"))

    def test_remixes(self):
        """Verify similarly labeled remixes are equal."""
        self.assertEqual(Song("Artist", "Title (remix)"), Song("Artist", "Title [Remix]"))


if __name__ == '__main__':
    unittest.main()
