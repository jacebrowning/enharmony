"""
Base class to extended by other song attribute classes.
"""


from comparable import CompoundComparable
from comparable.simple import TextTitle
from comparable.compound import Group


class TextTitle(CompoundComparable):
    """Represents a comparable text title."""

    attributes = {'prefix': 0.05,
                  'title': 0.80,
                  'suffix': 0.15}

    def __init__(self, value):
        super(TextTitle, self).__init__(value)
        self.prefix, self.title, self.suffix = self._split_title(self.value)

    def __str__(self):
        text = str(self.title)
        if self.prefix:
            text = "({0}) ".format(self.prefix) + text
        if self.suffix:
            text = text + " ({0})".format(self.suffix)
        return text

    @staticmethod
    def fromstring(text):
        """Return a new instance parsed from text.
        """
        if text is None:
            return TextTitle("")
        else:
            return TextTitle(text)

    @staticmethod
    def _split_title(text):
        """Split a title into parts.
        """
        prefix = suffix = ""
        text = text.strip("( )")
        if ')' in text:
            prefix, text = text.split(')')
        if '(' in text:
            text, suffix = text.split('(')
        return TextTitle(prefix.strip()), TextTitle(text.strip()), TextTitle(suffix.strip())


class TextList(Group):

    @staticmethod
    def fromtext(text):
        pass
