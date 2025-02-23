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

from vpype_cli import TextType, IntRangeType, FloatRangeType
from vpype_cli import LengthType, PathType

from .config import ConfigOption
from .enums import *


params = (

    # ------------------------------------------------------------------
    # G-Code Renderer Options
    # ------------------------------------------------------------------

    ConfigOption(
        name='length_units',
        type=LengthUnits,
        help="""
        Choose the unit of measurement for the output G-Code.
        """,
    ),
    ConfigOption(
        name='time_units',
        type=TimeUnits,
        help="""
        Choose the unit of time for the output G-Code. Used to specify
        program execution delays.
        """,
    ),
    ConfigOption(
        name='tool_mode',
        type=ToolMode,
        help="""
        Specifies the tool type for G-code generation. The generated
        code adapts to the selected tool type.
        """,
    ),
    ConfigOption(
        name='work_speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves while performing an operation
        (cutting, drawing, etc). Measured in units per minute.
        """,
    ),
    ConfigOption(
        name='plunge_speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves during the plunging phase,
        where it enters the material. The plunge is typically slower than
        the work speed to ensure controlled entry. Measured in units per
        minute.
        """,
    ),
    ConfigOption(
        name='travel_speed',
        type=LengthType(),
        help="""
        The speed at which the tool moves between operations, without
        interacting with the material or work surface, measured in units
        per minute.
        """,
    ),
    ConfigOption(
        name='power_level',
        type=IntRangeType(min=0),
        help="""
        Controls the intensity of energy-based tools such as laser
        cutters, plasma cutters, or 3D printer extruders.
        """,
    ),
    ConfigOption(
        name='spindle_rpm',
        type=IntRangeType(min=0),
        help="""
        Controls the rotational speed of the spindle, used for rotating
        tools such as  mills, drills, and routers. The value is measured
        in revolutions per minute (RPM).
        """,
    ),
    ConfigOption(
        name='spin_mode',
        type=SpinMode,
        help="""
        Sets the rotation direction of the spindle.
        """,
    ),
    ConfigOption(
        name='warmup_delay',
        type=FloatRangeType(min=0.001),
        help="""
        Time to wait in seconds after tool activation or deactivation
        before starting any movement. This ensures the tool reaches its
        target state (power, speed, etc) before operating.
        """,
    ),
    ConfigOption(
        name='rack_mode',
        type=RackMode,
        help="""
        Specifies if tool changes are needed between layers or if the
        machine can handle multiple tools.
        """,
    ),
    ConfigOption(
        name='coolant_mode',
        type=CoolantMode,
        help="""
        Selects the type of coolant used during operation.
        """,
    ),
    ConfigOption(
        name='work_z',
        type=LengthType(),
        help="""
        The Z-axis height at which the tool will perform its active work
        (cutting, drawing, printing, etc).
        """,
    ),
    ConfigOption(
        name='plunge_z',
        type=LengthType(),
        help="""
        The Z-axis height at which the tool begins plunging into the
        material. This is usually just above the final work Z, allowing
        the tool to gradually enter the material.
        """,
    ),
    ConfigOption(
        name='safe_z',
        type=LengthType(),
        help="""
        The Z-axis height the tool moves to when traveling between
        operations, ensuring it does not collide with the material.
        """,
    ),

    # ------------------------------------------------------------------
    # G-Code Output Options (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        name='outfile',
        type=PathType(dir_okay=False, writable=True),
        help="""
        File path where the generated G-Code will be saved. If not
        specified, the G-Code will be printed to the terminal.
        """,
    ),
    ConfigOption(
        name='header',
        type=PathType(exists=True, dir_okay=False),
        help="""
        Path to a file containing custom G-Code lines to be added at the
        beginning of the generated G-Code.
        """,
    ),
    ConfigOption(
        name='footer',
        type=PathType(exists=True, dir_okay=False),
        help="""
        Path to a file containing custom G-Code lines to be added at the
        end of the generated G-Code.
        """,
    ),
    ConfigOption(
        name='aerotech_include',
        is_flag=True,
        help="""
        Adds Aerotech-specific functions and variable definitions to the
        output G-Code, if applicable.
        """,
    ),
    ConfigOption(
        name='output_digits',
        type=IntRangeType(min=0),
        help="""
        Number of decimal places to include in G-Code coordinates and
        values.
        """,
    ),
    ConfigOption(
        name='lineend',
        type=TextType(),
        help="""
        Specifies the line-ending characters for the generated G-Code.
        Use 'os' to match the system default.
        """,
    ),
    ConfigOption(
        name='comment_char',
        type=TextType(),
        help="""
        Defines the character used to mark comments in the generated
        G-Code.
        """,
    ),

    # ------------------------------------------------------------------
    # Direct Writing to Printer (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        name='direct_write',
        is_flag=True,
        help="""
        Sends the generated G-Code directly to a connected printer via a
        socket or serial connection.
        """,
    ),
    ConfigOption(
        name='direct_write_mode',
        type=DirectWriteMode,
        help="""
        Communication method for direct writing. Used only if `direct_write`
        is enabled.
        """,
    ),
    ConfigOption(
        name='printer_host',
        type=TextType(),
        help="""
        The hostname or IP address of the printer when using direct
        writing over a network.
        """,
    ),
    ConfigOption(
        name='printer_port',
        type=IntRangeType(min=0),
        help="""
        The port number used for network communication with the printer
        when using direct writing.
        """,
    ),
    ConfigOption(
        name='baudrate',
        type=IntRangeType(min=0),
        help="""
        The communication speed (baud rate) for a serial connection to
        the printer when using direct writing.
        """,
    ),
    ConfigOption(
        name='two_way_comm',
        is_flag=True,
        help="""
        If enabled, the program will wait for a response from the printer
        after sending each G-Code command.
        """,
    ),

    # ------------------------------------------------------------------
    # Axis Naming (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        name='x_axis',
        type=TextType(),
        help="""
        Custom label for the machine's X axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        name='y_axis',
        type=TextType(),
        help="""
        Custom label for the machine's Y axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        name='z_axis',
        type=TextType(),
        help="""
        Custom label for the machine's Z axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        name='i_axis',
        type=TextType(),
        help="""
        Custom label for the machine's I axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        name='j_axis',
        type=TextType(),
        help="""
        Custom label for the machine's J axis in the generated G-Code.
        """,
    ),
    ConfigOption(
        name='k_axis',
        type=TextType(),
        help="""
        Custom label for the machine's K axis in the generated G-Code.
        """,
    ),

    # ------------------------------------------------------------------
    # 3D Printing Settings (mecode)
    # ------------------------------------------------------------------

    ConfigOption(
        name='extrude',
        is_flag=True,
        help="""
        Enables extrusion mode, where filament flow is calculated and
        added to move commands.
        """,
    ),
    ConfigOption(
        name='filament_diameter',
        type=LengthType(),
        help="""
        Diameter of the filament used for 3D printing.
        """,
    ),
    ConfigOption(
        name='layer_height',
        type=LengthType(),
        help="""
        The thickness of each printed layer for 3D printing.
        """,
    ),
    ConfigOption(
        name='extrusion_width',
        type=LengthType(),
        help="""
        The width of the extruded filament, including any flattening
        effect.
        """,
    ),
    ConfigOption(
        name='extrusion_multiplier',
        type=FloatRangeType(min=0.0),
        help="""
        Adjusts the amount of filament extruded. A value greater than 1
        increases extrusion; a value less than 1 reduces it.
        """,
    ),

)
