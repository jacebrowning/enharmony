"""
Album class used by song objects.
"""

import re
import logging

from comparable import SimpleComparable, CompoundComparable
from comparable.base import Similarity, Comparable
from comparable.simple import Number, TextTitle, TextEnum
from comparable.compound import Group

from enharmony.base import TextList
from enharmony import settings


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


class Year(Number):

    """Comparable album year."""

    threshold = settings.ALBUM_YEAR_THRESHOLD

    def __init__(self, value):
        self.value = value

    def equality(self, other):
        """Get equality allowing for blanks."""
        if not self and not other:
            return True
        elif False in (bool(self), bool(other)):
            return False
        else:
            return super().equality(other)

    def similarity(self, other):
        """Mathematical comparison of years."""
        if not self or not other:
            return self.Similarity(1.0)
        else:
            delta = int(abs(self.value - other.value))
            logging.debug("delta: {}".format(delta))
            if delta == 0:
                return self.Similarity(1.0,)
            elif delta == 1:
                return self.Similarity(0.5,)
            else:
                return self.Similarity(0.0,)


class Kind(TextEnum):

    """Comparable album kind."""

    def __str__(self):
        if self:
            return "[{}]".format(super().__str__())
        else:
            return super().__str__()

    def similarity(self, other):
        """Get similarity allowing for blanks."""
        if not self or not other:
            return self.Similarity(1.0)
        else:
            return super().similarity(other)


class Name(CompoundComparable):

    """Comparable album name."""

    threshold = settings.ALBUM_NAME_THRESHOLD
    attributes = settings.ALBUM_NAME_WEIGHTS

    def __init__(self, title, kind=None):
        """Initialize a new album.

        @param name: album title
        @param kind: album type

        """
        self.title, self.kind, self.featuring = self._split(title)
        self.kind = self.kind or Kind(kind)

    def __repr__(self):
        """Represent the album object."""
        if self.kind:
            return self._repr(self.title, kind=self.kind)
        else:
            return self._repr(self.title)

    def __str__(self):
        """Format the album as a string."""
        parts = []
        if self.title:
            parts.append(str(self.title))
        if self.kind:
            parts.append(str(self.kind))
        return ' '.join(str(part) for part in parts)

    @staticmethod
    def _split(text):  # TODO: make this logic common
        """Split an album title into parts.

        @param text: string to split into parts
        @return: title, kind
        """
        kind = featuring = None
        # Strip featured artists
        match = re.search(RE_FEATURING, text, re.IGNORECASE | re.VERBOSE)
        if match:
            featuring = match.group(1)
            logging.debug("match found: {0}".format(featuring))
            text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
        # Strip album kind
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
        return TextTitle(text), Kind(kind), featuring  # TODO: featuring not used


class Album(CompoundComparable):
    """Stores a song's album and provides comparison algorithms."""

    threshold = settings.ALBUM_THRESHOLD
    attributes = settings.ALBUM_WEIGHTS

    def __init__(self, name, year=None, kind=None, featuring=None):
        """Initialize a new album.

        @param name: provided name of song's album
        """
        self.name = Name(name)
        self.name.kind = self.name.kind or Kind(kind)
        self.name.featuring = self.name.featuring or featuring  # TODO: featuring not used
        self.year = Year(year)

    def __repr__(self):
        """Represent the album object."""
        kwargs = {}
        if self.name.kind:
            kwargs['kind'] = self.name.kind
        if self.name.featuring:
            kwargs['featuring'] = self.name.featuring
        return self._repr(self.name, self.year, **kwargs)

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
    def _split(text):  # TODO: make this logic common
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
