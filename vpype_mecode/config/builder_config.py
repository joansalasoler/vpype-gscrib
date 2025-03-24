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

from pydantic import BaseModel, Field

from vpype_mecode.builder.enums import DirectWrite
from .base_config import BaseConfig


@dataclasses.dataclass
class BuilderConfig(BaseModel, BaseConfig):
    """
    Configuration settings for the G-code builder.

    This class stores various options that are passed directly to the
    `GCodeBuilder` instance, which is responsible for generating the G-Code.
    See the :doc:`command line reference </cli>` for detailed information
    about the properties of this class.

    Example:
        >>> params = { 'output': 'output.gcode' }
        >>> builder_config = BuilderConfig.model_validate(params)
        >>> print(builder_config.output)
    """

    # Output settings
    output: Optional[str] = Field(None)
    decimal_places: int = Field(5, ge=0)
    comment_symbols: str = Field("(")
    line_endings: str = Field("os")
    print_lines: bool | str = Field(False)

    # Direct write settings
    direct_write: DirectWrite = Field(DirectWrite.OFF)
    host: str = Field("localhost")
    port: str = Field("8000")
    baudrate: int = Field(250000, ge=0)

    # Axis naming settings
    x_axis: str = Field("X")
    y_axis: str = Field("Y")
    z_axis: str = Field("Z")
