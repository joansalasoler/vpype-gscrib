Vpype-Mecode: G-Code Plugin for Vpype
=====================================

This `vpype` plugin provides a comprehensive toolkit and command line
interface for processing vector paths and generating G-code commands
for CNC machines, plotters, and other G-code compatible devices.

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
   Development Guide <dev-guide>
   Command Line Interface <cli>
   Example Configuration <config>
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

   vpype_mecode.codes
   vpype_mecode.config
   vpype_mecode.enums
   vpype_mecode.excepts
   vpype_mecode.processor
   vpype_mecode.renderer
   vpype_mecode.renderer.beds
   vpype_mecode.renderer.coolants
   vpype_mecode.renderer.fans
   vpype_mecode.renderer.heads
   vpype_mecode.renderer.racks
   vpype_mecode.renderer.tools
   vpype_mecode.utils
