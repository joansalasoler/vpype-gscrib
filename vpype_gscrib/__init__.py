# -*- coding: utf-8 -*-

"""
Vector Graphics to G-code Converter.

This `vpype` plugin provides a comprehensive toolkit and command line
interface for processing vector paths and generating G-code commands for
CNC machines, plotters, and other G-code compatible devices.
"""

from . import config
from . import enums
from . import excepts
from . import processor
from . import renderer
from . import heightmaps

__version__ = "1.1.0"

__all__ = [
    "config",
    "enums",
    "excepts",
    "processor",
    "renderer",
    "heightmaps",
]
