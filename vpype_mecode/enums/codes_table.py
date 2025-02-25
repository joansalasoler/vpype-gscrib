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

from . import *


"""
Mapping table to convert enum values to G-Code instructions.

This module contains a dictionary that translates our internal enum
values into their corresponding G-Code instructions. The `GBuilder`
class uses this mapping to generate valid G-Code output.

Notice that the dictionary keys are prefixed with their enum type
because the enums inherit from `str`. This namespacing prevents
conflicts between enums that might share the same value but represent
different commands.
"""


codes_table = {

    # ------------------------------------------------------------------
    # Length Units
    # ------------------------------------------------------------------

    (LengthUnits, LengthUnits.INCHES): (
        'G20', 'Set length units (inches)'
    ),

    (LengthUnits, LengthUnits.MILLIMETERS): (
        'G21', 'Set length units (millimeters)'
    ),

    # ------------------------------------------------------------------
    # Distance Modes
    # ------------------------------------------------------------------

    (DistanceMode, DistanceMode.ABSOLUTE): (
        'G90', 'Set distance mode (absolute)'
    ),

    (DistanceMode, DistanceMode.RELATIVE): (
        'G91', 'Set distance mode (relative)'
    ),

    # ------------------------------------------------------------------
    # Feed Rate Modes
    # ------------------------------------------------------------------

    (FeedMode, FeedMode.INVERSE_TIME): (
        'G93', 'Set feed rate mode (inverse time)'
    ),

    (FeedMode, FeedMode.MINUTE): (
        'G94', 'Set feed rate mode (units per minute)'
    ),

    (FeedMode, FeedMode.REVOLUTION): (
        'G95', 'Set feed rate mode (units per revolution)'
    ),

    # ------------------------------------------------------------------
    # Tool Control
    # ------------------------------------------------------------------

    (SpinMode, SpinMode.CLOCKWISE): (
        'M03', 'Start tool (clockwise)'
    ),

    (SpinMode, SpinMode.COUNTER): (
        'M04', 'Start tool (counterclockwise)'
    ),

    (SpinMode, SpinMode.OFF): (
        'M05', 'Stop tool'
    ),

    # ------------------------------------------------------------------
    # Tool Swap Modes
    # ------------------------------------------------------------------

    (RackMode, RackMode.AUTOMATIC): (
        'M06', 'Tool change (automatic)'
    ),

    (RackMode, RackMode.MANUAL): (
        'M06', 'Tool change (manual)'
    ),

    # ------------------------------------------------------------------
    # Coolant Control Modes
    # ------------------------------------------------------------------

    (CoolantMode, CoolantMode.FLOOD): (
        'M08', 'Turn on coolant (flood)'
    ),

    (CoolantMode, CoolantMode.MIST): (
        'M07', 'Turn on coolant (mist)'
    ),

    (CoolantMode, CoolantMode.OFF): (
        'M09', 'Turn off coolant'
    ),

    # ------------------------------------------------------------------
    # Plane Selection
    # ------------------------------------------------------------------

    (Plane, Plane.XY): (
        'G17', 'Select plane (XY)'
    ),

    (Plane, Plane.YZ): (
        'G19', 'Select plane (YZ)'
    ),

    (Plane, Plane.ZX): (
        'G18', 'Select plane (ZX)'
    ),

    # ------------------------------------------------------------------
    # Sleep/Dwell Modes
    # ------------------------------------------------------------------

    (TimeUnits, TimeUnits.SECONDS): (
        'G04', 'Sleep for a while (seconds)'
    ),

    (TimeUnits, TimeUnits.MILLISECONDS): (
        'G04', 'Sleep for a while (milliseconds)'
    ),

    # ------------------------------------------------------------------
    # Halt Modes
    # ------------------------------------------------------------------

    (HaltMode, HaltMode.PAUSE): (
        'M00', 'Pause program (forced)'
    ),

    (HaltMode, HaltMode.OPTIONAL_PAUSE): (
        'M01', 'Pause program (optional)'
    ),

    (HaltMode, HaltMode.END_WITHOUT_RESET): (
        'M02', 'End of program (no reset)'
    ),

    (HaltMode, HaltMode.END_WITH_RESET): (
        'M30', 'End of program (stop and reset)'
    ),

    (HaltMode, HaltMode.PALLET_EXCHANGE_AND_END): (
        'M60', 'Exchange pallet and end program'
    ),

}