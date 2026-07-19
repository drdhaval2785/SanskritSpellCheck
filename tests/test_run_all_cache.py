import sys
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DETECTORS = ROOT / 'detectors'
sys.path.insert(0, str(DETECTORS))

import run_all  # noqa: E402


def test_installed_version_fingerprint_includes_vcs_provenance(monkeypatch):
    class Distribution:
        version = '0.4.0'

        @staticmethod
        def read_text(name):
            assert name == 'direct_url.json'
            return json.dumps({
                'url': 'https://github.com/sanskrit-lexicon/sanskrit-util.git',
                'vcs_info': {'requested_revision': 'v0.7.0', 'commit_id': 'abc123'},
            })

    monkeypatch.setattr(run_all, 'INTERNAL_PACKAGES', ('sanskrit-util',))
    monkeypatch.setattr(run_all.metadata, 'distribution', lambda _name: Distribution())
    value = run_all._installed_versions()['sanskrit-util']
    assert value['version'] == '0.4.0'
    assert value['direct_url']['vcs_info']['requested_revision'] == 'v0.7.0'


@pytest.fixture
def cache_pipeline(tmp_path, monkeypatch):
    script = tmp_path / 'fake_detector.py'
    script.write_text(
        "import pathlib, sys\npathlib.Path(sys.argv[2]).write_text('MW:bad:good:n\\n', encoding='utf-8')\n",
        encoding='utf-8')
    source = tmp_path / 'sanhw1.txt'
    source.write_text('bad:MW\n', encoding='utf-8')
    monkeypatch.setattr(run_all, 'HERE', str(tmp_path))
    monkeypatch.setattr(run_all, 'ROOT', str(tmp_path))
    monkeypatch.setattr(run_all, 'CACHE_PATH', str(tmp_path / '.run_all_cache.json'))
    monkeypatch.setattr(run_all, 'INTERNAL_PACKAGES', ())
    monkeypatch.setattr(
        run_all, 'DETECTORS', [('fake', script.name, 'fake_output.txt', 'corrector')])
    monkeypatch.setattr(run_all.ua, 'union_path', lambda: str(tmp_path / 'missing-union.tsv'))
    return source, script, tmp_path / 'fake_output.txt', tmp_path / '.run_all_cache.json'


def test_forced_rerun_builds_verified_manifest(cache_pipeline):
    source, _script, output, manifest = cache_pipeline
    run_all.ensure_outputs(str(source), rerun=True)
    assert output.read_text(encoding='utf-8') == 'MW:bad:good:n\n'
    assert manifest.is_file()
    assert run_all._cache_problem(str(source)) is None
    run_all.ensure_outputs(str(source))


@pytest.mark.parametrize('mutation', ['input', 'detector', 'output'])
def test_changed_cache_material_is_rejected(cache_pipeline, mutation):
    source, script, output, _manifest = cache_pipeline
    run_all.ensure_outputs(str(source), rerun=True)
    target = {'input': source, 'detector': script, 'output': output}[mutation]
    with target.open('a', encoding='utf-8') as stream:
        stream.write('changed\n')
    with pytest.raises(SystemExit) as error:
        run_all.ensure_outputs(str(source))
    assert error.value.code == 2


def test_missing_manifest_is_rejected(cache_pipeline):
    source, _script, output, _manifest = cache_pipeline
    output.write_text('MW:bad:good:n\n', encoding='utf-8')
    with pytest.raises(SystemExit) as error:
        run_all.ensure_outputs(str(source))
    assert error.value.code == 2


def test_explicit_stale_override_warns_when_outputs_exist(cache_pipeline, capsys):
    source, _script, output, _manifest = cache_pipeline
    output.write_text('MW:bad:good:n\n', encoding='utf-8')
    run_all.ensure_outputs(str(source), allow_stale_cache=True)
    assert 'WARNING: using stale detector cache' in capsys.readouterr().err


def test_stale_override_cannot_supply_missing_outputs(cache_pipeline):
    source, _script, _output, _manifest = cache_pipeline
    with pytest.raises(SystemExit) as error:
        run_all.ensure_outputs(str(source), allow_stale_cache=True)
    assert error.value.code == 2
