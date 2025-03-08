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

from vpype_mecode.renderer.gcode_context import GContext
from vpype_mecode.enums import PowerMode
from .base_tool import BaseTool


class BeamTool(BaseTool):
    """Beam tool implementation.

    This class handles operations for a beam tool, such as a laser,
    including activation, power control, and deactivation.
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

        ctx.g.set_tool_power(ctx.power_level)
        ctx.g.sleep(ctx.time_units, ctx.warmup_delay)

    def power_off(self, ctx: GContext):
        """Power off the beam tool.

        Generates G-code commands to set the beam tool to its inactive
        power level and wait for the tool to cool down.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.set_tool_power(0)
        ctx.g.sleep(ctx.time_units, ctx.warmup_delay)

    def deactivate(self, ctx: GContext):
        """Deactivate the beam tool.

        Generates G-code commands to completely shut down the beam tool.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.power_off()
