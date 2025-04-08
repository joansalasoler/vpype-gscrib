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

import os
from abc import ABC
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any
from typeguard import typechecked

from gscrib.enums import LengthUnits
from .custom_fields import LengthFieldInfo, PathFieldInfo


@dataclass
class BaseConfig(ABC):
    """
    Abstract base class defining the interface for configuration objects.
    """

    @classmethod
    def validate_gt(cls, model: "BaseConfig", f1: str, f2: str):
        """Validate a field value is greater than another."""

        if getattr(model, f1) <= getattr(model, f2):
            raise ValueError(f"'{f1}' must be greater than '{f2}'")

    @classmethod
    def validate_ge(cls, model: "BaseConfig", f1: str, f2: str):
        """Validate a field value is greater or equal to another."""

        if getattr(model, f1) < getattr(model, f2):
            raise ValueError(f"'{f1}' must be greater or equal to '{f2}'")

    @typechecked
    def format_values(self, units: LengthUnits) -> Dict[str, str]:
        """
        Format configuration values for display.

        If applicable, numeric values are scaled to the given units,
        rounded to 6 decimal places and their units appended if the
        field is of type `LengthField`.

        Args:
            units (LengthUnits): The work units to use for formatting.

        Returns:
            Dict[str, str]: A dictionary containing the formatted
            configuration values.
        """

        return {
            field_name: self._format_value(field_name, value, units)
            for field_name, value in asdict(self).items()
        }

    def _format_value(self, field_name: str, value: Any, units: LengthUnits) -> str:
        """Format a single value as a human-readable string."""

        field_info = None

        if hasattr(self, "model_fields"):
            model_fields = getattr(self, "model_fields")
            field_info = model_fields[field_name]

        if isinstance(field_info, LengthFieldInfo):
            px_units = field_info._length_units_string
            units_str = self._length_units_short(units)
            work_units = px_units.replace("px", units_str)
            value = round(units.scale(value), 6)
            return f"{value} {work_units}"

        if isinstance(field_info, PathFieldInfo):
            return str(value) if not value else os.path.relpath(value)

        if isinstance(value, (int, float)):
            return str(round(value, 6))

        if isinstance(value, Enum):
            return value.value

        return str(value)

    def _length_units_short(self, units: LengthUnits) -> str:
        """Short representation of the given length units."""

        if units == LengthUnits.INCHES:
            return "in"

        if units == LengthUnits.MILLIMETERS:
            return "mm"

        return units.value
