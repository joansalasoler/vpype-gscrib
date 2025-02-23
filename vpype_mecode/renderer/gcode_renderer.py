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

from numpy import array
from typing import Tuple
from vpype import Document, LineCollection

from .gcode_builder import GBuilder
from .gcode_context import GContext
from .heads import HeadFactory
from .tools import ToolFactory
from .coolants import CoolantFactory
from .racks import RackFactory
from ..processor import DocumentRenderer
from ..enums import *
from ..config import *


class GRenderer(DocumentRenderer):

    def __init__(self, builder: GBuilder, config: RenderConfig):
        self._g = builder
        self._config = config
        self._context = GContext(builder, config)
        self._head = HeadFactory.create(config.head_mode)
        self._tool = ToolFactory.create(config.tool_mode)
        self._coolant = CoolantFactory.create(config.coolant_mode)
        self._rack = RackFactory.create(config.rack_mode)

    def begin_document(self, document: Document):
        length_units = self._context.length_units
        width, height = document.page_size

        self._g.setup()
        self._g.absolute()
        self._g.select_units(length_units)
        self._g.select_plane(Plane.XY)

        self._g.reflect(0)
        self._g.translate(0, height)
        self._g.scale(length_units.scale_factor)

    def begin_layer(self, layer: LineCollection):
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
        x, y = self._first_point_of_path(path)

        self._head.retract(self._context)
        self._head.travel_to(self._context, x, y)
        self._head.plunge(self._context)
        self._tool.power_on(self._context)

    def trace_segment(self, path: array, x: float, y: float):
        self._head.trace_to(self._context, x, y)

    def end_path(self, path: array):
        self._tool.power_off(self._context)
        self._head.retract(self._context)

    def end_layer(self, layer: LineCollection):
        self._head.safe_retract(self._context)
        self._tool.deactivate(self._context)
        self._coolant.turn_off(self._context)

    def end_document(self, document: Document):
        self._head.park_for_service(self._context)
        self._g.halt_program(HaltMode.END_WITH_RESET)
        self._g.teardown()

    def process_error(self, e: Exception):
        self._g.emergency_halt(str(e))
        self._g.teardown()

    def _first_path_of_layer(self, layer: LineCollection) -> array:
        return layer.lines[0]

    def _first_point_of_path(self, path: array) -> Tuple[float, float]:
        return path[0].real, path[0].imag

    def _write_layer_header(self, layer: LineCollection):
        """Write layer header with metadata and configuration."""

        layer_name = layer.property('vp_name')
        self._g.comment(f'layer = {layer_name}')
        self._write_config_info(self._config)

    def _write_config_info(self, config: BaseConfig):
        """Write configuration parameters as human-readable values."""

        units = self._context.length_units
        formated_dict = config.format_values(units)

        for key, value in formated_dict.items():
            self._g.comment(f'{key} = {value}')
