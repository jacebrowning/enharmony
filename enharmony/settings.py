"""
Settings for the enharmony package.
"""

import logging

# Logging settings
DEFAULT_LOGGING_FORMAT = "%(message)s"
VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s"
VERBOSE2_LOGGING_FORMAT = "%(asctime)s: %(levelname)s: %(message)s"
VERBOSE3_LOGGING_FORMAT = "%(asctime)s: %(levelname)s: %(module)s:%(lineno)d: %(message)s"
DEFAULT_LOGGING_LEVEL = logging.INFO
VERBOSE_LOGGING_LEVEL = logging.DEBUG

# Common constants
ARTICLES = 'a', 'an', 'the'
JOINERS = 'and', '&', '+'

# Title constants
VARIANTS = 'Live', 'Acoustic', 'Remix', 'Extended', 'Edit', 'Original'

# Album constants
KINDS = 'Single', 'EP'
EXTRA = 'Bonus', 'Deluxe'  # TODO: this is not used
ALBUM_YEAR_THRESHOLD = 0.50
ALBUM_NAME_THRESHOLD = 0.91
ALBUM_SIMILARITY_SAME_YEAR = 0.95  # TODO: this is not used


