"""
Album class used by song objects.
"""

from songprint.base import Base


class Album(Base):
    """Stores a song's album and provides comparison algorithms."""

    def __init__(self, name, year=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name = self._parse_string(name, "album name")
        self.year = self._parse_int(year, "year")
        super(Album, self).__init__()

    def compare(self, other):
        """Calculate percent similarity between two albums.

        @return: 0.0 to 1.0 where 1.0 indicates the two albums should be considered equal
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        # Compare attributes
        if self._strip_text(self.name) == self._strip_text(other.name):
            return 1.0
        else:
            return 0.0
