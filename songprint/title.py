from songprint.base import Base


class Title(Base):
    """Stores a song's title and provides comparison algorithms."""

    def __init__(self, name):
        """Initialize a new title.

        @param name: provided name of song
        """
        self.name = name
