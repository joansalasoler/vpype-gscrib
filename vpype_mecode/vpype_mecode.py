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

import click
import vpype
import vpype_cli

from typing import List
from vpype import ConfigManager
from vpype import Document
from vpype_cli import State
from pydantic import ValidationError

from vpype_mecode import vpype_options
from vpype_mecode.processor import DocumentProcessor
from vpype_mecode.renderer import GBuilder, GRenderer
from vpype_mecode.config import *


_config_exception = None


@vpype_cli.cli.command(
  name='mecode',
  group='Output',
  help= """
  Generate G-Code for CNC machines.

  This command processes a vpype Document and generates G-Code from
  it using the `mecode` library. The ouput can be sent to the teminal,
  a file or to a printer using mecode's direct write mode.

  The command accepts a number of options that can be used to configure
  the G-Code generation process. They can be provided in the command
  line as global defaults or in a TOML file than contains specific
  settings for each layer of the document.
  """
)
@vpype_cli.global_processor
@click.pass_context
def vpype_mecode(ctx: click.Context, document: Document, **kwargs) -> Document:
    """Main entry point for the `mecode` command."""

    if document.is_empty():
        raise click.UsageError(
            'Cannot generate G-Code from empty document')

    if document.page_size is None:
        raise click.UsageError(
            'It is required for the document to have a page size.')

    if _config_exception is not None:
        raise click.UsageError(_config_exception)

    try:
        print(ctx.params)
        # Read configuration parameters from the command line

        config_path = kwargs['render_config']
        mecode_config = MecodeConfig.model_validate(kwargs)
        render_config = [RenderConfig.model_validate(kwargs),]

        # The renderer can be configured with a TOML file or with
        # command line arguments.

        if config_path is not None:
            file_path = config_path
            render_config = read_config_file(file_path, document)

        # Mecode needs some values in work units, but the default
        # unit in Vpype is pixels. We need to convert them.

        defaults_config = render_config[0]
        length_units = defaults_config.length_units
        mecode_config.scale_lengths(length_units)

        # Initialize the G-Code renderer

        builder = GBuilder(**mecode_config.model_dump())
        renderer = GRenderer(builder, render_config)

        # Process the document using the configured renderer

        processor = DocumentProcessor(renderer)
        processor.process(document)
    except ValidationError as e:
        raise click.BadParameter(str(e))

    return document


# Utility functions

def validate_config(config: dict, params: List[ConfigOption]) -> dict:
    """Validate configuration parameters from a dict.

    This method is used to validate a dictionary of configuration
    parameters in the same way as the command line arguments are
    validated and converted to their types.
    """

    values = {}
    state = State()
    ctx = click.Context(vpype_mecode)

    for param in (o for o in params if o.name in config):
        value = param.process_value(ctx, config[param.name])
        value = state.preprocess_argument(value)
        values[param.name] = value

    return values


def read_config_file(path: str, document: Document) -> List[RenderConfig]:
    """Read layer settings from the configuration TOML file."""

    configs = []
    manager = vpype.config_manager
    manager.load_config_file(path)

    try:
        document_config = read_config_section('document', manager)
        configs.append(document_config)

        for index in range(len(document.layers)):
            layer_config = read_config_section(f'layer-{index}', manager)
            configs.append(layer_config)
    except click.BadParameter as e:
        message = f"Invalid value in file '{path}': {e.message}"
        raise click.UsageError(message)

    return configs


def read_config_section(section_name: str, manager: ConfigManager) -> RenderConfig:
    """Read a configuration section from the manager"""

    toml_values = manager.config.get(section_name, {})
    config = validate_config(toml_values, vpype_options.params)
    renderer_config = RenderConfig.model_validate(config)

    return renderer_config


# Initialize the command line options

for param in vpype_options.params:
    vpype_mecode.params.append(param)

# Read configuration values from the user TOML file and override the
# default values of the command line options with them.

try:
    cm = vpype.config_manager
    toml_values = cm.config.get('vpype-mecode', {})
    config = validate_config(toml_values, vpype_options.params)

    for param in vpype_options.params:
        if param.name in config:
            value = config[param.name]
            param.override_default_value(value)
except click.BadParameter as e:
    e.message = f"Invalid value in file 'vpype.toml': {e.message}"
    _config_exception = e
