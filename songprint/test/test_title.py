#!/usr/bin/env python

"""
Unit tests for the songprint.title module.
"""

import unittest

from songprint.title import Title

class TestParsing(unittest.TestCase):
    """Tests for parsing song titles."""

    def test_nominal(self):
        """Verify a normal title can be parsed."""
        title = Title("The Song Name")
        self.assertEqual("The Song Name", title.name)
        self.assertEqual(None, title.alternate)
        self.assertEqual(None, title.variant)
        self.assertEqual(None, title.featuring)

    def test_featuring(self):
        """Verify a song with a featured artist can be parsed."""
        title = Title("Song Title (feat. Artist B)")
        self.assertEqual("Song Title", title.name)
        self.assertEqual(None, title.alternate)
        self.assertEqual(None, title.variant)
        self.assertEqual("Artist B", title.featuring)

    def test_remix(self):
        """Verify a remix can be parsed."""
        title = Title("Another Song [Super Remix]")
        self.assertEqual("Another Song", title.name)
        self.assertEqual(None, title.alternate)
        self.assertEqual('remix', title.variant)
        self.assertEqual(None, title.featuring)

    def test_live(self):
        """Verify a remix can be parsed."""
        title = Title("Another Song (Live Extended Version)")
        self.assertEqual("Another Song", title.name)
        self.assertEqual(None, title.alternate)
        self.assertEqual('live', title.variant)
        self.assertEqual(None, title.featuring)


class TestFormatting(unittest.TestCase):
    """Tests for formatting song titles."""

    def test_nominal(self):
        """Verify a normal title can be formatted."""
        title = Title("The Song Name")
        self.assertEqual("The Song Name", str(title))
        self.assertEqual(title, eval(repr(title)))

    def test_featuring(self):
        """Verify a song with a featured artist can be formatted."""
        title = Title("Song Title (feat. Artist B)")
        self.assertEqual("Song Title", str(title))
        self.assertEqual(title, eval(repr(title)))

    def test_remix(self):
        """Verify a remix can be formatted."""
        title = Title("Another Song [Remix]")
        self.assertEqual("Another Song [Remix]", str(title))
        self.assertEqual(title, eval(repr(title)))

    def test_live(self):
        """Verify a live song can be formatted."""
        title = Title("Another Song (Live)")
        self.assertEqual("Another Song [Live]", str(title))
        self.assertEqual(title, eval(repr(title)))


class TestEquality(unittest.TestCase):
    """Tests for song title equality."""

    def test_exact(self):
        """Verify exact song title matches are equal."""
        self.assertEqual(Title("Song Title"), Title("Song Title"))
        self.assertEqual(Title(""), Title(""))

    def test_case(self):
        """Verify song title case does not matter."""
        self.assertEqual(Title("Song Title"), Title("Song title"))

    def test_articles(self):
        """Verify articles are ignored when compare song titles."""
        self.assertEqual(Title("The song name"), Title("Song  Name"))

    def test_remixes(self):
        """Verify similarly labeled song title remixes are equal."""
        self.assertEqual(Title("Title (remix)"), Title("Title [Remix]"))
        self.assertEqual(Title("Title [Remix]"), Title("Title (Dubstep Remix)"))

    def test_title_articles(self):
        """Verify song titles with missing articles are matched."""
        self.assertEqual(Title("The Song Name"), Title("Song Name"))

    def test_featuring(self):
        """Verify featured artists do not matter for comparison."""
        self.assertEqual(Title("Title"), Title("Title (featuring Someone)"))


class TestInequality(unittest.TestCase):
    """Tests for song title inequality."""

    def test_different(self):
        """Verify different song titles are not equal."""
        self.assertNotEqual(Title("Title A"), Title("Title B"))

    def test_live(self):
        """Verify a live song title does not match the original."""
        self.assertNotEqual(Title("Title"), Title("Title [Live]"))
        self.assertNotEqual(Title("Title"), Title("Title (live)"))

    def test_live_remix(self):
        """Verify a live remix does match a normal remix."""
        self.assertNotEqual(Title("Song Name [Remix]"), Title("Song Name (Live Remix)"))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_MESSAGE, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
