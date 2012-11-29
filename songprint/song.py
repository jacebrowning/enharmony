
class Song(object):
    """Stores identifying song information."""

    EQUALITY_PERCENT = 1.0

    def __init__(self, artist, title, album=None, year=None, track=None, duration=None):
        """Initialize a new song.
        """
        self.artist = Artist(artist)
        self.title = Title(title)
        self.album = Album(album, year)
        self.track = self.parse_track(track)
        self.duration = self.parse_duration(duration)

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def compare(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0

class Title(object):
    """Stores a song's title and provides comparison algorithms."""

    def __init__(self, name):
        """Initialize a new title.

        @param name: provided name of song
        """
        self.name = name


class Artist(object):
    """Stores a song's artist and provides comparison algorithms"""

    def __init__(self, name):
        """Initialize a new artist.

        @param name: provided name of song's artist
        """
        self.name = name


class Album(object):
    """Stores a song's album and provides comparison algorithms."""

    def __init__(self, name, year):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name = self.parse_name(name)
        self.year = self.parse_year(year)

    @staticmethod
    def parse_name(name):
        try:
            return name.strip()
        except ValueError:
            return None

    @staticmethod
    def parse_year(year):
        try:
            return int(year)
        except ValueError:
            return None
