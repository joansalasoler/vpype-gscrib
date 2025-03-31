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

from abc import ABC, abstractmethod
from vpype_gscrib.renderer.gcode_context import GContext


class BaseBed(ABC):
    """Base class for controlling machine bed/table.

    This abstract base class defines the interface for controlling
    bed-related functionalities such as heating, cooling, material
    holding, and leveling. It provides methods to prepare the bed
    and manage its state during operation.
    """

    @abstractmethod
    def turn_on(self, ctx: GContext):
        """Activate the bed system.

        Generates G-code commands to prepare the bed.

        Args:
            ctx (GContext): The G-code generation context
        """

    @abstractmethod
    def turn_off(self, ctx: GContext):
        """Deactivate the bed system.

        Generates G-code commands to stop the bed.

        Args:
            ctx (GContext): The G-code generation context
        """
