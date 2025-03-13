# Machine Modes for G-code Generation

Vpype-Mecode allows users to configure the machine operation by combining
different **renderer components**, or modes. These modes control essential
aspects of machine behavior, including the bed, coolant, fan, toolhead
movement, tool changes, and tool operations.

---

## Bed Modes

The bed mode defines how the machine bed is controlled during the
operation.

* **heated**: The bed is heated to a target temperature when activated
  and the system waits for it to reach the set temperature.
* **off**: No bed operations are performed. This disables bed control
  and is used when no specific bed-related functionality is required.

## Coolant Modes

Coolant systems control the cooling mechanisms of the machine, such as
flood coolant or mist coolant. These are important for temperature
regulation during machining processes.

* **flood**: Activates the flood coolant system during machining.
* **mist**: Activates the mist coolant system during machining.
* **off**: Disables the coolant system.

## Fan Modes

Fan modes control the cooling fan of the machine, which is typically
used to cool down the system or remove debris.

* **cooling**: Activates a basic fan to cool down the system.
* **off**: Disables the fan, leaving it inactive during operations.

## Head Movement Modes

The head movement mode defines how the machine's head (tool carrier)
behaves during operations. Different heads offer varying levels of
precision and compensation.

* **standard**: Basic head movement mode that handles safe retraction,
  plunging, traveling, and tracing.
* **auto-leveling**: This advanced head mode integrates a height map for
  compensation, ensuring consistent tool engagement on uneven surfaces.

## Rack Modes

Rack modes determine how tools are handled during the operation. This
includes how tools are changed or managed.

* **automatic**: Allows for automatic tool changes, meaning the machine
  can change tools without manual intervention.
* **manual**: Requires the operator to manually change tools.
* **off**: Disables the rack, meaning no tool changes will occur.

## Tool Modes

The tool mode controls which tool is being used and how it operates. The
tool can range from laser tools to spindles or even markers, and each
tool may require different activation and deactivation patterns.

* **beam**: A basic beam tool, such as a laser, that handles activation,
  power control, and deactivation.
* **adaptive-beam**: A more advanced beam tool that integrates height map
  based power modulation. This tool adjusts the power of the beam depending
  on surface variation and allows for applications like photo engraving,
  surface processing, and material adaptation.
* **blade**: A blade tool, typically used for cutting, which does not
  require power control or activation.
* **heated-extruder**: Used in 3D printing, this tool controls temperature,
  filament retraction, and extrusion during the printing process.
* **marker**: A non-activated tool, such as a pen or brush, used for
  drawing or marking.
* **spindle**: A tool used for milling or drilling, which requires
  activation and deactivation to control the spindle motor.

## Combining Modes for Advanced G-code Generation

To configure the G-code generation, you can combine the relevant modes
according to your machine's capabilities and requirements. For example,
if you want to mill an uneven surface using a spindle, you could combine
the spindle tool, auto-leveling head, and flood coolant modes. This
ensures the spindle maintains a consistent cutting depth on the uneven
surface while keeping the material cool during the process.

```bash
vpype \
  read drawing.svg \
  mecode \
    --tool-mode=spindle \
    --coolant-mode=flood \
    --head-mode=auto-leveling \
    --rack-mode=manual \
    --height-map-path=map.png \
    --height-map-tolerance=0.01 \
    --height-map-scale=50.0 \
    --output=output.gcode
```

**Explanation:**

* **--tool-mode=spindle** — Use a spindle for milling
* **--head-mode=auto-leveling** — Use a heightmap to adjust Z-height
* **--coolant-mode=flood** — Apply flood coolant
* **--rack-mode=manual** — Requires manual tool changes
* **--height-map-path=map.png** — Height map for Z-height compensation
* **--height-map-tolerance=0.01** — Tolerance for height adjustments
* **--height-map-scale=50.0** — Scaling of the height map

When combining modes, ensure that the selected modes are compatible with
your machine's hardware and capabilities to avoid any issues. For a more
detailed list of each mode's available options, refer to the full
[Command-Line Reference](cli).