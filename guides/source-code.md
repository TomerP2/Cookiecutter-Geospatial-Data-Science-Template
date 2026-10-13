# Reusable source code

Applies to Python package changes. The authoritative approval boundary is in
[shared rules](core.md); demonstrations follow [notebooks.md](notebooks.md).

## Decide which workflow applies

| Change | Workflow |
| --- | --- |
| New or materially changed transformation, feature, metric, or model behavior | Demonstrate in a notebook, execute/check, obtain user confirmation, then promote if useful |
| Fix that changes analytical results | Same analytical workflow; reproduce the problem and show the corrected result |
| Environment, paths, packaging, docs, formatting, behavior-preserving refactor/fix | Edit directly and run relevant checks; no forced notebook or promotion approval |
| One-off analysis | Keep in a notebook; promotion is optional |

User confirmation must concern the demonstrated behavior and proposed promotion;
do not infer it from silence or an initial general implementation request. While
waiting, keep the working analytical implementation in the notebook. Do not create
a parallel implementation in the package to bypass the boundary.

Promote only when logic is reused, runs repeatedly as a stable stage, or becomes
difficult to inspect in the notebook. After approval, move the demonstrated logic,
replace notebook duplicates with imports, and rerun relevant checks against the package.

## Package conventions

The package is already installed editable from `src/project_package/`.
`config.py` provides conventional directory constants, `project_path(*parts)`, and
`ensure_output_dir(path)`. Paths are anchored to the editable source checkout, not cwd;
these helpers are not intended for a standalone wheel without the project directory.
`run_logging.py` provides explicit scoped logging using the standard library; see
[run-reporting.md](run-reporting.md) before using or changing it. Imports do not create
folders, load secrets, or reconfigure logging.

Add modules such as processing.py, dataset.py, features.py, or plots.py only when
there is real code for them. Use simple functions with explicit inputs/outputs and
the documentation conventions below. Prefer pandas/NumPy/GeoPandas/Rasterio
operations and established abstractions such as sklearn Pipeline to custom frameworks.
Before writing a long algorithm or helper, look for a maintained library that expresses
the operation clearly. Add it when it improves readability and correctness; dependency
count alone is not a reason to reinvent it. Record versions through [Pixi](pixi.md).
Do not surround straightforward library calls with speculative validation wrappers.

Keep analytical parameters visible; use [data.md](data.md) for shared configuration
and provenance. Reuse the existing logging setup instead of building another wrapper
or tracking system. Avoid broad exception handling that hides errors. Select meaningful
verification from [validation.md](validation.md) and use [testing.md](testing.md)
when adding tests, rather than testing trivial glue.

## Functional programming principles

- Prefer small functions with one clear responsibility, explicit inputs, and returned
  outputs. Compose them into readable steps rather than building large functions with
  unrelated responsibilities or many mode flags.
- Keep analytical transformations pure where practical: the same inputs should produce
  the same outputs, without modifying caller-owned data, global state, or files. Avoid
  in-place DataFrame/array changes unless explicitly necessary and documented.
- Pass parameters and dependencies explicitly. Avoid hidden configuration, mutable
  default arguments, and implicit randomness; make seeds or generators explicit when
  randomness is part of the calculation.
- Separate calculations from side effects such as reading/writing files, network access,
  directory creation, and logging. Keep necessary side effects in clearly named boundary
  functions and document them; pure functions are a preference, not a ban on useful I/O.
- Prefer ordinary named functions and vectorized library operations. Do not introduce
  functional frameworks, nested lambdas, excessive tiny helpers, or forced map/reduce
  expressions. Use established stateful library objects such as sklearn estimators
  when they are the natural interface.

## Function signatures and documentation

Give every new or changed function meaningful names, parameter type annotations, a
return type annotation, and a docstring. Keep documentation proportional to the function,
but include a plain-language explanation, `Args`, `Returns`, and a concrete `Examples`
section. For a function without parameters, omit `Args`; document `None` for a function
without a returned value. Add `Raises` for meaningful exceptions callers need to handle.

Explain semantics beyond what the annotations show: units, expected columns/shapes,
missing-value behavior, assumptions, and mutation or other side effects where relevant.
State what the function actually guarantees; type annotations do not validate runtime
inputs. Examples should use small self-contained inputs and show the expected result.
Keep signatures, docstrings, and examples synchronized when behavior changes.

### Example: a pure, documented transformation

This illustrates the style; it is not a function every project needs to add.

```python
import pandas as pd


def celsius_to_kelvin(temperature_c: pd.Series) -> pd.Series:
    """Convert a numeric temperature series from degrees Celsius to kelvin.

    Add 273.15 elementwise without modifying the input. Preserve the index,
    series name, and missing values. Input values are assumed to represent
    temperatures in degrees Celsius; physical plausibility is not validated.

    Args:
        temperature_c: Numeric series of temperatures in degrees Celsius.

    Returns:
        A new series of temperatures in kelvin, with the original index and name.

    Examples:
        >>> readings = pd.Series([0.0, 100.0], name="temperature")
        >>> celsius_to_kelvin(readings).round(2).tolist()
        [273.15, 373.15]
        >>> readings.tolist()
        [0.0, 100.0]
    """
    return temperature_c + 273.15
```

Examples use `project_package` and initials `ab` as placeholders. Use the actual
package, initials, and notebook paths recorded in the project AGENTS.md/README.
