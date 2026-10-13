"""Explicit run logging using the Python standard library; no setup on import."""

from collections.abc import Iterator
from contextlib import contextmanager
import logging
from pathlib import Path
import time

from {{ cookiecutter.package_name }}.config import project_path


@contextmanager
def log_run(log_path: str | Path) -> Iterator[logging.Logger]:
    """Log a sequential run to an append-only UTF-8 file and the console.

    Create parent directories and temporarily configure this package's logger at
    INFO level with UTC timestamps. Capture package child loggers that propagate
    normally, but not print output, warnings, or unrelated libraries. Restore the
    logger settings and close the handlers on exit, including when the body fails.
    Start/end messages describe execution, not analytical validity.

    Args:
        log_path: Log filename. Relative paths are resolved from the project root;
            absolute paths are used as supplied. Existing content is retained.

    Returns:
        A context manager yielding the package logger for ordinary logging calls.

    Raises:
        RuntimeError: The package logger already has handlers, including when a
            log_run context is active. Use one context at a time per process.
        OSError: The log directory or file cannot be created/opened.
        BaseException: Errors or interruptions from the body are logged and re-raised.

    Examples:
        >>> from {{ cookiecutter.package_name }}.config import RUNS_DIR
        >>> with log_run(RUNS_DIR / "example.log") as logger:
        ...     logger.info("Input=%s; rows=%d", "synthetic example", 3)
    """
    logger = logging.getLogger("{{ cookiecutter.package_name }}")
    if logger.handlers:
        raise RuntimeError("Use one log_run context at a time on an unconfigured package logger.")

    # Keep file paths independent of the notebook's working directory.
    destination = project_path(log_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(destination, mode="a", encoding="utf-8")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)sZ %(levelname)s %(name)s: %(message)s",
                                  datefmt="%Y-%m-%dT%H:%M:%S")
    formatter.converter = time.gmtime

    # Configure only the package logger; leave root/Jupyter logging untouched.
    previous_level, previous_propagate = logger.level, logger.propagate
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in (file_handler, console_handler):
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    try:
        logger.info("Run started")
        yield logger
    except BaseException:
        logger.exception("Run failed or interrupted")
        raise
    else:
        logger.info("Run completed")
    finally:
        for handler in (file_handler, console_handler):
            logger.removeHandler(handler)
            handler.close()
        logger.setLevel(previous_level)
        logger.propagate = previous_propagate
