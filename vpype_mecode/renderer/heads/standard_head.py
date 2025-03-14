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
from .base_head import BaseHead


class StandardHead(BaseHead):
    """Standard machine head implementation.

    This class handles basic operations for controlling the machine's
    head, including safe retraction, plunging, traveling, tracing, and
    parking for service.
    """

    def safe_retract(self, ctx: GContext):
        """Retract the machine head to a safe height.

        Generates G-code commands to move the machine head to a safe
        height using rapid moves.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.rapid(z=ctx.safe_z)

    def retract(self, ctx: GContext):
        """Retract the machine head.

        Generates G-code commands to move the machine head to a safe
        height using rapid moves.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.rapid(z=ctx.safe_z)

    def plunge(self, ctx: GContext):
        """Plunge the machine head to the work height.

        Generates G-code commands to move the machine head to the
        plunge height at travel speed and then to the work height at
        controlled plunge speed.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.move(z=ctx.plunge_z, F=ctx.travel_speed)
        ctx.g.move(z=ctx.work_z, F=ctx.plunge_speed)

    def travel_to(self, ctx: GContext, x: float, y: float):
        """Move the machine head to a specified position.

        Generates G-code commands to move the machine head to the
        specified (x, y) coordinates at the configured travel speed.

        Args:
            ctx (GContext): The G-code generation context
            x (float): The target x-coordinate
            y (float): The target y-coordinate
        """

        ctx.g.move(x=x, y=y, F=ctx.travel_speed)

    def trace_to(self, ctx: GContext, x: float, y: float, tool_params: dict):
        """Trace a path to a specified position at work speed.

        Generates G-code commands to move the machine head to the
        specified (x, y) coordinates at the configured work speed.

        Args:
            ctx (GContext): The G-code generation context
            x (float): The target x-coordinate
            y (float): The target y-coordinate
            tool_params (dict): Tool-specific parameters
        """

        params = { "F": ctx.work_speed, **tool_params }
        ctx.g.move(x=x, y=y, **params)

    def park_for_service(self, ctx: GContext):
        """Park the machine head for service.

        Generates G-code commands to move the machine head to a safe
        height and then to the absolute home position (0, 0) for service
        using rapid moves.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.rapid(z=ctx.safe_z)
        park_z = ctx.scale_length(ctx.park_z)
        ctx.g.rapid_absolute(x=0, y=0, z=park_z)
