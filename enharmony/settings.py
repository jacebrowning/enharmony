"""
Settings for the enharmony package.
"""

import os
import logging

# Common constants
ARTICLES = 'a', 'an', 'the'
JOINERS = 'and', '&', '+'

# Title constants
VARIANTS = 'Live', 'Acoustic', 'Remix', 'Extended', 'Edit', 'Original'

# Album constants
KINDS = 'Single', 'EP'
EXTRA = 'Bonus', 'Deluxe'  # TODO: this is not used
ALBUM_SIMILARITY_SAME_YEAR = 0.95

# Logging settings
DEFAULT_LOGGING_FORMAT = "%(levelname)s: %(message)s"
if os.path.splitext(__file__)[1] == '.py':  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"
else:  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s"  # line number is unknown in executables
DEFAULT_LOGGING_LEVEL = logging.INFO
VERBOSE_LOGGING_LEVEL = logging.DEBUG
