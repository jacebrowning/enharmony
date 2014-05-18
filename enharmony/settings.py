"""Settings for the enharmony package."""

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

###################
# Album constants #
###################

# Album year
ALBUM_YEAR_THRESHOLD = 0.50

# Album kind
KINDS = 'Single', 'EP'
EXTRA = 'Bonus', 'Deluxe'  # TODO: this is not used

# Album name
ALBUM_NAME_THRESHOLD = 0.91
ALBUM_NAME_WEIGHTS = {'title': 0.90,
                      'kind': 0.10}

# Album
ALBUM_THRESHOLD = 0.95
ALBUM_WEIGHTS = {'name': 0.90,
                 'year': 0.10}
