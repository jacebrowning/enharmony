"""
Unit tests for the enharmony.song module.
"""

import unittest

from enharmony.song import Song, Artist, Title, Album


@unittest.skip("not implemented")
class TestParsing(unittest.TestCase):  # pylint: disable=R0904
    """Tests for parsing songs."""

    def test_nominal(self):
        """Verify a normal song can be parsed."""
        song = Song("Artist", "Title", "Album", 2000, 7, 123)
        self.assertEqual(Artist("Artist"), song.artist)
        self.assertEqual(Title("Title"), song.title)
        self.assertEqual(Album("Album"), song.album)
        self.assertEqual(7, song.track)
        self.assertEqual(123, song.duration)

    def test_errors(self):
        """Verify parsing errors are handled."""
        self.assertEqual(None, Song("A", "T", track=None).track)
        self.assertEqual(None, Song("A", "T", track="Year").track)


@unittest.skip("not implemented")
class TestEquality(unittest.TestCase):  # pylint: disable=R0904
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


@unittest.skip("not implemented")
class TestInequality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for song inequality."""

    def test_types(self):
        """Verify different types are not equal."""
        self.assertNotEqual(Song("Artist", "Title"), "Artist - Title")

    def test_live(self):
        """Verify a live song does not match."""
        self.assertNotEqual(Song("Artist", "Title"), Song("Artist", "Title (live)"))


if __name__ == '__main__':
    unittest.main()
