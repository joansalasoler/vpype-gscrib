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

from vpype_mecode.enums import *
from .gcode_table import GCodeEntry, GCodeTable


"""
Built-in enums to G-Code mappings.
"""

gcode_table = GCodeTable((

    # ------------------------------------------------------------------
    # Length Units
    # ------------------------------------------------------------------

    GCodeEntry(LengthUnits.INCHES,
        'G20', 'Set length units, inches'
    ),

    GCodeEntry(LengthUnits.MILLIMETERS,
        'G21', 'Set length units, millimeters'
    ),

    # ------------------------------------------------------------------
    # Distance Modes
    # ------------------------------------------------------------------

    GCodeEntry(DistanceMode.ABSOLUTE,
        'G90', 'Set distance mode, absolute'
    ),

    GCodeEntry(DistanceMode.RELATIVE,
        'G91', 'Set distance mode, relative'
    ),

    # ------------------------------------------------------------------
    # Feed Rate Modes
    # ------------------------------------------------------------------

    GCodeEntry(FeedMode.INVERSE_TIME,
        'G93', 'Set feed rate mode, inverse time'
    ),

    GCodeEntry(FeedMode.MINUTE,
        'G94', 'Set feed rate mode, units per minute'
    ),

    GCodeEntry(FeedMode.REVOLUTION,
        'G95', 'Set feed rate mode, units per revolution'
    ),

    # ------------------------------------------------------------------
    # Tool Control
    # ------------------------------------------------------------------

    GCodeEntry(SpinMode.CLOCKWISE,
        'M03', 'Start tool, clockwise'
    ),

    GCodeEntry(SpinMode.COUNTER,
        'M04', 'Start tool, counterclockwise'
    ),

    GCodeEntry(SpinMode.OFF,
        'M05', 'Stop tool'
    ),

    # ------------------------------------------------------------------
    # Tool Swap Modes
    # ------------------------------------------------------------------

    GCodeEntry(RackMode.AUTOMATIC,
        'M06', 'Tool change, automatic'
    ),

    GCodeEntry(RackMode.MANUAL,
        'M06', 'Tool change, manual'
    ),

    # ------------------------------------------------------------------
    # Coolant Control Modes
    # ------------------------------------------------------------------

    GCodeEntry(CoolantMode.FLOOD,
        'M08', 'Turn on coolant, flood'
    ),

    GCodeEntry(CoolantMode.MIST,
        'M07', 'Turn on coolant, mist'
    ),

    GCodeEntry(CoolantMode.OFF,
        'M09', 'Turn off coolant'
    ),

    # ------------------------------------------------------------------
    # Fan Control Modes
    # ------------------------------------------------------------------

    GCodeEntry(FanMode.ON,
        'M106', 'Set fan speed'
    ),

    GCodeEntry(FanMode.OFF,
        'M106', 'Turn off fan'
    ),

    # ------------------------------------------------------------------
    # Temperature Control
    # ------------------------------------------------------------------

    GCodeEntry(TemperatureUnits.CELSIUS,
        'M140', 'Set bed temperature, celsius'
    ),

    GCodeEntry(TemperatureUnits.KELVIN,
        'M140', 'Set bed temperature, kelvin'
    ),

    # ------------------------------------------------------------------
    # Plane Selection
    # ------------------------------------------------------------------

    GCodeEntry(Plane.XY,
        'G17', 'Select plane, XY'
    ),

    GCodeEntry(Plane.YZ,
        'G19', 'Select plane, YZ'
    ),

    GCodeEntry(Plane.ZX,
        'G18', 'Select plane, ZX'
    ),

    # ------------------------------------------------------------------
    # Sleep/Dwell Modes
    # ------------------------------------------------------------------

    GCodeEntry(TimeUnits.SECONDS,
        'G04', 'Sleep for a while, seconds'
    ),

    GCodeEntry(TimeUnits.MILLISECONDS,
        'G04', 'Sleep for a while, milliseconds'
    ),

    # ------------------------------------------------------------------
    # Halt Modes
    # ------------------------------------------------------------------

    GCodeEntry(HaltMode.PAUSE,
        'M00', 'Pause program, forced'
    ),

    GCodeEntry(HaltMode.OPTIONAL_PAUSE,
        'M01', 'Pause program, optional'
    ),

    GCodeEntry(HaltMode.END_WITHOUT_RESET,
        'M02', 'End of program, no reset'
    ),

    GCodeEntry(HaltMode.END_WITH_RESET,
        'M30', 'End of program, stop and reset'
    ),

    GCodeEntry(HaltMode.PALLET_EXCHANGE_AND_END,
        'M60', 'Exchange pallet and end program'
    ),

    GCodeEntry(HaltMode.WAIT_FOR_BED_TEMP,
        'M190', 'Wait for bed to reach temp, celsius'
    ),

))