import logging

from songprint.base import Base


class Album(Base):
    """Stores a song's album and provides comparison algorithms."""

    def __init__(self, name, year=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name = self.parse_string(name, "album name")
        self.year = self.parse_int(year, "year")

    def get_name(self, strip=False):
        """Return the album name and optionally strip extra information."""
        if strip:
            return self.strip_text(self.name)
        else:
            return self.name

    def compare(self, other):
        """Calculate percent similarity between two albums.

        @return: 0.0 to 1.0 where 1.0 indicates the two albums should be considered equal
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        self_text = self.get_name(strip=True)
        other_text = other.get_name(strip=True)
        if self_text == other_text:
            return 1.0
        else:
            return 0.0

