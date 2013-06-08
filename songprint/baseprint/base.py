"""
Base class to extended by other song attribute classes.
"""

import re
import logging
from itertools import permutations, combinations, chain
from difflib import SequenceMatcher


class Similarity(object):
    """Represents the similarity between two objects."""

    def __init__(self, value, threshold=1.0):
        self.value = value
        self.threshold = threshold

    def __str__(self):
        return "{:.1%} equal".format(self.value)

    def __cmp__(self, other):
        return cmp(self.value, other.value)

    def __nonzero__(self):
        return self.value >= self.threshold

    def __float__(self):
        return self.value


class _Base(object):
    """Base class defining 'equal' and 'similar' methods.

    Classes wishing to to "comparable" must extend this class and override the
    'EQUALITY_ATTRS' and 'SIMILARITY_ATTRS' attributes. Attributes names
    contained in these tuples must also extend this class.
    """

    THRESHOLD = 0.999  # similarity percent to consider "equal"
    EQUALITY_ATTRS = ('value')  # attribute names to consider for equality
    SIMILARITY_ATTRS = ()  # attribute names,weight to consider for similarity

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        """Maps the '==' operator to be a shortcut for "equality"."""
        return self.equal(other)

    def __ne__(self, other):
        return not (self == other)

    def __mod__(self, other):
        """Maps the '%' operator to be a shortcut for "similarity"."""
        return self.similar(other)

    def fromstring(self, text):
        """Return a new instance parsed from text."""
        raise NotImplementedError()

    def equal(self, other):
        """Compare two objects for equality.
        """
        for name in self.EQUALITY_ATTRS:
            if not hasattr(name, self):
                raise TypeError  # TODO: add message
            if not hasattr(name, self):
                raise TypeError  # TODO: add message
            if getattr(name, self) != getattr(name, other):
                return False
        return True

    def similar(self, other):
        """Compare two objects for similarity.
        """
        logging.debug("comparing {} to {}...".format(repr(self), repr(other)))
        ratio = 0.0
        total = 0.0
        # Calculate similarity ratio
        for name, weight in self.SIMILARITY_ATTRS:
            total += weight
            ratio += weight * getattr(name, self) % getattr(name, other)
        if total:
            ratio *= (1.0 / total)  # scale ratio so the total is 1.0
        else:
            ratio = self._similar(other)  # use the terminal similarity
        return Similarity(ratio, self.THRESHOLD)

    def _repr(self, args):
        """Return representation string from the provided arguments.
        @param args: list of arguments to __init__
        @return: __repr__ string
        """
        while args[-1] is None:  # remove unnecessary empty keywords arguments
            args = args[:-1]
        return self.__class__.__name__ + '(' + ','.join(repr(arg) for arg in args) + ')'

    def _similar(self, other):
        """Terminal comparison when objects have no similarity attributes.
        """
        return float(self == other)


class ComparableNumber(_Base):
    """Comparable positive numerical type."""

    def fromstring(self, text):
        try:
            value = int(text)
        except ValueError:
            try:
                value = float(text)  # might raise ValueError
            except ValueError:
                raise TypeError("unable to convert {0} to {1}".format(repr(text), self.__class__))
        return self.__class__(value)

    def _similar(self, other):
        """Mathematical comparison of numbers."""
        numerator, denominator = sorted((self.value, other.value))
        try:
            return float(numerator) / denominator
        except ZeroDivisionError:
            if not numerator:
                return 1.0
            else:
                return 0.0


class ComparableString(_Base):
    """Represents basic comparable text."""

    def fromstring(self, text):
        return self.__class__(text)

    def _similar(self, other):
        """Fuzzy comparison of text."""
        return SequenceMatcher(a=self.value, b=other.value).ratio()


class ComparableText(ComparableString):
    """Represents comparable text."""

    ARTICLES = 'a', 'an', 'the'
    JOINERS = 'and', '&', '+'

    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.stripped = self._strip_text(self.value)

    def _similar(self, other):
        """Fuzzy comparison of stripped title."""
        return SequenceMatcher(a=self.stripped, b=other.stripped).ratio()

    def _strip_text(self, text):
        """Strip articles/whitespace and remove case."""
        text = text.strip()
        text = text.replace('  ', ' ')  # remove duplicate spaces
        text = text.lower()
        for joiner in self.JOINERS:
            text = text.replace(joiner, 'and')
        for article in self.ARTICLES:
            if text.startswith(article + ' '):
                text = text.replace(article + ' ', '')
                break
        return text


class ComparableTextTitle(ComparableText):
    """Represents comparable text."""

    SIMILARITY_ATTRS = (('prefix', 0.05),
                        ('title', 0.80),
                        ('suffix', 0.15))

    RE_TITLE = re.compile(r"""
    ( \( [^)]+ \) )?  # optional prefix
    ( [^(]+ )         # title
    ( \( [^)]+ \) )?  # optional suffix
    """, re.VERBOSE)

    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.prefix, self.title, self.suffix = self._split_title(self.value)

    def _split_title(self, text):
        """Split a """
        match = self.RE_TITLE.match(text)
        if match:
            return match.groups()
        else:
            raise TypeError("unable to convert {0} to {1}".format(repr(text), self.__class__))







class _(object):
    """Base class for song attribute classes."""

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






