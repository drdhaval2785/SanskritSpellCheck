"""irr_build_inputs.py  (Python 3)  -- H453 step 1: blind second-annotator inputs.

Reads corrections_draft/file_first_verified.tsv (the committed FILE-FIRST artifact)
and emits corrections_draft/irr/irr_inputs.tsv with ONLY the evidence a blind second
annotator may see: dict code, candidate headword ("wrong"), proposed correction
("right"), and the dictionary's own entry text for the candidate headword (csl-orig
via triage_util.build_entry_index) -- NO verdicts, NO notes, NO tier labels.

Usage:  python detectors/irr_build_inputs.py
Output: corrections_draft/irr/irr_inputs.tsv  (tab-separated; entry text has tabs/
        newlines flattened to spaces)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import triage_util  # noqa: E402

SRC = os.path.join(ROOT, 'corrections_draft', 'file_first_verified.tsv')
OUT_DIR = os.path.join(ROOT, 'corrections_draft', 'irr')
OUT = os.path.join(OUT_DIR, 'irr_inputs.tsv')


def flatten(text, limit=4000):
    t = ' '.join(text.split())
    return t[:limit] + (' [...TRUNCATED]' if len(t) > limit else '')


def main():
    rows = []
    with open(SRC, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.rstrip('\n').split('\t')
            if parts[0] == 'dict':
                continue
            rows.append(parts[:3])  # dict, wrong, right -- verdict/note deliberately dropped

    idx_cache = {}
    csl = triage_util.csl_root()
    os.makedirs(OUT_DIR, exist_ok=True)
    missing = 0
    with open(OUT, 'w', encoding='utf-8', newline='\n') as out:
        out.write('row_id\tdict\twrong\tright\twrong_entry_text\tright_entry_text\n')
        for i, (dct, wrong, right) in enumerate(rows, 1):
            if dct not in idx_cache:
                idx_cache[dct] = triage_util.build_entry_index(csl, dct)
            idx = idx_cache[dct]
            bodies = idx.bodies(wrong) if idx else []
            if not bodies:
                missing += 1
                body = '[NO ENTRY FOUND under this headword in the current source]'
            else:
                body = ' ||| '.join(flatten(b) for b in bodies[:3])
            rbodies = idx.bodies(right) if idx else []
            rbody = (' ||| '.join(flatten(b) for b in rbodies[:3])
                     if rbodies else '[no separate entry under this headword]')
            out.write('%03d\t%s\t%s\t%s\t%s\t%s\n' % (i, dct, wrong, right, body, rbody))
    print('%d rows -> %s (%d without a body)' % (len(rows), OUT, missing))


if __name__ == '__main__':
    main()
