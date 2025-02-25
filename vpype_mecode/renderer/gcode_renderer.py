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

import vpype
import vpype_mecode

from numpy import array
from datetime import datetime
from collections import deque
from typing import List, Tuple
from vpype import Document, LineCollection
from vpype_mecode.config import RenderConfig
from vpype_mecode.processor import DocumentRenderer
from vpype_mecode.enums import *

from .gcode_builder import GBuilder
from .gcode_context import GContext
from .heads import HeadFactory
from .tools import ToolFactory
from .coolants import CoolantFactory
from .racks import RackFactory


class GRenderer(DocumentRenderer):
    """Converts vector graphics to G-Code machine instructions.

    This class implements the `DocumentRenderer` interface by delegating
    specific machine operations to specialized components:

    - Head: Controls machine head movements (travel, plunge, retract)
    - Tool: Manages tool operations (tool activation/deactivation)
    - Coolant: Handles coolant system control (turn on/off)
    - Rack: Manages tool changes and rack operations

    Each component is created through its respective factory based on
    the configuration modes, allowing different strategies to be swapped
    without changing the renderer's core logic. This allows for:

    - Easy addition of new machine head types
    - Support for different tool systems (laser, spindle, etc.)
    - Flexible coolant control strategies
    - Various tool rack configurations

    The renderer coordinates these components to process the document
    hierarchy: Document → Layers → Paths → Segments, generating
    appropriate G-code commands through the `GBuilder` instance.

    Args:
        builder (GBuilder): G-code builder instance
        config (RenderConfig): Configuration parameters

    Attributes:
        _g (GBuilder): G-code command builder instance
        _config (RenderConfig): Rendering configuration parameters
        _context (GContext): Current rendering context
        _head (Head): Machine head controller
        _tool (Tool): Tool controller (laser, spindle, etc.)
        _coolant (Coolant): Coolant system controller
        _rack (Rack): Tool rack controller
    """

    DOCUMENT_SEPARATOR = '=' * 60
    LAYER_SEPARATOR = '-' * 60

    def __init__(self, builder: GBuilder, configs: List[RenderConfig]):
        """G-code renderer initialization.

        Args:
            builder (GBuilder): G-code builder instance
            config (List[RenderConfig]): Configuration parameters
        """

        self._g = builder
        self._ctx_queue = self._build_contexts(builder, configs)
        self._context = self._switch_context()

    def _switch_context(self) -> GContext:
        """Switch to the next context in the queue."""

        context = self._ctx_queue[0]

        self._context = context
        self._head = HeadFactory.create(context.head_mode)
        self._tool = ToolFactory.create(context.tool_mode)
        self._coolant = CoolantFactory.create(context.coolant_mode)
        self._rack = RackFactory.create(context.rack_mode)
        self._ctx_queue.rotate(-1)

        return context

    def begin_document(self, document: Document):
        """This method is invoked once per document before any of the
        document layers are processed.

        Initializes the G-code generation environment by:

        - Setting up the coordinate system
        - Configuring absolute positioning
        - Setting the appropriate unit system
        - Establishing the XY plane
        - Applying initial transformations for document orientation

        Args:
            document (Document): Document being processed
        """

        length_units = self._context.length_units
        width, height = document.page_size

        self._write_document_header(document)

        self._g._write_header()
        self._g.set_distance_mode(DistanceMode.ABSOLUTE)
        self._g.set_feed_mode(FeedMode.MINUTE)
        self._g.select_units(length_units)
        self._g.select_plane(Plane.XY)

        self._g.reflect(0)
        self._g.translate(0, height)
        self._g.scale(length_units.scale_factor)

    def begin_layer(self, layer: LineCollection):
        """Each layer is composed of one or more paths. This method is
        invoked once per layer before any paths are processed.

        Prepares the machine for processing a new layer by:

        - Moving to service position for tool changes
        - Performing necessary tool changes
        - Positioning at the layer start point
        - Activating the tool and coolant systems

        Args:
            layer (LineCollection): Layer being processed
        """

        self._context = self._switch_context()

        first_path = self._first_path_of_layer(layer)
        x, y = self._first_point_of_path(first_path)
        self._write_layer_header(layer)

        self._head.park_for_service(self._context)
        self._rack.change_tool(self._context)

        self._head.safe_retract(self._context)
        self._head.travel_to(self._context, x, y)
        self._tool.activate(self._context)
        self._coolant.turn_on(self._context)

    def begin_path(self, path: array):
        """Each path is composed of one or more segments. This method is
        invoked once per path before any of its segments are processed.

        Prepares for machining operations by:

        - Retracting the tool head
        - Moving to the path start position
        - Plunging to working depth
        - Activating tool power

        Args:
            path (array): Path being processed
        """

        x, y = self._first_point_of_path(path)

        self._head.retract(self._context)
        self._head.travel_to(self._context, x, y)
        self._head.plunge(self._context)
        self._tool.power_on(self._context)

    def trace_segment(self, path: array, x: float, y: float):
        """This method is called once per segment within a path,
        receiving the segment's x and y coordinates.

        Generates G-code movement commands to trace the segment at the
        configured work speed with active tool settings.

        Args:
            path (array): Complete path being traced
            x (float): Target X coordinate of the segment
            y (float): Target Y coordinate of the segment
        """

        self._head.trace_to(self._context, x, y)

    def end_path(self, path: array):
        """This method is invoked once per path after all segments of
        the path have been processed.

        Performs path completion operations:

        - Turning off tool power
        - Retracting the tool head to safe height

        Args:
            path (array): Path being processed
        """

        self._tool.power_off(self._context)
        self._head.retract(self._context)

    def end_layer(self, layer: LineCollection):
        """This method is invoked once per layer after all paths on the
        layer have been processed.

        Performs layer cleanup operations:

        - Retracting to safe height
        - Deactivating the tool
        - Turning off coolant systems

        Args:
            layer (LineCollection): Layer being processed
        """

        self._head.safe_retract(self._context)
        self._tool.deactivate(self._context)
        self._coolant.turn_off(self._context)
        self._switch_context()

    def end_document(self, document: Document):
        """This method is invoked once per document after all layers on
        the document have been processed.

        Finalizes G-code generation by:

        - Moving to final park position
        - Adding program end commands
        - Performing cleanup operations

        Args:
            document (Document): Document being processed
        """

        self._head.park_for_service(self._context)
        self._g.halt_program(HaltMode.END_WITH_RESET)
        self._g.teardown()

    def process_error(self, e: Exception):
        """Invoked if an error occurs during the processing.

        Handles error conditions by:

        - Generating emergency stop commands
        - Performing safe shutdown procedures
        - Adding error information to the G-code output

        Args:
            e (Exception): The exception that occurred
        """

        self._g.emergency_halt(str(e))
        self._g.teardown()

    def _build_contexts(self, builder: GBuilder, configs: List[RenderConfig]) -> deque:
        """Builds a context queue from a list of configurations."""

        return deque([GContext(builder, c) for c in configs])

    def _first_path_of_layer(self, layer: LineCollection) -> array:
        """Get the first path to render from a layer."""

        return layer.lines[0]

    def _first_point_of_path(self, path: array) -> Tuple[float, float]:
        """Coordinates of the first point to render from a path."""

        return path[0].real, path[0].imag

    def _write_document_header(self, document: Document):
        """Write document information as G-code header comments."""

        version = vpype_mecode.__version__
        generator = f'vpype-mecode {version}'
        iso_datetime = datetime.now().isoformat()
        length_units = self._context.length_units.value
        time_units = self._context.time_units.value
        num_layers = len(document.layers)

        self._g.comment(self.DOCUMENT_SEPARATOR)
        self._g.comment(f'Generated by: {generator}')
        self._g.comment(f'Vpype version: {vpype.__version__}')
        self._g.comment(f'Program zero: bottom-left')
        self._g.comment(f'Number of layers: {num_layers}')
        self._g.comment(f'Length units: {length_units}')
        self._g.comment(f'Time units: {time_units}')
        self._g.comment(f'Date: {iso_datetime}')
        self._g.comment(self.DOCUMENT_SEPARATOR)

    def _write_layer_header(self, layer: LineCollection):
        """Write layer configuration as G-code comments."""

        layer_name = layer.property('vp_name')

        self._g.comment(self.LAYER_SEPARATOR)
        self._g.comment(f'layer = {layer_name}')
        self._write_config_info(self._context)
        self._g.comment(self.LAYER_SEPARATOR)

    def _write_config_info(self, context: GContext):
        """Write configuration parameters as G-code comments."""

        formated_dict = context.format_config_values()

        for key, value in formated_dict.items():
            self._g.comment(f'{key} = {value}')
