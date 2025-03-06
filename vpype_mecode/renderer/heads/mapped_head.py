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

from vpype_mecode.renderer.gcode_context import GContext
from vpype_mecode.utils import HeightMap
from .basic_head import BasicHead


class MappedHead(BasicHead):
    """Head implementation with height map compensation.

    This class handles basic operations for controlling the machine's
    head. All work movements are transformed according to a height map,
    which allows for various applications:

    - Surface compensation: Maintains consistent tool engagement on
      uneven surfaces by automatically adjusting the Z height.
    - Auto-leveling: Compensates for machine bed imperfections or
      misalignment without manual bed leveling.
    - Texture mapping: Can be used artistically to transfer height map
      patterns into the work piece.
    - Depth control: Enables precise control over tool engagement across
      the entire work area for consistent results.

    The height map adjusts the Z-axis position during plunging and work
    operations to maintain consistent tool engagement with the work
    surface. Work movements are interpolated across the height map to
    ensure smooth transitions between different surface heights.
    """

    def __init__(self):
        super().__init__()
        self._height_map = None

    def plunge(self, ctx: GContext):
        """Plunge the machine head to the work height.

        Generates G-code commands to move the machine head to the
        plunge height at travel speed and then to the work height at
        controlled plunge speed. The final Z position is adjusted based
        on the height map value at the current XY position taking into
        account the offset between plunge_z and work_z heights.

        Args:
            ctx (GContext): The G-code generation context
        """

        height_map = self._get_height_map(ctx)
        cx, cy, cz = ctx.g.current_head_position
        map_z = height_map.get_height_at(cx, cy)
        plunge_offset = ctx.plunge_z - ctx.work_z

        work_z = map_z + ctx.work_z
        plunge_z = work_z + plunge_offset

        ctx.g.move(z=plunge_z, F=ctx.travel_speed)
        ctx.g.move(z=work_z, F=ctx.plunge_speed)

    def trace_to(self, ctx: GContext, x: float, y: float):
        """Trace a path to a specified position at work speed.

        Generates G-code commands to move the machine head to the
        specified (x, y) coordinates at the configured work speed. The
        path is sampled against the height map and interpolated to ensure
        smooth Z-axis adjustments that follow the surface contours.

        Args:
            ctx (GContext): The G-code generation context
            x (float): The target x-coordinate
            y (float): The target y-coordinate
        """

        height_map = self._get_height_map(ctx)
        cx, cy, cz = ctx.g.current_head_position
        points = height_map.sample_path([cx, cy, x, y])

        for x, y, map_z in points[1:]:
            work_z = map_z + ctx.work_z
            ctx.g.move(x=x, y=y, z=work_z, F=ctx.work_speed)

    def _get_height_map(self, ctx: GContext):
        """Obtain or create the heightmap instance to use"""

        if not isinstance(self._height_map, HeightMap):
            self._height_map = HeightMap.from_path(ctx.height_map)
            self._height_map.set_scale(ctx.height_map_scale)

        return self._height_map
