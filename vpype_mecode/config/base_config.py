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

from abc import ABC
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any

from ..enums import LengthUnits


@dataclass
class BaseConfig(ABC):
    """Base class for configuration settings."""

    def scale_units(self, units: LengthUnits) -> None:
        """Scale numeric values according to the specified work units."""

        for field_name, px_units in self._fields_with_px_units.items():
            value = units.scale(getattr(self, field_name))
            setattr(self, field_name, value)

    def format_values(self, units: LengthUnits) -> Dict[str, str]:
        """Get configuration values as a human-readable dictionary."""

        return {
            field_name: self._format_value(field_name, value, units)
            for field_name, value in asdict(self).items()
        }

    def _format_value(self, field_name: str, value: Any, units: LengthUnits) -> str:
        """Format a single value as a human-readable string."""

        if hasattr(self, '_fields_with_px_units') \
           and field_name in self._fields_with_px_units:
            px_units = self._fields_with_px_units[field_name]
            work_units = px_units.replace('px', units.value)
            value = round(units.scale(value), 6)
            return f'{value} {work_units}'

        if isinstance(value, (int, float)):
            return str(round(value, 6))

        if isinstance(value, Enum):
            return value.value

        return str(value)
