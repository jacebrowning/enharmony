"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import permutations, combinations, chain
from difflib import SequenceMatcher


def equal(obj1, obj2):
    logging.debug("calculating {} == {}...".format(repr(obj1), repr(obj2)))
    equality = obj1.__equal__(obj2)
    logging.debug("equality: {}".format(equality))
    return equality


def similar(obj1, obj2):
    logging.debug("calculating {} % {}...".format(repr(obj1), repr(obj2)))
    similarity = obj1.__similar__(obj2)
    logging.debug("similarity: {}".format(similarity))
    return similarity


class Base(object):
    """Shared base class."""

    def _repr(self, *args, **kwargs):
        """Return representation string from the provided arguments.
        @param args: list of arguments to __init__
        @param kwarks: dictionary of keyword arguments to __init__
        @return: __repr__ string
        """
        # Remove unnecessary empty arguments
        while args[-1] is None:
            args = args[:-1]
        # Remove unnecessary empty keywords arguments
        for key, value in kwargs.items():
            if value is None:
                del kwargs[key]
        # Return the __repr__ string
        args_repr = ', '.join(repr(arg) for arg in args)
        kwargs_repr = ', '.join(k + '=' + repr(v) for k, v in kwargs.items())
        if args_repr and kwargs_repr:
            kwargs_repr = ', ' + kwargs_repr
        return "{}({}{})".format(self.__class__.__name__, args_repr, kwargs_repr)


class Similarity(Base):  # pylint: disable=R0903
    """Represents the similarity between two objects."""

    def __init__(self, value, threshold=1.0):
        self.value = value
        self.threshold = threshold

    def __repr__(self):
        return self._repr(self.value, threshold=self.threshold)

    def __str__(self):
        return "{:.1%} similar".format(self.value)

    def __eq__(self, other):
        return abs(float(self) - float(other)) < 0.001

    def __ne__(self, other):
        return not self == other

    def __cmp__(self, other):
        return cmp(float(self), float(other))

    def __nonzero__(self):
        return self.value >= self.threshold

    def __float__(self):
        return self.value

    def __add___(self, other):
        return Similarity(self.value + float(other), threshold=self.threshold)

    def __radd__(self, other):
        return Similarity(self.value + float(other), threshold=self.threshold)

    def __iadd__(self, other):
        self.value += float(other)
        return self

    def __mul__(self, other):
        return Similarity(self.value * float(other), threshold=self.threshold)

    def __rmul__(self, other):
        return Similarity(self.value * float(other), threshold=self.threshold)

    def __imul__(self, other):
        self.value *= float(other)
        return self


