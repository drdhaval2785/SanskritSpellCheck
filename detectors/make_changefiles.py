"""make_changefiles.py  (Python 3)  -- Phase 2.5: submission-prep (human-approved)

Turn accepted corrections (the review UI's exported accepted_sf.txt, or any
DICT:wrong:right[:y] file) into per-dictionary DRAFT change-files matching the
CORRECTIONS convention (dictionaries/<DICT>/issue-N/corrections.txt): a `;`-commented
case block per correction, with the source line located in the csl-orig dict file and
a proposed `old`/`new` updateByLine pair editing the headword key field.

This is PREP, not submission: it never edits dictionary source, never opens an issue,
and every `new` line is a DRAFT a human must verify against the scan before filing
(the Cologne maintainers are sensitive to bot noise). Headword occurrences inside the
entry BODY are not touched — only the <k1>/<k2> key field — so flag those for the human.

H454 / ruling D3 guard (load-bearing): FILE-FIRST queue rows carry a trailing
`:n` / `:y` scan-verification flag. Rows still marked `:n` are NEVER emitted as
change-file cases. Bare `DICT:wrong:right` lines (accepted_sf export without a
flag) remain accepted — they are already the human-approved export form.

  python make_changefiles.py [accepted_sf.txt] [csl-orig-root=../../csl-orig] [outdir=changefiles]
"""
import sys
import os
import re
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import triage_util

u.reconfigure_stdio()
SCAN = triage_util.SCAN_URL


def corrected(line, wrong, right):
    # fix the headword in BOTH key fields where the field value equals `wrong`
    for kf in ('k1', 'k2'):
        line = re.sub('(<%s>)%s(?=<|$)' % (kf, re.escape(wrong)),
                      lambda m: m.group(1) + right, line, count=1)
    return line


def _accepted_row(parts):
    """Return (dict, wrong, right) if this row may enter a change file, else None.

    Formats:
      DICT:wrong:right        — accepted export (no flag) → include
      DICT:wrong:right:y      — scan-verified approve → include
      DICT:wrong:right:n      — not yet scan-verified → skip
      DICT:wrong:right:<other> — unknown flag → skip (fail closed)
    """
    if len(parts) < 3 or not parts[0].isalnum() or parts[1] == parts[2]:
        return None
    if len(parts) >= 4:
        flag = parts[3].strip().lower()
        if flag != 'y':
            return None
    return (parts[0], parts[1], parts[2])


def main(infile, csl_root, outdir):
    by_dict = collections.defaultdict(list)   # DICT -> [(wrong, right)]
    seen = set()
    skipped_n = 0
    skipped_other_flag = 0
    for line in u._read_words(infile):
        # skip sf comment lines (the file_first_sf header + the auto-commented
        # "; REVIEWED-OUT ..." annotations); a real row is DICT:wrong:right:n with an
        # alphanumeric dict code, so guard p[0] to avoid manufacturing junk "dicts".
        if line.startswith((';', '#')):
            continue
        p = line.split(':')
        if len(p) >= 4 and p[0].isalnum() and p[1] != p[2]:
            flag = p[3].strip().lower()
            if flag == 'n':
                skipped_n += 1
                continue
            if flag != 'y':
                skipped_other_flag += 1
                continue
        row = _accepted_row(p)
        if row is None:
            continue
        key = row
        if key not in seen:
            seen.add(key)
            by_dict[row[0]].append((row[1], row[2]))

    if skipped_n or skipped_other_flag:
        print("gate: skipped %d :n row(s) (not scan-verified)%s" % (
            skipped_n,
            ('; %d other-flag row(s)' % skipped_other_flag) if skipped_other_flag else ''))

    if not by_dict:
        print("total: 0 corrections across 0 dicts "
              "(no approved rows — flip scan-verify votes n→y first, H454 gate)")
        return

    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), outdir), exist_ok=True)
    manifest = []
    for dictcode in sorted(by_dict):
        idx = triage_util.build_entry_index(csl_root, dictcode)
        located = 0
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), outdir, "%s_draft.txt" % dictcode)
        with open(out, 'w', encoding='utf-8') as f:
            f.write("; DRAFT corrections for %s — SanskritSpellCheck; VERIFY each against the scan before filing.\n" % dictcode)
            f.write("; updateByLine format; only the <k1>/<k2> key field is edited (check the entry body too).\n")
            f.write("; NOTE: each case targets the FIRST entry with that headword -- check for homographs\n")
            f.write(";       (multiple entries sharing a key) and that no two cases edit the same line.\n;\n")
            for n, (wrong, right) in enumerate(by_dict[dictcode], 1):
                f.write("; Case %d.  %s -> %s   scan=%s\n" % (n, wrong, right, SCAN % (dictcode, wrong)))
                e = idx.first(wrong) if idx else None   # first entry under k1 (or k2)
                if e:
                    lineno, src = e['lineno'], e['line']
                    f.write("%d old %s\n" % (lineno, src))
                    f.write("%d new %s\n;\n" % (lineno, corrected(src, wrong, right)))
                    located += 1
                else:
                    f.write(";   [NOT LOCATED in csl-orig — locate the entry manually]\n;\n")
        manifest.append((dictcode, len(by_dict[dictcode]), located, os.path.basename(out)))

    print("dict   corrections  located  file")
    for d, total, loc, fn in manifest:
        print("  %-6s %5d       %5d    %s" % (d, total, loc, "changefiles/" + fn))
    print("total: %d corrections across %d dicts" % (sum(m[1] for m in manifest), len(manifest)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    infile = args[0] if args else "accepted_sf.txt"
    csl_root = args[1] if len(args) > 1 else triage_util.csl_root()
    outdir = args[2] if len(args) > 2 else "changefiles"
    if not os.path.exists(infile):
        print("input %s not found — export accepted rows from combined_review.html first "
              "(or pass combined_sf.txt to dry-run)." % infile)
        sys.exit(1)
    main(infile, csl_root, outdir)
