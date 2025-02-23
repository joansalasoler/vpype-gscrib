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

from dataclasses import dataclass
from numpy import array
from typeguard import typechecked
from vpype import Document, LineCollection

from .document_renderer import DocumentRenderer


@dataclass
class DocumentProcessor:
    """
    Processes vector graphics documents by traversing their hierarchical
    structure and delegating operations to a renderer.

    This class walks through a document's hierarchical structure —layers,
    paths, and segments— calling the appropriate methods to process a
    document on a `DocumentRenderer` instance.

    The traversal order is:

      1. Start document processing.
      2. Process each layer of the document.
      3. Process each path within a layer.
      4. Process each segment within a path.
      5. End document processing.
    """

    def __init__(self, renderer: DocumentRenderer):
        self.renderer = renderer

    @typechecked
    def process(self, document: Document):
        """Process a document by iterating through its layers."""

        try:
            self._process_document(document)
        except Exception as e:
            self.renderer.process_error(e)
            raise e

    def _process_document(self, document: Document):
        """Process a single document layer by layer."""

        self.renderer.begin_document(document)

        for layer in document.layers.values():
            if any(len(path) > 0 for path in layer.lines):
                self._process_layer(layer)

        self.renderer.end_document(document)

    def _process_layer(self, layer: LineCollection):
        """Process a single layer of the document."""

        self.renderer.begin_layer(layer)

        for path in layer.lines:
            if len(path) > 0:
                self._process_path(path)

        self.renderer.end_layer(layer)

    def _process_path(self, path: array):
        """Process a single path of a layer."""

        self.renderer.begin_path(path)

        for segment in path:
            x, y = segment.real, segment.imag
            self.renderer.trace_segment(path, x, y)

        self.renderer.end_path(path)

