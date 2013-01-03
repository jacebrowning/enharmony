"""
Base class to extended by other song attribute classes.
"""

import pprint
import logging

from songprint import settings


class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 1.0

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def __repr__(self):
        return self._get_repr([])

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def __ne__(self, other):
        return not (self == other)

    def _get_repr(self, args):
        """
        Return representation string from the provided arguments.
        """
        return self.__class__.__name__ + '(' + ','.join(repr(arg) for arg in args) + ')'

    def compare(self, other):
        """Calculate percent similarity between two songs. Overwritten by subclasses.
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
    def _strip_text(text):
        """Return lowercase text with whitespace/articles stripped and special characters replaced.
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
