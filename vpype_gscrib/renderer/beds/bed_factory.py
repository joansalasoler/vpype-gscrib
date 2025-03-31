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

from vpype_gscrib.enums import BedType

from .base_bed import BaseBed
from .heated_bed import HeatedBed
from .no_bed import NoBed


class BedFactory:
    """A factory for creating bed managers.

    This factory creates specialized bed managers that handle the
    control of machine beds/tables.
    """

    @classmethod
    def create(cls, bed_type: BedType) -> BaseBed:
        """Create a new bed manger instance.

        Args:
            bed_type (BedType): Bed type.

        Returns:
            BaseBed: Bed manger instance.

        Raises:
            KeyError: If type is not valid.
        """

        providers = {
            BedType.OFF: NoBed,
            BedType.HEATED: HeatedBed,
        }

        return providers[bed_type]()
