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

from typing import List

import click
from click import Command
from vpype import ConfigManager, Document
from vpype_cli import State

from .render_config import RenderConfig


class ConfigLoader:
    """Utility class for loading and parsing configuration files.

    This class manages the loading of settings from TOML files and
    validates the configuration against the expected schema.
    """

    def __init__(self, command: Command):
        """Initialize a new `ConfigLoader` instance.

        Args:
            command (Command): The `click` command this loader
                               is associated with.
        """

        self._command = command

    def validate_config(self, config: dict) -> dict:
        """Validate configuration parameters from a dictionary.

        Processes and validates configuration parameters using Click's
        type system and command parameters. Each value is validated and
        converted according to its corresponding parameter type.

        Args:
            config (dict): Dictionary of configuration parameters

        Returns:
            dict: Validated and processed configuration parameters.
        """

        values = {}
        state = State()
        ctx = click.Context(self._command)
        params = self._command.params

        for param in (o for o in params if o.name in config):
            value = param.process_value(ctx, config[param.name])
            value = state.preprocess_argument(value)
            values[param.name] = value

        return values

    def read_config_file(
            self, path: str, document: Document) -> List[RenderConfig]:
        """Read and process a configuration file for all document layers.

        Loads the TOML configuration file and processes both document
        level and layer-specific configurations. A `RenderConfig` list
        is returned, where the first element is the document-level
        configuration followed by layer-specific configs.

        Args:
            path (str): Path to the TOML configuration file.
            document (Document): Document instance

        Returns:
            List[RenderConfig]: List of RenderConfig objects
        """

        configs = []
        manager = ConfigManager()
        manager.load_config_file(path)

        document_values = manager.config.get('document', {})
        document_config = self._to_config_model(document_values)
        configs.append(document_config)

        for index in reversed(range(len(document.layers))):
            layer_values = manager.config.get(f'layer-{index}', {})
            layer_values = {**document_values, **layer_values}
            layer_config = self._to_config_model(layer_values)

            layer_config.length_units = document_config.length_units
            layer_config.time_units = document_config.time_units

            configs.append(layer_config)

        return configs

    def _to_config_model(self, values: dict = {}) -> RenderConfig:
        """Read and validate a section from the configuration."""

        config = self.validate_config(values)
        return RenderConfig.model_validate(config)
