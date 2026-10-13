# Predictive modeling and evaluation

Applies only to predictive ML. Related: [notebooks](notebooks.md),
[source code](source-code.md), [data](data.md), [validation](validation.md).

Define the intended prediction situation (nearby locations, new regions, future
dates, or new sites/subjects), information available at prediction time, and a
question-appropriate metric before selecting models.

Start with a meaningful domain baseline or sklearn DummyClassifier/DummyRegressor
and one reasonable model. Compare them on the same splits and metric before tuning.
Choose random, grouped, temporal, or spatial splits to represent the prediction
situation; keep related observations together when separation would leak information.
Spatial data alone do not mandate spatial blocking. Document the split rationale.

Fit learned imputation, scaling and feature selection within training folds, normally
using sklearn Pipeline and ColumnTransformer where useful. Tune model choices and
decision thresholds on training/validation data. Reserve final test data for the
selected approach; if it informs further selection, do not call it an untouched test.

Use seeds and deterministic ordering where available; disclose nondeterministic GPU
or parallel behavior. Increase complexity only for meaningful improvement. New
analytical behavior still follows the confirmation boundary in [shared rules](core.md).

## Optional experiment tracking

Notebook/README notes suffice for one-off work. For repeated experiments, consider
local MLflow Tracking and its supported framework autologging; no server or registry
is needed by default. Add it through Pixi only when useful. Log source identifiers,
split strategy and the selected validation/test metric if not captured automatically.
Limit automatic model/dataset capture to what is actually needed; inspect supported
integration options before enabling autologging. Avoid duplicate custom JSON records.
See [run-reporting.md](run-reporting.md) for ordinary execution logs and where to
place a local tracking store if MLflow is adopted.

Tracking does not preserve uncommitted source or complete geospatial lineage. If
W3C PROV is explicitly required, use an established PROV library and explicit modeling
rather than writing a serializer. Neither tool belongs in every new project.
