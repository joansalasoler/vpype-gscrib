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

from vpype_mecode.renderer import GContext
from vpype_mecode.enums import ExtrusionMode, HaltMode, TemperatureUnits
from .base_tool import BaseTool


class HeatedExtruderTool(BaseTool):
    """Extruder tool implementation for 3D printing.

    This class handles operations for an extruder tool, including
    temperature control, filament retraction, and extrusion.
    """

    def activate(self, ctx: GContext):
        """Initialize and activate the extruder tool.

        Sets up the initial state of the extruder including:

        - Setting the hotend temperature
        - Waiting for the hotend to reach target temperature
        - Configuring absolute extrusion mode
        - Zeroing the extruder position

        Args:
            ctx (GContext): Current rendering context
        """

        units = TemperatureUnits.CELSIUS
        halt_mode = HaltMode.WAIT_FOR_HOTEND

        ctx.g.set_hotend_temperature(units, ctx.hotend_temperature)
        ctx.g.halt_program(halt_mode, S=ctx.hotend_temperature)
        ctx.g.set_extrusion_mode(ExtrusionMode.ABSOLUTE)
        ctx.g.set_home(E=0.0)

    def power_on(self, ctx: GContext):
        """Recover filament before tracing a path.

        Moves the filament forward by the configured retraction
        distance to prepare for printing.

        Args:
            ctx (GContext): Current rendering context
        """

        distance = ctx.length_units.scale(ctx.retract_length)
        current_position = ctx.g.current_position.get('E', 0.0)
        new_position = current_position + distance

        ctx.g.move(E=new_position, F=ctx.retract_speed)

    def power_off(self, ctx: GContext):
        """Retract filament after tracing a path.

        Retracts the filament by the configured distance to prevent
        oozing when moving without printing.

        Args:
            ctx (GContext): Current rendering context
        """

        distance = ctx.length_units.scale(ctx.retract_length)
        current_position = ctx.g.current_position.get('E', 0.0)
        new_position = current_position - distance

        ctx.g.move(E=new_position, F=ctx.retract_speed)

    def deactivate(self, ctx: GContext):
        """Deactivate the extruder tool.

        Turns off the hotend when the tool is no longer needed.

        Args:
            ctx (GContext): Current rendering context
        """

        units = TemperatureUnits.CELSIUS
        ctx.g.set_hotend_temperature(units, 0)

    def get_trace_params(self, ctx: GContext, x: float, y: float) -> dict:
        """Compute and set extruder parameters for work moves

        Computes the required extruder position based on the target
        coordinates and current position.

        Args:
            ctx (GContext): Current rendering context
            x (float): Target X coordinate of the movement
            y (float): Target Y coordinate of the movement

        Returns:
            dict: Dictionary with the extruder position set (E).
        """

        filament_length = self._filament_length(ctx, x, y)
        current_position = ctx.g.current_position.get('E', 0.0)
        new_position = current_position + filament_length

        return { 'E' : new_position }

    def _filament_length(self, ctx: GContext, x: float, y: float) -> float:
        """Calculates the required filament length for a move.

        This method calculates the length of filament needed to extrude
        for a given movement taking into account the filament length,
        nozzle diameter, and layer height.

        Args:
            ctx (GContext): Current rendering context
            x (float): Target X coordinate of the movement
            y (float): Target Y coordinate of the movement

        Returns:
            float: The required filament length in work units
        """

        cx, cy, cz = ctx.g.current_head_position

        radius = ctx.filament_diameter / 2.0
        cross_section = math.pi * radius * radius
        extrusion_area = ctx.nozzle_diameter * ctx.layer_height

        segment_length = math.hypot(x - cx, y - cy)
        extrusion_volume = extrusion_area * segment_length
        filament_length = extrusion_volume / cross_section

        return ctx.length_units.scale(filament_length)
