"""
Title class used by Song objects.
"""

import re
import logging

from songprint.base import Base
import songprint.settings as settings

RE_FEATURING = """
\(                            # opening parenthesis
(?:feat)(?:(?:\.)|(?:uring))  # "feat." or "featuring"
\ ([^)]+)                     # list of featured artists
\)                            # closing parenthesis
""".strip()

RE_VARIANT = """
[[({]            # opening bracket
(.*              # words before vairant
\\b<variant>\\b  # variant word
.*)              # words after variant
[\])}]           # closing bracket
""".strip()


class Title(Base):
    """Stores a song's title and provides comparison algorithms."""

    def __init__(self, name):
        """Initialize a new title.

        @param name: provided name of song
        """
        self.name, self.alternate, self.variant, self.featuring = self._parse_title(name)
        super(Title, self).__init__()

    def __str__(self):
        """Format the song title as a string."""
        parts = []
        if self.name:
            parts.append(self.name)
        if self.alternate:
            parts.append('(' + self.alternate + ')')
        if self.variant:
            parts.append('[' + self.variant.title() + ']')
        return ' '.join(parts)

    def __repr__(self):
        """Represent the title object."""
        return "{0}({1})".format(self.__class__.__name__, '"' + str(self) + '"')

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

    def _split_title(self, text):
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
        else:
            logging.debug("no match found: {0}".format(RE_FEATURING))
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
                logging.debug("no match found: {0}".format(re_variant))
        else:
            variant = None
        # Return parts
        return text, alternate, variant, featuring

    def get_name(self, strip=False):
        """Return the song title and optionally strip extra information."""
        if strip:
            return self._strip_text(self.name)
        else:
            return self.name

    def get_alternate(self, strip=False):
        """Return the alternate song title and optionally strip extra information."""
        if strip:
            return self._strip_text(self.alternate)
        else:
            return self.alternate

    def compare(self, other):
        """Calculate percent similarity between two song titles.

        @return: 0.0 to 1.0 where 1.0 indicates the two titles should be considered equal
        """
        # Compare types
        if type(self) != type(other):
            return 0.0
        # Compare attributes
        value = 0.0
        if self.get_name(strip=True) == other.get_name(strip=True):
            value += 0.5
        if self.get_alternate(strip=True) == other.get_alternate(strip=True):
            value += 0.25
        if self.variant == other.variant:
            value += 0.25
        return value
