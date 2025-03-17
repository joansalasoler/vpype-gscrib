# -*- coding: utf-8 -*-

"""
Defines machine modes and options.

This module contains enumeration classes that define different machine
states, options, and configurations for G-code generation. Each enum
value is linked to a specific G-Code instruction and a description, which
are stored in the `vpype_mecode.enums.codes_table`. The `GBuilder` class
uses this table to create the appropriate G-code statements.
"""

from .modes import BedMode
from .modes import CoolantMode
from .modes import FanMode
from .modes import HeadMode
from .modes import RackMode
from .modes import ToolMode

__all__ = [
    "BedMode",
    "CoolantMode",
    "FanMode",
    "HeadMode",
    "RackMode",
    "ToolMode",
]
