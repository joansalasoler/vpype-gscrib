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

import math
from typeguard import typechecked

from ..enums import *
from ..excepts import *
from ..enums import BaseEnum
from ..mecode import GMatrix


class GBuilder(GMatrix):
    """
    G-code command generator for CNC machines and similar devices.

    This class extends `GMatrix` from the `mecode` library to provide
    high-level methods to generate common G-code commands for machine
    control, including unit and plane selection, tool operations,
    coolant control, and program execution.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._current_tool = 0
        self._current_spin_mode = SpinMode.OFF
        self._current_coolant_mode = CoolantMode.OFF
        self._is_coolant_active = False
        self._is_tool_active = False

    @property
    def is_tool_active(self) -> bool:
        """Check if tool is currently active."""
        return self._is_tool_active

    @property
    def is_coolant_active(self) -> bool:
        """Check if coolant is currently active."""
        return self._is_coolant_active

    @property
    def current_tool(self) -> int:
        """Get the current tool number."""
        return self._current_tool

    @property
    def current_spin_mode(self) -> SpinMode:
        """Get the current spin mode."""
        return self._current_spin_mode

    @property
    def current_coolant_mode(self) -> CoolantMode:
        """Get the current coolant mode."""
        return self._current_coolant_mode

    @typechecked
    def select_units(self, length_units: LengthUnits) -> None:
        """Set the unit system for subsequent commands."""

        statement = self._get_gcode_from_table(length_units)
        self.write(statement)

    @typechecked
    def select_plane(self, plane: Plane) -> None:
        """Select the working plane for machine operations."""

        statement = self._get_gcode_from_table(plane)
        self.write(statement)

    @typechecked
    def sleep(self, units: TimeUnits, seconds: float) -> None:
        """Delays program execution for specified time"""

        self._validate_sleep_time(seconds)
        params = f'P{units.scale(seconds)}'
        statement = self._get_gcode_from_table(units, params)
        self.write(statement)

    @typechecked
    def tool_on(self, mode: SpinMode, power: float) -> None:
        """Activate the tool with specified direction and power."""

        self._prevent_mode_change(mode, SpinMode.OFF)
        self._prevent_mode_change(mode, ~self._current_spin_mode)
        self._validate_tool_power(power)
        self._current_spin_mode = mode
        self._is_tool_active = True

        params = f'S{power}'
        statement = self._get_gcode_from_table(mode, params)
        self.write(statement, resp_needed=True)

    def tool_off(self) -> None:
        """Deactivate the current tool."""

        self._current_spin_mode = SpinMode.OFF
        self._is_tool_active = False

        statement = self._get_gcode_from_table(SpinMode.OFF)
        self.write(statement, resp_needed=True)

    @typechecked
    def tool_change(self, mode: RackMode, number: int) -> None:
        """Execute a tool change operation."""

        self._validate_tool_number(number)
        self._prevent_mode_change(mode, RackMode.OFF)
        self._ensure_tool_is_inactive('Tool change request with tool on.')
        self._ensure_coolant_is_inactive('Tool change request with coolant on.')
        self._current_tool = number

        digits = 2 ** math.ceil(math.log2(len(str(number))))
        change_statement = self._get_gcode_from_table(mode)
        statement = f'T{number:0{digits}} {change_statement}'
        self.write(statement, resp_needed=True)

    @typechecked
    def coolant_on(self, mode: CoolantMode) -> None:
        """Activate coolant system."""

        self._prevent_mode_change(mode, CoolantMode.OFF)
        self._prevent_mode_change(mode, ~self._current_coolant_mode)
        self._current_coolant_mode = mode
        self._is_coolant_active = True

        statement = self._get_gcode_from_table(mode)
        self.write(statement, resp_needed=True)

    def coolant_off(self) -> None:
        """Deactivate coolant system."""

        self._current_coolant_mode = CoolantMode.OFF
        self._is_coolant_active = False

        statement = self._get_gcode_from_table(CoolantMode.OFF)
        self.write(statement, resp_needed=True)

    @typechecked
    def halt_program(self, mode: HaltMode) -> None:
        """Pause or stop program execution."""

        self._ensure_tool_is_inactive('Halt request with tool on.')
        self._ensure_coolant_is_inactive('Halt request with coolant on.')

        statement = self._get_gcode_from_table(mode)
        self.write(statement, resp_needed=True)

    @typechecked
    def emergency_halt(self, message: str) -> None:
        """Execute safety sequence and pause execution"""

        self.tool_off()
        self.coolant_off()
        self.comment(f'Emergency halt: {message}')
        self.halt_program(HaltMode.PAUSE)

    def rapid_absolute(self, **kwargs):
        """Rapid move to absolute coordinates (without transforms)."""

        kwargs['rapid'] = True
        self.move_absolute(**kwargs)

    def move_absolute(self, **kwargs):
        """Move to absolute coordinates (without transforms)."""

        if self.is_relative: self.absolute()
        super(GMatrix, self).move(**kwargs)
        if self.is_relative: self.relative()

    @typechecked
    def comment(self, message: str) -> None:
        """Write a comment to the output."""

        comment = self._as_comment(message)
        self.write(comment)

    def _ensure_tool_is_inactive(self, message: str) -> None:
        """Raise an exception if tool is active."""

        if self._is_tool_active:
            raise ToolStateError(message)

    def _ensure_coolant_is_inactive(self, message: str) -> None:
        """Raise an exception if coolant is active."""

        if self._is_coolant_active:
            raise CoolantStateError(message)

    def _prevent_mode_change(self, value: BaseEnum, mode: BaseEnum) -> None:
        """Raise an exception if `value` equals `mode`"""

        if value == mode:
            message = f'Invalid mode `{mode}` for `{type(mode)}`.'
            raise ValueError(message)

    def _validate_tool_number(self, number: int) -> None:
        """Validate tool number is within acceptable range."""

        if not isinstance(number, int) or number < 1:
            message = f'Invalid tool number `{number}`.'
            raise ValueError(message)

    def _validate_tool_power(self, power: float) -> None:
        """Validate tool power level is within acceptable range."""

        if not isinstance(power, int | float) or power < 1.0:
            message = f'Invalid tool power `{power}`.'
            raise ValueError(message)

    def _validate_sleep_time(self, seconds: float) -> None:
        """Validate tool power level is within acceptable range."""

        if not isinstance(seconds, int | float) or seconds < 0.001:
            message = f'Invalid sleep time `{seconds}`.'
            raise ValueError(message)

    def _get_gcode_from_table(self, value: BaseEnum, params: str = None) -> str:
        """Generate a G-code statement from the codes table."""

        code = value.get_instruction()
        description = value.get_description()
        comment = self._as_comment(description)
        args = f' {params}' if params else ''

        return f'{code}{args} {comment}'

    def _as_comment(self, text: str) -> None:
        """Format text as a G-code comment."""

        return self._commentify(text)
