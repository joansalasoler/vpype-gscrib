# TODO List (More Like a Wish List)

This is a collection of ideas, potential improvements, and experiments.
Most are purely theoretical or fantasious and may never be implemented,
but they are interesting to consider.

## Unit Tests

Add more test cases.

## Known Bugs (a.k.a. Hidden Features)

The heightmap is applied even when no component requires it, causing
unnecessary stroke splits if a heightmap is defined.

Moving the head to "park for service" is unnecessary when tool swapping
is disabled.

Prevent users from setting safe_z lower than work_z and plunge_z when
using heightmaps to avoid plunging below the material.

## Multipass Strategies

Vpype’s **multipass** command duplicates lines, useful for pens but not
ideal for Z-height control. A better approach would allow roughing and
finishing passes with different settings. Currently, this can be done by
duplicating layers manually, but it's not convenient.

## Z Height Adjustment by Pen Thickness

Vpype supports setting pen thickness. This could be used to adjust
Z height automatically for machines without built-in pressure control.
This can be handled by a heightmap generator.

## Artistic Painting with Acrylic Markers

A head mode that adjusts pressure (Z height) and speed based on stroke
type, angle, length, and randomness. Would create a more human-like
artistic effect. This can be handled by a heightmap generator.

## Custom Brush Strokes with AI

Develop an AI system that learns from existing artwork or brushstroke
patterns and can generate custom brush strokes or designs that match a
particular style or texture. A custom SDXL model to generate heightmaps
could be used for this purpose.

## DIY Automatic Tool Change

A system to bring the machine to the tool and grab it —or even dip a
brush into paint.

## G-code Optimization Postprocessor

The current implementation prioritizes safety and consistency by
explicitly setting all parameters in each G-code command. While this
approach works well for direct machine control, it generates redundant
commands and verbose output files.

A postprocessor could optimize the G-code by removing duplicate
parameters and omitting unchanged values, resulting in more compact and
efficient files while maintaining the same machine behavior.

## G-code Commands

* **G43, G44:** Tool Length Compensation
* **M106:** Support for multiple fans (P<index>)
* **M141:** Set Chamber Temperature
