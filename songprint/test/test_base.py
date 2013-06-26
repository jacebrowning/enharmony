#!/usr/bin/env python

"""
Unit tests for the songprint.base module.
"""

import unittest
import logging

from songprint.base import Base, Similarity, Comparable
from songprint.base import Number, Text, TextName, TextTitle, TextList
from songprint import settings


class TestCase(unittest.TestCase):  # pylint: disable=R0904
    """Common test case class with new assertion methods."""  # pylint: disable=C0103

    def assertComparison(self, obj1, obj2, expected_equality, expected_similarity):  # pylint:disable=R0913
        """Fail if objects do not match the expected equality and similarity.
        """
        logging.info("calculating equality...")
        equality = obj1 == obj2
        logging.info("calculating similarity...")
        similarity = obj1 % obj2
        logging.info("checking expected results...")
        self.assertEqual(expected_equality, equality)
        self.assertAlmostEqual(expected_similarity, similarity, 2)


class TestBase(TestCase):  # pylint: disable=R0904
    """Tests for the Base class."""

    class Sample(Base):  # pylint: disable=R0903
        """Test class to show __repr__ formatting."""

        def __init__(self, arg1, arg2, kwarg1=None, kwarg2=None):
            self.arg1 = arg1
            self.arg2 = arg2
            self.kwarg1 = kwarg1
            self.kwarg2 = kwarg2

        def __repr__(self):
            return self._repr(self.arg1, self.arg2, kwarg1=self.kwarg1, kwarg2=self.kwarg2)

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return self.__dict__ != other.__dict__

    def test_repr_all_args(self):
        """Verify a class with arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc', 456, 'def')
        self.assertEqual(sample, eval(repr(sample)))

    def test_repr_no_kwargs(self):
        """Verify a class with no keyword arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc')
        self.assertEqual(sample, eval(repr(sample)))

    def test_repr_empty_args(self):
        """Verify a class with empty keyword arguments is represented."""
        Sample = self.Sample  # pylint: disable=C0103
        sample = Sample(123, 'abc', None, kwarg2=None)
        self.assertEqual(sample, eval(repr(sample)))


class TestSimilarity(unittest.TestCase):  # pylint: disable=R0904
    """Tests for the Similarity class."""

    def test_str(self):
        """Verify similarity objects can be represented as strings."""
        self.assertEqual("100.0% similar", str(Similarity(1.0)))
        self.assertEqual("99.0% similar", str(Similarity(0.99)))
        self.assertEqual("0.0% similar", str(Similarity(0.0)))

    def test_repr(self):
        """Verify object representation works for similarity objects."""
        sim = Similarity(0.89, threshold=0.87)
        self.assertEqual(sim, eval(repr(sim)))

    def test_bool_true(self):
        """Verify a similarity of 1.0 is True."""
        self.assertTrue(Similarity(1.0))

    def test_bool_false(self):
        """Verify a similarity of <1.0 if False."""
        self.assertFalse(Similarity(0.99))

    def test_bool_true_with_threshold(self):
        """Verify a similarity of <1.0 is True with a threshold."""
        self.assertTrue(Similarity(0.89, threshold=0.88))

    def test_bool_false_with_threshold(self):
        """Verify a similarity is False if under the threshold."""
        self.assertFalse(Similarity(0.89, threshold=0.90))

    def test_float_equal(self):
        """Verify similarities and floats can be compared for equality."""
        self.assertEqual(Similarity(0.42), 0.42)

    def test_float_not_equal(self):
        """Verify similarities and floats can be compared for inequality."""
        self.assertNotEqual(0.12, Similarity(0.13))

    def test_add(self):
        """Verify two similarities can be added."""
        self.assertEqual(Similarity(0.42), Similarity(0.4) + Similarity(0.02))

    def test_add_with_number(self):
        """Verify a number can be added to a similarity."""
        self.assertEqual(Similarity(0.42), Similarity(0.4) + 0.02)

    def test_iadd(self):
        """Verify a similarity can be added to."""
        similarity = Similarity(0.4)
        similarity += Similarity(0.02)
        self.assertEqual(Similarity(0.42), similarity)

    def test_iadd_with_number(self):
        """Verify a similarity can be added to by a number."""
        similarity = Similarity(0.4)
        similarity += 0.02
        self.assertEqual(Similarity(0.42), similarity)

    def test_radd_with_number(self):
        """Verify a similarity can be added to a number."""
        self.assertEqual(Similarity(0.42), 0.4 + Similarity(0.02))

    def test_mul(self):
        """Verify two similarities can be multiplied."""
        self.assertEqual(Similarity(0.42), Similarity(0.6) * Similarity(0.7))

    def test_mul_with_number(self):
        """Verify a number can be multiplied with a similarity."""
        self.assertEqual(Similarity(0.42), Similarity(0.6) * 0.7)

    def test_imul(self):
        """Verify a similarity can be multiplied to."""
        similarity = Similarity(0.6)
        similarity *= Similarity(0.7)
        self.assertEqual(Similarity(0.42), similarity)

    def test_imul_with_number(self):
        """Verify a similarity can be multiplied to by a number."""
        similarity = Similarity(0.6)
        similarity *= 0.7
        self.assertEqual(Similarity(0.42), similarity)

    def test_rmul_with_number(self):
        """Verify a similarity can multiplied with a number."""
        self.assertEqual(Similarity(0.42), 0.6 * Similarity(0.7))


