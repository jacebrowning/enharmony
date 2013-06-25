"""
Album class used by song objects.
"""

import re
import logging

from songprint.base import Similarity, Comparable
from songprint.base import Text, TextEnum, TextTitle, TextList
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




class Year(Comparable):
    """Comparable year type."""

    def __similar__(self, other):
        """Mathematical comparison of years."""

        delta = int(abs(self.value - other.value))
        logging.debug("delta: {}".format(delta))
        if delta == 0:
            return Similarity(1.0, self.THRESHOLD)
        elif delta == 1:
            return Similarity(0.5, self.THRESHOLD)
        else:
            return Similarity(0.0, self.THRESHOLD)

    @staticmethod
    def fromstring(text):
        """Try to convert text to an year."""
        try:
            value = int(text)
        except ValueError:
            raise ValueError("unable to convert {0} to {1}".format(repr(text), Year))
        return Year(value)


class Album(Comparable):
    """Stores a song's album and provides comparison algorithms."""

    SIM_ATTRS = {'name': 0.95, 'kind': 0.01, 'year': 0.04}
    THRESHOLD = 0.95

    def __init__(self, name=None, year=None, kind=None, featuring=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name, self.kind, self.featuring = self._split_album(name)
        self.kind = self.kind or kind
        self.featuring = self.featuring or featuring
        self.year = Year(year)

    def __repr__(self):
        """Represent the album object."""
        return self._repr(self.name, self.year, self.kind, self.featuring)

    def __str__(self):
        """Format the album as a string."""
        parts = []
        if self.name:
            parts.append(self.name)
        if self.kind:
            parts.append("[{kind}]".format(kind=self.kind))
        if self.year:
            pass  # year is not part of the album's string representation
        return ' '.join(str(part) for part in parts)

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
        return TextTitle.fromstring(text), TextEnum.fromstring(kind), TextList.fromstring(featuring)
