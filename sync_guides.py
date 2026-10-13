"""Copy a local guide checkout into a project's offline snapshot."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(content):
    return hashlib.sha256(content).hexdigest()


def sync(project, source=None):
    project = Path(project).resolve()
    destination = project / 'guides'
    record = destination / 'source.json'
    previous = json.loads(record.read_text(encoding='utf-8')) if record.exists() else {}
    source = Path(source or previous.get('source', '')).expanduser().resolve()
    source_guides = source / 'guides'
    if source_guides == destination:
        raise ValueError('Source must be a separate guide repository.')
    if not (source_guides / 'core.md').is_file():
        raise ValueError(f'Guide repository unavailable: {source}. Keeping the existing snapshot.')
    contents = {p.name: p.read_bytes() for p in source_guides.glob('*.md')}
    old = previous.get('files', {})
    # Check every affected file before writing anything. Local overrides live elsewhere.
    for name in old.keys() | contents.keys():
        if Path(name).name != name or not name.endswith('.md'):
            raise ValueError(f'Invalid guide filename: {name}')
        target = destination / name
        if target.exists():
            actual = digest(target.read_bytes())
            if actual != old.get(name) and target.read_bytes() != contents.get(name):
                raise ValueError(f'Local edits in {target}; move them to AGENTS.md before syncing.')
        elif name in old:
            raise ValueError(f'Locally deleted guide: {target}; restore it before syncing.')
    def git(*args):
        try:
            result = subprocess.run(['git', '-C', str(source), *args],
                                    capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    revision = git('rev-parse', '--verify', 'HEAD')
    status = git('status', '--porcelain')
    metadata = {'source': str(source), 'revision': revision,
                'dirty': bool(status) if status is not None else None,
                'files': {name: digest(data) for name, data in sorted(contents.items())}}
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in contents.items():
        (destination / name).write_bytes(data)
    for name in old.keys() - contents.keys():
        (destination / name).unlink()
    record.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print(f'Synced {len(contents)} guides from {source}; revision={revision or "uncommitted"}, dirty={metadata["dirty"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source', type=Path, help='Local checkout; defaults to guides/source.json')
    args = parser.parse_args()
    try:
        sync(args.project, args.source)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
