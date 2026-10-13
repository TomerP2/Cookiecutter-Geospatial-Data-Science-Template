# Data science guides

Shared, project-neutral working rules for analytical projects. This is a standalone
local Git repository prepared for future GitHub hosting. No remote, commits, or
publication have been created. The enclosing template currently keeps this checkout
here for convenience; it can be moved independently.

Read [shared rules](guides/core.md), then the topic guides relevant to the work.
Paths mentioned in guides refer to the consuming project. `project_package` and
`ab` are example placeholders; the project's own AGENTS.md supplies actual values.
User instructions and project overrides take precedence over these guides.

## Maintenance and consumption

Edit the authoritative Markdown files in `guides/`. Consumers keep offline snapshots
and explicitly update from a local checkout, once at task start. Sync never fetches
from the network or overwrites a project's AGENTS.md. It refuses changes to locally
edited/deleted managed guides. Put project-specific overrides in that AGENTS.md.

From this repository, refresh a project or the template snapshot:

```text
python sync_guides.py --source . --project /path/to/project
python sync_guides.py --source . --project "/path/to/data_science_template/{{cookiecutter.project_slug}}"
```

The template distributes `sync_guides.py` as `scripts/sync_guides.py`; copy it there
when changing the updater. `guides/source.json` records the source checkout path,
Git revision (null before the first commit), dirty state, and exact content hashes.
Hashes identify uncommitted guide contents; a revision alone does not capture edits.
Commit the snapshot and its metadata together only when explicitly authorized.

After future GitHub hosting, clone the chosen revision locally and use
`python scripts/sync_guides.py --source /path/to/clone` in each project. This saves
the new source location. Updating that checkout remains an explicit Git operation;
sync does not follow a remote branch, make commits, or require submodules.
Without the checkout, existing snapshots remain usable but freshness is unknown.

Run repository tests with `python -m unittest discover -s tests -v`.
