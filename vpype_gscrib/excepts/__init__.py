# -*- coding: utf-8 -*-

"""
Top-level plugin exceptions and error handling.

This module defines a collection of exceptions to handle errors related
to G-code processing and generation.
"""

from .plugin_errors import FileLoadError
from .plugin_errors import ImageLoadError
from .plugin_errors import VpypeGscribError

__all__ = [
    "FileLoadError",
    "ImageLoadError",
    "VpypeGscribError",
]
