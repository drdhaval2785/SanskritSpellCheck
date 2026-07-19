import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "detectors"))

import run_all  # noqa: E402


def _payload(path):
    doc = path.read_text(encoding="utf-8")
    match = re.search(
        r'<script type="application/json" id="payload">(.*?)</script>',
        doc,
        flags=re.S,
    )
    assert match
    return doc, json.loads(match.group(1))


def _row():
    cand = run_all.Cand('x"</script>&देव')
    cand.detectors.update({"spell_correct", "phonotactic"})
    cand.sugg_dets["yदेव"].add("spell_correct")
    cand.sugg_dicts["yदेव"].add("MW")
    cand.dicts.update({"MW", "PW"})
    return (250, "A", 4, "yदेव", cand)


def test_payload_precedes_consumer_and_round_trips(tmp_path):
    out = tmp_path / "review.html"
    run_all.write_review_html([_row()], out)

    doc, data = _payload(out)
    assert doc.index('id="payload"') < doc.index("const DATA=JSON.parse")
    assert "&quot;" not in doc
    assert "</script>&" not in doc
    assert data[0]["w"] == 'x"</script>&देव'


def test_export_dicts_exclude_flagger_only_dictionaries(tmp_path):
    out = tmp_path / "review.html"
    run_all.write_review_html([_row()], out)
    doc, data = _payload(out)

    assert data[0]["dicts"] == ["MW", "PW"]
    assert data[0]["export_dicts"] == ["MW"]
    assert "r.export_dicts.forEach" in doc


def test_campaign_scope_limits_scans_and_exports(tmp_path):
    out = tmp_path / "review.html"
    run_all.write_review_html([_row()], out, dict_scope={"PW"})
    _, data = _payload(out)

    assert data[0]["dicts"] == ["PW"]
    assert data[0]["export_dicts"] == []