class TestComparable(TestCase):  # pylint: disable=R0904
    """Tests for the BaseComparable class."""

    def test_str(self):
        """Verify base comparable objects can be represented as strings."""
        self.assertEqual("abc", str(Comparable("abc")))

    def test_repr(self):
        """Verify object representation works for base comparable objects."""
        obj = Comparable(42)
        self.assertEqual(obj, eval(repr(obj)))

    def test_eq_true(self):
        """Verify base comparable objects can be compared for equality."""
        self.assertEqual(Comparable("hello world"), Comparable("hello world"))

    def test_eq_false(self):
        """Verify base comparable objects can be compared for inequality."""
        self.assertNotEqual(Comparable("hello world"), Comparable("hello world!"))


class TestNumber(TestCase):  # pylint: disable=R0904
    """Tests for the Number class."""

    def test_fromstring_int(self):
        """Verify an integer number can be created from string."""
        self.assertEqual(42, Number.fromstring("42 ").value)

    def test_fromstring_float(self):
        """Verify a float number can be created from a string."""
        self.assertEqual(1.23, Number.fromstring(" 1.230").value)

    def test_similar_zeros(self):
        """Verify zeros are similar."""
        similarity = Number(0) % Number(0.0)
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_one_zero(self):
        """Verify zero is not similar to other numbers."""
        similarity = Number(42) % Number(0)
        self.assertFalse(similarity)
        self.assertEqual(0.0, similarity)

    def test_similar_false(self):
        """Verify two different numbers are not similar."""
        similarity = Number(3.0) % Number(2)
        self.assertFalse(similarity)
        self.assertGreater(0.67, similarity)

    def test_similar_true(self):
        """Verify two equal numbers are similar."""
        similarity = Number(3.0) % Number(3)
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)


class TestText(TestCase):  # pylint: disable=R0904
    """Tests for the Text class."""

    def test_fromstring_int(self):
        """Verify a string can be created from string."""
        self.assertEqual("42 ", Text.fromstring("42 ").value)

    def test_fromstring_float(self):
        """Verify a string can be created from a string."""
        self.assertEqual(" 1.230", Text.fromstring(" 1.230").value)

    def test_similar_unequal(self):
        """Verify two different strings are not similar."""
        similarity = Text("abc") % Text("bcd")
        self.assertFalse(similarity)
        self.assertGreater(0.67, similarity)

    def test_similar_equal(self):
        """Verify two equal strings are similar."""
        similarity = Text("abc") % Text("abc")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)


