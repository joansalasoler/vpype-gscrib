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

from typing import Any
from pydantic.fields import FieldInfo
import vpype as vp


class LengthFieldInfo(FieldInfo):
    """Field info for length values that stores length units."""

    def __init__(self, default: float, units: str, **kwargs: Any) -> None:
        self._length_units_string = units
        super().__init__(default=default, **kwargs)


class PathFieldInfo(FieldInfo):
    """Field info for file path values."""

    def __init__(self, default: float | None, **kwargs: Any) -> None:
        super().__init__(default=default, **kwargs)


def LengthField(default: str, units: str, **kwargs):
    """Field for length values that stores their values in pixels."""

    length_in_px = vp.convert_length(default)
    return LengthFieldInfo(length_in_px, units, **kwargs)


def PathField(default: str | None, **kwargs):
    """Field for file path values."""

    return PathFieldInfo(default, **kwargs)
