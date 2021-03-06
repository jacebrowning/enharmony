#!/usr/bin/env python

"""
Unit tests for the enharmony.title module.
"""

import unittest
import logging

from enharmony.title import Title
import enharmony.settings as settings


@unittest.skip("not implemented")
class TestParsing(unittest.TestCase):  # pylint: disable=R0904
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
        self.assertEqual('Remix', title.variant)
        self.assertEqual(None, title.featuring)

    def test_live(self):
        """Verify a live title can be parsed."""
        title = Title("Another Song (Live Extended Version)")
        self.assertEqual("Another Song", title.name)
        self.assertEqual(None, title.alternate)
        self.assertEqual('Live', title.variant)
        self.assertEqual(None, title.featuring)

    def test_alternate(self):
        """Verify an alternate title can be parsed."""
        title = Title("The Song Name (For Real)")
        self.assertEqual("The Song Name", title.name)
        self.assertEqual("For Real", title.alternate)
        self.assertEqual(None, title.variant)
        self.assertEqual(None, title.featuring)

    def test_combination(self):
        """Verify a combination song title can be parsed."""
        title = Title("The Song Name (For Real) (Live Version) (feat. Artist B)")
        self.assertEqual("The Song Name", title.name)
        self.assertEqual("For Real", title.alternate)
        self.assertEqual('Live', title.variant)
        self.assertEqual("Artist B", title.featuring)

    def test_combination2(self):
        """Verify a remixed song title can be parsed."""
        title = Title("Song Name (Reprise) [Remix]")
        self.assertEqual("Song Name", title.name)
        self.assertEqual("Reprise", title.alternate)
        self.assertEqual('Remix', title.variant)
        self.assertEqual(None, title.featuring)

    def test_similar_titles(self):
        """Verify titles containing keywords are not accidentally matched."""
        self.assertEqual(None, Title("Song (Alive)").variant)
        self.assertEqual(None, Title("Want to Live").variant)


@unittest.skip("not implemented")
class TestFormatting(unittest.TestCase):  # pylint: disable=R0904
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
        title = Title("Another Song [remix]")
        self.assertEqual("Another Song [Remix]", str(title))
        self.assertEqual(title, eval(repr(title)))

    def test_live(self):
        """Verify a live song can be formatted."""
        title = Title("Another Song (Live)")
        self.assertEqual("Another Song [Live]", str(title))
        self.assertEqual(title, eval(repr(title)))

    def test_alternate(self):
        """Verify an alternate title can be formatted."""
        title = Title("The Song Name (For Real)")
        self.assertEqual("The Song Name (For Real)", str(title))
        self.assertEqual(title, eval(repr(title)))


@unittest.skip("not implemented")
class TestEquality(unittest.TestCase):  # pylint: disable=R0904
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

    def test_featuring(self):
        """Verify featured artists do not matter for comparison."""
        self.assertEqual(Title("Title"), Title("Title (featuring Someone)"))

    @unittest.expectedFailure  # TODO: support parsing bonus tracks
    def test_bonus_track(self):
        """Verify "bonus tracks" are equal."""
        self.assertEqual(Title("Song Title"), Title("Song Title (Bonus Track)"))
        self.assertEqual(Title("Song Title"), Title("Song Title [Bonus Track]"))


@unittest.skip("not implemented")
class TestInequality(unittest.TestCase):  # pylint: disable=R0904
    """Tests for song title inequality."""

    def test_types(self):
        """Verify different types are not equal."""
        self.assertNotEqual(Title("Title"), "Title")

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

    def test_alternate(self):
        """Verify alternate titles do not match."""
        self.assertNotEqual(Title("Song Name (Original)"), Title("Song Name (Reprise)"))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
