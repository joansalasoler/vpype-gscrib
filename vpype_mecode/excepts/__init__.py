# -*- coding: utf-8 -*-

"""
Exceptions and errors.

This module defines a collection of exceptions to handle errors related
to G-code processing and generation.
"""

from .gcode_error import GCodeError
from .tool_state_error import ToolStateError
from .coolant_state_error import CoolantStateError

__all__ = [
    "GCodeError",
    "ToolStateError",
    "CoolantStateError",
]
