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


class SpindleTool(BaseTool):
    """Spindle tool implementation.

    This class handles operations for a spindle tool, including
    activation and deactivation.
    """

    def activate(self, ctx: GContext):
        """Activate the spindle tool.

        Generates G-code commands to initialize and prepare the spindle
        tool for operation, setting the spindle speed, operation mode
        (clockwise or counterclockwise), turning it on and waiting for
        the tool to warm-up.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.tool_on(ctx.spin_mode, ctx.spindle_rpm)
        ctx.g.sleep(ctx.warmup_delay)

    def deactivate(self, ctx: GContext):
        """Deactivate the spindle tool.

        Generates G-code commands to completely shut down the spindle
        tool and wait for it to cool stop.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.tool_off()
        ctx.g.sleep(ctx.warmup_delay)

    def power_on(self, ctx: GContext):
        pass

    def power_off(self, ctx: GContext):
        pass
