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

from .base_coolant import BaseCoolant
from .flood_coolant import FloodCoolant
from .mist_coolant import MistCoolant
from .off_coolant import OffCoolant
from vpype_mecode.enums import CoolantMode


class CoolantFactory:

    @classmethod
    def create(self, mode: CoolantMode) -> BaseCoolant:
        providers = {
            CoolantMode.OFF: OffCoolant,
            CoolantMode.MIST: MistCoolant,
            CoolantMode.FLOOD: FloodCoolant,
        }

        return providers[mode]()
