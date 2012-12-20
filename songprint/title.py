from songprint.base import Base


class Title(Base):
    """Stores a song's title and provides comparison algorithms."""

    def __init__(self, name):
        """Initialize a new title.

        @param name: provided name of song
        """
        self.name, self.alternate, self.variant, self.featuring = self._parse_title(name)

    def _parse_title(self, value):
        """Attempt to split the value into a title's parts.
        @param value: value to convert
        @return: name, alternate, variant, featuring
        """
        text = self.parse_string(value, "song title")
        if not text:
            return None, None, None, None
        else:
            return split_title(text)

    def _split_title(self, text):
        """Split a song title into parts
        @param text: string to split into parts
        @return: name, alternate, variant, featuring
        """
        return text, None, None, None  # TODO: split title with regex

    def get_name(self, strip=False):
        """Return the song title and optionally strip extra information."""
        if strip:
            return self.strip_text(self.name)
        else:
            return self.name

    def compare(self, other):
        """Calculate percent similarity between two song titles.

        @return: 0.0 to 1.0 where 1.0 indicates the two titles should be considered equal
        """
        if type(self) != type(other):
            return 0.0
        self_text = self.get_name(strip=True)
        other_text = other.get_name(strip=True)
        if self_text == other_text:
            return 1.0
        else:
            return 0.0
