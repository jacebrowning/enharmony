"""
Unit tests for the songprint.album module.
"""

import unittest

from songprint.album import Album


class TestParsing(unittest.TestCase):  # pylint: disable=R0904
    """Tests for parsing album names."""

    def test_nominal(self):
        """Verify a normal album name can be parsed."""
        album = Album("Album Name")
        self.assertEqual("Album Name", album.name)
        self.assertEqual(None, album.kind)
        self.assertEqual(None, album.featuring)

    def test_ep(self):
        """Verify an EP can be parsed."""
        album = Album("Tracks (feat. The Artist) [EP]")
        self.assertEqual("Tracks", album.name)
        self.assertEqual('EP', album.kind)
        self.assertEqual('The Artist', album.featuring)


class TestFormatting(unittest.TestCase):  # pylint: disable=R0904
    """Tests for formatting album names."""

    def test_nominal(self):
        """Verify a normal album name can be formatted."""
        album = Album("Album Name", 1990)
        self.assertEqual("Album Name", str(album))
        self.assertEqual(album, eval(repr(album)))

    def test_single(self):
        """Verify a single can be formatted."""
        album = Album("One Hit [Single]")
        self.assertEqual("One Hit [Single]", str(album))
        self.assertEqual(album, eval(repr(album)))


class TestEquality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for album equality."""

    def test_exact(self):
        """Verify exact album name matches are equal."""
        self.assertEqual(Album("Album Name"), Album("Album Name"))

    def test_years(self):
        """Verify albums with the same name, but different years are equal."""
        self.assertEqual(Album("Album A", 1997), Album("Album A", 1998))

    def test_extra(self):
        """Verify albums with extra text are still equal."""
        self.assertEqual(Album("Album Name"), Album("Album Name (Bonus Tracks)"))
        self.assertEqual(Album("Album Name"), Album("Album Name (Deluxe)"))


class TestInequality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for album inequality."""

    def test_types(self):
        """Verify different types are not equal."""
        self.assertNotEqual(Album("Title"), "Title")

    def test_different(self):
        """Verify different album names are not equal."""
        self.assertNotEqual(Album("Album A"), Album("Album B"))

    def test_years(self):
        """Verify albums with different names, but the same year are not equal."""
        self.assertNotEqual(Album("Album A", 1997), Album("Album B", 1997))


if __name__ == '__main__':
    unittest.main()
