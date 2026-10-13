# Inputs, outputs, configuration, and provenance

Applies when acquiring data or writing analytical products. Related:
[setup](project-setup.md), [geospatial](geospatial.md), [validation](validation.md).

## Source and derived data

- Preserve acquisitions unchanged in `data/raw/`; use `data/external/` for external
  reference inputs. Keep releases identifiable without unexplained duplicate copies.
- Record source URL/catalog ID, version/date (or acquisition date), license, retrieval
  steps, and relevant spatial/temporal coverage in a README alongside the source.
  These notes are versioned even though data are ignored. Never include signed URLs
  or credentials in notes, logs, or notebook outputs.
- Write useful checkpoints to `data/interim/`, canonical analysis-ready/final datasets
  to `data/processed/`, and generated figures/tables/run artifacts to `runs/`.
  Reserve `reports/` for authored LaTeX reports and related writing assets. Save useful expensive
  intermediates and explain when to regenerate them; do not export every array.
- Use descriptive names with stage/area/date where helpful, UTC ISO 8601 timestamps
  when recording time, and document source time zones. Avoid final_final naming.
- Use CSV for simple tables; GeoPackage for analytical vectors; GeoTIFF for rasters;
  NetCDF/Zarr for multidimensional arrays. Use specialized formats only when needed.
  Document columns/bands, units, NoData and CRS. See [geospatial.md](geospatial.md).

## Configuration and reproducibility

Keep one-off parameters in a notebook settings cell. Add `configs/` when settings
are shared across notebooks or stages; avoid duplicate sources of truth. Keep secrets
in environment variables or ignored local files. Add a placeholder `.env.example`
only if needed; the package does not automatically load `.env`.

For important results retain input identifiers/releases, key parameters, code/notebook
reference, output locations, and a reproduction command. The Pixi manifest and lock
describe the environment. A commit ID does not capture uncommitted source: disclose
that limitation rather than creating commits, hashes, or source snapshots automatically.

Keep source, notebooks, notes, tiny intentional fixtures, styles, and environment files
under version control. Generated files are ignored by default; deliberately include
small review artifacts if useful. Check ignores before assuming a file will be tracked.

Use ordinary library writes. Add checksums, overwrite protection, atomic writes,
or data versioning only for concrete integrity or loss risks. Do not mutate sources.
Do not add custom cache invalidation, manifests, or tracing infrastructure by default.
Use [run-reporting.md](run-reporting.md) for execution logs and reports. Keep data
dictionaries and source references in the existing `references/` subfolders, linking
acquisition notes rather than duplicating them.

## Optional scaling tools

For expensive reruns or branching dependencies, DVC may be useful. If adopted, let
`dvc.yaml` declare stage commands, code/data dependencies, parameters and outputs;
track it with dvc.lock, keep cache/large outputs ignored, and document retrieval.
Have `pixi run pipeline` invoke `dvc repro` rather than duplicating dependency logic
in Pixi. No remote cache is required. Undeclared dependencies need explicit handling.
For repeated ML experiments, see [modeling.md](modeling.md) for optional MLflow.
