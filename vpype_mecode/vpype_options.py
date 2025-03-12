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

"""
Configuration options.

This module defines all available configuration options that can be used
to customize the G-Code generation process. They are used both to parse
the command line options and the TOML configuration files.
"""

from vpype_cli import TextType, IntRangeType, FloatRangeType
from vpype_cli import IntegerType, LengthType, PathType

from vpype_mecode.config import ConfigOption
from vpype_mecode.enums import *


command_options = (


    # ------------------------------------------------------------------
    # Global Options
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='output',
        type=PathType(dir_okay=False, writable=True),
        help="""
        File path where the generated G-Code will be saved. If not
        specified, the G-Code will be printed to the terminal.
        """,
    ),
    ConfigOption(
        option_name='config',
        type=PathType(exists=True, dir_okay=False, resolve_path=True),
        default=None,
        help="""
        Path to a TOML file containing configuration settings specific
        to the document and each of its layers.
        """,
    ),

    # ------------------------------------------------------------------
    # G-Code Renderer Options
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='length-units',
        type=LengthUnits,
        help="""
        Choose the unit of measurement for the output G-Code.
        """,
    ),
    ConfigOption(
        option_name='time-units',
        type=TimeUnits,
        help="""
        Choose the unit of time for the output G-Code. Used to specify
        program execution delays.
        """,
    ),
    ConfigOption(
        option_name='head-mode',
        type=HeadMode,
        help="""
        Specifies the head type for G-code generation. The head determines
        how axis movements are generated and coordinated.
        """,
    ),
    ConfigOption(
        option_name='tool-mode',
        type=ToolMode,
        help="""
        Specifies the tool type for G-code generation. The generated
        code adapts to the selected tool type.
        """,
    ),
    ConfigOption(
        option_name='rack-mode',
        type=RackMode,
        help="""
        Specifies if tool changes are needed between layers or if the
        machine can handle multiple tools.
        """,
    ),
    ConfigOption(
        option_name='coolant-mode',
        type=CoolantMode,
        help="""
        Selects the type of coolant used during operation.
        """,
    ),
    ConfigOption(
        option_name='fan-mode',
        type=FanMode,
        help="""
        Selects the type of fan used during operation.
        """,
    ),
    ConfigOption(
        option_name='bed-mode',
        type=BedMode,
        help="""
        Selects the type of bed used for operation.
        """,
    ),
    ConfigOption(
        option_name='work-speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves while performing an operation
        (cutting, drawing, etc). Measured in units per minute.
        """,
    ),
    ConfigOption(
        option_name='plunge-speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves during the plunging phase,
        where it enters the material. The plunge is typically slower than
        the work speed to ensure controlled entry. Measured in units per
        minute.
        """,
    ),
    ConfigOption(
        option_name='travel-speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves between operations, without
        interacting with the material or work surface, measured in units
        per minute.
        """,
    ),
    ConfigOption(
        option_name='fan-speed',
        type=IntRangeType(min=0, max=255),
        help="""
        The speed at which the fan rotates during operations. A value
        of 0 turns off the fan, while a value of 255 sets it to its
        maximum speed.
        """,
    ),
    ConfigOption(
        option_name='hotend-temperature',
        type=IntegerType(),
        help="""
        The temperature at which the hotend is set during operation,
        measured in celsius degrees.
        """,
    ),
    ConfigOption(
        option_name='bed-temperature',
        type=IntegerType(),
        help="""
        The temperature at which the heated bed is set during operation,
        measured in celsius degrees.
        """,
    ),
    ConfigOption(
        option_name='power-level',
        type=IntRangeType(min=0),
        help="""
        Controls the intensity of energy-based tools such as laser
        cutters, plasma cutters, or 3D printer extruders.
        """,
    ),
    ConfigOption(
        option_name='spindle-rpm',
        type=IntRangeType(min=0),
        help="""
        Controls the rotational speed of the spindle, used for rotating
        tools such as  mills, drills, and routers. The value is measured
        in revolutions per minute (RPM).
        """,
    ),
    ConfigOption(
        option_name='spin-mode',
        type=SpinMode,
        help="""
        Sets the rotation direction of the spindle.
        """,
    ),
    ConfigOption(
        option_name='power-mode',
        type=PowerMode,
        help="""
        Sets the power mode of the tool.
        """,
    ),
    ConfigOption(
        option_name='warmup-delay',
        type=FloatRangeType(min=0.001),
        help="""
        Time to wait in seconds after tool activation or deactivation
        before starting any movement. This ensures the tool reaches its
        target state (power, speed, etc) before operating.
        """,
    ),
    ConfigOption(
        option_name='tool-number',
        type=IntRangeType(min=1),
        help="""
        Specify the tool number to be used for machining operations.
        """,
    ),
    ConfigOption(
        option_name='work-z',
        type=LengthType(),
        help="""
        The Z-axis height at which the tool will perform its active work
        (cutting, drawing, printing, etc).
        """,
    ),
    ConfigOption(
        option_name='plunge-z',
        type=LengthType(),
        help="""
        The Z-axis height at which the tool begins plunging into the
        material. This is usually just above the final work Z, allowing
        the tool to gradually enter the material.
        """,
    ),
    ConfigOption(
        option_name='safe-z',
        type=LengthType(),
        help="""
        The Z-axis height the tool moves to when traveling between
        operations, ensuring it does not collide with the material.
        """,
    ),
    ConfigOption(
        option_name='park-z',
        type=LengthType(),
        help="""
        The Z-axis parking height where the tool retracts for maintenance
        operations, such as tool changes and program completion.
        """,
    ),

    # ------------------------------------------------------------------
    # G-Code Transform Options
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='height-map-path',
        type=PathType(exists=True, dir_okay=False, resolve_path=True),
        help="""
        Path to a heightmap image file that defines surface variations
        across the work area. The image is interpreted as a grid of
        values that can be used to dynamically adjust various parameters
        during operation, such as tool height or power levels.
        """,
    ),
    ConfigOption(
        option_name='height-map-scale',
        type=FloatRangeType(min=0.0),
        help="""
        Scaling factor applied to normalized heightmap values (0.0 to 1.0)
        to convert them into actual work units. For example, a scale of 10
        means a heightmap value of 1.0 becomes 10 units.
        """,
    ),
    ConfigOption(
        option_name='height-map-tolerance',
        type=FloatRangeType(min=0.0),
        help="""
        Minimum height difference threshold used when sampling points
        from the height map. Points with height differences below this
        value will be filtered out. Measured in work units.
        """,
    ),

    # ------------------------------------------------------------------
    # 3D Printing Settings
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='layer-height',
        type=LengthType(min=0.001),
        help="""
        The height of each extruded layer. This parameter is used to
        determine how much filament is extruded per layer.
        """,
    ),
    ConfigOption(
        option_name='nozzle-diameter',
        type=LengthType(min=0.001),
        help="""
        The diameter of the 3D printer's extrusion nozzle. This determines
        the width of the extruded filament and affects the extrusion rate.
        """,
    ),
    ConfigOption(
        option_name='filament-diameter',
        type=LengthType(min=0.001),
        help="""
        The diameter of the filament used for extrusion. This affects
        the volume of plastic extruded.
        """,
    ),
    ConfigOption(
        option_name='retract-length',
        type=LengthType(min=0.0),
        help="""
        The length of filament that is retracted to reduce stringing and
        oozing during non-extrusion moves.
        """,
    ),
    ConfigOption(
        option_name='retract-speed',
        type=LengthType(),
        help="""
        The speed at which the filament is retracted. Higher speeds help
        prevent stringing but may cause filament grinding.
        """,
    ),

    # ------------------------------------------------------------------
    # G-Code Output Options
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='header-gcode',
        hidden=True,
        type=PathType(exists=True, dir_okay=False, resolve_path=True),
        help="""
        Path to a file containing custom G-Code lines to be added at the
        beginning of the generated G-Code program.
        """,
    ),
    ConfigOption(
        option_name='footer-gcode',
        hidden=True,
        type=PathType(exists=True, dir_okay=False, resolve_path=True),
        help="""
        Path to a file containing custom G-Code lines to be added at the
        end of the generated G-Code program.
        """,
    ),

    # ------------------------------------------------------------------
    # Direct Writing to Device (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='direct-write-mode',
        type=DirectWriteMode,
        help="""
        Sends the generated G-Code directly to a connected machine via a
        socket or serial connection.
        """,
    ),
    ConfigOption(
        option_name='wait-for-response',
        is_flag=True,
        help="""
        When enabled, waits for an acknowledgment from the machine after
        sending each G-Code command. This ensures each command is received
        and processed before sending the next one.
        """,
    ),
    ConfigOption(
        option_name='host',
        type=TextType(),
        help="""
        The hostname or IP address of the machine when using direct
        writing over a network.
        """,
    ),
    ConfigOption(
        option_name='port',
        type=IntRangeType(min=0),
        help="""
        The port number used for network communication with the machine
        when using direct writing.
        """,
    ),
    ConfigOption(
        option_name='baudrate',
        type=IntRangeType(min=0),
        help="""
        The communication speed (baud rate) for a serial connection to
        the machine when using direct writing.
        """,
    ),

    # ------------------------------------------------------------------
    # G-Code Output Options (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='decimal-places',
        type=IntRangeType(min=0),
        help="""
        Maximum number of decimal places to include in G-Code coordinates
        and other numeric values.
        """,
    ),
    ConfigOption(
        option_name='comment-symbols',
        type=TextType(),
        help="""
        Defines the characters used to mark comments in the generated
        G-Code. For example, use --comment-symbols="(" to enclose the
        comments in parentheses.
        """,
    ),
    ConfigOption(
        option_name='line-endings',
        type=TextType(),
        help="""
        Specifies the line-ending characters for the generated G-Code.
        Use 'os' to match your system's default.
        """,
    ),

    # ------------------------------------------------------------------
    # Axis Naming (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='x-axis',
        type=TextType(),
        help="""
        Custom label for the machine's X axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        option_name='y-axis',
        type=TextType(),
        help="""
        Custom label for the machine's Y axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        option_name='z-axis',
        type=TextType(),
        help="""
        Custom label for the machine's Z axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        option_name='i-axis',
        type=TextType(),
        help="""
        Custom label for the machine's I axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        option_name='j-axis',
        type=TextType(),
        help="""
        Custom label for the machine's J axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        option_name='k-axis',
        type=TextType(),
        help="""
        Custom label for the machine's K axis in the generated G-Code.
        """,
    ),

    # ------------------------------------------------------------------
    # Unsupported Mecode Options (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        option_name='aerotech-include',
        hidden=True,
        is_flag=True,
        help="""
        Adds Aerotech-specific functions and variable definitions to the
        output G-Code, if applicable.
        """,
    ),

)
