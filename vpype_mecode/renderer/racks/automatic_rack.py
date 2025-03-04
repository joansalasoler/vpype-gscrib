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
from vpype_mecode.renderer.gcode_context import GContext
from .base_rack import BaseRack


class AutomaticRack(BaseRack):
    """Automatic tool rack implementation.

    This class handles tool changes automatically using the machine's
    built-in tool change capabilities.
    """

    def change_tool(self, ctx: GContext):
        """Execute an automatic tool change operation.

        Generates G-code commands to perform a tool change using the
        machine's automatic tool changer.

        Args:
            ctx (GContext): The G-code generation context
        """

        ctx.g.tool_change(RackMode.AUTOMATIC, ctx.tool_number)
