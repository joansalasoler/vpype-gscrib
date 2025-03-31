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

import inspect
from enum import Enum
from typing import Any

from click import Context, Option, Parameter, BadParameter
from click.core import ParameterSource
from vpype_cli import ChoiceType, LengthType

from vpype_gscrib.gscrib.enums import LengthUnits
from .builder_config import BuilderConfig
from .render_config import RenderConfig


class ConfigOption(Option):
    """
    Custom `click` option class that enforces units for length types
    and provides enhanced parameter handling.

    This class extends `click`'s `Option` class to provide:

    - Automatic unit enforcement for length parameters
    - Enhanced help text formatting
    - Support for enum choices
    - Default value handling from configuration

    Args:
        name (str): The name of the option
        **kwargs: Additional arguments passed to parent `Option`
    """

    _config_fields = (
        RenderConfig.model_fields |
        BuilderConfig.model_fields
    )

    def __init__(self, option_name: str, **kwargs):
        self._setup_option_params(option_name, kwargs)
        super().__init__(**kwargs)

    def override_default_value(self, default_value: Any) -> None:
        """Override the default value for the option."""

        self.default = default_value
        self.help = self._format_help_text(
            self._help_text, self.default, self.type)

    def _setup_option_params(self, option_name: str, kwargs: dict) -> None:
        """Setup parameters for the option."""

        option_type = kwargs.get("type")
        default_value = kwargs.get("default")
        help_text = kwargs.get("help", "")
        help_text = inspect.cleandoc(help_text)
        self._help_text = help_text

        kwargs["param_decls"] = [f"--{option_name}"]

        if "default" not in kwargs:
            default_value = self._default_for(option_name)
            kwargs["default"] = default_value

        if option_type is None:
            return

        if isinstance(option_type, LengthType):
            kwargs["callback"] = self._enforce_units

        if isinstance(option_type, type):
            if issubclass(option_type, Enum):
                kwargs["type"] = ChoiceType(option_type)

        kwargs["help"] = self._format_help_text(
            help_text, default_value, option_type)

    def _format_help_text(self, text: str, default: Any, otype: Any) -> str:
        """Append choices and default value to help text."""

        text = text.strip()
        units = LengthUnits.MILLIMETERS

        if isinstance(otype, LengthType):
            scale = round(units.scale(default), 6)
            return f"{text} [default: {scale}mm]"

        if isinstance(otype, type) and issubclass(otype, Enum):
            choices = ", ".join(s.value for s in otype)
            default_choice = f"[default: {default.value}]"
            return f"{text} Choices: {choices}. {default_choice}"

        return f"{text} [default: {default}]"

    @classmethod
    def _enforce_units(cls, ctx: Context, param: Parameter, value: Any) -> Any:
        """Ensure units are always provided for length types"""

        source = ctx.get_parameter_source(param.name)

        if source != ParameterSource.DEFAULT:
            str_value = str(value)

            if len(str_value) > 0 and not str_value[-1].isalpha():
                raise BadParameter(
                    f"Units are required for '{param.name}' (e.g., 10mm, 2in).")

        return value

    def _default_for(self, option_name: str) -> Any:
        """Obtain the default value for a parameter."""

        field_name = option_name.replace("-", "_")

        if field_name not in self._config_fields:
            raise ValueError(
                f"Default value is required for option: {field_name}")

        return self._config_fields[field_name].default
