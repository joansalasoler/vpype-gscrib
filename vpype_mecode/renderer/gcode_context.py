# -*- coding: utf-8 -*-
# pylint: disable=no-member

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

from dataclasses import asdict, FrozenInstanceError
from typeguard import typechecked
from vpype_mecode.builder.gcode_builder import GBuilder
from vpype_mecode.config import RenderConfig
from vpype_mecode.utils import BaseHeightMap, FlatHeightMap, RasterHeightMap
from vpype_mecode.enums import *


class GContext:
    """Context of the G-code generation.

    This class encapsulates all the configuration parameters needed
    for G-code generation, including units, speeds, z-axis positions,
    and machine-specific settings.

    Along with the `Gbuilder` instance it exposes all public fields from
    the provided `RenderConfig` as read-only properties. Values are
    automatically scaled according to the unit conventions below:

    - Times: seconds (will be scaled by `GBuilder`)
    - Lengths: pixels (will be scaled by `GBuilder`)
    - Speeds: units per minute (mm/min or in/min)

    Example:
        >>> ctx = GContext(builder, config)
        >>> print(config.work_speed)  # Speed in px/min
        >>> print(ctx.work_speed)  # Speed in units/min

    Args:
        builder (GBuilder): G-code builder instance
        config (RenderConfig): Configuration object
    """

    _scale_properties = (
        "work_speed",
        "plunge_speed",
        "travel_speed",
        "retract_speed",
    )

    @typechecked
    def __init__(self, builder: GBuilder, config: RenderConfig):
        """Initialize the G-code context.

        Args:
            builder (GBuilder): The G-code builder instance
            config (RenderConfig): Configuration object
        """

        self._g = builder
        self._config = config
        self._length_units = config.length_units
        self._height_map = self._build_height_map(config)
        self._init_properties(config)
        self._frozen = True

    @property
    def g(self) -> GBuilder:
        """The G-code builder instance"""

        return self._g

    @property
    def height_map(self) -> BaseHeightMap:
        """Height map instance for this context"""

        return self._height_map

    @typechecked
    def scale_length(self, length: float) -> float:
        """Scale a value to the configured length units.

        Args:
            length (float): A value to scale in pixels

        Returns:
            float: Scaled length value in the configured units
        """

        return self._length_units.scale(length)

    def format_config_values(self):
        """Return a formatted dictionary of configuration values"""

        return self._config.format_values(self._length_units)

    def _init_properties(self, config: RenderConfig):
        """Makes the config values availabe on this context"""

        for name, value in asdict(config).items():
            if name in self._scale_properties:
                value = self.scale_length(value)
            setattr(self, name, value)

    def _build_height_map(self, config: RenderConfig):
        """Builds a height map instance for a context."""

        if self._config.height_map_path is None:
            return FlatHeightMap()

        height_map = RasterHeightMap.from_path(config.height_map_path)
        height_map.set_tolerance(config.height_map_tolerance)
        height_map.set_scale(config.height_map_scale)

        return height_map

    def __setattr__(self, name, value):
        """Ensure all the properties of this class are read only"""

        if hasattr(self, "_frozen") and self._frozen:
            raise FrozenInstanceError(
                f"Cannot assign to field '{name}'.")

        super().__setattr__(name, value)
