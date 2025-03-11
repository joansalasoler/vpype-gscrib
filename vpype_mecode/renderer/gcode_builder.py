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
from collections import namedtuple
from typing import Optional
from typeguard import typechecked

from vpype_mecode.codes import gcode_table
from vpype_mecode.enums import BaseEnum
from vpype_mecode.excepts import *
from vpype_mecode.enums import *

from .gcode_state import GState
from ..mecode import GMatrix


Position = namedtuple('Position', 'x y z')


class GBuilder(GMatrix):
    """G-code command generator for CNC machines and similar devices.

    This class extends `GMatrix` to provide high-level methods for
    generating common G-code commands used in CNC machine control. It
    handles various aspects of machine operations including:

    - Unit and plane selection
    - Tool operations and changes
    - Coolant control
    - Bed control
    - Program execution control
    - Movement commands
    """

    def __init__(self, *args, **kwargs) -> None:
        self._state: GState = GState()
        super().__init__(*args, **kwargs)

    @property
    def state(self) -> GState:
        """Current machine state."""
        return self._state

    @property
    def current_head_position(self) -> Position:
        """Get the current head position."""

        return Position(
            self.current_position['x'],
            self.current_position['y'],
            self.current_position['z']
        )

    @typechecked
    def select_units(self, length_units: LengthUnits) -> None:
        """Set the unit system for subsequent commands.

        Args:
            length_units (LengthUnits): The unit system to use
        """

        self._state.set_length_units(length_units)
        statement = self._get_gcode_from_table(length_units)
        self.write(statement)

    @typechecked
    def select_plane(self, plane: Plane) -> None:
        """Select the working plane for machine operations.

        Args:
            plane (Plane): The plane to use for subsequent operations
        """

        self._state.set_plane(plane)
        statement = self._get_gcode_from_table(plane)
        self.write(statement)

    @typechecked
    def set_distance_mode(self, mode: DistanceMode) -> None:
        """Set the positioning mode for subsequent commands.

        Args:
            mode (DistanceMode): The distance mode to use
        """

        self._state.set_distance_mode(mode)
        self.is_relative = (mode == DistanceMode.RELATIVE)
        statement = self._get_gcode_from_table(mode)
        self.write(statement)

    @typechecked
    def set_extrusion_mode(self, mode: ExtrusionMode) -> None:
        """Set the extrusion mode for subsequent commands.

        Args:
            mode (ExtrusionMode): The extrusion mode to use
        """

        self._state.set_extrusion_mode(mode)
        statement = self._get_gcode_from_table(mode)
        self.write(statement)

    @typechecked
    def set_feed_mode(self, mode: FeedMode) -> None:
        """Set the feed rate mode for subsequent commands.

        Args:
            mode (FeedMode): The feed rate mode to use
        """

        self._state.set_feed_mode(mode)
        statement = self._get_gcode_from_table(mode)
        self.write(statement)

    @typechecked
    def set_tool_power(self, power: float) -> None:
        """Set the power level for the current tool.

        The power parameter represents tool-specific values that vary
        by machine type, such as:

        - Spindle rotation speed in RPM
        - Laser power output (typically 0-100%)
        - Other similar power settings

        Args:
            power (float): Power level for the tool (must be >= 0.0)

        Raises:
            ValueError: If power is less than 0.0
        """

        self._state.set_tool_power(power)
        self.write(f'S{power}')

    @typechecked
    def set_fan_speed(self, speed: int, fan_number: int = 0) -> None:
        """Set the speed of the main fan.

        Args:
            speed (int): Fan speed (must be >= 0 and <= 255)
            fan_number (int): Fan number (must be >= 0)

        Raises:
            ValueError: If speed is not in the valid range
        """

        if fan_number < 0:
            raise ValueError(f'Invalid fan number `{fan_number}`.')

        if speed < 0 or speed > 255:
            raise ValueError(f'Invalid fan speed `{speed}`.')

        params = f'P{fan_number} S{speed}'
        mode = FanMode.ON if speed > 0 else FanMode.OFF
        statement = self._get_gcode_from_table(mode, params)
        self.write(statement)

    @typechecked
    def set_bed_temperature(self, units: TemperatureUnits, temp: int) -> None:
        """Set the temperature of the bed and return immediately.

        Args:
            units (TemperatureUnits): Temperature units
            temp (float): Target temperature
        """

        bed_units = BedTemperature.from_units(units)
        statement = self._get_gcode_from_table(bed_units, f'S{temp}')
        self.write(statement)

    @typechecked
    def set_hotend_temperature(self, units: TemperatureUnits, temp: int) -> None:
        """Set the temperature of the hotend and return immediately.

        Args:
            units (TemperatureUnits): Temperature units
            temp (float): Target temperature
        """

        hotend_units = HotendTemperature.from_units(units)
        statement = self._get_gcode_from_table(hotend_units, f'S{temp}')
        self.write(statement)

    @typechecked
    def sleep(self, units: TimeUnits, seconds: float) -> None:
        """Delays program execution for the specified time.

        Args:
            units (TimeUnits): Time unit specification
            seconds (float): Sleep duration (minimum 1ms)

        Raises:
            ValueError: If seconds is less than 1ms
        """

        if seconds < 0.001:
            raise ValueError(f'Invalid sleep time `{seconds}`.')

        params = f'P{units.scale(seconds)}'
        statement = self._get_gcode_from_table(units, params)
        self.write(statement)

    @typechecked
    def tool_on(self, mode: SpinMode, speed: float) -> None:
        """Activate the tool with specified direction and speed.

        The speed parameter represents tool-specific values that vary
        by machine type, such as:

        - Spindle rotation speed in RPM

        Args:
            mode (SpinMode): Direction of tool rotation (CW/CCW)
            speed (float): Speed for the tool (must be >= 0.0)

        Raises:
            ValueError: If speed is less than 0.0
            ValueError: If mode is OFF or was already active
            ToolStateError: If attempting invalid mode transition
        """

        if mode == SpinMode.OFF:
            raise ValueError('Not a valid spin mode.')

        self._state.set_spin_mode(mode, speed)
        mode_statement = self._get_gcode_from_table(mode)
        statement = f'S{speed} {mode_statement}'
        self.write(statement, resp_needed=True)

    def tool_off(self) -> None:
        """Deactivate the current tool."""

        self._state.set_spin_mode(SpinMode.OFF)
        statement = self._get_gcode_from_table(SpinMode.OFF)
        self.write(statement, resp_needed=True)

    @typechecked
    def power_on(self, mode: PowerMode, power: float) -> None:
        """Activate the tool with specified mode and power.

        The power parameter represents tool-specific values that vary
        by machine type, such as:

        - Laser power output (typically 0-100%)
        - Other similar power settings

        Args:
            mode (PowerMode): Power mode of the tool
            power (float): Power level for the tool (must be >= 0.0)

        Raises:
            ValueError: If power is less than 0.0
            ValueError: If mode is OFF or was already active
            ToolStateError: If attempting invalid mode transition
        """

        if mode == PowerMode.OFF:
            raise ValueError('Not a valid power mode.')

        self._state.set_power_mode(mode, power)
        mode_statement = self._get_gcode_from_table(mode)
        statement = f'S{power} {mode_statement}'
        self.write(statement, resp_needed=True)

    def power_off(self) -> None:
        """Power off the current tool."""

        self._state.set_power_mode(PowerMode.OFF)
        statement = self._get_gcode_from_table(PowerMode.OFF)
        self.write(statement, resp_needed=True)

    @typechecked
    def tool_change(self, mode: RackMode, tool_number: int) -> None:
        """Execute a tool change operation.

        Performs a tool change sequence, ensuring proper safety
        conditions are met before proceeding.

        Args:
            mode (RackMode): Tool change mode to execute
            tool_number (int): Tool number to select (must be positive)

        Raises:
            ValueError: If tool number is invalid or mode is OFF
            ToolStateError: If tool is currently active
            CoolantStateError: If coolant is currently active
        """

        if mode == RackMode.OFF:
            raise ValueError('Not a valid rack mode.')

        self._state.set_rack_mode(mode, tool_number)
        tool_digits = 2 ** math.ceil(math.log2(len(str(tool_number))))
        change_statement = self._get_gcode_from_table(mode)
        statement = f'T{tool_number:0{tool_digits}} {change_statement}'
        self.write(statement, resp_needed=True)

    @typechecked
    def coolant_on(self, mode: CoolantMode) -> None:
        """Activate coolant system with the specified mode.

        Args:
            mode (CoolantMode): Coolant operation mode to activate

        Raises:
            ValueError: If mode is OFF or was already active
        """

        if mode == CoolantMode.OFF:
            raise ValueError('Not a valid coolant mode.')

        self._state.set_coolant_mode(mode)
        statement = self._get_gcode_from_table(mode)
        self.write(statement, resp_needed=True)

    def coolant_off(self) -> None:
        """Deactivate coolant system."""

        self._state.set_coolant_mode(CoolantMode.OFF)
        statement = self._get_gcode_from_table(CoolantMode.OFF)
        self.write(statement, resp_needed=True)

    @typechecked
    def halt_program(self, mode: HaltMode, **kwargs) -> None:
        """Pause or stop program execution.

        Args:
            mode (HaltMode): Type of halt to perform
            **kwargs: Arbitrary command parameters

        Raises:
            ToolStateError: If attempting to halt with tool active
            CoolantStateError: If attempting to halt with coolant active
        """

        if mode == HaltMode.OFF:
            raise ValueError('Not a valid halt mode.')

        self._state.set_halt_mode(mode)
        params = self._get_params_string_from_dict(kwargs)
        statement = self._get_gcode_from_table(mode, params)
        self.write(statement, resp_needed=True)

    @typechecked
    def emergency_halt(self, message: str) -> None:
        """Execute a safety sequence and pause execution.

        Performs an emergency shutdown sequence:

        1. Deactivates the tool
        2. Turns off coolant
        3. Adds a comment with the emergency message
        4. Halts program execution

        Args:
            message (str): Description of the emergency condition
        """

        self.tool_off()
        self.coolant_off()
        self.comment(f'Emergency halt: {message}')
        self.halt_program(HaltMode.PAUSE)

    def rapid_absolute(self, **kwargs):
        """Rapid move to absolute coordinates without transforms."""

        kwargs['rapid'] = True
        self.move_absolute(**kwargs)

    def move_absolute(self, **kwargs):
        """Move to absolute coordinates without transforms."""

        mode_was_relative = self.is_relative

        if mode_was_relative: self.absolute()
        super(GMatrix, self).move(**kwargs)
        if mode_was_relative: self.relative()

    def write(self, statement_in: str, resp_needed = False):
        """Write a G-code statement to the G-code output.

        Args:
            statement_in (str): G-code statement to write
            resp_needed (bool): Indicates if a response is expected
        """

        self._state.set_halt_mode(HaltMode.OFF)
        super(GMatrix, self).write(statement_in, resp_needed)

    @typechecked
    def comment(self, message: str) -> None:
        """Write a comment to the G-code output.

        Args:
            message (str): Text of the comment
        """

        comment = self._as_comment(message)
        self.write(comment)

    def _get_params_string_from_dict(self, params: dict) -> str:
        """Converts a dictionary to a G-Code parameters statement"""

        return ' '.join(f'{k}{v}' for k, v in params.items())

    def _get_gcode_from_table(self, value: BaseEnum, params: Optional[str] = None) -> str:
        """Generate a G-code statement from the codes table."""

        entry = gcode_table.get_entry(value)
        comment = self._as_comment(entry.description)
        args = f' {params}' if params else ''

        return f'{entry.instruction}{args} {comment}'

    def _as_comment(self, text: str) -> str:
        """Format text as a G-code comment."""

        return self._commentify(text)
