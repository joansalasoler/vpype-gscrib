# -*- coding: utf-8 -*-

"""
Defines machine modes and options.

This module contains enumeration classes that define different machine
states, options, and configurations for G-code generation. Each enum
value is linked to a specific G-Code instruction and a description, which
are stored in the `vpype_mecode.enums.codes_table`. The `GBuilder` class
uses this table to create the appropriate G-code statements.
"""

from .base_enum import BaseEnum
from .coolant_mode import CoolantMode
from .direct_write_mode import DirectWriteMode
from .distance_mode import DistanceMode
from .feed_mode import FeedMode
from .halt_mode import HaltMode
from .head_mode import HeadMode
from .length_units import LengthUnits
from .plane import Plane
from .rack_mode import RackMode
from .spin_mode import SpinMode
from .bed_mode import BedMode
from .time_units import TimeUnits
from .tool_mode import ToolMode

__all__ = [
    'BaseEnum',
    'CoolantMode',
    'DirectWriteMode',
    'DistanceMode',
    'FeedMode',
    'HaltMode',
    'HeadMode',
    'LengthUnits',
    'Plane',
    'RackMode',
    'SpinMode',
    'BedMode',
    'TimeUnits',
    'ToolMode',
]
