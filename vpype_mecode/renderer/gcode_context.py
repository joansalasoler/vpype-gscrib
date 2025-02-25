# -*- coding: utf-8 -*-

# G-Code generator for Vpype.
# Copyright (C) 2025 Joan Sala <contact@joansala.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from vpype_mecode.renderer.gcode_builder import GBuilder
from vpype_mecode.enums import LengthUnits, TimeUnits
from vpype_mecode.config import RenderConfig
from vpype_mecode.enums import *


class GContext():
    """Context of the G-code generation.

    This class encapsulates all the configuration parameters needed
    for G-code generation, including units, speeds, z-axis positions,
    and machine-specific settings.

    Times are given in seconds and lengths in pixels. Both will be
    automatically scaled by the `GBuilder` instance. Speeds are given
    in units per minute (mm/min or in/min).

    Args:
        builder (GBuilder): G-code builder instance
        config (RenderConfig): Configuration object

    Attributes:
        g (GBuilder): The G-code builder instance
        length_units (LengthUnits): Unit system for length measurements
        time_units (TimeUnits): Unit system for time measurements
        power_level (float): Power level for laser or tool
        spindle_rpm (float): Spindle rotation speed in RPM
        warmup_delay (float): Delay time for tool warmup
        work_z (float): Z-axis position for working/cutting
        safe_z (float): Z-axis position for safe travel
        plunge_z (float): Z-axis position for plunge movements
        work_speed (float): Feed rate during cutting operations
        plunge_speed (float): Feed rate during plunge movements
        travel_speed (float): Feed rate during rapid movements
    """

    def __init__(self, builder: GBuilder, config: RenderConfig):
        """Initialize the G-code context.

        Args:
            builder (GBuilder): The G-code builder instance
            config (RenderConfig): Configuration object
        """

        self._g = builder
        self._config = config

        self._head_mode = config.head_mode
        self._rack_mode = config.rack_mode
        self._spin_mode = config.spin_mode
        self._tool_mode = config.tool_mode
        self._coolant_mode = config.coolant_mode

        self._length_units = config.length_units
        self._time_units = config.time_units
        self._power_level = config.power_level
        self._spindle_rpm = config.spindle_rpm
        self._warmup_delay = config.warmup_delay
        self._tool_number = config.tool_number

        self._work_z = config.work_z
        self._safe_z = config.safe_z
        self._plunge_z = config.plunge_z
        self._park_z = config.park_z

        self._work_speed = self.scale_length(config.work_speed)
        self._plunge_speed = self.scale_length(config.plunge_speed)
        self._travel_speed = self.scale_length(config.travel_speed)

    def scale_length(self, length: float) -> float:
        """Scale a value to the configured length units.

        Args:
            length (float): A value to scale in pixels

        Returns:
            float: Scaled length value in the configured units
        """

        return self._length_units.scale(length)

    def format_config_values(self):
        """Return a firnated dictionary of configuration values"""

        return self._config.format_values(self._length_units)

    @property
    def g(self) -> GBuilder:
        return self._g

    @property
    def coolant_mode(self) -> CoolantMode:
        return self._coolant_mode

    @property
    def head_mode(self) -> HeadMode:
        return self._head_mode

    @property
    def rack_mode(self) -> RackMode:
        return self._rack_mode

    @property
    def spin_mode(self) -> SpinMode:
        return self._spin_mode

    @property
    def tool_mode(self) -> ToolMode:
        return self._tool_mode

    @property
    def length_units(self) -> LengthUnits:
        return self._length_units

    @property
    def time_units(self) -> TimeUnits:
        return self._time_units

    @property
    def power_level(self) -> float:
        return self._power_level

    @property
    def spindle_rpm(self) -> float:
        return self._spindle_rpm

    @property
    def warmup_delay(self) -> float:
        return self._warmup_delay

    @property
    def tool_number(self) -> str:
        return self._tool_number

    @property
    def work_z(self) -> float:
        return self._work_z

    @property
    def safe_z(self) -> float:
        return self._safe_z

    @property
    def plunge_z(self) -> float:
        return self._plunge_z

    @property
    def park_z(self) -> float:
        return self._park_z

    @property
    def work_speed(self) -> float:
        return self._work_speed

    @property
    def plunge_speed(self) -> float:
        return self._plunge_speed

    @property
    def travel_speed(self) -> float:
        return self._travel_speed
