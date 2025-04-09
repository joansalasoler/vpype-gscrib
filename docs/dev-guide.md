# Development Guide

Welcome to the development guide for **Vpype-Gscrib**. This guide will
walk you through the process of setting up your development environment
and extend the project with new features.

---

## Introduction

**Vpype-Gscrib** is a plugin for [vpype](https://github.com/abey79/vpype),
an extensible command-line tool designed for generating, optimizing, and
processing vector graphics for plotters. *Vpype* simplifies working
with SVG paths, provides powerful transformation capabilities, manages
multi-layer compositions, and optimizes toolpaths for efficient execution.

This plugin enables the generation of G-code programs directly from
*vpype* documents, making it possible to control CNC machines, pen
plotters, and other G-code-compatible devices. To achieve this, it
leverages [Gscrib](https://github.com/joansalasoler/gscrib), a Python
library that provides a set of tools for G-code generation.

By combining the flexibility of **Vpype** with the G-code generation
capabilities of **Gscrib**, Vpype-Gscrib serves as a versatile tool
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
git clone https://github.com/joansalasoler/vpype-gscrib.git
cd vpype-gscrib
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
vpype gscrib --help
```

## Project Structure

Here's a brief overview of the `vpype-gscrib` project structure:

```bash
vpype-gscrib/
├── vpype_gscrib/         # Main package directory
│   ├── __init__.py       # Package initialization
│   ├── vpype_gscrib.py   # Command line interface (CLI)
│   ├── vpype_options.py  # Command line options
│   ├── renderer          # Generates G-code from documents
│   └── ...               # Other module files
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
python -m pytest
```

## Extending the Plugin

### Adding Configuration Parameters

Configuration parameters allow users to customize the behavior of
various components within the system. These parameters can be set via
command-line options or TOML configuration files, and are tipically
accessed through the rendering context (`GContext`).

The following steps outline how to add a new parameter.

**Define the Option:**

1. Open `vpype_gscrib/vpype_options.py`.
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

1. Open `vpype_gscrib/config/renderer_config.py`.
2. Add a property to `RendererConfig` with the same name as the option.
3. Use [pydantic](https://docs.pydantic.dev/latest/) for validation
   (ensure correct type and range of values).

```python
@dataclass
class RenderConfig(BaseModel, BaseConfig):
    length_units: LengthUnits = Field(LengthUnits.MILLIMETERS)
```

### Adding New Renderer Components

This is the fun part! `GRenderer` delegates specific machine operations
to specialized components in order to generate a G-code program. This
modular approach allows different strategies to be swapped without
modifying the renderer's core logic. Each type of component has multiple
implementations, giving users flexibility in configuring their
machine's behavior.

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

**Define a New Type for the Component:**

Each renderer component is associated with a **type**, which defines the
available options for that component. These types are stored in an
enum —a predefined list of valid options that users can choose from.
To register your component, add a corresponding type to the enum.

```python
class HeadType(BaseEnum):
    STANDARD = 'standard'
    CUSTOM = 'custom'  # New type
```

**Map the Type to the Implementation:**

Now that the system recognizes your new type, you need to specify which
class should be instantiated when that type is selected. This is done in
the **component's factory**, which maps each type to its implementation.

```python
class HeadFactory:

    @classmethod
    def create(cls, head_type: HeadType) -> BaseHead:
        providers = {
            HeadType.STANDARD: StandardHead,
            HeadType.CUSTOM: CustomHead,  # Register new component
        }

        return providers[head_type]()
```

**Test your component:**

```bash
vpype read input.svg gscrib --head-type=custom --output=output.gcode
```

### Generating G-code Inside Renderer Components

All renderer component methods receive a [GCodeBuilder](https://gscrib.readthedocs.io/en/latest/api/gscrib.html#gscrib.GCodeBuilder)
instance through the `ctx.g` attribute. This object, provided by the
**Gscrib** library, is your main interface for generating G-code. Instead
of writing raw G-code strings, you'll use high-level methods that handle
syntax, state management, and safety for you.

`GCodeBuilder` makes it easier to build G-code programs by abstracting
away low-level details. It helps you keep track of things like the machine's
position, feed rate, tool state, and more. It also supports advanced
features such as path interpolation, and built-in safety checks.

For example, a retract and plunge sequence could be written like this:,

```python
ctx.g.rapid(Z=ctx.safe_z)
ctx.g.move(Z=ctx.work_z, F=ctx.plunge_speed)
```

You can also use it to generate more complex toolpaths like arcs and splines,
apply transformations like scaling or rotation, and insert comments or
conditional logic using standard Python syntax.

Using **Gscrib** has several advantages:

- **Safety**: It automatically validates commands to prevent unsafe
  operations.
- **Flexibility**: Use Python control structures to build dynamic,
  reusable routines.
- **Efficiency**: It simplifies repetitive tasks and reduces human error.
- **Readability**: It produces clean, structured code that's easier to
  maintain.

To dive deeper into everything **Gscrib** can do, check out the official
[Gscrib Documentation](https://gscrib.readthedocs.io).

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

* Check out the [documentation](https://vpype-gscrib.readthedocs.io/en/latest/).
* [Open an issue](https://github.com/joansalasoler/vpype-gscrib/issues) on GitHub.

Happy coding, and don't forget to have fun! We hope you enjoy working
with **vpype-gscrib** as much as we do. Feel free to contribute,
experiment, and bring your creative ideas to life!
