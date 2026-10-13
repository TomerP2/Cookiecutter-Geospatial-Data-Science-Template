"""Reject invalid names before Cookiecutter renders project files."""

import keyword
import re
import sys

# JSON-escaped string literals avoid interpolating raw user text into Python code.
slug = {{ cookiecutter.project_slug | tojson }}
package = {{ cookiecutter.package_name | tojson }}
initials = {{ cookiecutter.author_initials | tojson }}
reserved = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}

for label, value in (("project_slug", slug), ("package_name", package)):
    if not re.fullmatch(r"[a-z][a-z0-9_]*", value) or value in reserved:
        sys.exit(f"{label} must start with a lowercase letter and contain only "
                 "lowercase letters, digits, or underscores; avoid Windows reserved names.")

if keyword.iskeyword(package) or package in sys.stdlib_module_names:
    sys.exit("package_name must not be a Python keyword or standard-library module.")

if package in {"numpy", "pandas", "jupyter", "ipykernel", "nbconvert", "pytest",
               "geopandas", "rasterio", "leafmap", "shapely", "pyproj", "sklearn"}:
    sys.exit("package_name must not shadow a commonly used dependency.")

if not re.fullmatch(r"[a-z][a-z0-9]{0,11}", initials):
    sys.exit("author_initials must contain 1-12 lowercase letters/digits, starting with a letter.")
