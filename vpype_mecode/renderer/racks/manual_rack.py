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

from vpype_mecode.enums import RackMode
from vpype_mecode.builder.enums import HaltMode
from vpype_mecode.renderer.gcode_context import GContext
from .base_rack import BaseRack


class ManualRack(BaseRack):
    """Manual tool rack implementation.

    This class handles tool changes manually, requiring operator
    intervention to change tools.
    """

    def change_tool(self, ctx: GContext):
        """Execute a manual tool change operation.

        Generates G-code commands to pause the program and prompt the
        operator to change the tool manually.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.tool_change(RackMode.MANUAL, ctx.tool_number)
        ctx.g.halt_program(HaltMode.PAUSE)
