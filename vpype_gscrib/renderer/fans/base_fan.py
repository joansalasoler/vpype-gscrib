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


class BaseFan(ABC):
    """Base class for controlling machine fans."""

    @abstractmethod
    def turn_on(self, ctx: GContext):
        """Activate the fan system.

        Generates G-code commands to turn on the fans.

        Args:
            ctx (GContext): The G-code generation context
        """

    @abstractmethod
    def turn_off(self, ctx: GContext):
        """Deactivate the fan system.

        Generates G-code commands to stop the fans.

        Args:
            ctx (GContext): The G-code generation context
        """
