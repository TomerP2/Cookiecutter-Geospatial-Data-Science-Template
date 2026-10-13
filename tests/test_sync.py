import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync_guides', ROOT / 'sync_guides.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class SyncTests(unittest.TestCase):
    def test_guides_are_portable(self):
        for document in (ROOT / 'guides').glob('*.md'):
            text = document.read_text(encoding='utf-8')
            self.assertNotIn('{{', text)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target:
                    self.assertTrue((document.parent / target).is_file(), target)

    def test_updates_preserve_overrides_and_refuse_local_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'
            (source / 'guides').mkdir(parents=True)
            core = source / 'guides/core.md'
            core.write_text('first', encoding='utf-8')
            project = Path(temp) / 'project'
            project.mkdir()
            (project / 'AGENTS.md').write_text('local rules')
            updater.sync(project, source)
            core.write_text('second', encoding='utf-8')
            updater.sync(project)
            self.assertEqual((project / 'guides/core.md').read_text(), 'second')
            self.assertEqual((project / 'AGENTS.md').read_text(), 'local rules')
            (project / 'guides/core.md').write_text('user edits')
            (source / 'guides/new.md').write_text('new')
            before = (project / 'guides/source.json').read_bytes()
            with self.assertRaisesRegex(ValueError, 'Local edits'):
                updater.sync(project)
            self.assertFalse((project / 'guides/new.md').exists())
            self.assertEqual((project / 'guides/source.json').read_bytes(), before)
            self.assertEqual((project / 'guides/core.md').read_text(), 'user edits')

    def test_removed_upstream_file_and_unavailable_source(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'
            (source / 'guides').mkdir(parents=True)
            (source / 'guides/core.md').write_text('core')
            extra = source / 'guides/extra.md'
            extra.write_text('extra')
            project = Path(temp) / 'project'
            updater.sync(project, source)
            extra.unlink()
            updater.sync(project)
            self.assertFalse((project / 'guides/extra.md').exists())
            before = (project / 'guides/source.json').read_bytes()
            with self.assertRaisesRegex(ValueError, 'unavailable'):
                updater.sync(project, Path(temp) / 'missing')
            self.assertEqual((project / 'guides/source.json').read_bytes(), before)
            self.assertEqual((project / 'guides/core.md').read_text(), 'core')


if __name__ == '__main__':
    unittest.main()
