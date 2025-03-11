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
head_mode = "basic"         # basic, mapped
tool_mode = "marker"        # beam, blade, extruder, marker, spindle
rack_mode = "manual"        # off, manual, automatic
coolant_mode = "off"        # off, mist, flood
fan_mode = "off"            # off, on
bed_mode = "off"            # off, heated

# Tool configuration
tool_number = 1             # Tool identifier number
spin_mode = "clockwise"     # off, clockwise, counter
spindle_rpm = 1000          # Spindle speed in revolutions per minute
power_mode = "constant"     # off, constant, dynamic
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

# Extrusion parameters
nozzle_diameter = "0.4mm"     # Diameter of the extruder's noozle
filament_diameter = "1.75mm"  # Diameter of the extruded filament
layer_height = "0.2mm"        # Height of each layer
retraction_distance = "1.5mm" # How much filament to retract
retraction_speed = "2100mm"   # Speed at which to retract filament

# Heightmap configuration
height_map_path =           # Heightmap file path
height_map_scale = 50.0     # Scale of the heightmap
height_map_tolerance = 0.01 # Heightmap sampling tolerance

# Other parameters
fan_speed = 255             # min = 0, max = 255
bed_temperature = 60        # Celsius degrees
hotend_temperature = 120    # Celsius degrees

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
# fan_mode = "off"
# bed_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_mode = "constant"
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"
# nozzle_diameter = "0.4mm"
# filament_diameter = "1.75mm"
# layer_height = "0.2mm"
# retraction_distance = "1.5mm"
# retraction_speed = "2100mm"
# height_map_path =
# height_map_scale = 50.0
# height_map_tolerance = 0.01
# fan_speed = 255
# bed_temperature = 60
# hotend_temperature = 120

[layer-1]

# head_mode = "basic"
# tool_mode = "marker"
# rack_mode = "manual"
# coolant_mode = "off"
# fan_mode = "off"
# bed_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_mode = "constant"
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"
# nozzle_diameter = "0.4mm"
# filament_diameter = "1.75mm"
# layer_height = "0.2mm"
# retraction_distance = "1.5mm"
# retraction_speed = "2100mm"
# height_map_path =
# height_map_scale = 50.0
# height_map_tolerance = 0.01
# fan_speed = 255
# bed_temperature = 60
# hotend_temperature = 120

[layer-2]

# head_mode = "basic"
# tool_mode = "marker"
# rack_mode = "manual"
# coolant_mode = "off"
# fan_mode = "off"
# bed_mode = "off"
# tool_number = 1
# spin_mode = "clockwise"
# spindle_rpm = 1000
# power_mode = "constant"
# power_level = 50
# warmup_delay = 2.0
# work_speed = "500.0mm"
# plunge_speed = "100.0mm"
# travel_speed = "1000.0mm"
# work_z = "0.0mm"
# plunge_z = "1.0mm"
# safe_z = "10.0mm"
# park_z = "50.0mm"
# nozzle_diameter = "0.4mm"
# filament_diameter = "1.75mm"
# layer_height = "0.2mm"
# retraction_distance = "1.5mm"
# retraction_speed = "2100mm"
# height_map_path =
# height_map_scale = 50.0
# height_map_tolerance = 0.01
# fan_speed = 255
# bed_temperature = 60
# hotend_temperature = 120
```