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

from enum import Enum


class BaseEnum(str, Enum):
    """Base for all the G-Code enumerations."""

    def get_instruction(self):
        """Obtain the G-Code instruction code"""

        from .codes_table import codes_table
        key = (type(self), self)
        return codes_table[key][0]

    def get_description(self):
        """Obtain the G-Code instruction comment"""

        from .codes_table import codes_table
        key = (type(self), self)
        return codes_table[key][1]
