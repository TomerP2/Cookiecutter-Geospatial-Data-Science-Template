# Run logging and reports

Read before adding persistent logs, recording runs, or writing reports. Related:
[data and provenance](data.md), [modeling](modeling.md), [validation](validation.md),
[source code](source-code.md).

## Choose the smallest useful record

For one-off exploration, notebook output and brief conclusions normally suffice.
For substantial, expensive, or repeated processing, retain a readable log under
`runs/`. No custom run manifests, automatic code snapshots, hashes, cache
invalidation, function-level tracing, or logging service is required.

Use Python's standard-library `logging`. The package's `log_run()` context manager
only configures file/console handlers and their cleanup; use the ordinary logger API
for messages. It does not implement experiment tracking or automatic provenance.

## Runs and authored reports

- `runs/`: execution logs and optional concise run notes.
- `runs/figures/`: generated plots/maps for inspection and communication.
- `runs/tables/`: summary tables; canonical datasets still go in `data/processed/`.
- `runs/notebooks/`: generated executed copies/exports, never an editable second
  source. All authored notebooks belong in `notebooks/`.
- `reports/`: authored LaTeX sources, bibliographies, report assets, and writing notes;
  no logs, run notes, or routine generated outputs. Use `reports/<topic>/build/` for
  ignored LaTeX build products.

For substantial repeated work, keep related artifacts together in `runs/<run-id>/`.
The flat starter layout is enough for simple work; do not create a run framework.

Use a UTC timestamp and a meaningful stage name, such as
`20261009T140000Z-source-inspection.log`. Python's datetime formatting avoids Windows
filename colons. Separate concurrently running processes must use different files.

```python
from datetime import datetime, timezone

from project_package.config import RUNS_DIR
from project_package.run_logging import log_run

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
with log_run(RUNS_DIR / f"{stamp}-inspection.log") as logger:
    logger.info("Input=%s; version=%s", "synthetic example", "v1")
    logger.info("Notebook=%s", "notebooks/0.01-ab-getting-started.ipynb")
    logger.info("Check=%s; result=%s", "example row count", 3)
```

## What to record

At meaningful stages, log source identifiers/releases (or acquisition date), important
non-secret parameters, relevant notebook/script, useful counts/check outcomes, and
output locations. State the actual reproduction command, reference pyproject.toml and
pixi.lock, and record the Pixi version in README. Link a short run note or notebook
conclusion when interpreting results needs prose; do not duplicate a complete inventory
in several formats. Identify failed or incomplete outputs explicitly.

Use INFO for stage progress/results, WARNING for actionable concerns, and exceptions
for failures. `log_run` logs start, successful block completion, or an escaping error/
interruption, then re-raises it. A completed block is not proof of analytical validity.
Do not catch an error and continue as though its stage succeeded.

The helper appends to an existing file, emits UTC timestamps, and closes/removes its
handlers even after an error. Use a new filename for distinct runs; reusing a filename
preserves earlier content with additional run boundaries. Use one context at a time
per process. It refuses an already configured package logger rather than replacing
someone else's handlers. Package child loggers using `logging.getLogger(__name__)`
are captured if they propagate normally; root/Jupyter logging is left untouched.
Print statements, warnings, and unrelated libraries are not automatically captured.
For parallel workers, adopt logging's queue facilities only when needed.

## Privacy, version control, and limitations

Never log credentials, tokens, signed URLs, sensitive rows, or entire environment
variables. Exception tracebacks include exception messages: review them for sensitive
content before sharing. Logs and generated products are ignored by Git by default;
retain useful outputs in appropriate project storage and deliberately version only
small reviewed notes/artifacts. README files and directory placeholders remain tracked.

Record when results depend on uncommitted code. A commit ID, log, or tracking run does
not preserve those edits. Do not create automatic commits or snapshots to compensate.

For repeated ML experiments use optional local MLflow with supported autologging,
as described in [modeling.md](modeling.md), rather than building a custom metric store.
Add it only when useful; avoid duplicating its records in custom JSON. If used, keep
its local store under `runs/` with an explicitly documented tracking URI and
version-appropriate backend. Logs alone are not complete analytical provenance.

Reference: [Python logging](https://docs.python.org/3.12/library/logging.html).

Examples use `project_package` and initials `ab` as placeholders. Use the actual
package, initials, and notebook paths recorded in the project AGENTS.md/README.
