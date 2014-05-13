"""
Integration test for settings on type comparisons.
"""

from enharmony.album import Year


from enharmony.test.test_base import TestCase


class TestYear(TestCase):  # pylint: disable=R0904

    """Tests for Year comparisons."""  # pylint: disable=C0103

    def test_exact(self):
        """Verify comparison between two identical years."""
        a = Year(1987)
        b = Year(1987)
        self.assertComparison(a, b, True, True, 1.00)

    def test_different_by_many(self):
        """Verify comparison between two different years."""
        a = Year(1987)
        b = Year(1979)
        self.assertComparison(a, b, False, False, 0.00)

    def test_different_by_one(self):
        """Verify comparison between two sequential years."""
        a = Year(1987)
        b = Year(1986)
        self.assertComparison(a, b, False, True, 0.50)
