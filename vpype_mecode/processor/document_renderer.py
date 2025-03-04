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

from abc import ABC, abstractmethod
from numpy import array
from vpype import Document, LineCollection


class DocumentRenderer(ABC):
    """
    Abstract base class defining the interface for document renderers.

    This class defines a structured approach to processing a document by
    traversing its hierarchy: Document → Layers → Paths → Segments.
    Implementations of this class must provide methods to handle each
    stage of the traversal.
    """

    @abstractmethod
    def begin_document(self, document: Document):
        """
        This method is invoked once per document before any of the
        document layers are processed.
        """

    @abstractmethod
    def end_document(self, document: Document):
        """
        This method is invoked once per document after all layers on
        the document have been processed.
        """

    @abstractmethod
    def begin_layer(self, layer: LineCollection):
        """
        Each layer is composed of one or more paths. This method is
        invoked once per layer before any paths are processed.
        """

    @abstractmethod
    def end_layer(self, layer: LineCollection):
        """
        This method is invoked once per layer after all paths on the
        layer have been processed.
        """

    @abstractmethod
    def begin_path(self, path: array):
        """
        Each path is composed of one or more segments. This method is
        invoked once per path before any of its segments are processed.
        """

    @abstractmethod
    def end_path(self, path: array):
        """
        This method is invoked once per path after all segments of the
        path have been processed.
        """

    @abstractmethod
    def trace_segment(self, path: array, x: float, y: float):
        """
        This method is called once per segment within a path, receiving
        the segment's x and y coordinates.
        """

    @abstractmethod
    def process_error(self, e: Exception):
        """
        Invoked if an error occurs during the processing of a document.
        """
