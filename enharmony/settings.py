"""
Settings for the enharmony package.
"""

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
DEFAULT_LOGGING_FORMAT = "%(message)s"
VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s"
VERBOSE2_LOGGING_FORMAT = "%(asctime)s: %(levelname)s: %(message)s"
VERBOSE3_LOGGING_FORMAT = "%(asctime)s: %(levelname)s: %(module)s:%(lineno)d: %(message)s"
DEFAULT_LOGGING_LEVEL = logging.INFO
VERBOSE_LOGGING_LEVEL = logging.DEBUG