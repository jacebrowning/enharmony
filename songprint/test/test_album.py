"""
Unit tests for the songprint.album module.
"""

import unittest

from songprint.base import Text, TextEnum, TextName, TextTitle, TextList
from songprint.album import Album, Year


class TestParsing(unittest.TestCase):  # pylint: disable=R0904
    """Tests for parsing album names."""

    def test_nominal(self):
        """Verify a normal album name can be parsed."""
        album = Album("Album Name")
        self.assertEqual(TextTitle("Album Name"), album.name)
        self.assertEqual(None, album.kind)
        self.assertEqual(None, album.featuring)

    def test_ep(self):
        """Verify an EP can be parsed."""
        album = Album("Tracks (feat. The Artist) [EP]")
        self.assertEqual(TextTitle("Tracks"), album.name)
        self.assertEqual(TextEnum("EP"), album.kind)
        self.assertEqual(TextList("The Artist"), album.featuring)


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


class TestComparison(unittest.TestCase):  # pylint: disable=R0904
    """Tests for album comparison."""

    def assertComparison(self, obj1, obj2, equal, similar, ratio):
        equality = obj1 == obj2
        similarity = obj1 % obj2
        self.assertEqual(equal, equality)
        self.assertEqual(similar, bool(ratio))
        self.assertEqual(ratio, similarity)

    def test_exact(self):
        """Verify comparison between two identical albums."""
        self.assertComparison(Album("Album Name"), Album("Album Name"), True, True, 1.0)

    def test_extra(self):
        """Verify albums with extra text are still equal."""
        self.assertEqual(Album("Album Name"), Album("Album Name (Bonus Tracks)"))
        self.assertEqual(Album("Album Name"), Album("Album Name (Deluxe)"))

    def test_years_1(self):
        """Verify albums with the same name, but different years are equal."""
        self.assertEqual(Album("Album A", 1997), Album("Album A", 1998))

    def test_years_2(self):
        """Verify albums with the same year, but slightly different names are equal."""
        self.assertEqual(Album("This is the album title", 2013), Album("This is th' album title", 2013))

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
