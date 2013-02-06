"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import permutations, combinations, chain
from difflib import SequenceMatcher

from songprint import settings


class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 1.0

    def __eq__(self, other):
        return FuzzyBool(self.similarity(other), self.EQUALITY_PERCENT)

    def __ne__(self, other):
        return not (self == other)

    def similarity(self, other):  # pragma: no cover, this method is overwritten by subclasses
        """Calculates percent similar when overwritten by subclasses.
        """
        if type(self) != type(other):
            return 0.0
        else:
            return cmp(self.__dict__, other.__dict__)

    def _get_repr(self, args):
        """
        Return representation string from the provided arguments.
        """
        while not args[-1]:  # remove unnecessary empty keywords arguments
            args = args[:-1]
        return self.__class__.__name__ + '(' + ','.join(repr(arg) for arg in args) + ')'

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
    def _split_text_title(text):
        """Split text into its optional and required parts.
        """
        parts = text.replace(')', '(').split('(')
        return [part.strip("() ") for part in parts if part.strip("() ")]

    @staticmethod
    def _split_text_list(text):
        """Strip joining words and split text into list.
        """
        for word in settings.JOINERS:
            text = text.replace(word, ',')
        text = text.replace(', ', ',').replace(',,', ',')
        return [part.strip(", ") for part in text.split(',') if part.strip(", ")]

    @staticmethod
    def _compare_text_titles(text1, text2):
        """Compare two strings representing titles with optional portions.
        """
        best_ratio = 0.0
        parts1 = Base._split_text_title(text1)
        parts2 = Base._split_text_title(text2)
        combos1 = set(chain(*(combinations(parts1, r) for r  in range(len(parts1)))))
        combos2 = set(chain(*(combinations(parts2, r) for r  in range(len(parts2)))))
        for combo1 in combos1:
            for combo2 in combos2:
                ratio = Base._compare_text(', '.join(combo1), ', '.join(combo2))
                if ratio > best_ratio:
                    logging.debug("{0} ? {1} = {2}".format(combo1, combo2, ratio))
                    best_ratio = ratio
                    if best_ratio == 1.0:
                        break
        return best_ratio

    @staticmethod
    def _compare_text_lists(text1, text2):
        """Compare two strings representing multiple items while ignoring item order.
        """
        best_ratio = 0.0
        parts1 = Base._split_text_list(text1)
        parts2 = Base._split_text_list(text2)
        combos1 = set(permutations(parts1, len(parts1)))
        combos2 = set(permutations(parts2, len(parts2)))
        for combo1 in combos1:
            for combo2 in combos2:
                ratio = Base._compare_text(', '.join(combo1), ', '.join(combo2))
                if ratio > best_ratio:
                    logging.debug("{0} ? {1} = {2}".format(combo1, combo2, ratio))
                    best_ratio = ratio
                    if best_ratio == 1.0:
                        break
        return best_ratio

    @staticmethod
    def _compare_text(text1, text2):
        """Compare two strings using "fuzzy" comparison with disregard for case.
        """
        return SequenceMatcher(a=text1.lower(), b=text2.lower()).ratio()


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
