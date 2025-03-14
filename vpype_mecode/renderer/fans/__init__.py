# -*- coding: utf-8 -*-

"""
Handles machine fans.

This module provides implementations for controlling the machine's fans.
"""

from .base_fan import BaseFan
from .fan_factory import FanFactory
from .cooling_fan import CoolingFan
from .no_fan import NoFan

__all__ = [
    "BaseFan",
    "FanFactory",
    "CoolingFan",
    "NoFan",
]