class TestTextName(TestCase):  # pylint: disable=R0904
    """Tests for the TextName class."""

    def test_stripped_case(self):
        """Verify a name is stripped of case."""
        self.assertEqual("hello, world!", TextName("Hello,  World!").stripped)

    def test_stripped_joiner(self):
        """Verify the joiners in a name are replaced."""
        self.assertEqual("a and b", TextName("The A & B").stripped)

    def test_stripped_articles(self):
        """Verify a name is stripped of articles."""
        self.assertEqual("song", TextName(" the song ").stripped)

    def test_similar_unequal(self):
        """Verify two different text names are not similar."""
        similarity = TextName("abc") % TextName("bcd")
        self.assertFalse(similarity)
        self.assertGreater(0.67, similarity)

    def test_similar_equal(self):
        """Verify two equal text names are similar."""
        similarity = TextName("abc") % TextName("abc")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_close(self):
        """Verify two close text names are similar."""
        similarity = TextName("The song") % TextName("song")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)


class TestTextTitle(TestCase):  # pylint: disable=R0904
    """Tests for the TextTitle class."""

    def test_parse_title(self):
        """Verify a text title is parsed."""
        title = TextTitle("The Song Name ")
        self.assertEqual("", str(title.prefix))
        self.assertEqual("The Song Name", str(title.title))
        self.assertEqual("", str(title.suffix))
        self.assertEqual("The Song Name", str(title))

    def test_parse_title_suffix(self):
        """Verify a text title with a suffix is parsed."""
        title = TextTitle("The Song Name  (Original)")
        self.assertEqual("", str(title.prefix))
        self.assertEqual("The Song Name", str(title.title))
        self.assertEqual("Original", str(title.suffix))
        self.assertEqual("The Song Name (Original)", str(title))

    def test_parse_prefix_title(self):
        """Verify a text title with a prefix is parsed."""
        title = TextTitle("  (The Song) Name")
        self.assertEqual("The Song", str(title.prefix))
        self.assertEqual("Name", str(title.title))
        self.assertEqual("", str(title.suffix))
        self.assertEqual("(The Song) Name", str(title))

    def test_parse_prefix_title_suffix(self):
        """Verify a text title with a prefix and suffix is parsed."""
        title = TextTitle("(The Song) Name  (Original)")
        self.assertEqual("The Song", str(title.prefix))
        self.assertEqual("Name", str(title.title))
        self.assertEqual("Original", str(title.suffix))
        self.assertEqual("(The Song) Name (Original)", str(title))

    def test_similar_unequal(self):
        """Verify two different text titles are not similar."""
        similarity = TextTitle("The Song Name") % TextTitle("A Different Song Name")
        self.assertFalse(similarity)
        self.assertGreater(0.72, similarity)

    def test_similar_equal(self):
        """Verify two equal text titles are similar."""
        similarity = TextName("The Song Name") % TextName("The Song Name")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_close(self):
        """Verify two close text titles are similar."""
        similarity = TextName("This is the song name") % TextName("(this) is the song name.")
        self.assertTrue(similarity)
        self.assertLess(0.93, similarity)


class TestTextList(TestCase):  # pylint: disable=R0904
    """Tests for the TextList class."""

    def test_parse_list_with_and(self):
        """Verify a 3-item text list is parsed."""
        lst = TextList("This, That, and  the Other ")
        self.assertEqual((TextName("This"), TextName("That"), TextName("the Other")), lst.items)
        self.assertEqual("This, That, the Other", str(lst))

    def test_parse_pair(self):
        """Verify a 2-item text list is parsed."""
        lst = TextList(" Something &  This Thing")
        self.assertEqual((TextName("Something"), TextName("This Thing")), lst.items)
        self.assertEqual("Something, This Thing", str(lst))

    def test_similar_unequal(self):
        """Verify two different text lists are not similar."""
        similarity = TextList("This, That, and  the Other ") % TextList("This Other Thing & One")
        self.assertFalse(similarity)
        self.assertGreater(0.31, similarity)

    def test_similar_equal(self):
        """Verify two equal text lists are similar."""
        similarity = TextList("This + That") % TextList("This + That")
        self.assertTrue(similarity)
        self.assertEqual(1.0, similarity)

    def test_similar_close(self):
        """Verify two close text lists are similar."""
        similarity = TextList("This, That, and  the Other ") % TextList("That, This &  the Other ")
        self.assertTrue(similarity)
        self.assertLess(0.99, similarity)


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
