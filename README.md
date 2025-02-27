# G-Code Plugin for Vpype

Plug-in that adds G-code generation capabilities to [`vpype`](https://github.com/abey79/vpype).

This plugin allows you to convert vector graphics into G-code commands
suitable for CNC machines, plotters, and other G-code compatible devices.
This plugin processes a vpype document and generates G-Code from it
using a modified version of the [`mecode`](https://github.com/jminardi/mecode)
library. The ouput can be sent to the teminal, a file or to a printer
using `mecode`'s direct write mode.

⚠️ **Notice**: This project is currently under active development and is
mostly untested. Some features may be missing or not work as expected.
Use with caution in production environments.

⚠️ **Safety Warning**: Always test the generated G-code in a simulator
before running it. Incorrect G-code can damage your machine, tools, or
workpiece.

## Features

- Convert vector paths to optimized G-code
- Support for multiple tool types (marker, spindle, beam, blade, extruder)
- Configurable machine parameters (speeds, power levels, spindle settings)
- Automatic and manual tool change support
- Coolant control (mist/flood)
- Customizable units (metric/imperial)
- Per-layer configuration support via TOML files

## Examples

Here are some common usage examples:

```bash
# Basic G-code generation from an SVG file
vpype read input.svg mecode --outfile=output.gcode

# Specify custom length units
vpype read input.svg mecode --length_units=in --outfile=output.gcode

# Load per layer rendering configurations from a file
vpype read input.svg mecode --render_config=config.toml --outfile=output.gcode

# A more complete example using Vpype to optimize the G-Code output

vpype \
  read input.svg \
  linemerge --tolerance=0.5mm \
  linesimplify --tolerance=0.1mm \
  reloop --tolerance=0.1mm \
  linesort --two-opt --passes=250 \
  mecode --render_config=config.toml --outfile=output.gcode
```

## Configuration file

You can specify per-layer settings using a TOML configuration file.
Here's an example configuration for a pen plotter:

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

See the [config-template.toml](config-template.toml) file for a
complete configuration example.

## Documentation

The latest documentation of the project can be found at
[Read the Docs](https://vpype-mecode.readthedocs.io/en/latest/).

The command line documentation is also available using the `--help` flag:

```bash
$ vpype mecode --help
```

## Development setup

See the [installation instructions](https://vpype.readthedocs.io/en/latest/install.html)
for information on how to install `vpype`.

Here is how to clone the project for development:

```bash
$ git clone https://github.com/joansalasoler/vpype-mecode.git
$ cd vpype-mecode
```

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install `vpype-mecode` and its dependencies (including `vpype`):

```bash
$ pip install -e .
$ pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (```git checkout -b feature/amazing-feature```)
3. Commit your changes (```git commit -m 'Add some amazing feature'```)
4. Push to the branch (```git push origin feature/amazing-feature```)
5. Open a Pull Request

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the [LICENSE](LICENSE) file for more details.
