# -*- coding: utf-8 -*-

"""
Vector Graphics to G-code Converter.

This `vpype` plugin provides a comprehensive toolkit and command line
interface for processing vector paths and generating G-code commands for
CNC machines, plotters, and other G-code compatible devices.
"""

from . import mecode
from . import config
from . import enums
from . import excepts
from . import processor
from . import renderer

__version__ = '0.1.0'

__all__ = [
    'mecode',
    'config',
    'enums',
    'excepts',
    'processor',
    'renderer',
]