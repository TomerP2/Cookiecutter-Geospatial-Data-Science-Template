# QGIS layer definitions

Save drag-and-drop `.qlr` files directly in this folder for both vector and raster
outputs, including their symbology. Keep datasets under `data/` and use relative
references from each `.qlr`, such as `../data/processed/elevation.tif` or
`../data/processed/boundaries.gpkg`. Use matching dataset stems; add a grouped
definition when several layers form a useful view.

Drag a `.qlr` into QGIS to load its styled layers. It references rather than embeds
the data, so share both folders together and preserve their layout. Reload the
definition to pick up later styling changes. Verify loading and styling in a fresh
QGIS project; report any visual review still pending.

Keep optional inspection projects (.qgz/.qgs) in `projects/`; their relative data
paths start at `../../data/`. Create `styles/` only if separate reusable `.qml`
styles or `.xml` symbol/ramp libraries are useful.

Version definitions and meaningful projects; omit caches and editor backups. Put
the layer inventory, definition paths, CRS, units, layer/band names, and retrieval
instructions in the main README or notebook as appropriate.
Read [geospatial guidance](../guides/geospatial.md).
PyQGIS remains optional; these folders do not require QGIS for ordinary analysis.
