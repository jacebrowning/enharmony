class Song(object):

    EQUALITY_PERCENT = 1.0

    def __init__(self, artist, title, album=None, year=None, track=None, duration=None):
        """Initialize a new song.
        """
        self.artist = artist
        self.title = title
        self.album = album
        self.year = year
        self.track = track
        self.duration = duration

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def compare(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0
