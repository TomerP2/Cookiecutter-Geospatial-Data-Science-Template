"""Project paths for the editable checkout; no filesystem changes on import.

This research package is intended to be installed editable from its project folder.
Relocating a built wheel alone does not relocate the project's datasets.
"""

from pathlib import Path

# Resolve relative to this source file, not the notebook's working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
RUNS_DIR = PROJECT_ROOT / "runs"
FIGURES_DIR = RUNS_DIR / "figures"
TABLES_DIR = RUNS_DIR / "tables"
REFERENCES_DIR = PROJECT_ROOT / "references"
QGIS_DIR = PROJECT_ROOT / "qgis"
QGIS_PROJECTS_DIR = QGIS_DIR / "projects"
QGIS_STYLES_DIR = QGIS_DIR / "styles"


def project_path(*parts: str | Path) -> Path:
    """Join relative path components to this checkout's root.

    Uses normal pathlib semantics; this is not a sandbox or path validator.

    Args:
        *parts: Path components to join. An absolute component replaces the root.

    Returns:
        A path anchored to the project root unless an absolute path was supplied.

    Examples:
        >>> project_path("data", "raw") == RAW_DATA_DIR
        True
    """
    return PROJECT_ROOT.joinpath(*parts)


def ensure_output_dir(path: str | Path) -> Path:
    """Create an output directory and return it; relative paths use PROJECT_ROOT.

    Pass a directory, not a filename. Existing directory contents are preserved.
    """
    output_dir = Path(path)
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
