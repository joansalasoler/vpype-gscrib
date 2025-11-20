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

import dataclasses
from typing import Optional

import pydantic
from pydantic import BaseModel, Field

from vpype_gscrib.enums import *
from gscrib.enums import *
from .base_config import BaseConfig
from .custom_fields import LengthField, PathField


@dataclasses.dataclass
class RenderConfig(BaseModel, BaseConfig):
    """
    Configuration settings for G-Code generation.

    This class defines motion parameters, spindle settings, and Z-axis
    positions. The default values are chosen to be safe for a variety of
    CNC machines, including milling machines, pen plotters, laser
    engravers, and 3D printers. See the :doc:`command line reference </cli>`
    for detailed information about the properties of this class.

    Example:
        >>> params = { 'length_units': 'mm' }
        >>> renderer_config = RenderConfig.model_validate(params)
        >>> print(renderer_config.length_units)
    """

    # Custom program header and footer
    header_gcode: Optional[str] = PathField(None)
    footer_gcode: Optional[str] = PathField(None)

    # Length and time units
    length_units: LengthUnits = Field(LengthUnits.MILLIMETERS)
    time_units: TimeUnits = Field(TimeUnits.SECONDS)

    # Machine components modes
    coolant_type: CoolantType = Field(CoolantType.OFF)
    head_type: HeadType = Field(HeadType.STANDARD)
    rack_type: RackType = Field(RackType.MANUAL)
    tool_type: ToolType = Field(ToolType.MARKER)
    bed_type: BedType = Field(BedType.OFF)
    fan_type: FanType = Field(FanType.OFF)

    # Tool parameters
    spin_mode: SpinMode = Field(SpinMode.CLOCKWISE)
    power_mode: PowerMode = Field(PowerMode.CONSTANT)
    power_level: int = Field(50.0, ge=0)
    spindle_rpm: int = Field(1000, ge=0)
    warmup_delay: float = Field(2.0, ge=0.001)
    tool_number: int = Field(1, ge=1)

    # Motion parameters
    work_speed: float = LengthField("500mm", "px/min", ge=0)
    plunge_speed: float = LengthField("100mm", "px/min", ge=0)
    travel_speed: float = LengthField("1000mm", "px/min", ge=0)
    retract_speed: float = LengthField("2100mm", "px/min", ge=0)

    # Fan parameters
    fan_speed: int = Field(255, ge=0, le=255)

    # Bed and hotend parameters
    bed_temperature: int = Field(60)
    hotend_temperature: int = Field(120)

    # Predefined Z-axis positions
    work_z: float = LengthField("0mm", "px")
    plunge_z: float = LengthField("1mm", "px")
    safe_z: float = LengthField("10mm", "px")
    park_z: float = LengthField("50mm", "px")

    # Extrusion parameters
    nozzle_diameter: float = LengthField("0.4mm", "px", gt=0)
    filament_diameter: float = LengthField("1.75mm", "px", gt=0)
    layer_height: float = LengthField("0.2mm", "px", gt=0)
    retract_length: float = LengthField("1.5mm", "px", ge=0)

    # Heightmap transformation parameters
    height_map_path: Optional[str] = PathField(None)
    height_map_scale: float = Field(1.0, gt=0)
    height_map_tolerance: float = LengthField("0.1mm", "px", ge=0)

    # Path interpolation parameters
    resolution: float = LengthField("0.1mm", "px", gt=0)

    @pydantic.model_validator(mode="after")
    def validate_field_values(self) -> BaseConfig:
        """Validate field values are consistent."""

        self.validate_ge(self, "plunge_z", "work_z")
        self.validate_ge(self, "safe_z", "work_z")
        self.validate_ge(self, "park_z", "safe_z")

        return self
