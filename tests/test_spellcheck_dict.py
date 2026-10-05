"""tests for the versioned spell-check dictionary (A55 union + MWderivations):
the tools/build_spellcheck_dict.py builder and the detectors/slp1util loader."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "build_spellcheck_dict", ROOT / "tools" / "build_spellcheck_dict.py")
builder = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(builder)

sys.path.insert(0, str(ROOT / "detectors"))
import slp1util  # noqa: E402


UNION_FIXTURE = (
    "slp1\tiast\tn_dicts\tdicts\tgender\tfem_fold\n"
    "agni\tagni\t3\tmw pwg ap\tm\t\n"
    "aNga\taṅga\t2\tmw pw\tn\t\n"
    "AYjanA\tāñjanā\t1\tmw\tf\tfem_fold\n"
)
# analysis2.txt columns: Hcode, L, key1, key2, gender, parse, status, method
MWD_FIXTURE = (
    "3\t2\takAra\ta-kAra\tm\ta-kAra\tDONE\tcpd1\n"          # key2 -> akAra
    "1\t1\tagni\tagni\tm\t\tNTD\tinit\n"                    # key1 dup of union
    "9\t9\tzZqa\tzZ@qAfala\tm\t\tNTD\tinit\n"               # NTD key2 must NOT contribute
    "4\t7\tAYjanAByaYjana\tA@YjanA@ByaYjana\tm\tX-Y\tDONE\tcpd2\n"
    #  ^ real key1 is mark-free; DONE key2 cleans to the same word (dedup)
)


def _run_builder(tmp_path, out_dir):
    union = tmp_path / "union_headwords.tsv"
    union.write_text(UNION_FIXTURE, encoding="utf-8")
    mwd = tmp_path / "analysis2.txt"
    mwd.write_text(MWD_FIXTURE, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_spellcheck_dict.py"),
         "--union", str(union), "--mwderiv", str(mwd), "--out", str(out_dir)],
        capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    return out_dir / builder.ARTIFACT_NAME


def test_builder_dedup_sort_and_manifest(tmp_path):
    out_dir = tmp_path / "out"
    artifact = _run_builder(tmp_path, out_dir)
    words = artifact.read_text(encoding="utf-8").splitlines()
    # akAra (key2 of DONE), agni (dup), aNga, AYjanA, AYjanAByaYjana (cleaned @)
    # and NOT zZqAfala — the NTD row's key2 is a placeholder, never taken:
    assert set(words) == {"agni", "aNga", "AYjanA", "akAra",
                          "AYjanAByaYjana", "zZqa"}
    assert "zZqAfala" not in words
    assert len(words) == 6                       # no duplicate lines
    assert words == sorted(words, key=slp1util.sanskrit_sort_key)

    manifest = json.loads(
        (out_dir / (builder.ARTIFACT_NAME + ".meta.json")).read_text("utf-8"))
    assert manifest["version"] == builder.DICT_VERSION
    assert manifest["counts"]["combined_raw"] == 9      # 3 union + 4 key1 + 2 key2
    assert manifest["counts"]["deduped"] == 6
    assert manifest["counts"]["duplicates_removed"] == 3
    assert manifest["sha256"] == hashlib.sha256(
        artifact.read_bytes()).hexdigest()


def test_builder_rejects_bad_union(tmp_path):
    bad = tmp_path / "bad.tsv"
    bad.write_text("word\tfoo\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_spellcheck_dict.py"),
         "--union", str(bad), "--mwderiv", str(tmp_path / "x.txt"),
         "--out", str(tmp_path)],
        capture_output=True, text=True, encoding="utf-8")
    assert result.returncode != 0


def test_builder_is_byte_reproducible(tmp_path):
    """Two runs under different PYTHONHASHSEED must produce identical bytes:
    sanskrit_sort_key alone is not injective (M->homorganic ties), so the
    raw-string tiebreak is what makes the artifact deterministic."""
    union = tmp_path / "union_headwords.tsv"
    union.write_text(UNION_FIXTURE, encoding="utf-8")
    mwd = tmp_path / "analysis2.txt"
    mwd.write_text(MWD_FIXTURE, encoding="utf-8")
    digests = set()
    for seed, out in (("1", tmp_path / "a"), ("2", tmp_path / "b")):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_spellcheck_dict.py"),
             "--union", str(union), "--mwderiv", str(mwd), "--out", str(out)],
            capture_output=True, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONHASHSEED=seed))
        assert result.returncode == 0, result.stderr
        digests.add(hashlib.sha256(
            (out / builder.ARTIFACT_NAME).read_bytes()).hexdigest())
    assert len(digests) == 1


def test_load_spellcheck_dict_env_override_and_degrade(tmp_path, monkeypatch):
    wordfile = tmp_path / "dict.txt"
    wordfile.write_text("agni\n# comment\naNga\n\n", encoding="utf-8")
    monkeypatch.setenv("SANSKRIT_SPELLCHECK_DICT", str(wordfile))
    assert slp1util.load_spellcheck_dict() == {"agni", "aNga"}

    monkeypatch.setenv("SANSKRIT_SPELLCHECK_DICT",
                       str(tmp_path / "missing.txt"))
    assert slp1util.load_spellcheck_dict() == set()   # degrade, never raise

    monkeypatch.delenv("SANSKRIT_SPELLCHECK_DICT")
    assert slp1util.load_spellcheck_dict(str(wordfile)) == {"agni", "aNga"}


def test_committed_artifact_matches_manifest():
    artifact = ROOT / "HeadwordLists" / builder.ARTIFACT_NAME
    if not artifact.exists():                     # builder output not committed
        pytest.skip("spellcheck dict artifact not present")
    manifest = json.loads(
        (artifact.parent / (artifact.name + ".meta.json")).read_text("utf-8"))
    assert manifest["version"] == builder.DICT_VERSION
    assert manifest["sha256"] == hashlib.sha256(artifact.read_bytes()).hexdigest()

    words = artifact.read_text(encoding="utf-8").splitlines()
    assert len(words) == manifest["counts"]["deduped"]
    assert len(words) == len(set(words))          # dedup holds
    assert words == sorted(words, key=slp1util.sanskrit_sort_key)
    # spot checks against the sources (A55 union + MWderivations)
    for known in ("agni", "indra", "aNga"):
        assert known in words
    assert "@" not in "".join(words[:1000])       # analysis marks cleaned
