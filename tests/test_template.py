"""Generation regressions for the reusable template, using standard unittest."""

import json
from pathlib import Path
import re
import tempfile
import tomllib
import unittest

from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

TEMPLATE = Path(__file__).resolve().parents[1]


class TemplateTests(unittest.TestCase):
    def test_generated_backups_use_authoritative_guides(self):
        scaffold = TEMPLATE / '{{cookiecutter.project_slug}}'
        source_guides = TEMPLATE / 'templates/shared-guides'
        self.assertEqual({p.name for p in source_guides.glob('*.md')},
                         {p.name for p in (scaffold / 'guides').glob('*.md')})
        with tempfile.TemporaryDirectory() as temp:
            project = self.generate(temp)
            for guide in source_guides.glob('*.md'):
                self.assertEqual(guide.read_text(encoding='utf-8').strip(),
                                 (project / 'guides' / guide.name).read_text(encoding='utf-8').strip())
            self.assertFalse((project / 'scripts/sync_guides.py').exists())
            self.assertFalse((project / 'guides/source.json').exists())
            self.assertIn('not configured yet', (project / 'AGENTS.md').read_text())
            self.assertFalse((project / '.git').exists())

    def test_hosted_guide_url_is_configurable(self):
        url = 'https://raw.githubusercontent.com/example/guides/main/templates/shared-guides'
        with tempfile.TemporaryDirectory() as temp:
            project = self.generate(temp, guides_url=url)
            for name in ('AGENTS.md', 'README.md'):
                self.assertIn(url, (project / name).read_text())
            agent = (project / 'AGENTS.md').read_text()
            self.assertIn('first try to read', agent)
            self.assertIn('use the local `guides/` backup', agent)

    def test_authoritative_guide_links_are_portable(self):
        for document in (TEMPLATE / 'templates/shared-guides').glob('*.md'):
            text = document.read_text(encoding='utf-8')
            self.assertNotIn('{{', text)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target:
                    self.assertTrue((document.parent / target).is_file(), target)

    def generate(self, directory, **context):
        return Path(cookiecutter(
            str(TEMPLATE), no_input=True, output_dir=directory,
            extra_context=context,
            default_config={'replay_dir': str(Path(directory) / '.replay'),
                            'cookiecutters_dir': str(Path(directory) / '.cache')},
        ))

    def test_generated_project_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self.generate(
                temp, project_name='Quoted "title"', project_slug='example_project',
                package_name='example_package', author_name='A "quoted" author',
                description='A description with "quotes" and a backslash \\.',
            )
            manifest = tomllib.loads((project / 'pyproject.toml').read_text())
            self.assertEqual(manifest['project']['name'], 'example_package')
            self.assertEqual(manifest['project']['authors'][0]['name'], 'A "quoted" author')
            pixi = manifest['tool']['pixi']
            self.assertTrue(pixi['pypi-dependencies']['example_package']['editable'])
            self.assertEqual(manifest['tool']['hatch']['build']['targets']['wheel']['packages'],
                             ['src/example_package'])

            # Notebook JSON and code remain valid after rendering.
            notebooks = list((project / 'notebooks').glob('*.ipynb'))
            self.assertEqual(len(notebooks), 1)
            notebook = json.loads(notebooks[0].read_text(encoding='utf-8'))
            for index, cell in enumerate(notebook['cells']):
                if cell['cell_type'] == 'code':
                    self.assertEqual(notebook['cells'][index - 1]['cell_type'], 'markdown')
                    compile(''.join(cell['source']), str(notebooks[0]), 'exec')

            # Local instruction links must resolve from each document's directory.
            for document in project.rglob('*.md'):
                for target in re.findall(r'\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
                    if '://' not in target and not target.startswith('#'):
                        self.assertTrue((document.parent / target.split('#')[0]).exists(),
                                        f'{document}: broken link {target}')

            self.assertEqual(len(list((project / 'guides').glob('*.md'))), 11)
            for folder in ('tests/unit', 'tests/integration', 'tests/fixtures',
                           'reports', 'runs/figures', 'runs/tables', 'runs/notebooks',
                           'runs', 'references/sources',
                           'references/data_dictionaries', 'qgis', 'qgis/projects'):
                self.assertTrue((project / folder).is_dir(), folder)
            self.assertEqual(pixi['tasks']['test'], 'python -m pytest')
            for source_file in list((project / 'src').rglob('*.py')) + list((project / 'tests').rglob('*.py')):
                compile(source_file.read_text(encoding='utf-8'), str(source_file), 'exec')
            self.assertFalse((project / 'pixi.lock').exists())
            self.assertFalse((project / '.git').exists())

            # Starter helpers use the checkout regardless of caller working directory.
            source = project / 'src/example_package/config.py'
            namespace = {'__file__': str(source)}
            exec(compile(source.read_text(), str(source), 'exec'), namespace)
            self.assertEqual(namespace['project_path']('data', 'raw'), project / 'data/raw')
            self.assertEqual(namespace['RUNS_DIR'], project / 'runs')
            self.assertEqual(namespace['FIGURES_DIR'], project / 'runs/figures')
            self.assertEqual(namespace['TABLES_DIR'], project / 'runs/tables')
            self.assertEqual(namespace['REPORTS_DIR'], project / 'reports')
            self.assertFalse((project / 'reports/runs').exists())
            self.assertIn('--output-dir=runs/notebooks', pixi['tasks']['check-notebook'])
            output = namespace['ensure_output_dir']('runs/nested')
            marker = output / 'keep.txt'
            marker.write_text('keep')
            namespace['ensure_output_dir'](output)
            self.assertEqual(marker.read_text(), 'keep')

    def test_supported_platforms(self):
        for platform in ('win-64', 'linux-64', 'osx-arm64', 'osx-64'):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as temp:
                project = self.generate(temp, platform=platform)
                manifest = tomllib.loads((project / 'pyproject.toml').read_text())
                self.assertEqual(manifest['tool']['pixi']['workspace']['platforms'], [platform])

    def test_invalid_names_are_rejected(self):
        cases = [dict(project_slug='../escape'), dict(project_slug='con'),
                 dict(package_name='class'), dict(package_name='json'),
                 dict(package_name='pandas'), dict(package_name='bad-name'),
                 dict(author_initials='../bad')]
        for context in cases:
            with self.subTest(context=context), tempfile.TemporaryDirectory() as temp:
                with self.assertRaises(FailedHookException):
                    self.generate(temp, **context)


if __name__ == '__main__':
    unittest.main()
