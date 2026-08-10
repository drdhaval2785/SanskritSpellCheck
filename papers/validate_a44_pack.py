"""Selftest for the A44 submission pack (H2407).

Verifies the pack is internally consistent and that no pack file makes a claim the
repository contradicts. Run: python papers/validate_a44_pack.py
Exit 0 = pass, 1 = fail.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"

PACK = [
    PAPERS / "A44_cover_letter.md",
    PAPERS / "A44_submission_checklist.md",
    PAPERS / "A44_checklist.md",
    ROOT / "CITATION.cff",
]
MANUSCRIPT = PAPERS / "A44_body_grounded_triage_paper.md"

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


# 1. Every pack file exists and is non-trivial.
for path in PACK:
    check(path.exists(), f"missing pack file: {path.relative_to(ROOT)}")
    if path.exists():
        check(
            len(path.read_text(encoding="utf-8")) > 500,
            f"suspiciously short: {path.relative_to(ROOT)}",
        )

# 2. CITATION.cff parses and carries the canonical identity from Uprava/AUTHOR.md.
cff_path = ROOT / "CITATION.cff"
if cff_path.exists():
    cff = cff_path.read_text(encoding="utf-8")
    for token in ("0000-0003-4513-884X", "gasyoun@ya.ru", "Gasūns", "Mārcis"):
        check(token in cff, f"CITATION.cff missing canonical identity token: {token}")
    # The repo declares no license (README "License status") -- never invent one.
    check(
        "\nlicense:" not in cff,
        "CITATION.cff declares a license, but the repo states it has none",
    )
    # Never ship a fabricated DOI.
    check("doi:" not in cff.lower(), "CITATION.cff carries a DOI; none has been minted")
    try:
        import yaml

        yaml.safe_load(cff)
    except ImportError:
        print("note: PyYAML absent, skipped YAML parse")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"CITATION.cff is not valid YAML: {exc}")

# 3. Byline consistency: the manuscript frontmatter and the cover letter agree.
if MANUSCRIPT.exists():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    check("0000-0003-4513-884X" in manuscript, "manuscript lost its ORCID")
    letter = (PAPERS / "A44_cover_letter.md").read_text(encoding="utf-8")
    check("0000-0003-4513-884X" in letter, "cover letter lost its ORCID")
    check(
        "International Journal of Lexicography" in letter,
        "cover letter does not name the target venue",
    )

# 4. Figures claimed absent in the checklist must really be absent (alt-text rule).
if MANUSCRIPT.exists():
    check(
        "![" not in manuscript,
        "manuscript now contains an image; IJL alt text becomes mandatory "
        "(checklist item 7 says 'no figures')",
    )

# 5. The checklist must not silently re-open the two References defects fixed in H825.
if MANUSCRIPT.exists():
    check(
        "Artstein" in manuscript,
        "Artstein & Poesio reference vanished (H825 fixed this; do not regress)",
    )
    # The string survives in the audit notes that DOCUMENT the removal, so match on a
    # live References bullet rather than anywhere in the file.
    live_iscls_2026 = [
        line
        for line in manuscript.splitlines()
        if line.lstrip().startswith("- ISCLS (2026)")
    ]
    check(
        not live_iscls_2026,
        "the unverifiable ISCLS (2026) citation is back as a live reference; "
        "H825 removed it",
    )
    check(
        "Removed 12-07-2026" in manuscript,
        "the note recording the ISCLS (2026) removal is gone",
    )

if failures:
    print("FAIL — A44 pack selftest")
    for item in failures:
        print(f"  - {item}")
    sys.exit(1)

print(f"PASS — A44 pack selftest ({len(PACK)} pack files verified)")
sys.exit(0)
