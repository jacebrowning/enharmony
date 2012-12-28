"""
Settings for the songprint package.
"""

import os
import logging

__author__ = "Jace Browning"
__version__ = "0.0.x"

# Title constants
ARTICLES = 'a', 'an', 'the'
VARIANTS = 'live', 'acoustic', 'remix', 'extended', 'edit', 'original'

# Logging settings
DEFAULT_LOGGING_FORMAT = "%(levelname)s: %(message)s"
if os.path.splitext(__file__)[1] == '.py':  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"
else:  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s"  # line number is unknown in executables
DEFAULT_LOGGING_LEVEL = logging.INFO
VERBOSE_LOGGING_LEVEL = logging.DEBUG
