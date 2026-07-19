import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "faultfinder3a.php"
PHP = shutil.which("php")

pytestmark = pytest.mark.skipif(PHP is None, reason="PHP is not installed")


def _run(*args):
    return subprocess.run(
        [PHP, str(SCRIPT), *map(str, args)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


def test_missing_argument_prints_usage_without_creating_output(tmp_path):
    report = tmp_path / "report.txt"
    result = _run("MW", ROOT / "sanhw1.txt", report)
    assert result.returncode == 2
    assert "Usage:" in result.stderr
    assert not report.exists()


def test_unreadable_input_is_reported(tmp_path):
    result = _run("MW", tmp_path / "missing.txt", tmp_path / "a.txt", tmp_path / "b.txt")
    assert result.returncode == 1
    assert "not readable" in result.stderr


def test_output_paths_must_be_distinct(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("a:MW\n", encoding="utf-8")
    output = tmp_path / "same.txt"
    result = _run("MW", source, output, output)
    assert result.returncode == 2
    assert "distinct" in result.stderr


def test_minimal_four_argument_run(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("a:MW\nagni:MW\nakza:PW\n", encoding="utf-8")
    report = tmp_path / "report.txt"
    standard = tmp_path / "standard.txt"

    result = _run("MW", source, report, standard)
    assert result.returncode == 0, result.stderr
    assert report.exists()
    assert standard.exists()
