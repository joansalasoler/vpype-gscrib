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

from vpype_gscrib.enums import HeadType

from .base_head import BaseHead
from .standard_head import StandardHead
from .auto_leveling_head import AutoLevelingHead


class HeadFactory:
    """A factory for creating head managers.

    This factory creates specialized head managers that handle the control
    of machine tool heads. Head managers are responsible for controlling
    the movement, positioning, and operational parameters of the machine's
    tool head, which is the assembly that holds the active tool.
    """

    @classmethod
    def create(cls, head_type: HeadType) -> BaseHead:
        """Create a new head manger instance.

        Args:
            head_type (HeadType): Head type.

        Returns:
            BaseHead: Head manger instance.

        Raises:
            KeyError: If type is not valid.
        """

        providers = {
            HeadType.STANDARD: StandardHead,
            HeadType.AUTO_LEVELING: AutoLevelingHead,
        }

        return providers[head_type]()
