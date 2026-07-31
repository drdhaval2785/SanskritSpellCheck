import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DETECTORS = ROOT / 'detectors'
METER = DETECTORS / 'meter'
sys.path.insert(0, str(DETECTORS))
sys.path.insert(0, str(METER))

import meter_ident  # noqa: E402


def _pythonpath(*paths):
    return os.pathsep.join(str(path) for path in paths)


def test_compatibility_module_prefers_installed_package(tmp_path):
    package = tmp_path / 'sanskrit_util'
    package.mkdir()
    (package / '__init__.py').write_text(
        "__all__ = ['MARKER']\nMARKER = 'installed-first'\n", encoding='utf-8')
    env = os.environ.copy()
    env['PYTHONPATH'] = _pythonpath(tmp_path, DETECTORS)
    result = subprocess.run(
        [sys.executable, '-c',
         'import sanskrit_util_compat as value; print(value.MARKER)'],
        env=env, capture_output=True, text=True, encoding='utf-8', check=True)
    assert result.stdout.strip() == 'installed-first'


def test_compatibility_module_supports_legacy_sibling():
    sibling = ROOT.parent / 'sanskrit-util' / 'py' / 'sanskrit_util' / '__init__.py'
    if not sibling.is_file():
        pytest.skip('legacy sibling checkout is not available')
    env = os.environ.copy()
    env['PYTHONPATH'] = str(DETECTORS)
    result = subprocess.run(
        [sys.executable, '-S', '-c',
         'import sanskrit_util_compat as value; print(value.to_slp1("ā"))'],
        env=env, capture_output=True, text=True, encoding='utf-8', check=True)
    assert result.stdout.strip() == 'A'


def test_vidyut_path_precedence(tmp_path, monkeypatch):
    explicit = tmp_path / 'explicit.tsv'
    configured = tmp_path / 'configured.tsv'
    monkeypatch.setenv('VIDYUT_CHANDAS_DATA', str(configured))
    assert meter_ident._vidyut_data_path(str(explicit)) == str(explicit.resolve())
    assert meter_ident._vidyut_data_path() == str(configured.resolve())


def test_missing_vidyut_data_warns_and_degrades(tmp_path, monkeypatch):
    chandas_module = types.ModuleType('vidyut.chandas')
    chandas_module.Chandas = lambda _path: object()
    vidyut_module = types.ModuleType('vidyut')
    monkeypatch.setitem(sys.modules, 'vidyut', vidyut_module)
    monkeypatch.setitem(sys.modules, 'vidyut.chandas', chandas_module)
    monkeypatch.setattr(meter_ident, '_vidyut_chandas', None)
    missing = tmp_path / 'missing.tsv'
    with pytest.warns(RuntimeWarning, match='VIDYUT_CHANDAS_DATA'):
        assert meter_ident._vidyut(str(missing)) is None
