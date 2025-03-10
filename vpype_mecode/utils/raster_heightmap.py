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

from numbers import Real
from typing import Sequence, Union

import numpy
import cv2 as cv

from typeguard import typechecked
from numpy.typing import ArrayLike
from numpy import float32, uint16, ndarray
from scipy.interpolate import BivariateSpline, RectBivariateSpline
from skimage import draw

from vpype_mecode.excepts import ImageLoadError
from .base_heightmap import BaseHeightMap


UINT8_MAX = 255.0
UINT16_MAX = 65535.0


class RasterHeightMap(BaseHeightMap):
    """Interpolates height map data from images.

    This class processes grayscale image data into a normalized height
    map and provides methods for height interpolation at specific
    coordinates and along paths.

    Attributes:
        _scale_z (float): Scaling factor for height values (default: 1.0)
        _height_map (ndarray): Normalized height map data as a 2D numpy array
        _interpolator (BivariateSpline): Spline interpolator for height values

    Example:
        >>> height_map = RasterHeightMap.from_path('terrain.png')
        >>> height_map.set_scale(2.0)
        >>> height = height_map.get_height_at(100, 100)
    """

    @typechecked
    def __init__(self, image_data: ndarray) -> None:
        self._scale_z = 1.0
        self._tolerance = 0.01
        self._height_map = self._to_height_map(image_data)
        self._interpolator = self._create_interpolator(self._height_map)

    @classmethod
    def from_path(cls, path: str) -> 'RasterHeightMap':
        """Create a HeightMap instance from an image file.

        Args:
            path (str): Path to the grayscale image file

        Returns:
            HeightMap: New HeightMap instance

        Raises:
            ImageLoadError: If the image file cannot be read.
        """

        flags = cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH
        image_data = cv.imread(path, flags)

        if image_data is None:
            raise ImageLoadError(
                f'Could not load heightmap from `{path}`. '
                f'File does not exist or is not a valid image.'
            )

        return cls(image_data)

    @typechecked
    def set_scale(self, scale_z: float) -> None:
        """Set the vertical scaling factor for height values.

        Args:
            scale_z (float): Scaling factor to apply to normalized
                height values.
        """

        self._scale_z = scale_z

    @typechecked
    def set_tolerance(self, tolerance: float) -> None:
        """Set height difference threshold for path sampling.

        Args:
            tolerance (float): The minimum height difference between
                consecutive points that will be considered significant
                during path sampling. Points with height differences below
                this value will be filtered out when using sample_path().
        """

        self._tolerance = tolerance

    @typechecked
    def get_height_at(self, x: Real, y: Real) -> float:
        """Get the interpolated height value at specific coordinates.

        Args:
            x (float): X-coordinate in the height map.
            y (float): Y-coordinate in the height map.

        Returns:
            float: Interpolated height scaled by the scale factor.
        """

        return self._scale_z * self._interpolator(y, x)[0, 0]

    @typechecked
    def sample_path(self, line: Union[Sequence[float], ArrayLike]) -> ndarray:
        """Sample height values along a straight line path.

        Generates a series of points along the line with their corresponding
        heights, filtering out points where height differences are below
        the specified tolerance.

        Args:
            line: Sequence containing start and end points of the line
                to sample in the format (x1, y1, x2, y2).
            tolerance (float, optional): Minimum height difference between
                consecutive points to be included in the output.

        Returns:
            ndarray: Array of points (x, y, z) along the line where
                height changes exceed the tolerance.

        Raises:
            ValueError: If line does not contain exactly 4 elements or
                cannot be converted to float values.
        """

        line_array = numpy.asarray(line, dtype=float)

        if line_array.shape != (4,):
            raise ValueError('Line must contain exactly 4 elements')

        points = self._interpolate_line(line_array)
        filtered = self._filter_points(points, self._tolerance)

        return filtered

    def _interpolate_line(self, line: ndarray) -> ndarray:
        """Get interpolated points along a straight line."""

        line_points = [round(i) for i in line]
        rows, cols = draw.line(*line_points)

        return numpy.array([
            (x, y, self.get_height_at(x, y))
            for x, y in zip(rows, cols)
        ])

    def _filter_points(self, points: ndarray, tolerance: float) -> ndarray:
        """Extracts points where height differences exceed tolerance"""

        first_point = points[0]
        last_point = points[-1]
        lines = [first_point]
        last_z = first_point[2]

        for point in points:
            if abs(point[2] - last_z) >= tolerance:
                lines.append(point)
                last_z = point[2]

        if not numpy.array_equal(lines[-1], last_point):
            lines.append(last_point)

        return numpy.array(lines)

    def _to_height_map(self, image_data: ndarray) -> ndarray:
        """Creates a normalized heightmap from an image array."""

        height_map = numpy.empty(image_data.shape, dtype=float32)
        max_value = (UINT16_MAX if image_data.dtype == uint16 else UINT8_MAX)
        return numpy.divide(image_data, max_value, out=height_map)

    def _create_interpolator(self, height_map: ndarray) -> BivariateSpline:
        """Create a bivariate spline interpolator for a heightmap."""

        width, height = height_map.shape

        return RectBivariateSpline(
            numpy.arange(width),
            numpy.arange(height),
            height_map
        )
