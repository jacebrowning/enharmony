"""
Title class used by song objects.
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

RE_VARIANT = r"""
[[({]            # opening bracket
([^)]*           # words before variant
\b<variant>\b    # variant word
.*)              # words after variant
[\])}]           # closing bracket
""".strip()

RE_ALTERNATE = r"""
[^(]+    # main song title
\(       # opening parenthesis
([^)]+)  # alternate wording
\)       # closing parenthesis
""".strip()


class Title(Base):
    """Stores a song's title and provides comparison algorithms."""

    def __init__(self, name, alternate=None, variant=None, featuring=None):
        """Initialize a new title.

        @param name: provided name of song (which may need to be split into parts)
        @param alternate: (optional) part of song title in parenthesis
        @param variant: (optional) bracketed song variant (e.g. 'remix', 'live', etc.)
        @param featuring: (optional) featured artist text
        """
        self.name, self.alternate, self.variant, self.featuring = self._parse_title(name)
        self.alternate = self.alternate or alternate
        self.variant = self.variant or variant
        self.featuring = self.featuring or featuring
        super(Title, self).__init__()

    def __str__(self):
        """Format the song title as a string."""
        parts = []
        if self.name:
            parts.append(self.name)
        if self.alternate:
            parts.append('(' + self.alternate + ')')
        if self.variant:
            parts.append('[' + self.variant + ']')
        return ' '.join(parts)

    def __repr__(self):
        """Represent the title object."""
        return self._get_repr([self.name, self.alternate, self.variant, self.featuring])

    def _parse_title(self, value):
        """Attempt to split the value into a title's parts.
        @param value: value to convert
        @return: name, alternate, variant, featuring
        """
        text = self._parse_string(value, "song title")
        if not text:
            return None, None, None, None
        else:
            return self._split_title(text)

    @staticmethod
    def _split_title(text):  # TODO: make this logic common
        """Split a song title into parts
        @param text: string to split into parts
        @return: name, alternate, variant, featuring
        """
        alternate = variant = featuring = None
        # Strip featured artists
        logging.debug("searching for featured artists in: {0}".format(text))
        match = re.search(RE_FEATURING, text, re.IGNORECASE | re.VERBOSE)
        if match:
            featuring = match.group(1)
            logging.debug("match found: {0}".format(featuring))
            text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
        # Strip song variants
        for variant in settings.VARIANTS:
            re_variant = RE_VARIANT.replace('<variant>', variant)
            logging.debug("searching for '{0}' variant in: {1}".format(variant, text))
            match = re.search(re_variant, text, re.IGNORECASE | re.VERBOSE)
            if match:
                logging.debug("match found: {0}".format(variant))
                text = text.replace(match.group(0), '').strip()  # remove the match from the remaining text
                break
        else:
            variant = None
        # Strip alternate song title
        logging.debug("searching for alternate title: {0}".format(text))
        match = re.match(RE_ALTERNATE, text, re.IGNORECASE | re.VERBOSE)
        if match:
            alternate = match.group(1)
            logging.debug("match found: {0}".format(alternate))
            text = text.replace(alternate, '').strip("() ")
        # Return parts
        return text, alternate, variant, featuring

    def compare(self, other):
        """Calculate percent similarity between two song titles.
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        # Compare attributes
        value = 0.0
        if self._strip_text(self.name) == self._strip_text(other.name):
            value += 0.5
        if self._strip_text(self.alternate) == self._strip_text(other.alternate):
            value += 0.25
        if self.variant == other.variant:
            value += 0.25
        return value
