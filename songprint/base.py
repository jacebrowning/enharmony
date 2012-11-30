import pprint
import logging


class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 1.0

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def compare(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0

    @staticmethod
    def parse_string(value, kind):
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
    def parse_int(value, kind):
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
    def strip_text(text):
        """Return lowercase text with whitespace and articles stripped.
        """
        text = text.strip()
        text = text.replace('  ', ' ')  # remove duplicate spaces
        text = text.lower()
        for article in ('a', 'an', 'the'):
            if text.startswith(article):
                text = text.split(article, 1)[-1].strip()
                break
        return text
