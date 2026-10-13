# Validation and delivery

Applies when choosing checks or finishing work. Read [shared rules](core.md) for
universal rules, then only relevant topic guides.

## Match verification to the change

For analytical MVPs, execute the notebook and inspect the result needed to answer the
question. Verification is not a quota of assertions, tables, or representative files.
For infrastructure, use a relevant command/import/runtime check. Add small automated
tests when justified by [testing.md](testing.md), which owns automated-test conventions.
Do not retest external libraries or mirror trivial glue code.

Trust known project-created data unless a contract changes, a bug is suspected, or
a risky new operation introduces uncertainty. Do not reopen representative TIFFs to
recount pixels, reassert known CRS/shape/NoData, or build all-true audit tables by default.
Use an existing summary when it answers the question. Keep any necessary check close
to the operation and explain the specific failure it catches.

Validate at the relevant boundary when a plausible silent error could materially
change the result. Examples, not universal requirements: pandas join cardinality,
unmatched spatial joins, units conversions, missing CRS, raster grid alignment and
NoData. Prefer a built-in check or short summary over a generic validation framework.

For notebooks, verify clean-kernel execution and representative inputs. For package
promotion, rerun checks through installed imports after user confirmation. Where
feasible reproduce in a clean environment; report when only the existing environment
was tested. Avoid repeated full scans merely to produce verification reports.

## Before handoff

- Always: inspect relevant changes, preserve user work, check for secrets/large
  artifacts, leave changes uncommitted, and summarize checks and unresolved failures.
- If commands/setup changed: update the README with implemented reproduction steps.
- If analytical results changed: state inputs, important settings, outputs, and
  conclusions supported by checks; distinguish uncommitted-code reproducibility limits.
- If persistent run records are useful: follow [run-reporting.md](run-reporting.md)
  for logs and concise report notes; do not add a mandatory run manifest.
- If spatial work: resolve uncertain CRS/grid/NoData only where consequential; deliver useful
  QGIS-readable outputs. State visual review that remains pending.
- If predictive ML: verify baseline comparison, appropriate splits, leakage controls,
  and honest treatment of final test data.

These are conditional completion criteria, not requirements to create maps, models,
styles, tests, or reports for unrelated work. Do not claim that writing a notebook
equals executing it, or that execution alone establishes analytical validity.
