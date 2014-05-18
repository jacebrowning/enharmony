"""
Integration test for settings on type comparisons.
"""

from enharmony.album import Year, Kind, Name, Album


from enharmony.test.test_base import TestCase

import sys
import logging
logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestYear(TestCase):  # pylint: disable=R0904

    """Tests for album year comparisons."""  # pylint: disable=C0103

    def test_exact(self):
        """Verify comparison between identical years."""
        a = Year(1987)
        b = Year(1987)
        self.assertComparison(a, b, True, True, 1.00)

    def test_different_by_many(self):
        """Verify comparison between different years."""
        a = Year(1987)
        b = Year(1979)
        self.assertComparison(a, b, False, False, 0.00)

    def test_different_by_one(self):
        """Verify comparison between sequential years."""
        a = Year(1987)
        b = Year(1986)
        self.assertComparison(a, b, False, True, 0.50)

    def test_one_blank(self):
        """Verify comparison between a year and None."""
        a = Year(1987)
        b = Year(None)
        self.assertComparison(a, b, False, True, 1.00)

    def test_both_blank(self):
        """Verify comparison between None and None."""
        a = Year(None)
        b = Year(None)
        self.assertComparison(a, b, True, True, 1.00)


class TestKind(TestCase):  # pylint: disable=R0904

    """Tests for album kind comparisons."""  # pylint: disable=C0103

    def test_exact(self):
        """Verify comparison between identical kinds."""
        a = Kind('EP')
        b = Kind('EP')
        self.assertComparison(a, b, True, True, 1.00)

    def test_different(self):
        """Verify comparison between different kinds."""
        a = Kind('EP')
        b = Kind('Single')
        self.assertComparison(a, b, False, False, 0.00)

    def test_one_blank(self):
        """Verify comparison between a kind and None."""
        a = Kind('EP')
        b = Kind(None)
        self.assertComparison(a, b, False, True, 1.00)

    def test_both_blank(self):
        """Verify comparison between None and None."""
        a = Kind(None)
        b = Kind(None)
        self.assertComparison(a, b, True, True, 1.00)


class TestName(TestCase):  # pylint: disable=R0904

    """Tests for album name comparisons."""  # pylint: disable=C0103

    def test_exact(self):
        """Verify comparison between identical names."""
        a = Name("The White Album")
        b = Name("The White Album")
        self.assertComparison(a, b, True, True, 1.00)

    def test_similar(self):
        """Verify comparison between similar names."""
        a = Name("The White Album")
        b = Name("white album")
        self.assertComparison(a, b, False, True, 1.00)

    def test_differnt(self):
        """Verify comparison between different names."""
        a = Name("The White Album")
        b = Name("Abbey Road")
        self.assertComparison(a, b, False, False, 0.36)

    def test_close(self):
        """Verify comparison between close names."""
        a = Name("American Idiot")
        b = Name("American Pie")
        self.assertComparison(a, b, False, False, 0.79)

    def test_exact_one_kind(self):
        """Verify comparison between identical names (one with kind)."""
        a = Name("My Name Is Skrillex")
        b = Name("My Name Is Skrillex [EP]")
        self.assertComparison(a, b, False, True, 1.00)

    def test_exact_differnt_kind(self):
        """Verify comparison between identical names with different kinds."""
        a = Name("My Name Is Skrillex [Single]")
        b = Name("My Name Is Skrillex [EP]")
        self.assertComparison(a, b, False, False, 0.90)


class TestAlbum(TestCase):  # pylint: disable=R0904

    """Tests for album comparisons."""  # pylint: disable=C0103

    def test_exact(self):
        """Verify comparison between identical albums."""
        a = Album("The White Album")
        b = Album("The White Album")
        self.assertComparison(a, b, True, True, 1.00)

    def test_exact_different_years(self):
        """Verify comparison between identical albums with different years."""
        a = Album("The White Album", year=1999)
        b = Album("The White Album", year=1968)
        self.assertComparison(a, b, False, False, 0.90)

    def test_different_year_different_kind(self):
        """Verify comparison between identical albums with different years."""
        a = Album("Bangarang", kind='EP', year=2011)
        b = Album("Bangarang", kind='Single', year=2012)
        self.assertComparison(a, b, False, False, 0.86)

    def test_same_year_different_kind(self):
        """Verify comparison between identical albums with different years."""
        a = Album("Scary Monsters and Nice Sprites", kind='EP', year=2010)
        b = Album("Scary Monsters and Nice Sprites", kind='Single', year=2010)
        self.assertComparison(a, b, False, False, 0.91)
