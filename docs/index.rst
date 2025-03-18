Vpype-Mecode: G-Code Plugin for Vpype
=====================================

This `vpype` plugin provides a comprehensive toolkit and command line
interface for processing vector paths and generating G-code commands
for CNC machines, plotters, and other G-code compatible devices.

Is This the Right Tool for You?
-------------------------------

**Vpype-Mecode** is designed for a wide range of users, from hobbyists
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

The goal of **vpype-mecode** is to provide a seamless and flexible way
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

By achieving these goals, **vpype-mecode** aims to be a valuable tool for
designers, engineers, and makers looking to bridge the gap between digital
vector graphics and automated manufacturing.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   Home <self>
   User Guide <user-guide>
   Machine Modes <machine-modes>
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

   vpype_mecode.config
   vpype_mecode.enums
   vpype_mecode.excepts
   vpype_mecode.heightmaps
   vpype_mecode.processor
   vpype_mecode.builder
   vpype_mecode.builder.codes
   vpype_mecode.builder.enums
   vpype_mecode.builder.formatters
   vpype_mecode.builder.writters
   vpype_mecode.builder.utils
   vpype_mecode.renderer
   vpype_mecode.renderer.beds
   vpype_mecode.renderer.coolants
   vpype_mecode.renderer.fans
   vpype_mecode.renderer.heads
   vpype_mecode.renderer.racks
   vpype_mecode.renderer.tools
