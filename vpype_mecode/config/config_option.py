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

from click import Context, Option, Parameter, BadParameter
from click.core import ParameterSource
from vpype_cli import ChoiceType, LengthType
from typing import Any
from enum import Enum

from vpype_mecode.enums import LengthUnits
from . import RenderConfig, MecodeConfig


class ConfigOption(Option):
    """
    Custom Click option class that enforces units for length types and
    provides enhanced parameter handling.

    This class extends Click's Option class to provide:

    - Automatic unit enforcement for length parameters
    - Enhanced help text formatting
    - Support for enum choices
    - Default value handling from configuration

    Args:
        name (str): The name of the option
        **kwargs: Additional arguments passed to Click's Option
    """

    _config_fields = (
        RenderConfig.model_fields |
        MecodeConfig.model_fields
    )

    def __init__(self, name: str, **kwargs):
        self._setup_option_params(name, kwargs)
        super().__init__(**kwargs)

    def _setup_option_params(self, name: str, kwargs: dict) -> None:
        """Setup parameters for the option."""

        option_type = kwargs.get('type')
        help_text = kwargs.get('help', '')
        default_value = self._default_for(name)

        kwargs['default'] = default_value
        kwargs['param_decls'] = [f'--{name}']

        if option_type is None:
            return

        if isinstance(option_type, LengthType):
            kwargs['callback'] = self._enforce_units

        if isinstance(option_type, type):
            if issubclass(option_type, Enum):
                kwargs['type'] = ChoiceType(option_type)

        kwargs['help'] = self._format_help_text(
            help_text, default_value, option_type)

    def _format_help_text(self, text: str, default: Any, otype: Any) -> str:
        """Append choices and default value to help text."""

        text = text.strip()
        units = LengthUnits.MILLIMETERS

        if isinstance(otype, LengthType):
            scale = round(units.scale(default), 6)
            return f'{text} [default: {scale}mm]'

        if isinstance(otype, type) and issubclass(otype, Enum):
            choices = ', '.join(s.value for s in otype)
            default_choice = f'[default: {default.value}]'
            return f'{text} Choices: {choices}. {default_choice}'

        return f'{text} [default: {default}]'

    @classmethod
    def _enforce_units(cls, ctx: Context, param: Parameter, value: Any) -> Any:
        """Ensure units are always provided for length types"""

        source = ctx.get_parameter_source(param.name)

        if source != ParameterSource.DEFAULT:
            str_value = str(value)

            if len(str_value) and not str_value[-1].isalpha():
                raise BadParameter(
                    f'Units are required (e.g., 10mm, 2in).')

        return value

    @classmethod
    def _default_for(cls, field_name: str) -> Any:
        """Obtain the default value for a parameter."""

        return cls._config_fields[field_name].default
