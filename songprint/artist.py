"""
Artist class used by song objects.
"""

from songprint.base import Base


class Artist(Base):
    """Stores a song's artist and provides comparison algorithms"""

    def __init__(self, name):
        """Initialize a new artist.

        @param name: provided name of song's artist
        """
        self.name = self._parse_string(name, "artist name")
        super(Artist, self).__init__()

    def __str__(self):
        """Format the artist as a string."""
        return self.name

    def __repr__(self):
        """Represent the artist object."""
        return self._get_repr([self.name])

    def compare(self, other):
        """Calculate percent similarity between two artists.

        @return: 0.0 to 1.0 where 1.0 indicates the two artists should be considered equal
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        # Compare attributes
        value = 0.0
        if self._strip_text(self.name) == self._strip_text(other.name):
            value += 1.0
        return value
