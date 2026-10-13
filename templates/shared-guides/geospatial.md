# GIS, remote sensing, and QGIS

Applies only to spatial work. Related: [data](data.md), [notebooks](notebooks.md),
[validation](validation.md), and [Pixi](pixi.md). Spatial requirements do not apply
to ordinary non-spatial tasks.

## CRS and grid correctness

For unfamiliar sources, establish the CRS, units, raster grid and NoData needed by
the operation. Reuse documented contracts for project-created data; do not repeat
metadata inspections or assertions without a concrete reason.
Do not infer missing CRS solely from coordinate ranges. CRS assignment labels
coordinates; reprojection transforms them. Do not measure metres in degrees or use
Web Mercator as a universal analytical CRS.

Choose and document a principal CRS suitable for extent, operations, and accuracy;
use an appropriate projected CRS locally and an equal-area CRS when area accuracy
drives the work. Preserve raw sources and use the principal CRS for analytical
inputs/outputs. Justify limited exceptions: WGS84 display copies, geodesic operations,
or global work where one planar CRS is inadequate.

For combined rasters, align CRS, resolution, transform and extent to a reference grid
where required. Use library reprojection/alignment functions. Use nearest-neighbour
for categorical values and appropriate interpolation/aggregation for continuous data;
document conservation needs and avoid repeated resampling. Preserve masks and NoData.
Check axis order and, for elevation, vertical datum/units. Handle antimeridian/polar
coverage and required datum grids when relevant to accuracy.

## Choose useful visualizations

Make a map when it answers a spatial question or reveals a meaningful change. Skip
maps for bookkeeping, nearly unchanged data, or a result already clear in an existing
view or short table. Do not make an interactive map at every processing step.

Prefer a static matplotlib map (including GeoPandas plotting) for fixed extents,
side-by-side comparisons, small datasets, and report/publication figures. Choose an
interactive map when zooming, layer toggles, attribute inspection, or exploration at
multiple scales helps the reader. State the reason briefly in the visualization section.

When interactivity is useful, leafmap is an option; select a suitable backend and
check its documented capabilities. Add a basemap, named layers, AOI, legend/colorbar,
or hover/pixel inspection only as useful to the question. Basemaps are not
contemporaneous ground truth. Label previews/downsampling and keep displays readable.
Use shared extents and color scales for comparisons where appropriate.

If the agent cannot inspect a map, state that visual review remains pending.
Widget/local tile-server dependencies can prevent standalone HTML reproduction;
provide persistent data or a static figure when useful. Follow the numbered
processing/visualization sections in [notebooks.md](notebooks.md).

## QGIS outputs and layer definitions

Write useful vector intermediates as GeoPackage and raster intermediates as GeoTIFF.
Embed CRS, transform and NoData; document units and band/layer meanings. Use compression,
tiling and overviews as appropriate. Validate actual COG structure when a COG is needed.
Use WGS84 GeoJSON for small web interchange copies, not as the analytical default.
Avoid Shapefile unless required; retain sidecars. Export selected array slices for QGIS.

Provide a concise layer inventory (path, layer/band, meaning, CRS, units, symbology)
in notebook/README notes, including the corresponding `.qlr` path.

For vector and raster outputs intended for QGIS, create `.qlr` layer definitions
directly in `qgis/`, with matching dataset stems. Keep actual datasets in the
appropriate `data/` subdirectory. Include suitable symbology and useful labels:
meaningful vector classes/ranges and colors, and appropriate raster bands, color
ramps, display ranges and NoData transparency. When several layers form a useful
view, also export a grouped `.qlr` with the intended layer order.

Export relative data paths from the saved `.qlr` location, not the repository root
(for example, `../data/processed/elevation.tif`). A `.qlr` contains data references
and styling, not the datasets: share it together with the data and preserve the
folder structure. Avoid external symbol dependencies. Dragging the `.qlr` into QGIS
loads its styled layers; later edits to the definition require reloading it.

Prefer QGIS/PyQGIS export APIs over custom complex XML generators. PyQGIS is optional
and may use the installed QGIS runtime rather than the project's Pixi Python; do not
make ordinary analysis depend on it. If unavailable, provide styling instructions
and report the missing or unverified `.qlr` deliverable explicitly. Verify exported
definitions in a fresh QGIS project: data sources resolve and intended styling is
restored. State when visual review remains pending.

Version `.qlr` files in `qgis/`. Keep optional inspection projects in `qgis/projects/`
with paths relative to their saved location (`../../data/`). Create `qgis/styles/`
only when separate reusable `.qml` styles or Style Manager `.xml` symbol/ramp
libraries are needed; these are supplementary to the `.qlr` deliverable.
