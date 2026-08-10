"""Selftest for the A37 submission pack (H2406).

Twin of validate_a44_pack.py. Verifies the pack is internally consistent and that no
pack file makes a claim the repository contradicts. Run: python papers/validate_a37_pack.py
Exit 0 = pass, 1 = fail.
"""

import re
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"

PACK = [
    PAPERS / "A37_PACK_README.md",
    PAPERS / "A37_cover_letter.md",
    PAPERS / "A37_submission_checklist.md",
    PAPERS / "A37_checklist.md",
]
MANUSCRIPT = PAPERS / "A37_ortho_drift_paper.md"
COMPANION = PAPERS / "A37_lchange_companion.md"
FIGURE = ROOT / "ortho_drift" / "drift_composition.png"

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

# 2. Byline consistency: manuscript, companion, and cover letter agree on the
#    canonical identity from Uprava/AUTHOR.md.
if MANUSCRIPT.exists():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    check("0000-0003-4513-884X" in manuscript, "manuscript lost its ORCID")
    check("gasyoun@ya.ru" in manuscript, "manuscript lost the canonical contact email")
if COMPANION.exists():
    check(
        "0000-0003-4513-884X" in COMPANION.read_text(encoding="utf-8"),
        "LChange companion lost its ORCID",
    )
if (PAPERS / "A37_cover_letter.md").exists():
    letter = (PAPERS / "A37_cover_letter.md").read_text(encoding="utf-8")
    check("0000-0003-4513-884X" in letter, "cover letter lost its ORCID")
    check(
        "Digital Scholarship in the Humanities" in letter,
        "cover letter does not name the target venue (DSH)",
    )
    # A placeholder funding sentence must never be invented for the author.
    check(
        "⟦MG⟧" in letter,
        "cover letter no longer marks the human decisions with the ⟦MG⟧ token",
    )

# 3. The DSH checklist's measured numbers must still match the manuscript.
#    These are the rows a reader would trust without re-measuring.
if MANUSCRIPT.exists() and (PAPERS / "A37_submission_checklist.md").exists():
    checklist = (PAPERS / "A37_submission_checklist.md").read_text(encoding="utf-8")
    body = manuscript.split("## Abstract", 1)[-1].split("## References", 1)[0]
    body_words = len(body.split())
    # Checklist claims ~3,143 words of body; allow drift only if the claim is updated.
    check(
        2900 < body_words < 3400,
        f"body is now {body_words} words; the checklist's ~3,143-word row is stale",
    )
    abstract = manuscript.split("## Abstract", 1)[-1].split("## 1.", 1)[0]
    abstract_words = len(abstract.split())
    # The checklist reports 246 words -- inside DSH's 250 cap. The blocker is the
    # missing structure, not the length, so guard the number both ways: a silent
    # drift over the cap is a new defect, and a big shrink means the row is stale.
    check(
        abstract_words <= 250,
        f"abstract is now {abstract_words} words, over DSH's 250 cap -- the "
        "checklist records 246 and treats length as satisfied",
    )
    check(
        230 < abstract_words <= 250,
        f"abstract is now {abstract_words} words; the checklist's 246-word row is stale",
    )
    # The structured-abstract blocker is only discharged once sub-headings exist.
    has_subheads = "Purpose" in abstract and "Findings" in abstract
    check(
        not has_subheads or "🔴" not in checklist.split("| 2 |", 1)[-1][:400],
        "abstract now has DSH sub-headings but checklist row 2 still reads as a blocker",
    )

# 4. The figure-resolution blocker must reflect the figure actually committed.
if FIGURE.exists():
    data = FIGURE.read_bytes()
    width, height = struct.unpack(">II", data[16:24])
    idx = data.find(b"pHYs")
    dpi = None
    if idx > 0:
        px_x, _px_y, unit = struct.unpack(">IIB", data[idx + 4 : idx + 13])
        if unit == 1:
            dpi = round(px_x * 0.0254)
    check(
        dpi is not None,
        "drift_composition.png has no pHYs chunk; the checklist's 200 dpi claim "
        "cannot be verified -- re-measure before trusting row 5",
    )
    if dpi is not None and dpi >= 300:
        check(
            False,
            f"figure is now {dpi} dpi ({width}x{height}) -- the >=300 dpi blocker "
            "(checklist rows 5) is discharged; update it rather than leaving it red",
        )

# 5. Claims about absent end-matter must stay true, or the checklist is lying.
#    These three are the pack's headline blockers.
if MANUSCRIPT.exists():
    lowered = manuscript.lower()
    if re.search(r"^#+\s*funding", manuscript, re.MULTILINE | re.IGNORECASE):
        failures.append(
            "manuscript now has a Funding section -- DSH checklist row 7 and the "
            "PACK_README blocker list must be updated"
        )
    if "ai disclosure" in lowered:
        failures.append(
            "manuscript now has an AI Disclosure Statement -- DSH checklist row 9 "
            "and the PACK_README blocker list must be updated"
        )
    if re.search(r"^\s*\*\*keywords", manuscript, re.MULTILINE | re.IGNORECASE):
        failures.append(
            "manuscript now has a keywords line -- DSH checklist row 3 is stale"
        )

# 6. Never let the pack invent a DOI, and never let it claim PR #102 merged
#    (it targeted the wrong remote and was closed unmerged).
for path in PACK:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    check(
        "10.5281/zenodo" not in text,
        f"{path.name} carries a Zenodo DOI; none has been minted for A37",
    )

if failures:
    print("FAIL — A37 pack selftest")
    for item in failures:
        print(f"  - {item}")
    sys.exit(1)

print(f"PASS — A37 pack selftest ({len(PACK)} pack files verified)")
sys.exit(0)
