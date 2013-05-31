"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import permutations, combinations, chain
from difflib import SequenceMatcher

from songprint import settings


class _Base(object):
    """Base class defining 'equal' and 'similar' methods.

    Classes wishing to to "comparable" must extend this class and override the
    'EQUALITY_ATTRS' and 'SIMILARITY_ATTRS' attributes. Attributes names
    contained in these tuples must also extend this class.
    """

    THRESHOLD = 0.999  # similarity percent to consider "equal"
    EQUALITY_ATTRS = ()  # attribute names to consider for equality
    SIMILARITY_ATTRS = ()  # attribute names,weight to consider for similarity

    def __eq__(self, other):
        """Maps the '==' operator to be a shortcut for "equality"."""
        return self.equal(other)

    def __ne__(self, other):
        return not (self == other)

    def __mod__(self, other):
        """Maps the '%' operator to be a shortcut for "similarity"."""
        return self.similar(other)

    def equal(self, other):
        for name in self.EQUALITY_ATTRS:
            if not hasattr(name, self):
                raise TypeError  # TODO: add message
            if not hasattr(name, self):
                raise TypeError  # TODO: add message
            if getattr(name, self) != getattr(name, other):
                return False
        return True

    def similar(self, other):
        logging.debug("comparing {} to {}...".format(repr(self), repr(other)))
        ratio = 0.0
        total = 0.0
        # Calculate similarity ratio
        for name, weight in self.SIMILARITY_ATTRS:
            total += weight
            ratio += weight * getattr(name, self) % getattr(name, other)
        # Scale ratio so the total is 1.0
        if total:
            ratio *= (1.0 / total)
        return FuzzyBool(radio, self.THRESHOLD)








class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 0.999

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
            return self._average_similarity([(self.__dict__[key],
                                              other.__dict__[key],
                                              1.0, None) for key in self.__dict__])

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
        len1 = len(parts1)
        len2 = len(parts2)
        logging.debug("parts 1: {0}".format(parts1))
        logging.debug("parts 2: {0}".format(parts2))
        combos1 = set(chain(*(combinations(parts1, r) for r in range(min(len1, len2), len1 + 1))))
        combos2 = set(chain(*(combinations(parts2, r) for r in range(min(len1, len2), len2 + 1))))
        for combo1 in combos1:
            for combo2 in combos2:
                ratio = Base._compare_text(' '.join(combo1), ' '.join(combo2))
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

    @staticmethod
    def _average_similarity(data):
        """Calculates of weighted average of similarity based on a sequence of (item1, item2, weight).
        """
        ratio = 0.0
        total = 0.0
        # Calculate similarity ratio
        for item1, item2, weight, function in data:
            if None not in (item1, item2):
                total += weight
                if function:
                    ratio += weight * float(function(item1, item2))
                else:
                    ratio += weight * float(item1 == item2)
        # Scale ratio so the total is 1.0
        if total:
            ratio *= (1.0 / total)
        return ratio


class FuzzyBool(object):
    """
    Multipurpose return value for '__eq__' and '__ne__' to allow for similarity comparisons.

    This object is evaluated True/False in boolean expressions and a floating point in all others.
    """

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
        return "{:.1%} equal".format(self.value)

    def __nonzero__(self):
        return self.value >= self.threshold

    def __float__(self):
        return self.value

    def __repr__(self):
        return "{name}({value}, threshold={threshold})".format(name=self.__class__.__name__,
                                                               value=self.value,
                                                               threshold=self.threshold)
