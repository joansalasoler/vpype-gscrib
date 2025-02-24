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

from .base_tool import BaseTool
from ..gcode_context import GContext
from vpype_mecode.enums import SpinMode


class BeamTool(BaseTool):

    def activate(self, ctx: GContext):
        ctx.g.tool_on(SpinMode.CLOCKWISE, 0)

    def power_on(self, ctx: GContext):
        ctx.g.set_tool_power(ctx.power_level)
        ctx.g.sleep(ctx.time_units, ctx.warmup_delay)

    def power_off(self, ctx: GContext):
        ctx.g.set_tool_power(0)
        ctx.g.sleep(ctx.time_units, ctx.warmup_delay)

    def deactivate(self, ctx: GContext):
        ctx.g.tool_off()
