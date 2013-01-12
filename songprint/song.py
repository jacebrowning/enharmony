"""
Song class to provide textual comparison based on attributes.
"""

from songprint.base import Base
from songprint.title import Title
from songprint.artist import Artist
from songprint.album import  Album


class Song(Base):
    """Stores identifying song information."""

    EQUALITY_PERCENT = 1.0

    def __init__(self, artist, title, album=None, year=None, track=None, duration=None):
        """Initialize a new song.

        @param artist: name of song's artist
        @param title: name song
        @param album: name of song's album
        @param year: year of song's album's release
        @param track: track number on album
        @param duration: length of song in seconds
        """
        self.title = Title(title)
        self.artist = Artist(artist)
        self.album = Album(album, year)
        self.track = self._parse_int(track, "track number")
        self.duration = self._parse_int(duration, "song duration")
        super(Song, self).__init__()

    def compare(self, other):
        """Calculate percent similarity between two songs.

        @return: 0.0 to 1.0 where 1.0 indicates the two songs should be considered equal
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        # Compare attributes
        value = 0.0
        if self.title == other.title:
            value += 0.5
        if self.artist == other.artist:
            value += 0.5
        return value
