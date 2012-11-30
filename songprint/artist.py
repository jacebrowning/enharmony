from songprint.base import Base


class Artist(Base):
    """Stores a song's artist and provides comparison algorithms"""

    def __init__(self, name):
        """Initialize a new artist.

        @param name: provided name of song's artist
        """
        self.name = name
