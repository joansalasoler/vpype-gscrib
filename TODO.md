# TODO List (More Like a Wish List)

This is a collection of ideas, potential improvements, and experiments.
Most are purely theoretical or fantasious and may never be implemented,
but they are interesting to consider.

## Unit Tests

Add more test cases.

## Simplify and Improve Mecode

While the Mecode library is great, it has some options that I feel
should be removed or better implemented as machine components. For
example, extrusion, filament and layer height settings.

## Multipass Strategies

Vpype’s **multipass** command duplicates lines, useful for pens but not
ideal for Z-height control. A better approach would allow roughing and
finishing passes with different settings. Currently, this can be done by
duplicating layers manually, but it's not convenient.

## Heightmap Tool Compensation

While currently used for Z-height adjustment, future implementations
could use height maps to modulate tool power instead. For example, to
adjust a laser’s intensity or control extrusion rates.

## Z Height Adjustment by Pen Thickness

Vpype supports setting pen thickness. This could be used to adjust
Z height automatically for machines without built-in pressure control.

## Artistic Painting with Acrylic Markers

A head mode that adjusts pressure (Z height) and speed based on stroke
type, angle, length, and randomness. Would create a more human-like
artistic effect.

## Custom Brush Strokes with AI

Develop an AI system that learns from existing artwork or brushstroke
patterns and can generate custom brush strokes or designs that match a
particular style or texture. A custom SDXL model to generate heightmaps
could be used for this purpose.

## DIY Automatic Tool Change

A system to bring the machine to the tool and grab it —or even dip a
brush into paint.

## G-code Commands

* **G43, G44:** Tool Length Compensation
* **M106:** Support for multiple fans (P<index>)
* **M141:** Set Chamber Temperature
