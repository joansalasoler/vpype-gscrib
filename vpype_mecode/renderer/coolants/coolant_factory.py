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

from vpype_mecode.enums import CoolantType

from .base_coolant import BaseCoolant
from .flood_coolant import FloodCoolant
from .mist_coolant import MistCoolant
from .no_coolant import NoCoolant


class CoolantFactory:
    """A factory for creating coolant managers.

    This factory creates specialized coolant managers that handle the
    control of coolant systems in CNC machines. Coolant managers control
    the flow of cutting fluid or coolant during machining operations to
    reduce heat, clear chips, and extend tool life.
    """

    @classmethod
    def create(cls, coolant_type: CoolantType) -> BaseCoolant:
        """Create a new coolant manger instance.

        Args:
            coolant_type (CoolantType): Coolant type.

        Returns:
            BaseCoolant: Coolant manger instance.

        Raises:
            KeyError: If type is not valid.
        """

        providers = {
            CoolantType.OFF: NoCoolant,
            CoolantType.MIST: MistCoolant,
            CoolantType.FLOOD: FloodCoolant,
        }

        return providers[coolant_type]()
