# Project setup and scope

Applies when starting a project or changing its structure. Universal rules and the
approval boundary are in [shared rules](core.md).

1. Read the README, existing files, environment manifest, data inventory, and Git diff.
   Establish the question, intended outputs, source access, and constraints before analysis.
2. For spatial work, record the AOI, dates, and appropriate principal analytical CRS;
   use [geospatial.md](geospatial.md). For predictive ML, establish the intended
   prediction situation and metric using [modeling.md](modeling.md).
3. Set up the existing environment using [pixi.md](pixi.md). This template is already
   generated: never run Cookiecutter or CCDS over it. Do not create another manifest.
4. Run the starter notebook and verify the kernel and editable import before expanding
   analysis. See [notebooks.md](notebooks.md).
5. Keep the README current with purpose, inputs, decisions, commands, output locations,
   and blockers. Add data retrieval notes as described in [data.md](data.md).

## Layout grows with the work

Use the existing data folders, notebooks, source package, authored reports, generated runs, tests, references,
and QGIS directories. Read [testing.md](testing.md) before adding tests and
[run-reporting.md](run-reporting.md) before logging runs. Keep QGIS layer definitions
in `qgis/`, optional inspection projects in `qgis/projects/`, and reference material
in its designated subfolders; these locations are provided
for convenience, not requirements to manufacture content. Add configs for shared
parameters and models for actual model artifacts. Avoid duplicate metadata directories
and empty processing/model modules.

Keep the package in `src/` and install it editable. Do not add a root-level duplicate,
sys.path hacks, a Makefile, or a CLI just to fill out a template. Use Pixi tasks for
implemented repeatable commands. A stable pipeline may eventually justify a `pipeline`
task, but exploratory projects may remain notebook-based.

Generated projects record their template version. Apply future template improvements
selectively and review diffs rather than regenerating. Initialization of Git is separate
from generation; do not create an initial commit. See [validation.md](validation.md)
for completion evidence.
