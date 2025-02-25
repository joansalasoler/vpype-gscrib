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

import vpype as vp
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional

from .base_config import BaseConfig
from vpype_mecode.enums import DirectWriteMode


@dataclass
class MecodeConfig(BaseModel, BaseConfig):
    """
    Configuration settings for the `mecode` library.

    This class stores various options that are passed directly to the
    `mecode` library, which is responsible for generating the G-Code.
    See the `vpype_options` module.
    """

    # Predefined settings (do not change!)
    setup: bool = Field(False)
    absolute: bool = Field(True)
    print_lines: bool | str = Field('auto')

    # Output settings
    outfile: Optional[str] = Field(None)
    header: Optional[str] = Field(None)
    footer: Optional[str] = Field(None)
    aerotech_include: bool = Field(False)
    output_digits: int = Field(6, ge=0)
    lineend: str = Field('os')
    comment_char: str = Field('(')

    # Direct write settings
    direct_write: bool = Field(False)
    direct_write_mode: DirectWriteMode = Field(DirectWriteMode.SOCKET)
    printer_host: str = Field('localhost')
    printer_port: int = Field(8000, ge=0)
    baudrate: int = Field(250000, ge=0)
    two_way_comm: bool = Field(False)

    # Axis naming settings
    x_axis: str = Field('X')
    y_axis: str = Field('Y')
    z_axis: str = Field('Z')
    i_axis: str = Field('I')
    j_axis: str = Field('J')
    k_axis: str = Field('K')

    # 3D printing settings
    extrude: bool = Field(False)
    filament_diameter: float = Field(vp.convert_length('1.75mm'))
    layer_height: Optional[float] = Field(vp.convert_length('0.19mm'))
    extrusion_width: Optional[float] = Field(vp.convert_length('0.35mm'))
    extrusion_multiplier: float = Field(1.0)


    # Vpype's default unit of measure is pixels, so we may need to
    # convert some values to work units (millimeters or inches).

    _fields_with_px_units = {
        'extrusion_width': 'px',
        'filament_diameter': 'px',
        'layer_height': 'px',
    }