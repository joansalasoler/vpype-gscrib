Configuration File for vpype-mecode
===================================

```ini
# =====================================================================
# Global Document Settings
# ---------------------------------------------------------------------
# These settings control the machine's behavior and apply to all layers
# unless specifically overridden in a layer section.
# =====================================================================

[document]

# Length and time units
length_units = "mm"         # mm (millimeters), in (inches)
time_units = "s"            # s (seconds), ms (milliseconds)

# Component modes specify how to generate the G-Code
head_mode = "basic"         # basic
tool_mode = "marker"        # beam, blade, extruder, marker, spindle
rack_mode = "manual"        # off, manual, automatic
coolant_mode = "off"        # off, mist, flood

# Tool configuration
tool_number = 1             # Tool identifier number
spin_mode = "clockwise"     # clockwise, counter
spindle_rpm = 1000          # Spindle speed in revolutions per minute
power_level = 50            # Power level for energy-based tools
warmup_delay = 2.0          # Delay after tool start/stop in time_units

# Speeds in units per minute
work_speed = "500.0mm"      # Speed during operations
plunge_speed = "100.0mm"    # Speed when tool enters material
travel_speed = "1000.0mm"   # Speed between operations

# Z-axis heights
work_z = "0.0mm"            # Z height during operations
plunge_z = "1.0mm"          # Z height for initial material contact
safe_z = "10.0mm"           # Z height for movements between operations
park_z = "50.0mm"           # Z height when parked

# =====================================================================
# Layer-Specific Settings
#
# - Create a new [layer-N] section for each layer.
# - Settings not specified here will inherit from the [document] section.
# - Layers are numbered in the order they appear in the document.
# =====================================================================

[layer-0]

# head_mode = "basic"
# tool_mode = "marker"
# rack_mode = "manual"
# coolant_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"

[layer-1]

# head_mode = "basic"
# tool_mode = "marker"
# rack_mode = "manual"
# coolant_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"

[layer-2]

# head_mode = "basic"
# tool_mode = "marker"
# rack_mode = "manual"
# coolant_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"
```