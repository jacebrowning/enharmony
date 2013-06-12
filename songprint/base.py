"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import permutations, combinations, chain
from difflib import SequenceMatcher


class Base(object):
    """Shared base class."""

    def _repr(self, *args):
        """Return representation string from the provided arguments.
        @param args: list of arguments to __init__
        @return: __repr__ string
        """
        while args[-1] is None:  # remove unnecessary empty keywords arguments
            args = args[:-1]
        return self.__class__.__name__ + '(' + ','.join(repr(arg) for arg in args) + ')'


class Similarity(Base):  # pylint: disable=R0903
    """Represents the similarity between two objects."""

    def __init__(self, value, threshold=1.0):
        self.value = value
        self.threshold = threshold

    def __str__(self):
        return "{:.1%} equal".format(self.value)

    def __repr__(self):
        return self._repr(self.value, self.threshold)

    def __cmp__(self, other):
        return cmp(float(self), float(other))

    def __nonzero__(self):
        return self.value >= self.threshold

    def __float__(self):
        return self.value


class Comparable(Base):
    """Base class for objects that are comparable.

    Subclasses directly comparable should override the 'similar' method to
    return 'Similarity' object between the two compared objects.

    Subclasses comparable by attributes should override the 'EQUALITY_ATTRS' and
    'SIMILARITY_ATTRS' tuples to define which attributes should be considered.
    Attributes names contained in these tuples must also extend this class.
    """

    THRESHOLD = 1.0  # similarity percent to consider "equal"
    EQUALITY_ATTRS = ('value',)  # attribute names to consider for equality
    SIMILARITY_ATTRS = (('value', 1.0),)  # attribute names,weight to consider for similarity

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self._repr(self.value)

    def __eq__(self, other):
        """Maps the '==' operator to be a shortcut for "equality"."""
        return self.equal(other)

    def __ne__(self, other):
        return not (self == other)

    def __mod__(self, other):
        """Maps the '%' operator to be a shortcut for "similarity"."""
        return self.similar(other)

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        raise NotImplementedError()

    def equal(self, other):
        """Compare two objects for equality.
        """
        for name in self.EQUALITY_ATTRS:
            if not hasattr(self, name):
                raise TypeError  # TODO: add message
            if not hasattr(self, name):
                raise TypeError  # TODO: add message
            if getattr(self, name) != getattr(other, name):
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
        return Similarity(ratio, self.THRESHOLD)


class Number(Comparable):
    """Comparable positive numerical type."""

    @staticmethod
    def fromstring(text):
        """Try to convert text to an int or float."""
        try:
            value = int(text)
        except ValueError:
            try:
                value = float(text)  # might raise ValueError
            except ValueError:
                raise TypeError("unable to convert {0} to {1}".format(repr(text), Number))
        return Number(value)

    def similar(self, other):
        """Mathematical comparison of numbers."""
        numerator, denominator = sorted((self.value, other.value))
        try:
            ratio = float(numerator) / denominator
        except ZeroDivisionError:
            ratio = 0.0 if numerator else 1.0
        return Similarity(ratio, self.THRESHOLD)


class Text(Comparable):
    """Represents basic comparable text."""

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return Text("")
        else:
            return Text(text)

    def similar(self, other):
        """Fuzzy comparison of text."""
        ratio = SequenceMatcher(a=self.value, b=other.value).ratio()
        return Similarity(ratio, self.THRESHOLD)


class TextName(Text):
    """Represents comparable text."""

    ARTICLES = 'a', 'an', 'the'
    JOINERS = 'and', '&', '+'

    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.stripped = self._strip_text(self.value)

    def similar(self, other):
        """Fuzzy comparison of stripped title."""
        ratio = SequenceMatcher(a=self.stripped, b=other.stripped).ratio()
        return Similarity(ratio, self.THRESHOLD)

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


class TextTitle(Comparable):
    """Represents comparable text."""

    SIMILARITY_ATTRS = (('prefix', 0.05),
                        ('title', 0.80),
                        ('suffix', 0.15))

#     RE_TITLE = re.compile(r"""
#     ( \( [^)]+ \) )?  # optional prefix
#     ( [^(]+ )         # title
#     ( \( [^)]+ \) )?  # optional suffix
#     """, re.VERBOSE)

    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.prefix, self.title, self.suffix = self._split_title(self.value)

    def __str__(self):
        text = self.title
        if self.prefix:
            text = "({0}) ".format(self.prefix) + text
        if self.suffix:
            text = text + " ({0})".format(self.suffix)

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return Text("")
        else:
            return Text(text)

    def _split_title(self, text):
        """Split a title into parts."""
        prefix = suffix = None
        text = text.strip().strip("()")
        if ')' in text:
            prefix, text = text.split(')')
        if '(' in text:
            text, suffix = text.split('(')
        return TextName(prefix), TextName(suffix), TextName(suffix)


#     def _split_title(self, text):
#         """Split a title into parts."""
#         match = self.RE_TITLE.match(text)
#         if match:
#             return match.groups()
#         else:
#             raise TypeError("unable to convert {0} to {1}".format(repr(text), self.__class__))

    ###########
    @staticmethod
    def _split_text_title(text):
        """Split text into its optional and required parts.
        """
        parts = text.replace(')', '(').split('(')
        return [part.strip("() ") for part in parts if part.strip("() ")]

    @staticmethod
    def _compare_text_titles(text1, text2):
        """Compare two strings representing titles with optional portions.
        """
        best_ratio = 0.0
        parts1 = TextTitle._split_text_title(text1)
        parts2 = TextTitle._split_text_title(text2)
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




class TextList(Comparable):
    """Represents comparable text."""


    ###########
    @staticmethod
    def _split_text_list(text):
        """Strip joining words and split text into list.
        """
        for word in settings.JOINERS:
            text = text.replace(word, ',')
        text = text.replace(', ', ',').replace(',,', ',')
        return [part.strip(", ") for part in text.split(',') if part.strip(", ")]



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




