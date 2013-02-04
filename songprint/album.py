"""
Album class used by song objects.
"""

import re
import logging

from songprint.base import Base
import songprint.settings as settings


RE_FEATURING = r"""
\(                            # opening parenthesis
(?:feat)(?:(?:\.)|(?:uring))  # "feat." or "featuring"
\ ([^)]+)                     # list of featured artists
\)                            # closing parenthesis
""".strip()

RE_KIND = r"""
[[({]            # opening bracket
([^)]*           # words before album kind
\b<kind>\b       # kind of album
.*)              # words after album kind
[\])}]           # closing bracket
""".strip()


class Album(Base):
    """Stores a song's album and provides comparison algorithms."""

    def __init__(self, name=None, year=None, kind=None, featuring=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name, self.kind, self.featuring = self._parse_album(name)
        self.kind = self.kind or kind
        self.featuring = self.featuring or featuring
        self.year = self._parse_int(year, "year")
        super(Album, self).__init__()

    def __str__(self):
        """Format the album as a string."""
        parts = []
        if self.name:
            parts.append(self.name)
        if self.kind:
            parts.append("[{kind}]".format(kind=self.kind))
        if self.year:
            pass  # year is not part of the album's string representation
        return ' '.join(parts)

    def __repr__(self):
        """Represent the album object."""
        return self._get_repr([self.name, self.year, self.kind, self.featuring])

    def _parse_album(self, value):
        """Attempt to split the value into an album's parts.

        @param value: value to convert
        @return: name, kind, featuring
        """
        text = self._parse_string(value, "album title")
        if not text:
            return None, None, None
        else:
            return self._split_album(text)

    @staticmethod
    def _split_album(text):  # TODO: make this logic common
        """Split an album title into parts.

        @param text: string to split into parts
        @return: name, kind, featuring
        """
        kind = featuring = None
        # Strip featured artists
        logging.debug("searching for featured artists in: {0}".format(text))
        match = re.search(RE_FEATURING, text, re.IGNORECASE | re.VERBOSE)
        if match:
            featuring = match.group(1)
            logging.debug("match found: {0}".format(featuring))
            text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
        # Strip song kinds
        for kind in settings.KINDS:
            re_kind = RE_KIND.replace('<kind>', kind)
            logging.debug("searching for '{0}' kind in: {1}".format(kind, text))
            match = re.search(re_kind, text, re.IGNORECASE | re.VERBOSE)
            if match:
                logging.debug("match found: {0}".format(kind))
                text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
                break
        else:
            kind = None
        # Return parts
        return text, kind, featuring

    def similarity(self, other):
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
