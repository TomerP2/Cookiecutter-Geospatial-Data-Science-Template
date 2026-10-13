# Tests

Use `unit/` for small behavior/regression tests, `integration/` for connected stages
when needed, and `fixtures/` for tiny non-sensitive test inputs. The initial unit
tests demonstrate safe run logging with pytest's temporary directories.

Run `pixi run test`. Read [the testing guide](../guides/testing.md) before adding tests.
