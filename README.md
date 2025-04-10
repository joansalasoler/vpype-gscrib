[![PyPI version](https://img.shields.io/pypi/v/vpype-gscrib.svg)](https://pypi.org/project/vpype-gscrib/)
[![Python versions](https://img.shields.io/pypi/pyversions/vpype-gscrib.svg)](https://pypi.org/project/vpype-gscrib/)
[![Downloads](https://pepy.tech/badge/vpype-gscrib/month)](https://pepy.tech/project/vpype-gscrib)
[![codecov](https://codecov.io/gh/joansalasoler/vpype-gscrib/branch/main/graph/badge.svg)](https://codecov.io/gh/joansalasoler/vpype-gscrib)
[![License](https://img.shields.io/pypi/l/vpype-gscrib.svg)](https://pypi.org/project/vpype-gscrib/)

# Vpype-Gscrib: G-Code Plugin for Vpype

Plug-in that adds G-code generation capabilities to [`vpype`](https://github.com/abey79/vpype).

This plugin allows you to convert vector graphics into G-code commands
suitable for CNC machines, plotters, and other G-code compatible devices.
This plugin processes a vpype document and generates G-Code from it
using the [`Gscrib`](https://github.com/joansalasoler/gscrib) library.
The ouput can be sent to the teminal, a file or to a connected device
using `Gscrib`'s direct write mode.

## Features

- Convert vector paths to optimized G-code
- Support for multiple tool types (marker, spindle, beam, blade, extruder)
- Configurable machine parameters (speeds, power levels, spindle settings)
- Automatic and manual tool change support
- Coolant control (mist/flood)
- Bed control (heat/cool down)
- Fan speed control (on/off)
- Customizable units (metric/imperial)
- Use heightmaps for Z height compensation
- Per-layer configuration support via TOML files

## Documentation

Documentation for the latest version of the project can be found at
[Read the Docs](https://vpype-gscrib.readthedocs.io/en/latest/).

## Examples

Here are some common usage examples:

```bash
# Basic G-code generation from an SVG file
vpype read input.svg gscrib --output=output.gcode

# Specify custom length units
vpype read input.svg gscrib --length-units=inches --output=output.gcode

# Load per layer rendering configurations from a file
vpype read input.svg gscrib --config=config.toml --output=output.gcode

# A more complete example using Vpype to optimize the G-Code output

vpype \
  read input.svg \
  linemerge --tolerance=0.5mm \
  linesimplify --tolerance=0.1mm \
  reloop --tolerance=0.1mm \
  linesort --two-opt --passes=250 \
  gscrib --config=config.toml --output=output.gcode
```

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

## Development setup

Here is how to clone the project for development:

```bash
$ git clone https://github.com/joansalasoler/vpype-gscrib.git
$ cd vpype-gscrib
```

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install `vpype-gscrib` and its dependencies (including `vpype`):

```bash
$ pip install --upgrade pip
$ pip install -e .
$ pip install -r requirements.txt
$ pip install -r requirements.dev.txt
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
