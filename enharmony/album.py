"""
Album class used by song objects.
"""

import re
import logging

from enharmony.base import Similarity, Comparable
from enharmony.base import TextEnum, TextTitle, TextList
import enharmony.settings as settings


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
            return Year(int(text))
        except (TypeError, ValueError):
            logging.warning("unable to convert {} to {}".format(repr(text), Year))
            return None


class Album(Comparable):
    """Stores a song's album and provides comparison algorithms."""

    THRESHOLD = 0.95
    SIM_ATTRS = {'name': 0.89,
                 'kind': 0.01,
                 'year': 0.10,
                 'featuring': 0.0}

    def __init__(self, name, year=None, kind=None, featuring=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name, self.kind, self.featuring = self._split_album(name)
        self.kind = self.kind or kind
        self.featuring = self.featuring or featuring
        self.year = Year.fromstring(year)

    def __repr__(self):
        """Represent the album object."""
        return self._repr(self.name, self.year, kind=self.kind, featuring=self.featuring)

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
        match = re.search(RE_FEATURING, text, re.IGNORECASE | re.VERBOSE)
        if match:
            featuring = match.group(1)
            logging.debug("match found: {0}".format(featuring))
            text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
        # Strip song kinds
        for kind in settings.KINDS:
            re_kind = RE_KIND.replace('<kind>', kind)
            match = re.search(re_kind, text, re.IGNORECASE | re.VERBOSE)
            if match:
                logging.debug("match found: {0}".format(kind))
                text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
                break
        else:
            kind = None
        # Return parts
        return TextTitle.fromstring(text), TextEnum.fromstring(kind), TextList.fromstring(featuring)
