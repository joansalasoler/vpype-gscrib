# User Guide

Thank you for choosing **Vpype-Mecode**. This guide will help you get
started with converting vector graphics into G-code for CNC machines,
plotters, laser engravers, and other compatible devices.

**What You'll Learn:**

* How to install and use the plugin
* How to configure your machine settings
* How to optimize G-code for efficiency

---

## Introduction

**Vpype-Mecode** extends [vpype](https://github.com/abey79/vpype) with
G-code generation capabilities. It allows you to convert SVG files and
other vector graphics into machine-compatible G-code, with support for
multiple tool types, speed control, and per-layer configurations.

**Key Features:**

* Converts vector paths into optimized G-code
* Supports multiple tool types (pens, lasers, spindles, etc.)
* Configurable speeds, units, and tool changes
* Per-layer settings using TOML configuration files
* Direct output to terminal, file, or machine

```{warning}
This project is currently under active development and is mostly
untested. Some features may be missing or not work as expected. Use with
caution in production environments.
```

## Installation

To install the latest development version:

**Clone the repository:**

```bash
git clone https://github.com/joansalasoler/vpype-mecode.git
cd vpype-mecode
```

**Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

**Install dependencies:**

```bash
pip install --upgrade pip  # Upgrade pip
pip install -e .  # Install in development mode
pip install -r requirements.txt  # Install additional dependencies
```

## Basic Usage

```{warning}
Always test the generated G-code in a simulator before running it.
Incorrect G-code can damage your machine, tools, or workpiece.
```

### Converting an SVG to G-code

Use the `mecode` pipe to generate G-code from an SVG:

```bash
vpype read drawing.svg mecode --outfile=output.gcode
```

### Specifying Length Units

You can use metric (mm) or imperial (inches) units:

```bash
vpype read drawing.svg mecode --length_units=in --outfile=output.gcode
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
  mecode --outfile=output.gcode
```

**What Each Command Does:**

* **linemerge**: Merges nearly identical lines.
* **linesimplify**: Reduces complexity while preserving shape.
* **reloop**: Optimizes loop paths.
* **linesort**: Sorts paths to minimize travel moves.

For a complete list of options to generate your G-code programs, check
the [Vpype-Mecode Command-Line Reference](cli). You may also find
[Vpype's Command-line Reference](https://vpype.readthedocs.io/en/latest/reference.html)
and
[Cookbook](https://vpype.readthedocs.io/en/latest/cookbook.html)
helpful for mastering this powerful tool.

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
length_units = "mm"          # Using metric units
tool_mode = "marker"         # Using marker mode for pen plotting
rack_mode = "manual"         # Manual tool changes for different pens
travel_speed = "3000mm"      # Speed for non-drawing moves
safe_z = "1cm"               # Safe height for non-drawing moves
plunge_z = "1mm"             # Height at which to begin plunging

# Settings for first layer (black fine liner)

[layer-0]
work_speed = "1200mm"        # Faster speed for simple lines
plunge_speed = "500mm"       # Gentle pen lowering speed

# Settings for second layer (red marker)

[layer-1]
work_speed = "800mm"         # Slower for better ink flow
plunge_speed = "400mm"       # Gentler pen lowering for softer tip

# Settings for third layer (thick marker)

[layer-2]
work_speed = "600mm"         # Even slower for thick lines
plunge_speed = "50mm"        # Very gentle pen lowering
```

### Using a Configuration File

To apply a configuration file:

```bash
vpype read drawing.svg mecode --render_config=config.toml --outfile=output.gcode
```