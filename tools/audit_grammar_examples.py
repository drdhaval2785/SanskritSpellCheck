#!/usr/bin/env python3
"""audit_grammar_examples.py -- grammar-example audit prototype (bashspell pattern, Lane A).

Crawls grammar-book source material (csl-kale chapter display files), extracts the
Sanskrit example words marked with <span class="san">...</span>, checks each against
the sanhw1.txt headword list, the MW/PW/VCP headword lists, and a vidyut parse vote
(vendored stems + optional sandhi/compound splitting), and emits per-page + per-word
candidate reports for LINGUISTIC REVIEW -- never auto-verdicts.

This produces candidates for review, NOT automatically valid test cases. Grammar
sources also mark translations, transcriptions, historical forms and deliberately
incorrect spellings (bashspell measured: 1,461 rejects != 1,461 defects). Provenance:
AigizK/bashspell tools/audit_grammar_reference.py pattern ported for
SanskritSpellCheck (H4154; context reports/bashspell-lessons-2026-09-05.md).

Outputs (reports/grammar-examples-audit-<date>/):
  pages.tsv                 page, title, examples, accepted, rejected, sha256
  scan.json                 every word verdict + SHA-256 of every source file AND
                            of the dictionaries used; unparsable lines recorded
  review-candidates.tsv     rejected words: word, source pages, dict hits, vidyut
  review-candidates.csv       vote, register tag, tier (dual export of the same rows)
  review-payload.json       same rows in the combined_review.html payload schema
                            ({w, s, tier, score, dets, dicts, reason}; :y/:n export)

vidyut attribution: stems derived from vidyut (Arun Prasad / ambuda-org, MIT;
https://github.com/ambuda-org/vidyut) via detectors/gen_vidyut_stems.py.

Run:
  python tools/audit_grammar_examples.py [--repo DIR] [--kale DIR] [--output DIR]
                                         [--vidyut-stems FILE] [--sandhi-csv FILE]
Python >= 3.9; stdlib only at core (sanskrit-util + vidyut optional, degrade
gracefully and record the degraded mode in scan.json).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

TOOL = "audit_grammar_examples.py"

SPAN_RE = re.compile(r"<span\s+class=[\"']san[\"']\s*>(.*?)</span>", re.I)
TAG_RE = re.compile(r"<[^>]+>")
PAGE_RE = re.compile(r"^(kale_Page_\d+)(?:\s+(.*))?$")
REGISTER_RE = re.compile(r"\b(vedic|classical|epic)\b", re.I)
MAX_WORD_LEN = 40

# Conservative nominal endings for the ending-strip heuristic. The stripped form is
# only accepted if it is a real vidyut stem (membership oracle decides; the heuristic
# never invents stems -- bashspell lesson: split only at proven boundaries).
NOMINAL_ENDINGS = (
    "sH", "H", "sU", "au", "ai", "os", "Am", "At", "Byas", "ByAm", "ByaH", "su",
    "ezu", "Am", "i", "u",
)

# Used only when sanskrit-util is unavailable; kept in lockstep with its alphabet.
SLP1_ALPHABET_FALLBACK = "aAiIuUfFxXeEoOMH~kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL"

KALE_CHAPTER_GLOB = "kale*.txt"
KALE_CHROME = {"kalefiles.txt", "kaletop.txt"}


def slp1_alphabet() -> str:
    try:
        from sanskrit_util import SLP1_ALPHABET
        return SLP1_ALPHABET
    except Exception:
        return SLP1_ALPHABET_FALLBACK


def is_slp1(token: str, alphabet: str) -> bool:
    return bool(token) and all(ch in alphabet for ch in token)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_source(raw: bytes) -> tuple[str, str]:
    """BOM-aware charset sniff with cp1251-style fallback (bashspell lesson).

    Returns (text, charset_used). Never raises: latin-1 decodes any bytes, and the
    fallback usage is recorded in scan.json via charset_used.
    """
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8", errors="strict"), "utf-8-sig"
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        pass
    try:
        return raw.decode("cp1251"), "cp1251-fallback"
    except UnicodeDecodeError:
        return raw.decode("latin-1"), "latin-1-fallback"


def extract_examples(content: str, alphabet: str) -> tuple[list[str], list[dict], int]:
    """Extract candidate words from one source line's spans.

    Returns (words, unparsable_pieces, single_letter_skipped). Multi-token spans
    contribute each token; single letters are counted, not candidates (documented
    extraction filter, bashspell len>2 analog); invalid-SLP1 or over-long pieces are
    recorded in unparsable_pieces -- never silently dropped.
    """
    words: list[str] = []
    unparsable: list[dict] = []
    single_letter = 0
    for raw_span in SPAN_RE.finditer(content):
        piece = " ".join(unescape(raw_span.group(1)).split())
        if not piece:
            continue
        for token in piece.split():
            if len(token) > MAX_WORD_LEN:
                unparsable.append({"piece": token, "reason": f"too_long>{MAX_WORD_LEN}"})
            elif len(token) == 1:
                single_letter += 1
            elif not is_slp1(token, alphabet):
                unparsable.append({"piece": token, "reason": "not_slp1"})
            else:
                words.append(token)
    return words, unparsable, single_letter


def strip_tags(text: str) -> str:
    return " ".join(unescape(TAG_RE.sub("", text)).split())


class DictOracle:
    """sanhw1 + MW/PW/VCP headword membership (exact SLP1 match)."""

    def __init__(self, sanhw1: Path, mw: Path, pw: Path, vcp: Path):
        self.paths = {"sanhw1": sanhw1, "MW": mw, "PW": pw, "VCP": vcp}
        self.sanhw1: dict[str, list[str]] = {}
        for line in self._lines(sanhw1):
            word, _, dicts = line.partition(":")
            if word:
                self.sanhw1[word] = [d for d in dicts.split(",") if d]
        self.lists = {
            name: set(self._lines(path)) for name, path in (("MW", mw), ("PW", pw), ("VCP", vcp))
        }

    @staticmethod
    def _lines(path: Path) -> list[str]:
        text, _ = decode_source(path.read_bytes())
        return [ln.strip() for ln in text.splitlines() if ln.strip()]

    def manifests(self) -> dict:
        out = {}
        for name, path in self.paths.items():
            out[name] = {"path": str(path), "sha256": sha256_file(path),
                         "entries": len(self.sanhw1) if name == "sanhw1" else len(self.lists[name])}
        return out

    def check(self, word: str) -> dict:
        sanhw1_dicts = self.sanhw1.get(word)
        hits = {name: word in words for name, words in self.lists.items()}
        return {
            "in_sanhw1": sanhw1_dicts is not None,
            "sanhw1_dicts": sanhw1_dicts or [],
            "dict_hits": sorted(name for name, hit in hits.items() if hit),
            "dict_membership": hits,
        }


class VidyutOracle:
    """vidyut parse vote: vendored stems + optional compound/sandhi split check."""

    def __init__(self, stems_path: Path, sandhi_csv: Path | None = None):
        self.stems_path = stems_path
        text, _ = decode_source(stems_path.read_bytes())
        self.stems = {ln.strip() for ln in text.splitlines() if ln.strip()}
        self.splitter = None
        self.sandhi_csv = None
        if sandhi_csv is not None and sandhi_csv.is_file():
            try:
                from vidyut.sandhi import Splitter
                self.splitter = Splitter.from_csv(str(sandhi_csv))
                self.sandhi_csv = sandhi_csv
            except Exception:
                self.splitter = None

    def manifest(self) -> dict:
        mode = "full" if self.splitter is not None else "stems-only"
        out = {
            "stems_path": str(self.stems_path),
            "stems_sha256": sha256_file(self.stems_path),
            "stems_count": len(self.stems),
            "mode": mode,
        }
        if self.sandhi_csv is not None:
            out["sandhi_csv"] = str(self.sandhi_csv)
            out["sandhi_csv_sha256"] = sha256_file(self.sandhi_csv)
        return out

    def vote(self, word: str) -> tuple[str, str]:
        if word in self.stems:
            return "stem-exact", "word is a vidyut pratipadika stem"
        if self.splitter is not None:
            for idx in range(1, len(word)):
                try:
                    splits = self.splitter.split_at(word, idx)
                except Exception:
                    continue
                for split in splits:
                    if (split.first in self.stems and split.second in self.stems):
                        return "compound-split", f"{split.first}+{split.second}"
        for ending in NOMINAL_ENDINGS:
            if word.endswith(ending):
                base = word[: -len(ending)]
                if len(base) >= 2 and base in self.stems:
                    return "ending-strip", f"{base}+<{ending}>"
        return "unparsed", "no stem match, proven split, or conservative ending strip"


def audit_source_file(path: Path, alphabet: str, oracle_dicts: DictOracle,
                      oracle_vid: VidyutOracle, checked: dict, rejected: dict,
                      unparsable: list, stats: dict) -> list[dict]:
    """Crawl one kale chapter file; return its pages.tsv rows (plus scan.json extras)."""
    raw = path.read_bytes()
    text, charset_used = decode_source(raw)
    pages: dict[str, dict] = {}
    lines = text.splitlines()
    for line_no, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        match = PAGE_RE.match(line)
        if not match:
            unparsable.append({"source": "csl-kale", "file": path.name, "page": None,
                               "line_no": line_no, "piece": line[:120],
                               "reason": "no_page_anchor"})
            stats["lines_unparsable"] += 1
            continue
        page_id, content = match.group(1), match.group(2) or ""
        words, bad_pieces, single_letter = extract_examples(content, alphabet)
        for piece in bad_pieces:
            piece.update({"source": "csl-kale", "file": path.name, "page": page_id,
                          "line_no": line_no})
            unparsable.append(piece)
        stats["single_letter_skipped"] += single_letter
        register_m = REGISTER_RE.search(content)
        register = register_m.group(1).lower() if register_m else ""
        page = pages.setdefault(page_id, {
            "page": page_id, "source_file": path.name,
            "title": strip_tags(content)[:80] if content else "",
            "examples": [], "accepted": 0, "rejected": 0, "register": register,
        })
        seen_on_page = set(page["examples"])
        for word in words:
            if word not in checked:
                dict_verdict = oracle_dicts.check(word)
                vote, detail = oracle_vid.vote(word)
                checked[word] = {**dict_verdict, "vidyut_vote": vote,
                                 "vidyut_detail": detail, "register": register}
            if word in seen_on_page:
                continue
            seen_on_page.add(word)
            page["examples"].append(word)
            if checked[word]["in_sanhw1"]:
                page["accepted"] += 1
            else:
                page["rejected"] += 1
                rejected.setdefault(word, [])
                if page_id not in rejected[word]:
                    rejected[word].append(page_id)
    rows = []
    for page_id in sorted(pages):
        page = pages[page_id]
        page["sha256"] = hashlib.sha256(
            f"{path.name}:{page_id}".encode("utf-8")).hexdigest()
        rows.append(page)
    stats["files"].append({
        "path": path.name, "sha256": hashlib.sha256(raw).hexdigest(), "charset_used": charset_used,
        "lines_total": len(lines), "lines_parsed": sum(1 for p in pages.values()),
        "pages": len(pages),
    })
    return rows


def tier_for(record: dict) -> str:
    """Review priority over rejected words: A = probable sanhw1 gap (vidyut stem),
    B = parsed or attested in MW/PW/VCP, C = unparsed and unattested."""
    if record["vidyut_vote"] == "stem-exact":
        return "A"
    if record["vidyut_vote"] in ("compound-split", "ending-strip") or record["dict_hits"]:
        return "B"
    return "C"


def score_for(record: dict, tier: str) -> int:
    return {"A": 300, "B": 200, "C": 100}[tier] + 10 * len(record["dict_hits"])


def write_outputs(out: Path, pages_rows: list, checked: dict, rejected: dict,
                  unparsable: list, sources: dict, counts: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)

    with (out / "pages.tsv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(("page", "title", "examples", "accepted", "rejected", "sha256"))
        for page in pages_rows:
            writer.writerow((page["page"], page["title"], len(page["examples"]),
                             page["accepted"], page["rejected"], page["sha256"]))

    scan = {
        "tool": TOOL,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "framing": "candidates for linguistic review, NOT automatically valid test cases",
        "sources": sources,
        "dictionaries": counts["dict_manifest"],
        "vidyut": counts["vidyut_manifest"],
        "counts": counts["summary"],
        "pages": [{k: page[k] for k in ("page", "source_file", "title", "examples",
                                        "accepted", "rejected", "register", "sha256")}
                   for page in pages_rows],
        "checked": checked,
        "rejected": rejected,
        "unparsable": unparsable,
    }
    (out / "scan.json").write_text(
        json.dumps(scan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    candidates = []
    for word in sorted(rejected, key=lambda w: (-score_for(checked[w], tier_for(checked[w])), w)):
        record = checked[word]
        tier = tier_for(record)
        candidates.append({
            "word": word,
            "source_pages": ";".join(rejected[word]),
            "dict_hits": ",".join(record["dict_hits"]) or "-",
            "vidyut_vote": record["vidyut_vote"],
            "vidyut_detail": record["vidyut_detail"],
            "register": record["register"] or "-",
            "tier": tier,
        })
    header = ("word", "source_pages", "dict_hits", "vidyut_vote", "vidyut_detail",
              "register", "tier")
    for suffix, delimiter in (("tsv", "\t"), ("csv", ",")):
        with (out / f"review-candidates.{suffix}").open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh, delimiter=delimiter, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(tuple(row[col] for col in header) for row in candidates)

    payload = []
    for row in candidates:
        record = checked[row["word"]]
        dicts = record["dict_hits"] or ["MW"]
        reason = f"{record['vidyut_vote']}({record['vidyut_detail']})"
        if record["dict_hits"]:
            reason += f" attested:{','.join(record['dict_hits'])}"
        else:
            reason += " no MW/PW/VCP hit; MW scan for eyeball"
        payload.append({
            "w": row["word"],
            "s": record["vidyut_detail"] if record["vidyut_vote"] in
                 ("compound-split", "ending-strip") else None,
            "tier": row["tier"],
            "score": score_for(record, row["tier"]),
            "dets": ["grammar_example"],
            "dicts": dicts,
            "reason": reason,
        })
    (out / "review-payload.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1],
                        help="SanskritSpellCheck repo root")
    parser.add_argument("--kale", type=Path, default=None,
                        help="csl-kale repo root (default: sibling csl-kale checkout)")
    parser.add_argument("--output", type=Path, default=None,
                        help="output dir (default reports/grammar-examples-audit-2026-09-05)")
    parser.add_argument("--vidyut-stems", type=Path, default=None,
                        help="vidyut stem list (default detectors/vidyut_stems.txt)")
    parser.add_argument("--sandhi-csv", type=Path, default=None,
                        help="vidyut sandhi rules.csv (optional, enables compound-split)")
    args = parser.parse_args(argv)

    repo: Path = args.repo.resolve()
    kale = (args.kale or repo.parent / "csl-kale").resolve()
    files_dir = kale / "disp" / "files1"
    if not files_dir.is_dir():
        print(f"csl-kale chapter files not found at {files_dir} -- pass --kale", file=sys.stderr)
        return 2
    out = (args.output or repo / "reports" / "grammar-examples-audit-2026-09-05").resolve()
    stems_path = args.vidyut_stems or repo / "detectors" / "vidyut_stems.txt"
    if not stems_path.is_file():
        print(f"vidyut stems not found at {stems_path} -- pass --vidyut-stems "
              f"(run detectors/gen_vidyut_stems.py)", file=sys.stderr)
        return 2
    sandhi_csv = args.sandhi_csv or kale.parent / "vidyut-data" / "sandhi" / "rules.csv"

    alphabet = slp1_alphabet()
    oracle_dicts = DictOracle(repo / "sanhw1.txt", repo / "MWslp.txt",
                              repo / "PWslp.txt", repo / "VCPslp.txt")
    oracle_vid = VidyutOracle(stems_path, sandhi_csv if sandhi_csv.is_file() else None)

    checked: dict = {}
    rejected: dict = {}
    unparsable: list = []
    pages_rows: list = []
    stats: dict = {"files": [], "lines_unparsable": 0, "single_letter_skipped": 0}
    chapter_files = sorted(p for p in files_dir.glob(KALE_CHAPTER_GLOB)
                           if p.name not in KALE_CHROME)
    for path in chapter_files:
        pages_rows.extend(audit_source_file(path, alphabet, oracle_dicts, oracle_vid,
                                            checked, rejected, unparsable, stats))

    sources = {
        "csl-kale": {
            "root": str(files_dir),
            "excluded_chrome": sorted(KALE_CHROME),
            "files": stats["files"],
        }
    }
    accepted_total = sum(1 for r in checked.values() if r["in_sanhw1"])
    summary = {
        "source_files": len(chapter_files),
        "pages": len(pages_rows),
        "unique_examples": len(checked),
        "accepted_in_sanhw1": accepted_total,
        "rejected_candidates": len(rejected),
        "unparsable_pieces": len(unparsable),
        "unparsable_lines": stats["lines_unparsable"],
        "single_letter_skipped": stats["single_letter_skipped"],
        "tiers": {
            t: sum(1 for w in rejected if tier_for(checked[w]) == t)
            for t in ("A", "B", "C")
        },
    }
    counts = {"dict_manifest": oracle_dicts.manifests(), "vidyut_manifest": oracle_vid.manifest(),
              "summary": summary}
    write_outputs(out, pages_rows, checked, rejected, unparsable, sources, counts)

    print(f"Files: {summary['source_files']}; pages: {summary['pages']}; "
          f"unique examples: {summary['unique_examples']}; "
          f"accepted (in sanhw1): {summary['accepted_in_sanhw1']}; "
          f"review candidates: {summary['rejected_candidates']} "
          f"(A {summary['tiers']['A']} / B {summary['tiers']['B']} / C {summary['tiers']['C']}); "
          f"unparsable: {summary['unparsable_pieces']} pieces + "
          f"{summary['unparsable_lines']} lines")
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
