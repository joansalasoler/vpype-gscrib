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

from .base_bed import BaseBed
from .off_bed import OffBed
from .heated_bed import HeatedBed
from vpype_mecode.enums import BedMode


class BedFactory:
    """A factory for creating bed managers.

    This factory creates specialized bed managers that handle the
    control of machine beds/tables.
    """

    @classmethod
    def create(self, mode: BedMode) -> BaseBed:
        """Create a new bed manger instance.

        Args:
            mode (BedMode): Bed mode.

        Returns:
            BaseBed: Bed manger instance.

        Raises:
            KeyError: If mode is not valid.
        """

        providers = {
            BedMode.OFF: OffBed,
            BedMode.HEATED: HeatedBed,
        }

        return providers[mode]()
