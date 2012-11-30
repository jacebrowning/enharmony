import logging

from songprint.base import Base


class Album(Base):
    """Stores a song's album and provides comparison algorithms."""

    def __init__(self, name, year=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name = self.parse_name(name)
        self.year = self.parse_year(year)

    @staticmethod
    def parse_name(name):
        try:
            return name.strip()
        except AttributeError:
            logging.debug("could not convert to an album name: {0}".format(repr(name)))
            return None

    @staticmethod
    def parse_year(year):
        try:
            return int(year)
        except TypeError:
            logging.debug("could not convert to a year: {0}".format(repr(year)))
            return None
        except ValueError:
            logging.warning("could not convert to a year: {0}".format(repr(year)))
            return None
