# Change log

## 1.2.0 (2025-11-20)

* Adds support for Python 3.13.
* Adds support for Gscrib 1.2.0.
* Adds support for Vpype 1.15.0.
* Adds `tox` for multi-version testing with Poetry.
* Relaxes dependency constraints and upgrades multiple dependencies.

## 1.1.1 (2025-05-01)

* Rename HeightMap.get_height_at to HeightMap.get_depth_at.
* Adds width/height accessors for raster heightmap images.
* Adds an export to image method for sparse heightmaps.
* Fix: Raster interpolation out-of-range values.
* Fix: Sparse heightmaps returning NaN.
* Fix: Sparse heightmaps transposing rows/cols.

## 1.1.0 (2025-04-29)

* Upgrades Gscrib to version 1.1.0.
* Adds support for sparse heightmaps (.csv and similar formats).
* Adds command-line option to set resolution for interpolated moves.
* Displays Gscrib version in output headers.
* Sets default heightmap Z scale to 1.0.

## 1.0.1 (2025-04-18)

* End G-code programs with M02 instead of M30.
* Fix port type in direct write to socket.
* Upgrade to GScrib 1.0.1 (direct write fix).

## 1.0.0 (2025-04-16)

* First stable release

## 0.1.1 (2025-04-09)

* First release of Vpype-Gscrib.

## 0.1.0 (UNRELEASED)

* Initial release
