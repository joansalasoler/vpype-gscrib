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

from vpype_gscrib.renderer.gcode_context import GContext
from .base_tool import BaseTool


class AdaptiveBeamTool(BaseTool):
    """Beam implementation with height map-based power modulation.

    This class handles basic operations for controlling the machine's
    beam tool with power adjustments based on a height map. All work
    movements are processed with the height map to modify beam power,
    which enables various applications such as:

    - Photo engraving: Converts grayscale images into varying beam
      intensities to create detailed photographic engravings.
    - Surface processing: Maintains consistent cutting/engraving depth
      on uneven surfaces by automatically modulating beam power.
    - Material adaptation: Maintains consistent cutting depth across
      materials with varying thickness or density.
    - Artistic effects: Uses height maps as power maps to create
      controlled variations in cutting or engraving intensity.
    """

    def activate(self, ctx: GContext):
        """Activate the beam tool.

        Generates G-code commands to initialize and prepare the beam
        tool for operation, setting initial power level to zero.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.power_on(ctx.power_mode, 0)

    def power_on(self, ctx: GContext):
        """Power on the beam tool.

        Generates G-code commands to set the beam tool to its working
        power level and wait for the tool to warm up.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.sleep(ctx.warmup_delay)

    def power_off(self, ctx: GContext):
        """Power off the beam tool.

        Generates G-code commands to set the beam tool to its inactive
        power level and wait for the tool to cool down.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.set_tool_power(0)
        ctx.g.sleep(ctx.warmup_delay)

    def deactivate(self, ctx: GContext):
        """Deactivate the beam tool.

        Generates G-code commands to completely shut down the beam tool.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.power_off()

    def get_trace_params(self, ctx: GContext, x: float, y: float) -> dict:
        """Sets the beam power according to the height map.

        This method sets the appropriate beam power parameter for the
        current position being traced by querying the height map. The
        power level is adjusted based on the height value at the specified
        coordinates and the heightmap scaling factor.

        Args:
            ctx (GContext): Current rendering context
            x (float): Target X coordinate of the movement
            y (float): Target Y coordinate of the movement

        Returns:
            dict: Dictionary with the power parameter set (S).
        """

        z_in_pixels = ctx.height_map.get_depth_at(x, y)
        z_in_units = ctx.scale_length(z_in_pixels)

        return { "S": z_in_units }
