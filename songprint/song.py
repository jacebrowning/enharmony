import logging

from songprint.base import Base
from songprint.title import Title
from songprint.artist import Artist
from songprint.album import  Album


class Song(Base):
    """Stores identifying song information."""

    EQUALITY_PERCENT = 1.0

    def __init__(self, artist, title, album=None, year=None, track=None, duration=None):
        """Initialize a new song.
        """
        self.title = Title(title)
        self.artist = Artist(artist)
        self.album = Album(album, year)
        self.track = self.parse_track(track)
        self.duration = self.parse_duration(duration)

    @staticmethod
    def parse_track(track):
        try:
            return int(track)
        except TypeError:
            logging.debug("could not convert to a track number: {0}".format(repr(track)))
            return None
        except ValueError:
            logging.warning("could not convert to a track number: {0}".format(repr(track)))
            return None

    @staticmethod
    def parse_duration(duration):
        try:
            return int(duration)
        except TypeError:
            logging.debug("could not convert to a duration: {0}".format(repr(duration)))
            return None
        except ValueError:
            logging.warning("could not convert to a duration: {0}".format(repr(duration)))
            return None

    def compare(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0
