# Data science guides and Cookiecutter template

Shared analytical working guides and a small Pixi + Jupyter + `src/` project
template, inspired by
[Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science)
and Tomer's GIS / remote sensing workflow preferences. Template version: **0.1.0**.

This is an independent template for the standard `cookiecutter` command. CCDS v2
uses its own `ccds` generator; do not use `ccds` to generate this template.

## Generate a project

Install [Cookiecutter](https://cookiecutter.readthedocs.io/) and
[Pixi](https://pixi.prefix.dev/). From the directory that should contain the new project:

```powershell
cookiecutter "C:/Users/tomer/OneDrive/Home/Projects/data_science_template"
```

The path above is this template's current location; replace it when moving the template.
With Pixi installed, an alternative that supplies Cookiecutter is:

```powershell
pixi exec --spec cookiecutter cookiecutter "C:/Users/tomer/OneDrive/Home/Projects/data_science_template"
```

Then follow the generated README: run `pixi install`, followed by `pixi run notebook`.
Generation only writes files. It does not install environments, download data, initialize
Git, or create commits. Python hooks validate safe folder/package names.

Prompts cover the project title, folder name, importable package name, description,
author, notebook initials, target platform, and the optional hosted guide URL. Python 3.12 is the starting environment;
adjust deliberately when dependencies require it. Add additional platforms only when
needed and verify them. Windows is the first/default platform.

## What is included

- An editable package with `config.py`: conventional path constants, `project_path()`
  for paths independent of notebook working directory, and `ensure_output_dir()` for
  creating an output directory explicitly. `run_logging.py` supplies scoped console
  and file logging using Python's standard library, without a new dependency.
- A small executable getting-started notebook demonstrating the installed package,
  kernel, and a visible pandas summary without downloads.
- A unified `pyproject.toml`, Pixi notebook/test tasks, and conservative Git ignores.
- A short generated `AGENTS.md` routing to shared rules and ten topic guides: setup, Pixi, notebooks,
  source code, data, geospatial, modeling, validation, testing, and run reporting.
- Data directories; tests/unit, integration, and fixtures; authored LaTeX reports; runs/figures, tables,
  and notebooks; references/data_dictionaries and sources; qgis/ for styled raster/vector
  layer definitions (.qlr), with qgis/projects for optional inspection projects.
- Pytest examples checking error propagation and safe repeated logging contexts.

The base environment includes JupyterLab, ipykernel, nbconvert, pandas, NumPy, and pytest.
Geospatial packages, ML frameworks, PyQGIS, MLflow, and DVC are added only as needed.

## Workflow choices

New or materially changed analytical logic is first demonstrated in an executed
notebook. **User confirmation is required before promoting that logic into `src/`.**
Routine infrastructure changes, documentation, and behavior-preserving fixes can
be made directly with suitable verification. The starter package is infrastructure
explicitly requested as part of this template.

The original preference document is consolidated into linked guides rather than
copied verbatim. Universal rules have one home; GIS and ML requirements only apply
to relevant work. PyQGIS remains an optional QGIS integration. The original Obsidian
file has not been modified.

## Maintenance and verification

Install Cookiecutter in your development Python environment, then run:

```text
python -m unittest discover -s tests -v
```

The tests generate temporary projects, check rendered metadata/notebooks and guide
links, and reject unsafe names. For a full runtime check, generate a fresh project:

```text
cookiecutter . --no-input --output-dir .checks project_slug=smoke_project package_name=smoke_package
cd .checks/smoke_project
pixi install
pixi run --locked test
pixi run --locked check-notebook
```

Use a fresh output location/name on repeat runs. Inspect the executed notebook in
`runs/notebooks/`; do not claim that an interactive GIS map was checked by this smoke test.

The current TODO changes are verified using a fresh scratch project; see the completion
notes in [TODO.md](TODO.md). Existing scratch projects are retained unchanged and may
still use the previous `reports/runs/` layout. Linux/macOS generation is covered by
tests; runtime checks are performed on Windows only.

Update the version in `cookiecutter.json` and this README when releasing changes.
Generated projects record the version in their README. They are independent copies:
apply selected template changes manually and review diffs. Cookiecutter replay is
for repeating generation inputs, not merging updates into existing projects.

## Design references

- [CCDS structure and rationale](https://cookiecutter-data-science.drivendata.org/)
- [Cookiecutter hooks](https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html)
- [Pixi pyproject integration](https://pixi.prefix.dev/latest/python/pyproject_toml/)

CCDS informed the layout and conventional path names. The implementation here is
written for this template; upstream placeholder processing code is not copied.

## Shared guides: GitHub first, local backup

This repository contains one authoritative guide set under
`templates/shared-guides/`, alongside the Cookiecutter template. Start with
[shared rules](templates/shared-guides/core.md), then read relevant topic guides.
Paths in shared guides refer to the consuming project. Examples use
`project_package` and `ab`; project AGENTS.md supplies actual values.

```text
templates/shared-guides/         # Authoritative Markdown guides
cookiecutter.json                # Includes the hosted guide directory URL
hooks/                          # Folder/package name validation
{{cookiecutter.project_slug}}/
  guides/                       # One-line includes, rendered into local backups
  AGENTS.md                     # GitHub-first instructions and project overrides
tests/
```

Cookiecutter's built-in shared-template includes put the guides into each new
project as a local backup. The files under the project template's `guides/` contain
only include statements, so there is one authored version of each guide in this
repository. Edit the files in `templates/shared-guides/`; no snapshot refresh or
sync command is required. When adding a guide, add its one-line include and route
it from the generated AGENTS.md.

After publishing this repository, set `guides_url` in `cookiecutter.json` to the
raw GitHub URL of the shared guide directory, using the actual owner, repository,
and branch. For example (replace the uppercase placeholders):

```text
https://raw.githubusercontent.com/OWNER/REPOSITORY/BRANCH/templates/shared-guides
```

The generation prompt can override that URL. Until hosting is configured its
default is empty, so generated projects use their local backup. Nothing has been
published and no GitHub URL has been assumed.

At task start, agents read the hosted `core.md` and relevant topic guides first.
If the URL is unconfigured or required hosted guidance cannot be read, they use the
local backup for that task and briefly report the fallback. Agents read guide
contents directly with their available browsing tools; no Python syncing scripts,
source tracking files, or automatic downloads are needed. Keep the guidance already
read throughout the task and read newly relevant guides if scope changes.

User instructions and project-specific AGENTS.md overrides take precedence.
Reading hosted guidance does not overwrite local project files. The backup reflects
the template used at generation and can be older than the hosted guides. Existing
projects are unaffected; update their hosted URL explicitly when needed rather than
regenerating over them.

Run `python -m unittest discover -s tests -v` to verify generation, local backup
contents and links, and hosted-guide configuration. Hosted reads can only be checked
once the repository is published.
