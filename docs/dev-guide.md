# Development Guide

Welcome to the development guide for **Vpype-Mecode**. This guide will
walk you through the process of setting up your development environment
and extend the project with new features.

---

## Introduction

**Vpype-Mecode** is a plugin for [vpype](https://github.com/abey79/vpype),
an extensible command-line tool designed for generating, optimizing, and
processing vector graphics for plotters. *Vpype* simplifies working
with SVG paths, provides powerful transformation capabilities, manages
multi-layer compositions, and optimizes toolpaths for efficient execution.

This plugin enables the generation of G-code programs directly from
*vpype* documents, making it possible to control CNC machines, pen
plotters, and other G-code-compatible devices. To achieve this, it
leverages [mecode](https://github.com/jminardi/mecode), a Python library
that provides a set of tools for G-code generation.

By combining the flexibility of **vpype** with the G-code generation
capabilities of **mecode**, *vpype-mecode* serves as a versatile tool
for translating vector-based designs into precise machine instructions.
Whether you're an artist, maker, or engineer, this tool empowers you to
bring intricate designs to life with precision and efficiency.

## Getting Started

### Prerequisites

Before you start, make sure you have the following installed on your
machine:

- **Python** (3.10 or newer)
- **Pip** (Python package manager)
- **Git** (Version control tool)

If you need help installing any of these, check out their official
installation guides:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Setting Up the Development Environment

Follow these steps to set up your development environment:

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
pip install -r requirements.dev.txt  # Install development dependencies
```

**Check the plugin is working:**

```bash
vpype mecode --help
```

## Project Structure

Here's a brief overview of the `vpype-mecode` project structure:

```bash
vpype-mecode/
├── vpype_mecode/         # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── vpype_mecode.py   # Command line interface (CLI)
│   ├── vpype_options.py  # Command line options
│   └── ...               # Other module files
├── mecode/               # Modified Mecode library
├── tests/                # Tests directory
└── docs/                 # Documentation builder
```

## Documentation and Testing

To build the documentation locally run the following commands. This will
generate the documentation in the `./docs/html` directory. Open `index.html`
in a web browser to view it.

```bash
cd docs
pip install -r requirements.txt
python -m sphinx . ./html
```

To run the test suite, use `pytest`. This will automatically discover
and run all the tests in the project. You can also run specific tests
by referring to the [pytest documentation](https://docs.pytest.org/en/stable/).

```bash
pytest
```

## Extending the Plugin

### Adding Configuration Parameters

Configuration parameters allow users to customize the behavior of
various components within the system. These parameters can be set via
command-line options or TOML configuration files, and are tipically
accessed through the rendering context (`GContext`).

The following steps outline how to add a new parameter.

**Define the Option:**

1. Open `vpype_mecode/vpype_options.py`.
2. Add an option with a name, type, and short help message.
3. Use the correct type (e.g.,
   [LengthType](https://vpype.readthedocs.io/en/latest/api/vpype_cli.html)
   for lengths).

```python
ConfigOption(
    option_name='length-units',
    help="Choose the unit of measurement for the output G-Code.",
    type=LengthUnits,
)
```

**Store the Option:**

1. Open `vpype_mecode/config/renderer_config.py`.
2. Add a property to `RendererConfig` with the same name as the option.
3. Use [pydantic](https://docs.pydantic.dev/latest/) for validation
   (ensure correct type and range of values).

```python
@dataclass
class RenderConfig(BaseModel, BaseConfig):
    length_units: LengthUnits = Field(LengthUnits.MILLIMETERS)
```

### Adding G-code Commands

G-code commands define specific machine instructions within the system.
These commands are implemented using enums and mapped to their
corresponding G-code instructions. The `GBuilder` class provides
high-level methods to generate and manage these commands.

The following steps outline how to add a new G-code command.

**Define the Command:**

1. Create a new enum for command inside `vpype_mecode/enums/`.
2. Make sure the enum extends `BaseEnum`.

```python
from vpype_mecode.builder.enums import BaseEnum

class LengthUnits(BaseEnum):
    INCHES = 'in'
    MILLIMETERS = 'mm'
```

**Map the Command:**

1. Open `vpype_mecode/codes/mappings.py`.
2. Add the enum values and their G-code instructions.

```python
gcode_table = GCodeTable((
    GCodeEntry(LengthUnits.INCHES, 'G20', 'Set length units, inches'),
    GCodeEntry(LengthUnits.MILLIMETERS, 'G21', 'Set length units, millimeters'),
))
```

**Implement the Command:**

1. Open `vpype_mecode/renderer/gcode_builder.py`.
2. Modify `GBuilder` to support the new command by adding a new method.
3. Use `self._get_statement()` to build the G-code statement.
4. Write the G-code statement using `self.write(statement)`.

```python
@typechecked
def select_units(self, length_units: LengthUnits) -> None:
    statement = self._get_statement(length_units)
    self.write(statement)
```

By following these steps, you ensure that the new G-code command
integrates seamlessly with the existing system while maintaining
consistency and correctness.

### Adding New Renderer Components

This is the fun part! `GRenderer` delegates specific machine operations
to specialized components in order to generate a G-code program. This
modular approach allows different strategies to be swapped without
modifying the renderer’s core logic. Each type of component has multiple
implementations, giving users flexibility in configuring their
machine’s behavior.

Currently, the system supports the following component types:

* **Tool** — Handles tool operations (activation, deactivation).
* **Head** — Controls machine movements (travel, plunge, retract).
* **Coolant** — Manages the coolant system (flood, mist).
* **Fan** — Manages the machine fans (on, off ).
* **Rack** — Manages tool changes and rack operations.
* **Bed** — Manages the machine bed or table.

The renderer coordinates these components to process the document
hierarchy and create the G-code program. They are instantiated from
their respective factory classes based on user choices. For example,
combining the following components for a standard milling setup:

* A spindle tool (`SpindleTool`)
* Manual tool changes (`ManualRack`)
* Flood coolant (`FloodCoolant`)

Here's how to add a new component.

**Implement the Component:**

Define a new component by extending the appropriate abstract base class
(`BaseTool`, `BaseHead`, `BaseCoolant`, `BaseFan`, `BaseRack`, `BaseBed`).
Each method receives a `GContext`, which holds the configuration for the
specific document layer or the entire document being rendered.

```python
class CustomHead(BaseHead):

    def safe_retract(self, ctx):
        ctx.g.rapid(Z=ctx.safe_z)

    def retract(self, ctx):
        ctx.g.rapid(Z=ctx.safe_z)

    def plunge(self, ctx):
        ctx.g.move(Z=ctx.plunge_z, F=ctx.travel_speed)
        ctx.g.move(Z=ctx.work_z, F=ctx.plunge_speed)

    def travel_to(self, ctx, x, y):
        ctx.g.move(x, y, F=ctx.travel_speed)

    def trace_to(self, ctx, x, y):
        ctx.g.move(x, y, F=ctx.work_speed)

    def park_for_service(self, ctx: GContext):
        ctx.g.rapid(Z=ctx.park_z)
        ctx.g.rapid_absolute(0, 0)
```

**Define a New Mode for the Component:**

Each renderer component is associated with a **mode**, which defines the
available options for that component type. These modes are stored in an
enum —a predefined list of valid options that users can choose from.
To register your component, add a corresponding mode to the enum.

```python
class HeadMode(BaseEnum):
    STANDARD = 'standard'
    CUSTOM = 'custom'  # New mode
```

**Map the Mode to the Implementation:**

Now that the system recognizes your new mode, you need to specify which
class should be instantiated when that mode is selected. This is done in
the **component’s factory**, which maps each mode to its implementation.

```python
class HeadFactory:

    @classmethod
    def create(cls, mode: HeadMode) -> BaseHead:
        providers = {
            HeadMode.STANDARD: StandardHead,
            HeadMode.CUSTOM: CustomHead,  # Register new component
        }

        return providers[mode]()
```

**Test your component:**

```bash
vpype read input.svg mecode --head-mode=custom --output=output.gcode
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. **Fork the repository** on GitHub.
2. **Create your feature branch**:

```bash
git checkout -b feature/your-new-feature
```

3. **Make your changes** and commit them:

```bash
git commit -m "Add a detailed description of your feature"
```

4. **Push your changes** to the branch:

```bash
git push origin feature/your-new-feature
```

5. **Open a Pull Request** on GitHub.

Please ensure your code follows a style consistent with the project's
own and includes tests for any new functionality.

## Getting Help

If you need help or have questions, feel free to:

* Check out the [documentation](https://vpype-mecode.readthedocs.io/en/latest/).
* [Open an issue](https://github.com/joansalasoler/vpype-mecode/issues) on GitHub.

Happy coding, and don't forget to have fun! We hope you enjoy working
with **vpype-mecode** as much as we do. Feel free to contribute,
experiment, and bring your creative ideas to life!
