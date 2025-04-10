"""
utils/logger.py

Provides defined global logger.
"""


import logging


logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


