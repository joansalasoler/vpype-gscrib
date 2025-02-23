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

from .gcode_builder import GBuilder
from ..enums import LengthUnits, TimeUnits
from ..config import RenderConfig


class GContext():

    def __init__(self, builder: GBuilder, config: RenderConfig):
        self._g = builder

        self._length_units = config.length_units
        self._time_units = config.time_units
        self._power_level = config.power_level
        self._spindle_rpm = config.spindle_rpm
        self._warmup_delay = config.warmup_delay

        self._work_z = config.work_z
        self._safe_z = config.safe_z
        self._plunge_z = config.plunge_z

        self._work_speed = self.scale_length(config.work_speed)
        self._plunge_speed = self.scale_length(config.plunge_speed)
        self._travel_speed = self.scale_length(config.travel_speed)

    @property
    def g(self) -> GBuilder:
        return self._g

    @property
    def length_units(self) -> LengthUnits:
        return self._length_units

    @property
    def time_units(self) -> TimeUnits:
        return self._time_units

    @property
    def power_level(self) -> float:
        return self._power_level

    @property
    def spindle_rpm(self) -> float:
        return self._spindle_rpm

    @property
    def warmup_delay(self) -> float:
        return self._warmup_delay

    @property
    def work_z(self) -> float:
        return self._work_z

    @property
    def safe_z(self) -> float:
        return self._safe_z

    @property
    def plunge_z(self) -> float:
        return self._plunge_z

    @property
    def work_speed(self) -> float:
        return self._work_speed

    @property
    def plunge_speed(self) -> float:
        return self._plunge_speed

    @property
    def travel_speed(self) -> float:
        return self._travel_speed

    def scale_length(self, length: float) -> float:
        return self._length_units.scale(length)
