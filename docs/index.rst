Vpype-Gscrib: G-Code Plugin for Vpype
=====================================

This `vpype` plugin provides a comprehensive toolkit and command line
interface for processing vector paths and generating G-code commands
for CNC machines, plotters, and other G-code compatible devices.

Is This the Right Tool for You?
-------------------------------

**Vpype-Gscrib** is designed for a wide range of users, from hobbyists
to professional CNC programmers. If you're working with vector-based
designs and need precise, customizable control over G-code generation,
this tool is made for you.

**You might find this tool useful if:**

- **You use CNC machines, laser cutters, or plotters** and need a simple,
  streamlined way to generate G-code from SVG files.
- **You need full control** over tool movements, speeds, and intricate
  multi-layer operations for maximum precision.
- **You need to adjust tool movements** for uneven surfaces, curved
  objects, and detailed engraving, ensuring precision every time.
- **You work with different machine types** and need a tool that supports
  customizable configurations for pens, lasers, spindles, and more.
- **You are an artist or designer** working with pen plotters or laser
  engravers for creative projects.
- **You are a maker or researcher** experimenting with computational
  design, generative manufacturing, or cutting-edge machining techniques.
- **You are a developer or engineer** needing to automate or customize
  G-code generation for specialized applications.

Aim of the Project
------------------

The goal of **vpype-gscrib** is to provide a seamless and flexible way
to generate G-code programs from vector-based designs.

**Key Objectives:**

- **Accuracy & Reliability** — Generate correct and consistent G-code
  output, ensuring compatibility with different machines and workflows.
- **Flexibility** — Support a wide range of use cases, from CNC milling
  to pen plotting, by allowing users to configure and adapt the G-code
  generation process to meet their specific needs.
- **Extensibility** — Provide a highly modular and developer-friendly
  architecture that makes it easy to add new features, support additional
  hardware, and adapt to different workflows with minimal effort.
- **Ease of Use** — Provide an intuitive and well-documented API that
  seamlessly integrates with existing *vpype* workflows, making it easy
  for developers to adopt and use.
- **Open-Source Collaboration** — Encourage contributions from the
  community to enhance the plugin's capabilities and adapt it to new
  use cases.

By achieving these goals, **vpype-gscrib** aims to be a valuable tool for
designers, engineers, and makers looking to bridge the gap between digital
vector graphics and automated manufacturing.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   Home <self>
   User Guide <user-guide>
   Machine Components <machine-modes>
   Development Guide <dev-guide>
   Command Line Interface <cli>
   Configuration Template <config>
   G-Code Mappings Table <gcode-table>
   Module Index <modindex>
   General Index <genindex>
   License <license>

API Reference
-------------

.. autosummary::
   :toctree: api
   :caption: API Reference
   :template: module.rst
   :recursive:

   vpype_gscrib.config
   vpype_gscrib.enums
   vpype_gscrib.excepts
   vpype_gscrib.heightmaps
   vpype_gscrib.processor
   vpype_gscrib.gscrib
   vpype_gscrib.gscrib.codes
   vpype_gscrib.gscrib.enums
   vpype_gscrib.gscrib.excepts
   vpype_gscrib.gscrib.formatters
   vpype_gscrib.gscrib.writers
   vpype_gscrib.renderer
   vpype_gscrib.renderer.beds
   vpype_gscrib.renderer.coolants
   vpype_gscrib.renderer.fans
   vpype_gscrib.renderer.heads
   vpype_gscrib.renderer.racks
   vpype_gscrib.renderer.tools
