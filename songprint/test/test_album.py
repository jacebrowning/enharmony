"""
Unit tests for the songprint.album module.
"""

import unittest
import logging

from songprint.base import Text, TextEnum, TextName, TextTitle, TextList
from songprint.album import Album, Year
from songprint import settings

from songprint.test.test_base import TestCase


class TestParsing(TestCase):  # pylint: disable=R0904
    """Tests for parsing album names."""

    def test_nominal(self):
        """Verify a normal album name can be parsed."""
        album = Album("Album Name")
        self.assertEqual(TextTitle("Album Name"), album.name)
        self.assertEqual(None, album.year)
        self.assertEqual(None, album.kind)
        self.assertEqual(None, album.featuring)
        self.assertEqual("Album Name", str(album))
        # self.assertEqual(album, eval(repr(album)))

    def test_year(self):
        """Verify a normal album name can be formatted."""
        album = Album("Album Name", 1990)
        self.assertEqual(Year(1990), album.year)
        self.assertEqual("Album Name", str(album))
        # self.assertEqual(album, eval(repr(album)))

    def test_ep(self):
        """Verify an EP can be parsed."""
        album = Album("Tracks (feat. The Artist) [EP]")
        self.assertEqual(TextTitle("Tracks"), album.name)
        self.assertEqual(TextEnum("EP"), album.kind)
        self.assertEqual(TextList("The Artist"), album.featuring)
        self.assertEqual("Tracks [EP]", str(album))
        # self.assertEqual(album, eval(repr(album)))

    def test_single(self):
        """Verify a single can be formatted."""
        album = Album("One Hit [Single]")
        self.assertEqual("One Hit [Single]", str(album))
        # self.assertEqual(album, eval(repr(album)))


class TestComparison(TestCase):  # pylint: disable=R0904
    """Tests for album comparison."""

    def test_exact(self):
        """Verify comparison between two identical albums."""
        self.assertComparison(Album("Album Name"),
                              Album("Album Name"),
                              True, 1.00)

    def test_one_suffix(self):
        """Verify comparison between an album with and without a suffix."""
        self.assertComparison(Album("Album Name"),
                              Album("Album Name (Bonus Tracks)"),
                              False, 0.85)

    def test_one_prefix(self):
        """Verify comparison between an album with and without a prefix."""
        self.assertComparison(Album("(What's the Story) Morning Glory?"),
                              Album("Morning Glory"),
                              False, 0.92)

    def test_different_suffixes(self):
        """Verify comparison between two albums with different suffixes."""
        self.assertComparison(Album("Album Name (ABC)"),
                              Album("Album Name (DEF)"),
                              False, 0.85)

    def test_same_name_different_year(self):
        """Verify comparison between the same album with (+-1) different years. """
        self.assertComparison(Album("Album A", 1997),
                              Album("Album A", 1998),
                              False, 0.95)

    def test_same_name_different_year_2(self):
        """Verify comparison between the same album with (+-2) different years. """
        self.assertComparison(Album("Album A", 1996),
                              Album("Album A", 1998),
                              False, 0.90)

    def test_different_name_same_year(self):
        """Verify comparison between albums with the same year, but slightly different names."""
        self.assertComparison(Album("This is the album title", 2013),
                              Album("This is th' album title", 2013),
                              False, 0.97)

    def test_different_types(self):
        """Verify comparison between objects of different types."""
        self.assertComparison(Album("Title"),
                              "Title",
                              False, 0.00)

    def test_similar_names(self):
        """Verify comparison between similar album names."""
        self.assertComparison(Album("Album A"),
                              Album("Album B"),
                              False, 0.89)

    def test_smilar_names_same_years(self):
        """Verify comparison between albums with different names, but the same year."""
        self.assertComparison(Album("Album A", 1997),
                              Album("Album B", 1997),
                              False, 0.90)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
