# Maintaining this guide repository

This repository owns shared guidance, not an analytical project. Edit topic rules
in their owning file under `guides/`; universal rules belong in `guides/core.md`.
Keep guidance project-neutral and links within the guide set. Keep project-specific
package names and overrides in consuming projects. Preserve user work, leave changes
uncommitted, and do not publish or configure a remote without a request.

Use only the Python standard library for the updater. Preserve consumer edits and
offline snapshots. Run `python -m unittest discover -s tests -v` after changes.