class Comparable(Base):
    """Base class for objects that are comparable.

    Subclasses directly comparable should override the 'similar' method to
    return 'Similarity' object between the two compared objects.

    Subclasses comparable by attributes should override the 'EQUALITY_ATTRS' and
    'SIMILARITY_ATTRS' tuples to define which attributes should be considered.
    Attributes names contained in these tuples must also extend this class.
    """

    SIM_ATTRS = {'value': 1.0}  # attribute weights considered for similarity
    THRESHOLD = 1.0  # similarity percent to consider "equal"

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self._repr(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        """Maps the '==' operator to be a shortcut for "equality"."""
        return equal(self, other)

    def __ne__(self, other):
        return not (self == other)

    def __mod__(self, other):
        """Maps the '%' operator to be a shortcut for "similarity"."""
        return similar(self, other)

    def __equal__(self, other):
        """Custom special method for similarity invoked by calling equal(a, b)."""
        return self.equality(other)

    def __similar__(self, other):
        """Custom special method for similarity invoked by calling similar(a, b)."""
        return self.similarity(other)

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        raise NotImplementedError

    def equality(self, other, names=None):
        """Compare two objects for equality.
        @param self: first object to compare
        @param other: second object to compare
        @param names: list or dictionary of attribute names to compare
        @return: boolean result of comparison
        """
        if names is None:
            names = self.SIM_ATTRS.keys()
        if type(self) != type(other):
            logging.warning("types are different")
            return False
        for name in names:
            attr1 = getattr(self, name)
            attr2 = getattr(other, name)
            equality = attr1 == attr2
            logging.debug("{}: {} == {} = {}".format(name, repr(attr1), repr(attr2), equality))
            if not equality:
                return False
        return True

    def similarity(self, other, names=None):
        """Compare two objects for similarity.
        @param self: first object to compare
        @param other: second object to compare
        @param names: dictionary of attribute name->weight to compare
        @return: L{Similarity} result of comparison
        """
        if names is None:
            names = self.SIM_ATTRS.iteritems()
        similarity = Similarity(0.0, self.THRESHOLD)
        total = 0.0
        # Calculate similarity ratio
        for name, weight in names:
            attr_1 = getattr(self, name)
            attr_2 = getattr(other, name)
            attr_similarity = attr_1 % attr_2
            logging.debug("{}: {} % {} = {}".format(name, repr(attr_1), repr(attr_2), attr_similarity))
            total += weight
            similarity += attr_similarity * weight
        if total:
            similarity *= (1.0 / total)  # scale ratio so the total is 1.0
        return similarity


class Number(Comparable):
    """Comparable positive numerical type."""

    def __similar__(self, other):
        """Mathematical comparison of numbers."""
        numerator, denominator = sorted((self.value, other.value))
        try:
            ratio = float(numerator) / denominator
        except ZeroDivisionError:
            ratio = 0.0 if numerator else 1.0
        similarity = Similarity(ratio, self.THRESHOLD)
        return similarity

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


class Text(Comparable):
    """Represents basic comparable text."""

    def __similar__(self, other):
        """Fuzzy comparison of text."""
        ratio = SequenceMatcher(a=self.value, b=other.value).ratio()
        similarity = Similarity(ratio, self.THRESHOLD)
        return similarity

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return Text("")
        else:
            return Text(text)


class TextName(Text):
    """Represents a comparable text name."""

    THRESHOLD = 0.90

    ARTICLES = 'a', 'an', 'the'
    JOINERS = 'and', '&', '+'

    def __init__(self, value):
        super(TextName, self).__init__(value)
        self.stripped = self._strip_text(self.value)

    def __similar__(self, other):
        """Fuzzy comparison of stripped title."""
        ratio = SequenceMatcher(a=self.stripped, b=other.stripped).ratio()
        similarity = Similarity(ratio, self.THRESHOLD)
        return similarity

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
    """Represents a comparable text title."""

    SIM_ATTRS = {'prefix': 0.05,
                 'title': 0.80,
                 'suffix': 0.15}

#     RE_TITLE = re.compile(r"""
#     ( \( [^)]+ \) )?  # optional prefix
#     ( [^(]+ )         # title
#     ( \( [^)]+ \) )?  # optional suffix
#     """, re.VERBOSE)

    def __init__(self, value):
        super(TextTitle, self).__init__(value)
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
        prefix = suffix = ""
        text = text.strip("( )")
        if ')' in text:
            prefix, text = text.split(')')
        if '(' in text:
            text, suffix = text.split('(')
        return TextName(prefix.strip()), TextName(text.strip()), TextName(suffix.strip())


#     def _split_title(self, text):
#         """Split a title into parts."""
#         match = self.RE_TITLE.match(text)
#         if match:
#             return match.groups()
#         else:
#             raise TypeError("unable to convert {0} to {1}".format(repr(text), self.__class__))

    ###########
#     @staticmethod
#     def _split_text_title(text):
#         """Split text into its optional and required parts.
#         """
#         parts = text.replace(')', '(').split('(')
#         return [part.strip("() ") for part in parts if part.strip("() ")]
#
#     @staticmethod
#     def _compare_text_titles(text1, text2):
#         """Compare two strings representing titles with optional portions.
#         """
#         best_ratio = 0.0
#         parts1 = TextTitle._split_text_title(text1)
#         parts2 = TextTitle._split_text_title(text2)
#         len1 = len(parts1)
#         len2 = len(parts2)
#         logging.debug("parts 1: {0}".format(parts1))
#         logging.debug("parts 2: {0}".format(parts2))
#         combos1 = set(chain(*(combinations(parts1, r) for r in range(min(len1, len2), len1 + 1))))
#         combos2 = set(chain(*(combinations(parts2, r) for r in range(min(len1, len2), len2 + 1))))
#         for combo1 in combos1:
#             for combo2 in combos2:
#                 ratio = Base._compare_text(' '.join(combo1), ' '.join(combo2))
#                 if ratio > best_ratio:
#                     logging.debug("{0} ? {1} = {2}".format(combo1, combo2, ratio))
#                     best_ratio = ratio
#                     if best_ratio == 1.0:
#                         break
#         return best_ratio


class TextList(Comparable):
    """Represents a comparable text list."""

    def __init__(self, value):
        super(TextList, self).__init__(value)
        self.items = self._split_text_list(self.value)

    def __str__(self):
        return ', '.join(self.items)

    def __similar__(self, other):
        """Permutation comparison of list items."""
        logging.debug("comparing {} to {} for similarity...".format(repr(self), repr(other)))
        ratio = 0.0

        items1 = list(self.items)
        items2 = list(other.items)

        count = max(len(items1), len(items2))

        for item1 in items1:
            item_ratio = 0.0
            for item2 in items2:
                item_ratio = max(item_ratio, item1 % item2)



                ratio += max(item1 % item2 for item2 in items2)





        for combo1 in set(permutations(self.items, len(self.items))):
            for combo2 in set(permutations(other.items, len(other.items))):




                ratio2 = TextName(', '.join(combo1)) % TextName(', '.join(combo2))



                if ratio2 > ratio:
                    logging.debug("{0} % {1} = {2}".format(combo1, combo2, ratio2))
                    ratio = ratio2
                    if ratio == 1.0:
                        break
        similarity = Similarity(ratio, self.THRESHOLD)
        logging.debug("similarity: {}".format(similarity))
        return similarity

    @staticmethod
    def _split_text_list(text):
        """Strip joining words and split text into list.
        """
        for word in TextName.JOINERS:
            text = text.replace(word, ',')
        text = text.replace(', ', ',').replace(',,', ',')
        return tuple(TextName(part) for part in text.split(','))


