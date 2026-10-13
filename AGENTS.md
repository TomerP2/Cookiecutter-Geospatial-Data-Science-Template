# Working on this template

This repository generates projects with standard Cookiecutter. The project instructions
live in `{{cookiecutter.project_slug}}/AGENTS.md` and its linked `guides/` files;
they govern generated analytical projects, not template maintenance.

- Preserve user work and leave all changes uncommitted. Do not publish without a request.
- Keep the template small and compatible with Windows, Linux, and macOS.
- Change shared rules in `templates/shared-guides/core.md` and topic rules in
  their owning guide there; these are included in generated local backups.
  Keep project adapters and overrides in the generated AGENTS.md.
- Template infrastructure and the explicitly requested starter package can be edited
  directly. Do not require an analytical notebook approval for template maintenance.
- Run `python -m unittest discover -s tests -v` in an environment with Cookiecutter.
- For environment or package changes, also generate a project, install it with Pixi,
  and execute its getting-started notebook. Report checks that could not run.
- Never regenerate over an existing project. Use a fresh scratch directory.
- Keep shared guidance project-neutral and guide links within the guide set.
- Keep one authoritative guide set. Generated projects read the hosted guides first
  and fall back to their local backup; no guide sync scripts are needed.

See [README.md](README.md) for template use and design decisions.
