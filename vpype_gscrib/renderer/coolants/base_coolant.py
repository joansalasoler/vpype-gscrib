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


class BaseCoolant(ABC):
    """Base class for coolant system implementations.

    This abstract base class defines the interface for controlling
    machine coolant systems. It handles the activation and deactivation
    of cooling mechanisms like mist coolant, flood coolant, or air
    blast systems.

    Different machines may implement cooling differently:

    - Some machines support multiple coolant types (mist/flood)
    - Some machines might require warmup or cooldown sequences
    - Air blast systems might need pressure ramping
    """

    @abstractmethod
    def turn_on(self, ctx: GContext):
        """Activate the coolant system.

        Generates G-code commands to start the coolant flow.

        Args:
            ctx (GContext): The G-code generation context
        """

    @abstractmethod
    def turn_off(self, ctx: GContext):
        """Deactivate the coolant system.

        Generates G-code commands to stop the coolant flow.

        Args:
            ctx (GContext): The G-code generation context
        """
