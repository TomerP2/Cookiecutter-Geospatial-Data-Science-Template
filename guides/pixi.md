# Pixi environment and commands

Applies to dependencies, kernels, environments, and execution tasks. Related:
[setup](project-setup.md), [notebooks](notebooks.md), [source code](source-code.md).

- Keep one environment in the existing `pyproject.toml` under `[tool.pixi]`. Use
  conda-forge for compiled scientific/geospatial dependencies; use declared PyPI
  dependencies when needed, never the same library through both ecosystems.
- First setup: `pixi install` resolves the manifest and writes `pixi.lock`. Once the
  lock exists, use `pixi install --locked` for reproduction so inconsistencies fail.
  Make dependency updates deliberately; preserve the resulting manifest and lockfile
  for the user to commit. Ignore `.pixi/` and record `pixi --version` in the README.
- Prefer a suitable maintained library to lengthy custom notebook or package code.
  Add dependencies when they simplify the actual work; do not minimize dependency count
  at the expense of clarity. Check the library documentation and supported environment.
  Record explicit tested version constraints in `[tool.pixi.dependencies]` or
  `[tool.pixi.pypi-dependencies]`, and retain resolved versions in `pixi.lock`. This
  project uses `pyproject.toml` as its Pixi manifest, so do not add a competing `pixi.toml`.
  Avoid unconstrained `*` entries for added libraries. PyQGIS remains optional;
  see [geospatial.md](geospatial.md).
- Keep the local package declared editable in `[tool.pixi.pypi-dependencies]` and
  the existing Hatchling `src/` discovery configuration. Installation must work before
  notebook imports; do not compensate with manually modified Python paths.
- Run through `pixi run`. For locked reproduction use `pixi run --locked <task>`.
  Launch `pixi run notebook` and inspect `sys.executable` inside the notebook.
  A global Jupyter kernel may point to a different environment.
- Read the target platform from the project manifest. Add platforms only
  when needed, resolve the lock, and distinguish solving from actual runtime testing.

## Tasks

The scaffold implements `notebook`, `check-notebook`, and `test`. The notebook check
executes the starter into `runs/notebooks/`; it does not validate future analyses
automatically. The test task runs pytest; read [testing.md](testing.md).
Add stage tasks only when their implementation exists, and update the README with
the same commands. Prefer portable Python commands over shell-specific pipelines.
Never add placeholder lint/test/pipeline commands or install packages in notebook cells.

See the official [Pixi manifest integration](https://pixi.prefix.dev/latest/python/pyproject_toml/)
and [locked install behavior](https://pixi.prefix.dev/latest/reference/cli/pixi/install/).
