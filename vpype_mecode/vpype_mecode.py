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
import vpype_cli
import vpype as vp
from vpype import Document
from pydantic import ValidationError

from . import vpype_options
from .processor import DocumentProcessor
from .renderer import GBuilder, GRenderer
from .config import *


@click.command(name='mecode')
@vpype_cli.global_processor
def vpype_mecode(document: Document, **kwargs) -> Document:
    """
    This command processes a vpype Document and generates G-Code from
    it using the `mecode` library. The ouput can be sent to the teminal,
    a file or to a printer using mecode's direct write mode.
    """

    try:
        # Parse and validate the command line options

        mecode_config = MecodeConfig.model_validate(kwargs)
        render_config = RenderConfig.model_validate(kwargs)

        # Mecode needs some values in work units, but the default
        # unit in Vpype is pixels. We need to convert them.

        mecode_config.scale_units(render_config.length_units)

        # Initialize the G-Code renderer

        builder = GBuilder(**mecode_config.model_dump())
        renderer = GRenderer(builder, render_config)

        # Process the document using the configured renderer

        processor = DocumentProcessor(renderer)
        processor.process(document)
    except ValidationError as e:
        raise click.BadParameter(str(e))

    return document


# Initialize the commabd when this module is loaded

vpype_mecode.help_group = 'Output'
vpype_mecode.help = 'Generate G-Code for CNC machines.'

for param in vpype_options.params:
    vpype_mecode.params.append(param)
