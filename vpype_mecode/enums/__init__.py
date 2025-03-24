# -*- coding: utf-8 -*-

"""
Machine component types and operation modes.

This module contains enumeration classes that define different machine
states, options, and configurations for G-code generation. Each enum
value is linked to a specific G-Code instruction and a description, which
are stored in the `vpype_mecode.enums.codes_table`. The `GCodeBuilder` class
uses this table to create the appropriate G-code statements.
"""

from .types import BedType
from .types import CoolantType
from .types import FanType
from .types import HeadType
from .types import RackType
from .types import ToolType

__all__ = [
    "BedType",
    "CoolantType",
    "FanType",
    "HeadType",
    "RackType",
    "ToolType",
]
