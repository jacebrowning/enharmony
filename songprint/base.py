from pprint import pformat


class Base(object):
    """Base class for song attribute classes."""

    EQUALITY_PERCENT = 1.0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def compare(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0
