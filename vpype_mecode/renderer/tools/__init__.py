# -*- coding: utf-8 -*-

"""
Tool activation and parameter control.

This module provides implementations for different machine tools such as
lasers, spindles, and other end effectors. Each implementation handles
tool initialization, activation, power control, and shutdown, generating
the corresponding G-code commands for various tool types and behaviors.
"""

from .base_tool import BaseTool
from .beam_tool import BeamTool
from .blade_tool import BladeTool
from .extruder_tool import ExtruderTool
from .heated_extruder_tool import HeatedExtruderTool
from .adaptive_beam_tool import AdaptiveBeamTool
from .marker_tool import MarkerTool
from .spindle_tool import SpindleTool
from .tool_factory import ToolFactory

__all__ = [
    "BaseTool",
    "ToolFactory",
    "BeamTool",
    "BladeTool",
    "ExtruderTool",
    "HeatedExtruderTool",
    "AdaptiveBeamTool",
    "MarkerTool",
    "SpindleTool",
]
