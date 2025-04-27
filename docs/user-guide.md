# User Guide

Thank you for choosing **Vpype-Gscrib**. This guide will help you get
started with converting vector graphics into G-code for CNC machines,
plotters, laser engravers, and other compatible devices.

**What You'll Learn:**

* How to install and use the plugin
* How to configure your machine settings
* How to optimize G-code for efficiency

---

## Introduction

**Vpype-Gscrib** extends [vpype](https://github.com/abey79/vpype) with
G-code generation capabilities. It allows you to convert SVG files and
other vector graphics into machine-compatible G-code, with support for
multiple tool types, speed control, and per-layer configurations.

**Key Features:**

* Converts vector paths into optimized G-code
* Supports multiple tool types (pens, lasers, spindles, etc.)
* Configurable speeds, units, and tool changes
* Per-layer settings using TOML configuration files
* Direct output to terminal, file, or machine

## Installation

Before you begin, ensure **Vpype** is installed by following the
[official installation guide](https://vpype.readthedocs.io/en/latest/install.html). Once **Vpype** is installed, you can install the latest version
of **Vpype-Gscrib** by running:

```bash
pipx inject vpype vpype-gscrib
```

Verify the installation by running:

```bash
vpype gscrib --help
```

Want to add new modes to **Vpype-Gscrib**? Check out our [Development Guide](dev-guide.md)
for step-by-step instructions on setting it up in development mode.

## Basic Usage

```{warning}
Always test the generated G-code in a simulator before running it.
Incorrect G-code can damage your machine, tools, or workpiece.
```

### Converting an SVG to G-code

Use the `gscrib` pipe to generate G-code from an SVG:

```bash
vpype read drawing.svg gscrib --output=output.gcode
```

### Specifying Length Units

You can use metric (millimeters) or imperial (inches) units:

```bash
vpype read drawing.svg gscrib --length-units=inches --output=output.gcode
```

## Advanced Usage & Optimization

For better G-code output, optimize your paths using *Vpype* commands:

```bash
vpype \
  read drawing.svg \
  linemerge --tolerance=0.5mm \
  linesimplify --tolerance=0.1mm \
  reloop --tolerance=0.1mm \
  linesort --two-opt --passes=250 \
  gscrib --output=output.gcode
```

**What Each Command Does:**

* **linemerge**: Merges nearly identical lines.
* **linesimplify**: Reduces complexity while preserving shape.
* **reloop**: Optimizes loop paths.
* **linesort**: Sorts paths to minimize travel moves.

For a complete list of options to generate your G-code programs, check
the [Vpype-Gscrib Command-Line Reference](cli). You may also find
[Vpype's Command-line Reference](https://vpype.readthedocs.io/en/latest/reference.html)
and
[Cookbook](https://vpype.readthedocs.io/en/latest/cookbook.html)
helpful for mastering this powerful tool.

## Component Types for G-code Generation

Vpype-Gscrib allows users to configure their machine's behavior during
G-code generation by selecting different modes. These modes control
various aspects of your machine's operation, including how the bed,
coolant, fan, head and the tools themselves function.

By combining the right modes, you can optimize your workflow and tailor
the G-code output to match your machine's capabilities and the specific
requirements of your project.

### What Are Component Types?

Component types are configurable components that govern machine behavior.
Each type is responsible for a different aspect of the machine's operation:

* **Bed Types**: Control the behavior of the machine's bed.
* **Coolant Types**: Manage the machine's coolant system.
* **Fan Types**: Activate or deactivate machine fans.
* **Head Movement Types**: Define how the tool head moves.
* **Rack Types**: Control how tools are changed during the process.
* **Tool Types**: Define how specific tools operate.

### Why Use Component Types?

By selecting and combining different modes, you can fine-tune your
G-code generation to match your machine's capabilities and your specific
use case. For example, if you're working with a laser cutter on an uneven
bed surface, you may choose to use an auto-leveling head or an adaptive
beam tool for optimal results.

Component types give you the flexibility to customize your workflow,
whether you're doing engraving, milling, 3D printing, or any other
CNC-related task.

### Learn More About Component Types

To explore the available types and how to combine them effectively,
please refer to our [Component Types Documentation](machine-modes.md),
which provides detailed descriptions and examples for each types.

## Height Maps

One of the most powerful features of this plugin is its ability to use
**height maps** to dynamically adjust tool operation based on surface
variations. Whether you're engraving on a curved object, compensating
for an uneven machine bed, or creating intricate textures, height maps
unlock new creative and technical possibilities.

### What Can You Do with Height Maps

* **Consistent depth**: Ensure uniform cutting, even if the material
  isn't perfectly flat.
* **Automatic bed leveling**: Compensate for an uneven bed without
  tedious manual adjustments.
* **Work on curved or irregular surfaces**: Effortlessly engrave, draw,
  or cut on cylinders, domed objects, wavy surfaces, or even complex
  freeform shapes like a hand-shaped sculpture.
* **Texture mapping**: Transform grayscale patterns into detailed
  topographical engravings, creating intricate artistic designs,
  functional surface textures, or even depth-based shading effects.
* **Photorealistic engraving**: Use height maps to control laser power,
  creating smooth gradients for photo engraving.
* **Dynamic tool modulation**: Adjust not just height, but also laser
  intensity, or other tool parameters based on image data.

### Reading Height Maps

Height maps can be provided in two primary formats, CSV files and grayscale
images (.tiff, .png, etc). Each format has its unique advantages, depending
on the level of precision needed and the specific application.

* **CSV files** store height data as (x, y, z) coordinates in a tabular
  format. Each row represents a single point on the surface with its
  corresponding height value. This method is useful for **precise**
  **height adjustments** and can handle **sparse data**.

* **Grayscale images** define surface variations based on pixel brightness,
  where **darker pixels** represent lower areas and **lighter pixels**
  represent higher areas. The pixel data is interpreted as a 2D grid where
  each pixel's brightness is mapped to a specific height value.

### Using Height Maps for Z Compensation

Here's an example of using a height map to dynamically adjust the Z
height during machining:

```bash
vpype \
  read drawing.svg \
  gscrib \
    --length-units=millimeters \
    --head-type=auto-leveling \
    --height-map-path=heightmap.csv \
    --output=output.gcode
```

By setting the head mode to `auto-leveling`, the system smoothly
interpolates between height values, ensuring precise tool movement
across the surface.

**Understanding the Options:**

* **--head-type=auto-leveling**: Enables Z-axis height map compensation.
* **--height-map-path**: Grayscale image defining height variations.

### Using Height Maps for Laser Power Modulation

Height maps can also be used to dynamically adjust laser power based on
a grayscale image, making it possible to engrave detailed photographs
with depth-based shading. Instead of modifying the Z height, the grayscale
values control the laser's intensity, allowing for smooth tonal transitions.

For example, in a laser engraving workflow, darker areas of the height
map correspond to lower laser power, while lighter areas increase
intensity. This technique is particularly useful for photo engraving, as
it preserves fine details and creates natural gradients.

Here's an example of generating G-code with laser power modulation:

```bash
vpype \
  read drawing.svg \
  gscrib \
    --tool-type=adaptive-beam \
    --power-mode=dynamic \
    --height-map-path=heightmap.png \
    --height-map-scale=100.0 \
    --output=output.gcode
```

**Key Options Explained**:

* **--tool-type=adaptive-beam**: Enable heightmap to control laser power.
* **--power-mode=dynamic**: Dynamically adjust laser power.
* **--height-map-scale=100**: Scale factor for power adjustments

By leveraging this technique, you can transform photographs into detailed
engravings with smooth shading and precise contrast.

## Advanced Configuration

The plugin supports per-layer configurations via a TOML file. This lets
you set different speeds, tools, and work depths for each layer of
the document.

### Example Configuration

Here's a basic example configuration for a pen plotter. See the
[config-template.toml](config.md) file for a complete configuration
example.

```ini
# Document-level configuration. These settings control the machine's
# behavior between layer operations. All layers inherit these values
# unless specifically overridden in their [layer-X] section.

[document]
length-units = "millimeters" # Using metric units
tool-type = "marker"         # Using marker mode for pen plotting
rack-type = "manual"         # Manual tool changes for different pens
travel-speed = "3000mm"      # Speed for non-drawing moves
safe-z = "1cm"               # Safe height for non-drawing moves
plunge-z = "1mm"             # Height at which to begin plunging

# Settings for first layer (black fine liner)

[layer-1]
work-speed = "1200mm"        # Faster speed for simple lines
plunge-speed = "500mm"       # Gentle pen lowering speed

# Settings for second layer (red marker)

[layer-2]
work-speed = "800mm"         # Slower for better ink flow
plunge-speed = "400mm"       # Gentler pen lowering for softer tip

# Settings for third layer (thick marker)

[layer-3]
work-speed = "600mm"         # Even slower for thick lines
plunge-speed = "50mm"        # Very gentle pen lowering
```

### Using a Configuration File

To apply a configuration file:

```bash
vpype read drawing.svg gscrib --config=config.toml --output=output.gcode
```