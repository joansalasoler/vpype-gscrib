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

"""G-Code generator plugin for Vpype.

This module provides a Vpype plugin that generates G-Code for CNC
machines using the `mecode` library. It supports configuration through
command line parameters and TOML configuration files.
"""

from typing import List

import click
import vpype
import vpype_cli

from tomli import TOMLDecodeError
from pydantic import ValidationError
from vpype import Document

from vpype_mecode import __version__
from vpype_mecode.vpype_options import command_options
from vpype_mecode.builder import GCodeBuilder
from vpype_mecode.builder.excepts import DeviceError
from vpype_mecode.excepts import VpypeMecodeError
from vpype_mecode.processor import DocumentProcessor
from vpype_mecode.renderer import GRenderer
from vpype_mecode.config import ConfigLoader, BuilderConfig, RenderConfig


@vpype_cli.cli.command(
    name="mecode",
    group="Output",
    help="""
    Generate G-Code for CNC machines.

    This command processes a vpype Document and generates G-Code from
    it using the `mecode` library. The ouput can be sent to the teminal,
    a file or to a printer using mecode's direct write mode.

    The command accepts a number of options that can be used to configure
    the G-Code generation process. They can be provided in the command
    line as global defaults or in a TOML file than contains specific
    settings for each layer of the document.
    """,
)
@click.version_option(
    version=__version__,
    prog_name="vpype-mecode",
    message="%(prog)s %(version)s"
)
@vpype_cli.global_processor
def vpype_mecode(document: Document, **kwargs) -> Document:
    """Main entry point for the `mecode` command.

    Args:
        document: The Vpype document to process
        **kwargs: Command line parameters

    Returns:
        The processed Document instance

    Raises:
        click.BadParameter: If the configuration is invalid
        click.UsageError: If the document cannot be processed
    """

    try:
        _validate_document(document)
        _validate_user_config()

        render_configs = _setup_render_configs(document, kwargs)
        builder_config = _setup_builder_config(kwargs)

        # Initialize the G-Code renderer

        builder = GCodeBuilder(**builder_config.model_dump())
        renderer = GRenderer(builder, render_configs)

        # Process the document using the configured renderer

        processor = DocumentProcessor(renderer)
        processor.process(document)
    except DeviceError as e:
        raise click.Abort(str(e))
    except VpypeMecodeError as e:
        raise click.UsageError(str(e))
    except ValidationError as e:
        error_message = e.errors()[0]["msg"]
        raise click.UsageError(error_message)
    except TOMLDecodeError as e:
        error_message = f"Cannot read configuration file: {e}"
        raise click.UsageError(error_message)
    except FileNotFoundError as e:
        raise click.UsageError(f"File not found: {e.filename}")

    return document


# ---------------------------------------------------------------------
# Utility methods
# ---------------------------------------------------------------------


def _validate_user_config():
    """Raises an exception if the user's vpype.toml file had errors"""

    if _config_exception is not None:
        raise _config_exception


def _validate_document(document: Document):
    """Validate that the document meets the requirements."""

    if document.is_empty():
        raise click.UsageError(
            "Cannot generate G-Code from empty document")

    if document.page_size is None:
        raise click.UsageError(
            "It is required for the document to have a page size.")


def _setup_builder_config(params) -> BuilderConfig:
    """Create and validate the Mecode configuration."""

    return BuilderConfig.model_validate(params)


def _setup_render_configs(document: Document, params) -> List[RenderConfig]:
    """Create and validate the rendering configurations, either from
    the command line parameters or a TOML file."""

    config_path = params["config"]

    if config_path is None:
        return [RenderConfig.model_validate(params),]

    return _config_loader.read_config_file(config_path, document)


# ---------------------------------------------------------------------
# Initialize the command line interface
# ---------------------------------------------------------------------

_config_exception = None
_config_loader = ConfigLoader(vpype_mecode)

for param in command_options:
    vpype_mecode.params.append(param)

try:
    cm = vpype.config_manager
    toml_values = cm.config.get("vpype-mecode", {})
    config = _config_loader.validate_config(toml_values)

    for param in command_options:
        if param.name in config:
            default_value = config[param.name]
            param.override_default_value(default_value)
except ValidationError as e:
    message = e.errors()[0]["msg"]
    message = f"Invalid value in file 'vpype.toml': {message}"
    _config_exception = click.UsageError(message)
except click.BadParameter as e:
    message = f"Invalid value in file 'vpype.toml': {e.message}"
    _config_exception = click.UsageError(message)
except TOMLDecodeError as e:
    message = f"Cannot read 'vpype.toml': {e.message}"
    _config_exception = click.UsageError(message)
