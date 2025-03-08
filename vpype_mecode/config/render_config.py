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
import vpype as vp
from pydantic import BaseModel, Field

from vpype_mecode.enums import *
from .base_config import BaseConfig


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

    # Length and time units
    length_units: LengthUnits = Field(LengthUnits.MILLIMETERS)
    time_units: TimeUnits = Field(TimeUnits.SECONDS)

    # Machine components modes
    coolant_mode: CoolantMode = Field(CoolantMode.OFF)
    head_mode: HeadMode = Field(HeadMode.BASIC)
    power_mode: PowerMode = Field(PowerMode.CONSTANT)
    rack_mode: RackMode = Field(RackMode.MANUAL)
    spin_mode: SpinMode = Field(SpinMode.CLOCKWISE)
    tool_mode: ToolMode = Field(ToolMode.MARKER)
    bed_mode: BedMode = Field(BedMode.OFF)
    fan_mode: FanMode = Field(FanMode.OFF)

    # Tool parameters
    power_level: int = Field(50.0, ge=0)
    spindle_rpm: int = Field(1000, ge=0)
    warmup_delay: float = Field(2.0, ge=0.001)
    tool_number: int = Field(1, ge=1)

    # Motion parameters
    work_speed: float = Field(vp.convert_length('500mm'), ge=0)
    plunge_speed: float = Field(vp.convert_length('100mm'), ge=0)
    travel_speed: float = Field(vp.convert_length('1000mm'), ge=0)

    # Fan parameters
    fan_speed: int = Field(255, ge=0, le=255)

    # Bed parameters
    bed_temperature: int = Field(60)

    # Predefined Z-axis positions
    work_z: float = Field(vp.convert_length('0mm'))
    plunge_z: float = Field(vp.convert_length('1mm'))
    safe_z: float = Field(vp.convert_length('10mm'))
    park_z: float = Field(vp.convert_length('50mm'))

    # Heightmap transformation parameters
    height_map: Optional[str] = Field(None)
    height_map_scale: float = Field(50.0, gt=0)
    height_map_tolerance: float = Field(0.01, ge=0)


    @pydantic.model_validator(mode="after")
    @classmethod
    def validate_field_values(cls, model: BaseConfig) -> BaseConfig:
        """Validate field values are consistent."""

        cls.validate_ge(model, 'plunge_z', 'work_z')
        cls.validate_ge(model, 'safe_z', 'work_z')
        cls.validate_ge(model, 'park_z', 'safe_z')

        return model


    # Vpype's default unit of measure is pixels, so we may need to
    # convert some values to work units (millimeters or inches).

    _fields_with_px_units = {
        'work_speed': 'px/min',
        'plunge_speed': 'px/min',
        'travel_speed': 'px/min',
        'work_z': 'px',
        'plunge_z': 'px',
        'safe_z': 'px',
        'park_z': 'px',
    }
