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
        self.track = self.parse_int(track, "track number")
        self.duration = self.parse_int(track, "song duration")

    def compare(self, other):
        """Calculate percent similarity between two songs.

        @return: 0.0 to 1.0 where 1.0 indicates the two songs should be considered equal
        """
        return 0.0
