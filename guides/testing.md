# When and how to write tests

Read before writing or changing automated tests. Related:
[validation](validation.md), [source code](source-code.md), [Pixi](pixi.md).

## Choose a consequential behavior

An executed notebook with a concise relevant result remains the default for an
analytical MVP. Add pytest tests for consequential custom logic, a known regression,
or behavior that is hard to verify reliably in a notebook. A folder and installed
pytest do not imply a coverage target or a test for every function.

Good candidates include a join that must not duplicate observations, a known NoData
bug, or an error path that must not report success. Do not retest pandas/Rasterio,
assert every intermediate value, mirror the implementation, or build a generic
validation framework. Use independent expected results tied to the intended behavior.

## Locations and execution

- `tests/unit/`: small isolated tests of project behavior.
- `tests/integration/`: a few tests of connected stages when actually needed.
- `tests/fixtures/`: tiny, non-sensitive representative files; prefer inline values
  or pytest's `tmp_path` when a committed fixture is unnecessary.

Run `pixi run test`; for locked reproduction use `pixi run --locked test`. To focus:

```text
pixi run test tests/unit/test_run_logging.py
pixi run test -k failed_run
```

Tests import the installed package by name. No sys.path changes, project-data writes,
network downloads, credentials, or dependency installation inside tests. Use descriptive
`test_*.py` / `test_*` names, arrange/act/assert structure, and few readable assertions.
Use `pytest.raises` for errors, `pytest.approx` for justified numerical tolerances,
and parametrization for genuinely related cases. Share fixtures only when useful.

The included example tests (`tests/unit/test_run_logging.py`) protect two real
logging risks: swallowing failures and duplicate/leaked handlers on notebook reruns.
They use `tmp_path` so tests leave the project's runs, reports, and data untouched.

If a test needs unavailable inputs or optional GIS software, explain the prerequisite
and distinguish skipped checks from passed checks. Keep expensive/external checks
explicitly opt-in if introduced. For regression fixes, reproduce the failure before
the fix when feasible, then verify the correction. Tests do not replace the notebook
demonstration and user confirmation required for analytical package promotion.

See [pytest temporary directories](https://docs.pytest.org/en/stable/how-to/tmp_path.html).
