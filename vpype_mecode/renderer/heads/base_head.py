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
from ..gcode_context import GContext


class BaseHead(ABC):

    @abstractmethod
    def safe_retract(self, ctx: GContext):
        pass

    @abstractmethod
    def retract(self, ctx: GContext):
        pass

    @abstractmethod
    def plunge(self, ctx: GContext):
        pass

    @abstractmethod
    def travel_to(self, ctx: GContext, x: float, y: float):
        pass

    @abstractmethod
    def trace_to(self, ctx: GContext, x: float, y: float):
        pass

    @abstractmethod
    def park_for_service(self, ctx: GContext):
        pass
