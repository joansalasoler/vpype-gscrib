# -*- coding: utf-8 -*-
# pylint: disable=no-member

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

from typing import Optional
from typeguard import typechecked

from vpype_mecode.excepts import *
from vpype_mecode.enums import *
from vpype_mecode.builder.enums import *


class GState:
    """Manages and tracks the state of the G-code machine.

    This class maintains the current state of various G-code machine
    parameters. It provides methods to retrieve and safely modify these
    states while enforcing validation rules.
    """

    def __init__(self) -> None:
        self._current_tool_number: int = 0
        self._current_tool_power: float = 0
        self._current_spin_mode: SpinMode = SpinMode.OFF
        self._current_power_mode: PowerMode = PowerMode.OFF
        self._current_distance_mode: DistanceMode = DistanceMode.ABSOLUTE
        self._current_extrusion_mode: ExtrusionMode = ExtrusionMode.ABSOLUTE
        self._current_coolant_mode: CoolantMode = CoolantMode.OFF
        self._current_feed_mode: FeedMode = FeedMode.UNITS_PER_MINUTE
        self._current_rack_mode: RackMode = RackMode.OFF
        self._current_halt_mode: HaltMode = HaltMode.OFF
        self._current_length_units: Optional[LengthUnits] = None
        self._current_plane: Optional[Plane] = None
        self._is_coolant_active: bool = False
        self._is_tool_active: bool = False

    @property
    def is_coolant_active(self) -> bool:
        """Check if coolant is currently active."""
        return self._is_coolant_active

    @property
    def is_tool_active(self) -> bool:
        """Check if tool is currently active."""
        return self._is_tool_active

    @property
    def is_relative(self) -> bool:
        """Check if relative distance mode is active."""
        return self._current_distance_mode == DistanceMode.RELATIVE

    @property
    def current_tool_number(self) -> int:
        """Get the current tool number."""
        return self._current_tool_number

    @property
    def current_tool_power(self) -> float:
        """Get the current tool power."""
        return self._current_tool_power

    @property
    def current_spin_mode(self) -> SpinMode:
        """Get the current spin mode."""
        return self._current_spin_mode

    @property
    def current_power_mode(self) -> PowerMode:
        """Get the current power mode."""
        return self._current_power_mode

    @property
    def current_coolant_mode(self) -> CoolantMode:
        """Get the current coolant mode."""
        return self._current_coolant_mode

    @property
    def current_distance_mode(self) -> DistanceMode:
        """Get the current distance mode."""
        return self._current_distance_mode

    @property
    def current_extrusion_mode(self) -> ExtrusionMode:
        """Get the current extrusion mode."""
        return self._current_extrusion_mode

    @property
    def current_feed_mode(self) -> FeedMode:
        """Get the current feed mode."""
        return self._current_feed_mode

    @property
    def current_rack_mode(self) -> RackMode:
        """Get the current rack mode."""
        return self._current_rack_mode

    @property
    def current_halt_mode(self) -> HaltMode:
        """Get the current halt mode."""
        return self._current_halt_mode

    @property
    def current_length_units(self) -> LengthUnits:
        """Get the current length units sytem."""
        return self._current_length_units

    @property
    def current_plane(self) -> Plane:
        """Get the current working plane."""
        return self._current_plane

    @typechecked
    def set_length_units(self, length_units: LengthUnits) -> None:
        """Set the length measurement unit system.

        Args:
            length_units (LengthUnits): The unit system to use.
        """

        self._current_length_units = length_units

    @typechecked
    def set_plane(self, plane: Plane) -> None:
        """Set the working plane for circular movements.

        Args:
            plane (Plane): The plane to use.
        """

        self._current_plane = plane

    @typechecked
    def set_tool_power(self, power: float) -> None:
        """Set the current tool power level.

        Args:
            power (float): The power level to set (must be >= 0).

        Raises:
            ValueError: If power is negative or not a number.
        """

        self._validate_tool_power(power)
        self._current_tool_power = power

    @typechecked
    def set_distance_mode(self, mode: DistanceMode) -> None:
        """Set the coordinate input mode for position commands.

        Args:
            mode (DistanceMode): The distance mode to use
        """

        self._current_distance_mode = mode

    @typechecked
    def set_extrusion_mode(self, mode: ExtrusionMode) -> None:
        """Set the coordinate input mode for extrusion.

        Args:
            mode (ExtrusionMode): The extrusion mode to use
        """

        self._current_extrusion_mode = mode

    @typechecked
    def set_feed_mode(self, mode: FeedMode) -> None:
        """Set the feed rate interpretation mode.

        Args:
            mode (FeedMode): The feed mode to use.
        """

        self._current_feed_mode = mode

    @typechecked
    def set_coolant_mode(self, mode: CoolantMode) -> None:
        """Set the current coolant mode.

        Args:
            mode (CoolantMode): The coolant mode to set.

        Raises:
            CoolantStateError: If attempting to change mode while
                coolant is active.
        """

        if mode != CoolantMode.OFF:
            self._ensure_coolant_is_inactive("Coolant already active.")

        self._is_coolant_active = mode != CoolantMode.OFF
        self._current_coolant_mode = mode

    @typechecked
    def set_spin_mode(self, mode: SpinMode, speed: float = 0) -> None:
        """Set the current tool spin mode and speed.

        Args:
            mode (SpinMode): The spin mode to set.
            speed (float): The spindle speed (must be >= 0).

        Raises:
            ValueError: If speed is negative or not a number.
            ToolStateError: If attempting to change mode while
                the spindle is active.
        """

        if mode != SpinMode.OFF:
            self._ensure_tool_is_inactive("Spindle already active.")

        self.set_tool_power(speed)
        self._is_tool_active = (mode != SpinMode.OFF)
        self._current_spin_mode = mode

    @typechecked
    def set_power_mode(self, mode: PowerMode, power: float = 0) -> None:
        """Set the current tool power mode and level.

        Args:
            mode (PowerMode): The power mode to set.
            power (float): The power level (must be >= 0).

        Raises:
            ValueError: If power is negative or not a number.
            ToolStateError: If attempting to change mode while tool
                power is active.
        """

        if mode != PowerMode.OFF:
            self._ensure_tool_is_inactive("Power already active.")

        self.set_tool_power(power)
        self._is_tool_active = (mode != PowerMode.OFF)
        self._current_power_mode = mode

    @typechecked
    def set_rack_mode(self, mode: RackMode, tool_number: int) -> None:
        """Set the current rack mode and tool number.

        Args:
            mode (RackMode): The rack mode to set.
            tool_number (int): The tool number to select.

        Raises:
            ValueError: If tool_number is less than 1.
            ToolStateError: If attempting to set the rack mode while
                the tool is active.
            CoolantStateError: If attempting to set the rack mode while
                coolant is active.
        """

        self._validate_tool_number(tool_number)
        self._ensure_tool_is_inactive("Tool change with tool on.")
        self._ensure_coolant_is_inactive("Tool change with coolant on.")
        self._current_tool_number = tool_number
        self._current_rack_mode = mode

    @typechecked
    def set_halt_mode(self, mode: HaltMode) -> None:
        """Set the current halt mode.

        Args:
            mode (HaltMode): The halt mode to set.

        Raises:
            ToolStateError: If attempting to halt while a tool is active.
            CoolantStateError: If attempting to halt while coolant is active.
        """

        if mode != HaltMode.OFF:
            self._ensure_tool_is_inactive("Halt with tool on.")
            self._ensure_coolant_is_inactive("Halt with coolant on.")

        self._current_halt_mode = mode

    def _ensure_tool_is_inactive(self, message: str) -> None:
        """Raise an exception if tool is active."""

        if self._is_tool_active:
            raise ToolStateError(message)

    def _ensure_coolant_is_inactive(self, message: str) -> None:
        """Raise an exception if coolant is active."""

        if self._is_coolant_active:
            raise CoolantStateError(message)

    def _validate_tool_number(self, number: int) -> None:
        """Validate tool number is within acceptable range."""

        if not isinstance(number, int) or number < 1:
            message = f"Invalid tool number '{number}'."
            raise ValueError(message)

    def _validate_tool_power(self, power: float) -> None:
        """Validate tool power level is within acceptable range."""

        if not isinstance(power, int | float) or power < 0.0:
            message = f"Invalid tool power '{power}'."
            raise ValueError(message)
