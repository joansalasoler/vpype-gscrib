# -*- coding: utf-8 -*-

"""
Plugin exceptions and errors.

This module defines a collection of exceptions to handle errors related
to G-code processing and generation.
"""

from .plugin_errors import ImageLoadError
from .plugin_errors import VpypeMecodeError

__all__ = [
    "ImageLoadError",
    "VpypeMecodeError",
]
