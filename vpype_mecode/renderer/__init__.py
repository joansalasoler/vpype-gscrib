# -*- coding: utf-8 -*-

"""
Generates G-code programs from `vpype` documents.

This module provides the main tools to generate G-code programs for CNC
machines and similar devices. `GRenderer` is the main class that generates
the G-code program from a `vpype` document.
"""

from .gcode_builder import GBuilder
from .gcode_renderer import GRenderer
from .gcode_context import GContext

__all__ = [
    'GBuilder',
    'GContext',
    'GRenderer',
]