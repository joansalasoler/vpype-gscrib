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

from vpype_mecode.enums import RackType

from .automatic_rack import AutomaticRack
from .base_rack import BaseRack
from .manual_rack import ManualRack
from .no_rack import NoRack


class RackFactory:
    """A factory for creating tool rack managers.

    This factory creates specialized managers that handle tool rack
    operations. Rack managers control the tool in use and the changing
    process, including picking up and putting away tools from/to an
    automatic tool changer (ATC) or providing instructions for manual
    tool changes.
    """

    @classmethod
    def create(cls, rack_type: RackType) -> BaseRack:
        """Create a new tool rack manger instance.

        Args:
            rack_type (RackType): Rack type.

        Returns:
            BaseRack: Rack manger instance.

        Raises:
            KeyError: If type is not valid.
        """

        providers = {
            RackType.OFF: NoRack,
            RackType.MANUAL: ManualRack,
            RackType.AUTOMATIC: AutomaticRack,
        }

        return providers[rack_type]()
