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

from .base_head import BaseHead
from ..gcode_context import GContext


class BasicHead(BaseHead):

    def safe_retract(self, ctx: GContext):
        ctx.g.rapid(z=ctx.safe_z)

    def retract(self, ctx: GContext):
        ctx.g.rapid(z=ctx.safe_z)

    def plunge(self, ctx: GContext):
        ctx.g.move(z=ctx.plunge_z, F=ctx.travel_speed)
        ctx.g.move(z=ctx.work_z, F=ctx.plunge_speed)

    def travel_to(self, ctx: GContext, x: float, y: float):
        ctx.g.move(x=x, y=y, F=ctx.travel_speed)

    def trace_to(self, ctx: GContext, x: float, y: float):
        ctx.g.move(x=x, y=y, F=ctx.work_speed)

    def park_for_service(self, ctx: GContext):
        ctx.g.rapid(z=ctx.safe_z)
        ctx.g.rapid_absolute(x=0, y=0)
