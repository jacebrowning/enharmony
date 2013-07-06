"""
Base class to extended by other song attribute classes.
"""

import logging
from itertools import permutations
from difflib import SequenceMatcher


def equal(obj1, obj2):
    """Calculate equality between two (Comparable) objects.
    """
    logging.info("{} == {} : ...".format(repr(obj1), repr(obj2)))
    equality = obj1.__equal__(obj2)
    logging.info("{} == {} : {}".format(repr(obj1), repr(obj2), equality))
    return equality


def similar(obj1, obj2):
    """Calculate similarity between two (Comparable) objects.
    """
    logging.info("{} % {} : ...".format(repr(obj1), repr(obj2)))
    similarity = obj1.__similar__(obj2)
    logging.info("{} % {} : {}".format(repr(obj1), repr(obj2), similarity))
    return similarity


class Base(object):
    """Shared base class."""

    def _repr(self, *args, **kwargs):
        """Return representation string from the provided arguments.
        @param args: list of arguments to __init__
        @param kwarks: dictionary of keyword arguments to __init__
        @return: __repr__ string
        """
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
        """Similarity is True if the threshold is met."""
        return self.value >= self.threshold

    def __float__(self):
        """In non-boolean scenarios, similarity is treated like a float."""
        return self.value

    def __add__(self, other):
        return Similarity(self.value + float(other), threshold=self.threshold)

    def __radd__(self, other):
        return Similarity(float(other) + self.value, threshold=self.threshold)

    def __iadd__(self, other):
        self.value += float(other)
        return self

    def __sub__(self, other):
        return Similarity(self.value - float(other), threshold=self.threshold)

    def __rsub__(self, other):
        return Similarity(float(other) - self.value, threshold=self.threshold)

    def __isub__(self, other):
        self.value -= float(other)
        return self

    def __mul__(self, other):
        return Similarity(self.value * float(other), threshold=self.threshold)

    def __rmul__(self, other):
        return Similarity(float(other) * self.value, threshold=self.threshold)

    def __imul__(self, other):
        self.value *= float(other)
        return self

    def __abs__(self):
        return Similarity(abs(self.value), threshold=self.threshold)


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

    def __nonzero__(self):
        return bool(self.value)

    @staticmethod
    def fromstring(text):  # pragma: no cover - # TODO: are these methods needed?
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
            names = self.SIM_ATTRS
        if type(self) != type(other):
            logging.warning("types are different")
            return False
        for name in names.iterkeys():
            attr_1 = getattr(self, name)
            attr_2 = getattr(other, name)
            logging.debug("{}.{}: {} == {} : ...".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2)))
            equality = attr_1 == attr_2
            logging.debug("{}.{}: {} == {} : {}".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2), equality))
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
            names = self.SIM_ATTRS
        similarity = Similarity(0.0, self.THRESHOLD)
        total = 0.0
        # Calculate similarity ratio
        for name, weight in names.iteritems():
            try:
                attr_1 = getattr(self, name)
                attr_2 = getattr(other, name)
            except AttributeError:
                logging.debug("{}.{}: skipped due to missing".format(self.__class__.__name__, name))
                continue
            logging.debug("{}.{}: {} % {} : ...".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2)))
            if attr_1 is None or attr_2 is None:
                logging.debug("{}.{}: skipped due to None".format(self.__class__.__name__, name))
                continue
#             if not weight:
#                 logging.debug("{}.{}: skipped due to no weight".format(self.__class__.__name__, name))
#                 continue
            attr_similarity = attr_1 % attr_2
            logging.debug("{}.{}: {} % {} : {}".format(self.__class__.__name__, name, repr(attr_1), repr(attr_2), attr_similarity))
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


class TextEnum(Text):
    """Represents comparable enumerated text."""

    def __similar__(self, other):
        """Only case-insensitive equivalent text is similar."""
        if str(self).lower() == str(other).lower():
            return super(TextEnum, self).__similar__(other)
        else:
            return Similarity(0.0, self.THRESHOLD)

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return TextEnum("")
        else:
            return TextEnum(text)


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

    def __init__(self, value):
        super(TextTitle, self).__init__(value)
        self.prefix, self.title, self.suffix = self._split_title(self.value)

    def __str__(self):
        text = str(self.title)
        if self.prefix:
            text = "({0}) ".format(self.prefix) + text
        if self.suffix:
            text = text + " ({0})".format(self.suffix)
        return text

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return TextTitle("")
        else:
            return TextTitle(text)

    @staticmethod
    def _split_title(text):
        """Split a title into parts."""
        prefix = suffix = ""
        text = text.strip("( )")
        if ')' in text:
            prefix, text = text.split(')')
        if '(' in text:
            text, suffix = text.split('(')
        return TextName(prefix.strip()), TextName(text.strip()), TextName(suffix.strip())


class TextList(Comparable):
    """Represents a comparable text list."""

    def __init__(self, value):
        super(TextList, self).__init__(value)
        self.items = self._split_text_list(self.value)

    def __getattr__(self, name):
        """Allows self.items[<i>] to be accessed as self.item<i+1>."""
        if name.startswith('item'):
            try:
                return self.items[int(name.replace('item', '')) - 1]
            except (ValueError, IndexError):
                logging.debug("{0} cannot be mapped to an index in self.items[]".format(repr(name)))
                return TextName("")
        raise AttributeError

    def __str__(self):
        return ', '.join(str(item) for item in self.items)

    def __similar__(self, other):
        """Permutation comparison of list items."""

        similarity = Similarity(0.0, self.THRESHOLD)

        backup1 = list(self.items)
        backup2 = list(other.items)
        names = {"item{}".format(i + 1): 1 for i in range(max(len(self.items), len(other.items)))}

        for combo1 in permutations(self.items, len(self.items)):
            self.items = combo1
            for combo2 in permutations(other.items, len(other.items)):
                other.items = combo2

                logging.debug("permutation self: {0}".format(repr(self.items)))
                logging.debug("permutation other: {0}".format(repr(other.items)))
                similarity = max(similarity, self.similarity(other, names=names))
                logging.debug("highest similarity: {0}".format(similarity))

        logging.debug("similarity: {}".format(similarity))
        self.items = backup1
        other.items = backup2
        return similarity

    @staticmethod
    def _split_text_list(text):
        """Strip joining words and split text into list.
        """
        for word in TextName.JOINERS:  # TODO: this will match words containing 'and'
            text = text.replace(word, ',')
        text = text.replace(', ', ',').replace(',,', ',')
        return tuple(TextName(part.strip()) for part in text.split(','))

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text."""
        if text is None:
            return TextList("")
        else:
            return TextList(text)

