"""Synthetic-fixture tests for tools/audit_grammar_examples.py (H4154).

No estate data dependency: every test builds its own kale-format file, headword
lists and stem list under a temp dir. Collectable by both unittest discover and
pytest.
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import audit_grammar_examples as age  # noqa: E402


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


KALE_LINE = (
    "kale_Page_049 &sect; 61. Nouns in <span class=\"san\">a</span>.  "
    "<span class=\"san\">rAma</span>  <span class=\"san\">jYAna</span>"
)


class DecodeSourceTest(unittest.TestCase):
    def test_utf8_plain(self):
        text, charset = age.decode_source("rAma".encode("utf-8"))
        self.assertEqual((text, charset), ("rAma", "utf-8"))

    def test_utf8_bom(self):
        text, charset = age.decode_source(b"\xef\xbb\xbfrAma")
        self.assertEqual((text, charset), ("rAma", "utf-8-sig"))

    def test_cp1251_fallback_is_recorded_not_silent(self):
        raw = "привет".encode("cp1251")  # invalid UTF-8
        text, charset = age.decode_source(raw)
        self.assertEqual(text, "привет")
        self.assertEqual(charset, "cp1251-fallback")


class ExtractExamplesTest(unittest.TestCase):
    def setUp(self):
        self.alphabet = age.slp1_alphabet()

    def test_spans_and_entities(self):
        words, bad, single = age.extract_examples(
            "Nouns in <span class=\"san\">a</span>. <span class=\"san\">rAma</span>"
            " <span class=\"san\">jYAna&amp;co</span>", self.alphabet)
        self.assertEqual(words, ["rAma"])
        self.assertEqual([b["piece"] for b in bad], ["jYAna&co"])
        self.assertEqual(single, 1)

    def test_multi_token_span_splits(self):
        words, bad, single = age.extract_examples(
            "<span class=\"san\">rAma gopA</span>", self.alphabet)
        self.assertEqual(words, ["rAma", "gopA"])
        self.assertEqual((bad, single), ([], 0))

    def test_length_guard(self):
        long_token = "a" * (age.MAX_WORD_LEN + 1)
        words, bad, single = age.extract_examples(
            f"<span class=\"san\">{long_token}</span>", self.alphabet)
        self.assertEqual(words, [])
        self.assertEqual(bad[0]["reason"], f"too_long>{age.MAX_WORD_LEN}")

    def test_no_silent_drop_of_unparsable(self):
        words, bad, single = age.extract_examples(
            "<span class=\"san\">rAm4</span>", self.alphabet)
        self.assertEqual(words, [])
        self.assertEqual(bad, [{"piece": "rAm4", "reason": "not_slp1"}])


class ParseKaleLineTest(unittest.TestCase):
    def test_page_anchor(self):
        match = age.PAGE_RE.match(KALE_LINE)
        self.assertEqual(match.group(1), "kale_Page_049")
        self.assertIn("rAma", match.group(2))

    def test_line_without_anchor_is_recorded(self):
        self.assertIsNone(age.PAGE_RE.match("&sect; 99. orphan line"))


class RegisterTagTest(unittest.TestCase):
    def test_vedic_tag_carried(self):
        words, _, _ = age.extract_examples(
            "<span class=\"san\">gAvi</span> Vedic form", age.slp1_alphabet())
        self.assertEqual(words, ["gAvi"])
        match = age.REGISTER_RE.search("kale_Page_010 Vedic form")
        self.assertEqual(match.group(1).lower(), "vedic")

    def test_no_register_by_default(self):
        self.assertIsNone(age.REGISTER_RE.search(KALE_LINE))


class VidyutOracleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.stems_path = _write(
            Path(self.tmp.name) / "stems.txt", "rAma\nguru\ngopA\nkaraRa\n")
        self.oracle = age.VidyutOracle(self.stems_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_stem_exact(self):
        self.assertEqual(self.oracle.vote("rAma"), ("stem-exact", "word is a vidyut pratipadika stem"))

    def test_ending_strip_uses_oracle_not_invention(self):
        vote, detail = self.oracle.vote("rAmaH")
        self.assertEqual(vote, "ending-strip")
        self.assertEqual(detail, "rAma+<H>")

    def test_unparsed_verdict_recorded(self):
        self.assertEqual(self.oracle.vote("zAstra"), ("unparsed", self.oracle.vote("zAstra")[1]))

    def test_manifest_hashes_stems(self):
        manifest = self.oracle.manifest()
        self.assertEqual(manifest["stems_count"], 4)
        self.assertEqual(manifest["mode"], "stems-only")
        self.assertTrue(manifest["stems_sha256"])


class EndToEndSyntheticTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.kale = root / "csl-kale"
        _write(self.kale / "disp" / "files1" / "kale02.txt",
               "kale_Page_020 <span class=\"san\">rAma</span> <span class=\"san\">guru</span>\n"
               "kale_Page_021 Vedic <span class=\"san\">zAstra</span>\n"
               "orphan line without anchor\n")
        _write(self.kale / "disp" / "files1" / "kale03.txt",
               "kale_Page_030 <span class=\"san\">gopA</span>\n")
        _write(root / "repo" / "sanhw1.txt", "rAma:MW,PW\nguru:MW\ngopA:MW,VCP\n")
        _write(root / "repo" / "MWslp.txt", "rAma\nguru\nzAstra\n")
        _write(root / "repo" / "PWslp.txt", "rAma\n")
        _write(root / "repo" / "VCPslp.txt", "guru\n")
        _write(root / "repo" / "detectors" / "vidyut_stems.txt", "rAma\nguru\ngopA\nzAstra\n")
        self.repo = root / "repo"

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self):
        out = Path(self.tmp.name) / "out"
        code = age.main(["--repo", str(self.repo), "--kale", str(self.kale),
                         "--output", str(out)])
        return code, out

    def test_exit_zero_and_outputs_exist(self):
        code, out = self._run()
        self.assertEqual(code, 0)
        for name in ("pages.tsv", "scan.json", "review-candidates.tsv",
                     "review-candidates.csv", "review-payload.json"):
            self.assertTrue((out / name).is_file(), name)

    def test_pages_tsv_counts(self):
        _, out = self._run()
        rows = list(csv.DictReader((out / "pages.tsv").open(encoding="utf-8"), delimiter="\t"))
        by_page = {r["page"]: r for r in rows}
        self.assertEqual(by_page["kale_Page_020"]["examples"], "2")
        self.assertEqual(by_page["kale_Page_020"]["accepted"], "2")
        self.assertEqual(by_page["kale_Page_021"]["rejected"], "1")
        self.assertEqual(by_page["kale_Page_030"]["accepted"], "1")

    def test_scan_json_records_everything(self):
        _, out = self._run()
        scan = json.loads((out / "scan.json").read_text(encoding="utf-8"))
        self.assertIn("zAstra", scan["rejected"])
        self.assertIn("orphan line", scan["unparsable"][0]["piece"])
        self.assertEqual(scan["counts"]["unparsable_pieces"], 1)
        for src in scan["sources"]["csl-kale"]["files"]:
            self.assertEqual(len(src["sha256"]), 64)
            self.assertEqual(src["charset_used"], "utf-8")
        self.assertEqual(len(scan["dictionaries"]["sanhw1"]["sha256"]), 64)
        self.assertEqual(scan["vidyut"]["stems_count"], 4)
        self.assertIn("kale_Page_021", scan["rejected"]["zAstra"])
        self.assertEqual(scan["checked"]["zAstra"]["vidyut_vote"], "stem-exact")
        self.assertEqual(scan["checked"]["zAstra"]["register"], "vedic")
        self.assertEqual(scan["counts"]["tiers"]["A"], 1)

    def test_review_candidates_tsv_csv_dual_export_identical(self):
        _, out = self._run()
        tsv = list(csv.DictReader((out / "review-candidates.tsv").open(encoding="utf-8"), delimiter="\t"))
        csvr = list(csv.DictReader((out / "review-candidates.csv").open(encoding="utf-8")))
        self.assertEqual(tsv, csvr)
        self.assertEqual([r["word"] for r in tsv], ["zAstra"])
        self.assertEqual(tsv[0]["dict_hits"], "MW")
        self.assertEqual(tsv[0]["tier"], "A")
        self.assertEqual(tsv[0]["register"], "vedic")

    def test_review_payload_matches_combined_review_schema(self):
        _, out = self._run()
        payload = json.loads((out / "review-payload.json").read_text(encoding="utf-8"))
        self.assertEqual(len(payload), 1)
        row = payload[0]
        for key in ("w", "s", "tier", "score", "dets", "dicts", "reason"):
            self.assertIn(key, row)
        self.assertEqual(row["w"], "zAstra")
        self.assertEqual(row["dets"], ["grammar_example"])
        self.assertEqual(row["dicts"], ["MW"])


class TierTest(unittest.TestCase):
    def test_priority_order(self):
        self.assertEqual(age.tier_for({"vidyut_vote": "stem-exact", "dict_hits": []}), "A")
        self.assertEqual(age.tier_for({"vidyut_vote": "unparsed", "dict_hits": ["PW"]}), "B")
        self.assertEqual(age.tier_for({"vidyut_vote": "ending-strip", "dict_hits": []}), "B")
        self.assertEqual(age.tier_for({"vidyut_vote": "unparsed", "dict_hits": []}), "C")


if __name__ == "__main__":
    unittest.main()
