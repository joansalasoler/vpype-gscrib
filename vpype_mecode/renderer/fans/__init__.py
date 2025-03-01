# -*- coding: utf-8 -*-

"""
Handles machine fans.

This module provides implementations for controlling the machine's fans.
"""

from .base_fan import BaseFan
from .fan_factory import FanFactory
from .on_fan import OnFan
from .off_fan import OffFan

__all__ = [
    'BaseFan',
    'FanFactory',
    'OnFan',
    'OffFan',
]
