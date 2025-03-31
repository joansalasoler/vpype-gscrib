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

from vpype_gscrib.enums import FanType

from .base_fan import BaseFan
from .cooling_fan import CoolingFan
from .no_fan import NoFan


class FanFactory:
    """A factory for creating fan managers."""

    @classmethod
    def create(cls, fan_type: FanType) -> BaseFan:
        """Create a new fan manger instance.

        Args:
            fan_type (FanType): Fan type.

        Returns:
            BaseFan: Fan manger instance.

        Raises:
            KeyError: If type is not valid.
        """

        providers = {
            FanType.COOLING: CoolingFan,
            FanType.OFF: NoFan,
        }

        return providers[fan_type]()
