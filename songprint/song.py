class Song(object):

    EQUALITY_PERCENT = 1.0

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.compare(other) >= self.EQUALITY_PERCENT

    def match(self, other):
        """Calculate percent similarity between two songs.
        """
        return 0.0
