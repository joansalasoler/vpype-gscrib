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
from vpype_mecode.renderer.gcode_context import GContext


class BaseHead(ABC):
    """Base class for machine head movement implementations.

    This abstract base class defines the interface for controlling the
    movement of the machine's head (tool carrier). It handles all axis
    movements including safe positioning, rapid travels, and controlled
    motion paths. The movement is independent of the tool operation.
    """

    @abstractmethod
    def safe_retract(self, ctx: GContext):
        """Move the head to a safe Z height.

        Generates G-code commands for a Z-axis retraction to a safe
        height. This is typically used to move the head out of the way
        of the workpiece or to a height where it can be safely moved
        to a different location.

        Args:
            ctx (GContext): The G-code generation context
        """

        pass

    @abstractmethod
    def retract(self, ctx: GContext):
        """Move the head to the normal Z travel height.

        Generates G-code commands for normal Z-axis retraction used
        between regular operations.

        Args:
            ctx (GContext): The G-code generation context
        """

        pass

    @abstractmethod
    def plunge(self, ctx: GContext):
        """Lower the head to the working height.

        Generates G-code commands to move the Z-axis down to the
        configured working height for the current operation.

        Args:
            ctx (GContext): The G-code generation context
        """

        pass

    @abstractmethod
    def travel_to(self, ctx: GContext, x: float, y: float):
        """Move the head to a new XY position.

        Generates G-code commands for positioning the head to a new
        XY position. Used for non-working movements between operations.

        Args:
            ctx (GContext): The G-code generation context
            x (float): Target X coordinate in current coordinate system.
            y (float): Target Y coordinate in current coordinate system.
        """

        pass

    @abstractmethod
    def trace_to(self, ctx: GContext, x: float, y: float):
        """Move the head to a new XY position using controlled movement.

        Generates G-code commands for controlled, working moves. Used
        for actual cutting, drawing, or other operations where the tool
        is actively working.

        Args:
            ctx (GContext): The G-code generation context
            x (float): Target X coordinate in current coordinate system.
            y (float): Target Y coordinate in current coordinate system.
        """

        pass

    @abstractmethod
    def park_for_service(self, ctx: GContext):
        """Move the head to the machine's service/parking position.

        Generates G-code commands to safely move the head to a position
        suitable for tool changes, maintenance, or end of operation.
        This typically involves moving the head to a safe Z height and
        then moving to a predefined XY position.

        Args:
            ctx (GContext): The G-code generation context
        """

        pass
