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

from .base_enum import BaseEnum


class HaltMode(BaseEnum):
    """Program termination and pause modes."""

    OFF = 'off'
    PAUSE = 'pause'
    OPTIONAL_PAUSE = 'optional_pause'
    END_WITHOUT_RESET = 'end_without_reset'
    END_WITH_RESET = 'end_with_reset'
    PALLET_EXCHANGE_AND_END = 'pallet_exchange_and_end'
    WAIT_FOR_BED_TEMP = 'wait_for_bed_temp'
