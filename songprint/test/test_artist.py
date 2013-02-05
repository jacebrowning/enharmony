"""
Unit tests for the songprint.artist module.
"""

import unittest

from songprint.artist import Artist


class TestParsing(unittest.TestCase):  # pylint: disable=R0904
    """Tests for parsing artists."""

    def test_nominal(self):
        """Verify a normal artist can be parsed."""
        artist = Artist("The Something")
        self.assertEqual("The Something", artist.name)


class TestFormatting(unittest.TestCase):  # pylint: disable=R0904
    """Tests for formatting artists."""

    def test_nominal(self):
        """Verify a normal artist can be formatted."""
        artist = Artist("The Something")
        self.assertEqual("The Something", str(artist))
        self.assertEqual(artist, eval(repr(artist)))


class TestEquality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for artist equality."""

    def test_exact(self):
        """Verify exact artist name matches are equal."""
        self.assertEqual(Artist("Artist Name"), Artist("Artist Name"))

    def test_case(self):
        """Verify artist name case does not matter."""
        self.assertEqual(Artist("Artist Name"), Artist("Artist name"))

    def test_ands(self):
        """Verify artist "and" operators do not matter."""
        self.assertEqual(Artist("Artist + Others"), Artist("Artist & others"))

    def test_and_order(self):
        """Verify order of multiple artists does not matter."""
        self.skipTest("TODO: support multiple artists")
        self.assertEqual(Artist("Artist + Others"), Artist("Others & Artist"))


class TestInequality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for artist inequality."""

    def test_types(self):
        """Verify different types are not equal."""
        self.assertNotEqual(Artist("Name"), "Name")

    def test_different(self):
        """Verify different artist names are not equal."""
        self.assertNotEqual(Artist("Artist A"), Artist("Artist B"))


if __name__ == '__main__':
    unittest.main()
