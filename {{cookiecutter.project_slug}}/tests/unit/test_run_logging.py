"""Example pytest regressions for failure visibility and safe notebook reruns."""

import logging
from pathlib import Path

import pytest

from {{ cookiecutter.package_name }}.run_logging import log_run


def test_failed_run_is_logged_and_reraised(tmp_path: Path) -> None:
    """A failed stage must remain a failure while retaining useful diagnostics.

    Args:
        tmp_path: Isolated temporary directory supplied by pytest.

    Returns:
        None.

    Examples:
        Run with `pixi run test tests/unit/test_run_logging.py`.
    """
    log_path = tmp_path / "runs" / "failure.log"

    # Exercise the real context manager without touching project data.
    with pytest.raises(ValueError, match="example failure"):
        with log_run(log_path) as logger:
            logger.info("Input=%s", "synthetic fixture")
            raise ValueError("example failure")

    # Verify the externally observable contract, not logging's internals.
    content = log_path.read_text(encoding="utf-8")
    assert "Input=synthetic fixture" in content
    assert "Run failed or interrupted" in content
    assert "ValueError: example failure" in content
    assert "Run completed" not in content


def test_repeated_runs_preserve_logs_and_restore_logger(tmp_path: Path) -> None:
    """Notebook reruns should append once per message without leaving handlers.

    Args:
        tmp_path: Isolated temporary directory supplied by pytest.

    Returns:
        None.

    Examples:
        Run with `pixi run test tests/unit/test_run_logging.py`.
    """
    log_path = tmp_path / "repeat.log"
    package_logger = logging.getLogger("{{ cookiecutter.package_name }}")
    original_settings = (package_logger.level, package_logger.propagate)
    root_handlers = tuple(logging.getLogger().handlers)

    # Reusing a path intentionally appends; sequential contexts must be independent.
    for _ in range(2):
        with log_run(log_path) as logger:
            logger.info("one message per run")

    content = log_path.read_text(encoding="utf-8")
    assert content.count("one message per run") == 2
    assert content.count("Run completed") == 2
    assert not package_logger.handlers
    assert (package_logger.level, package_logger.propagate) == original_settings
    assert tuple(logging.getLogger().handlers) == root_handlers
