"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import combinations
from difflib import SequenceMatcher

from songprint import settings


class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 1.0

    def __eq__(self, other):
        return FuzzyBool(self.similarity(other), self.EQUALITY_PERCENT)

    def __ne__(self, other):
        return not (self == other)

    def _get_repr(self, args):
        """
        Return representation string from the provided arguments.
        """
        while not args[-1]:  # remove unnecessary empty keywords
            args = args[:-1]
        return self.__class__.__name__ + '(' + ','.join(repr(arg) for arg in args) + ')'

    def similarity(self, other):  # pragma: no cover, this method is overwritten by subclasses
        """Calculates percent similar when overwritten by subclasses.
        """
        if type(self) != type(other):
            return 0.0
        else:
            return cmp(self.__dict__, other.__dict__)

    @staticmethod
    def _parse_string(value, kind):
        """Attempt to convert a value to text.

        @param value: value to convert
        @param kind: text to use in logging messages
        """
        try:
            return value.strip()
        except AttributeError:
            logging.debug("could not convert to {kind}: {0}".format(repr(value), kind=kind))
            return None

    @staticmethod
    def _parse_int(value, kind):
        """Attempt to convert a value to a number.

        @param value: value to convert
        @param kind: text to use in logging messages
        @return: the parsed integer or None if unable to parse
        """
        try:
            return int(value)
        except TypeError:
            logging.debug("could not convert to {kind}: {0}".format(repr(value), kind=kind))
            return None
        except ValueError:
            logging.warning("could not convert to {kind}: {0}".format(repr(value), kind=kind))
            return None

    @staticmethod
    def _strip_text(text):  # TODO: is this still needed after fuzzy string comparison is added?
        """Remove the case, strip whitespace/articles, and replace special characters.

        @param text: string to strip
        """
        if text:
            text = text.strip()
            text = text.replace('  ', ' ')  # remove duplicate spaces
            text = text.lower()
            text = text.replace('&', 'and').replace('+', 'and')
            for article in settings.ARTICLES:
                if text.startswith(article):
                    text = text.split(article, 1)[-1].strip()
                    break
            return text
        else:
            return None

    @staticmethod
    def _split_text(text):
        """Split text into the permutations of its parts.
        """

        parts = text.split('(', 1)
        parts = parts[:-1] + parts[-1].rsplit(')')

    @staticmethod
    def _compare_text_options(text1, text2):
        """Compare two strings representing titles with optional portions.
        """
        return 0.0

    @staticmethod
    def _compare_text_list(text1, text2):
        """Compare two strings representing multiple items while ignoring item order.
        """
        return 0.0

    @staticmethod
    def _compare_text(text1, text2):
        """Compare two strings using "fuzzy" comparison.
        """
        return SequenceMatcher(a=text1, b=text2).ratio()


class FuzzyBool(object):

    def __init__(self, value, threshold=1.0):
        self.value = value
        self.threshold = threshold

    def __eq__(self, other):
        if type(other) == type(self):
            return (self.value == other.value) and (self.threshold == other.threshold)
        elif type(other) == bool:
            return bool(self) == other
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "{0}% equal".format(self.value * 100)

    def __nonzero__(self):
        return self.value >= self.threshold

    def __repr__(self):
        return "{name}({value}, threshold={threshold})".format(name=self.__class__.__name__,
                                                               value=self.value,
                                                               threshold=self.threshold)
