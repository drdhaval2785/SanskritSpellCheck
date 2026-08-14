#!/usr/bin/env python3
"""Build the IJL double-blind submission pair for A44 from the single source manuscript.

Why a script and not a hand-edited second copy: the manuscript is ~719 lines and will keep
being revised. Two divergent copies drift, and the anonymised one silently rots — the copy a
reviewer sees would stop matching the copy the author edits. So the anonymised main file and
the Title Page are *derived*, never edited, and regenerating after any revision is one
command. `--check` makes staleness a test failure rather than something noticed at upload.

IJL requires (Stylesheet 2024 §1.1, from the gated Author Pack):
  - a Title Page carrying title, names, affiliations, countries, emails;
  - a main file with title, abstract, keywords but NOT the authors;
  - all self-identifying information removed for double-blind review;
  - explicitly NOT replacing names with "Author"/"Authors" ("this usually identifies you").

The four-vector ruling this implements (approved 10-08-2026), each vector treated
differently because the identification risk differs:

  1. Frontmatter author line  -> moved to the Title Page. Zero information lost: IJL
     requires that file anyway.
  2. sanskrit-lexicon/csl-orig -> KEPT. A third-party organisation repo that identifies
     nobody, and the paper's data provenance depends on it.
  3. CORRECTIONS #447 (x3)     -> withheld. The issue's GitHub author is the paper's author,
     so the URL is a byline in disguise. Replaced by a description, restored at camera-ready.
  4. 35 relative ../ paths     -> Supplementary Online Material (no word limit per §1.1,
     unlike appendices which count against the 4,000-8,000 band). These links are dead in a
     submitted PDF regardless of anonymity, so this fixes a real defect, not just a blind-review one.

Plus: draft-status blockquotes naming internal review files and handoff rulings are dropped.

Usage:
    python papers/build_a44_anonymous.py            # write the pair
    python papers/build_a44_anonymous.py --check    # verify up to date + anonymous (CI/selftest)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

PAPERS = Path(__file__).resolve().parent
SOURCE = PAPERS / "A44_body_grounded_triage_paper.md"
OUT_MAIN = PAPERS / "A44_ijl_main_anonymous.md"
OUT_TITLE = PAPERS / "A44_ijl_title_page.md"
OUT_SUPP = PAPERS / "A44_ijl_supplementary_index.md"

# Vector 3: the issue author is the paper author, so a bare URL identifies them.
CORRECTIONS_ISSUE_RE = re.compile(
    r"\[(?:CORRECTIONS #447|umbrella issue #447)\]\(https://github\.com/sanskrit-lexicon/CORRECTIONS/issues/447\)"
)
CORRECTIONS_REPLACEMENT = (
    "a public umbrella issue in the CDSL `CORRECTIONS` repository "
    "*(reference withheld for anonymous review)*"
)

# Vector 2: kept verbatim. Listed so the anonymity check can whitelist it deliberately
# rather than by accident.
ALLOWED_GITHUB = ("github.com/sanskrit-lexicon/csl-orig",)

# Vector 4: every ../ target -> supplementary file id. Grouped by role so the index reads as
# an apparatus, not a file dump. Order fixed => stable S-numbers across regenerations.
SUPPLEMENTARY: list[tuple[str, str, str]] = [
    # (relative path in repo, supplement id, human description)
    (
        "detectors/combined_candidates.txt",
        "S1",
        "Tier-A candidate lists per dictionary (engine output)",
    ),
    ("sanhw1.txt", "S2", "Headword spine used by the toolset"),
    (
        "detectors/get_external_source.py",
        "S3",
        "External-source attribution for headwords",
    ),
    ("detectors/triage_lang.py", "S4", "Declared-language settlement"),
    ("detectors/slp1util.py", "S5", "SLP1 utilities, incl. load_whitelist()"),
    (
        "detectors/gen_do_not_file_suppress.py",
        "S6",
        "Generator for the do-not-file suppress list",
    ),
    (
        "nochange/do_not_file_suppress.txt",
        "S7",
        "Do-not-file suppress list (2,297 deduped headwords)",
    ),
    ("detectors/eval.py", "S8", "Evaluation harness (false-positive gate)"),
    ("detectors/gold_corrections.tsv", "S9", "Held-out gold correction set"),
    ("detectors/bodyaware_workflow.js", "S10", "Body-aware triage workflow"),
    ("detectors/", "S11", "Triage scripts (detectors/triage_*.py)"),
    (
        ".claude/commands/dict-triage.md",
        "S12",
        "Operational triage procedure per dictionary",
    ),
    ("corrections_draft/", "S13", "Per-dictionary triage working directories"),
    ("corrections_draft/README.md", "S14", "Triage overview across 33 dictionaries"),
    (
        "corrections_draft/SHS/readme.md",
        "S15",
        "Entry-decidable error classes with evidence lines",
    ),
    (
        "corrections_draft/VERIFICATION_2026_07.md",
        "S16",
        "Per-row source re-verification narrative",
    ),
    (
        "corrections_draft/file_first_verified.tsv",
        "S17",
        "Per-row re-verification record",
    ),
    ("corrections_draft/irr/", "S18", "Inter-rater reliability inputs and outputs"),
    ("detectors/irr_build_inputs.py", "S19", "IRR input builder"),
    ("detectors/irr_agreement.py", "S20", "IRR agreement (exact rational arithmetic)"),
    (
        "corrections_draft/irr/agreement_stats.md",
        "S21",
        "Computed agreement statistics",
    ),
    ("detectors/irr_cross_family.py", "S22", "Cross-family IRR re-run"),
    (
        "corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md",
        "S23",
        "Open human-anchor requirement",
    ),
    ("docs/PRIOR_ART.md", "S24", "Prior-art survey"),
]

# Longest path first: without this, "corrections_draft/" would match inside
# "corrections_draft/irr/agreement_stats.md" and mis-number half the apparatus.
_SUPP_BY_LEN = sorted(SUPPLEMENTARY, key=lambda row: len(row[0]), reverse=True)
_SUPP_IDS = {path: sid for path, sid, _ in SUPPLEMENTARY}

MD_LINK_RE = re.compile(r"\[(?P<label>[^\]]*)\]\(\.\./(?P<target>[^)]*)\)")


def _strip_frontmatter(text: str) -> tuple[str, dict[str, str]]:
    """Split YAML frontmatter off the body. Vector 1 lives here."""
    if not text.startswith("---\n"):
        return text, {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return text, {}
    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')
    return body, meta


def _drop_draft_blockquotes(text: str) -> str:
    """Drop leading draft-status blockquotes (internal review files, handoff rulings).

    Only the run of blockquotes before the first prose section: later blockquotes are the
    paper's own argument (caveats, definitions) and must survive.
    """
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    seen_section = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            seen_section = True
        if not seen_section and line.startswith("> "):
            while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
                i += 1
            # keep exactly one blank line where the block stood
            if out and out[-1].strip():
                out.append("")
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _rewrite_supplementary(text: str) -> tuple[str, set[str]]:
    """Vector 4: relative repo paths -> Supplementary File ids."""
    used: set[str] = set()

    def repl(match: re.Match[str]) -> str:
        target = match.group("target")
        label = match.group("label")
        for path, sid, _desc in _SUPP_BY_LEN:
            if target == path or target.rstrip("/") == path.rstrip("/"):
                used.add(sid)
                return f"{label} (Supplementary File {sid})"
        for path, sid, _desc in _SUPP_BY_LEN:
            if target.startswith(path) and path.endswith("/"):
                used.add(sid)
                return f"{label} (Supplementary File {sid})"
        raise SystemExit(
            f"anonymise: relative link with no supplementary mapping: {target!r}\n"
            f"  Add it to SUPPLEMENTARY in {Path(__file__).name}."
        )

    return MD_LINK_RE.sub(repl, text), used


def build() -> tuple[str, str, str, set[str]]:
    text = SOURCE.read_text(encoding="utf-8")
    body, meta = _strip_frontmatter(text)
    body = _drop_draft_blockquotes(body)
    body = CORRECTIONS_ISSUE_RE.sub(CORRECTIONS_REPLACEMENT, body)
    body, used = _rewrite_supplementary(body)

    title = meta.get("title", "").strip('"')
    generated = (
        "<!-- GENERATED by papers/build_a44_anonymous.py from "
        "A44_body_grounded_triage_paper.md — do not edit; edit the source and regenerate. -->\n"
    )

    main = generated + body.lstrip("\n")
    if not main.endswith("\n"):
        main += "\n"

    title_page = generated + "\n".join(
        [
            "# Title Page",
            "",
            f"**Title.** {title}",
            "",
            f"**Author.** {meta.get('author', '')}",
            "",
            "**Affiliation.** Independent scholar",
            "",
            "**Country.** Latvia",
            "",
            "**Journal.** International Journal of Lexicography",
            "",
            "> Submitted as the separate Title Page required by IJL Stylesheet 2024 §1.1. The",
            "> companion main file carries the title, abstract and keywords but no author, per the",
            "> journal's double-blind review process.",
            "",
        ]
    )

    supp_lines = [
        generated.rstrip("\n"),
        "",
        "# A44 — Supplementary Online Material index",
        "",
        "Supplementary Online Material carries no word limit under IJL Stylesheet 2024 §1.1",
        "(unlike appendices, which count against the 4,000–8,000 band), so the reproducibility",
        "apparatus ships here rather than inline.",
        "",
        "Each file is supplied with author-identifying paths and remote URLs removed for",
        "double-blind review; the live repository URLs are restored at camera-ready.",
        "",
        "| Supplement | Contents | Source path |",
        "|---|---|---|",
    ]
    for path, sid, desc in SUPPLEMENTARY:
        flag = "" if sid in used else " _(cited indirectly)_"
        supp_lines.append(f"| **{sid}** | {desc}{flag} | `{path}` |")
    supp_lines += [
        "",
        "**Note on S1.** `detectors/combined_candidates.txt` is generated and git-ignored, so it",
        "is not in the repository: it must be regenerated before packaging. This is a genuine",
        "reproducibility gap the anonymisation pass surfaced, not an artefact of anonymising.",
        "",
    ]
    return main, title_page, "\n".join(supp_lines), used


def check_anonymous(main: str) -> list[str]:
    """Fail loudly on anything that could identify the author in the main file."""
    problems: list[str] = []
    lowered = main.lower()

    for needle in ("gasyoun", "gasūns", "gasuns", "drdhaval2785", "orcid", "@ya.ru"):
        if needle in lowered:
            problems.append(f"main file still contains identifying token {needle!r}")

    if "issues/447" in main:
        problems.append(
            "main file still links CORRECTIONS #447 (author is the paper's author)"
        )

    for match in re.finditer(r"github\.com/[A-Za-z0-9_./-]*", main):
        url = match.group(0)
        if not any(url.startswith(ok) for ok in ALLOWED_GITHUB):
            problems.append(f"unexpected github URL in main file: {url}")

    if MD_LINK_RE.search(main):
        problems.append(
            "main file still has relative ../ links (dead in a submitted PDF)"
        )

    # The stylesheet explicitly bans this workaround.
    if re.search(
        r"\b(?:Author|Authors)\b\s*\(withheld\)|\[Author\]|\bAuthor et al\b", main
    ):
        problems.append("main file replaces a name with 'Author' — IJL forbids this")

    if "author:" in lowered.split("\n")[0:6]:
        problems.append("main file appears to retain frontmatter author")

    return problems


def check_completeness(main: str) -> list[str]:
    """Structural requirements for the main file, separate from anonymity.

    IJL §1.1 requires the main file to carry title, abstract AND keywords. A missing
    keywords line is a submission blocker, but it is not an anonymity failure — so it is
    reported without blocking the write, which would otherwise make an unrelated open
    checklist item (#6) prevent generating an anonymous file at all.
    """
    warnings: list[str] = []
    if not re.search(r"^\*{0,2}Keywords:?\*{0,2}", main, re.MULTILINE):
        warnings.append(
            "no 'Keywords:' line — IJL §1.1 requires it in the main file, below the Abstract "
            "(checklist item #6; the controlled list is only visible inside ScholarOne)"
        )
    if "## Abstract" not in main:
        warnings.append(
            "no '## Abstract' section — IJL §1.1 requires it in the main file"
        )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="verify generated files are current"
    )
    args = parser.parse_args()

    main_text, title_text, supp_text, used = build()
    problems = check_anonymous(main_text)
    warnings = check_completeness(main_text)

    unused = [sid for _p, sid, _d in SUPPLEMENTARY if sid not in used]

    if args.check:
        for path, expected in (
            (OUT_MAIN, main_text),
            (OUT_TITLE, title_text),
            (OUT_SUPP, supp_text),
        ):
            if not path.exists():
                problems.append(
                    f"{path.name} missing — run: python papers/{Path(__file__).name}"
                )
            elif path.read_text(encoding="utf-8") != expected:
                problems.append(
                    f"{path.name} is stale — regenerate after editing the source"
                )
        if problems:
            print("FAIL — A44 anonymisation")
            for problem in problems:
                print(f"  - {problem}")
            return 1
        print(
            f"PASS — A44 anonymisation ({len(SUPPLEMENTARY)} supplements, "
            f"{len(used)} directly cited)"
        )
        for warning in warnings:
            print(f"  OPEN (not an anonymity defect): {warning}")
        return 0

    if problems:
        print("FAIL — refusing to write a non-anonymous main file")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    OUT_MAIN.write_text(main_text, encoding="utf-8")
    OUT_TITLE.write_text(title_text, encoding="utf-8")
    OUT_SUPP.write_text(supp_text, encoding="utf-8")
    print(f"wrote {OUT_MAIN.name}, {OUT_TITLE.name}, {OUT_SUPP.name}")
    print(f"  supplements: {len(SUPPLEMENTARY)} ({len(used)} directly cited)")
    if unused:
        print(f"  not directly cited: {', '.join(unused)}")
    for warning in warnings:
        print(f"  OPEN (not an anonymity defect): {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
