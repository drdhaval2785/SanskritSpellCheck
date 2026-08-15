#!/usr/bin/env python3
"""build_netnew_worklist.py -- collect the NET_NEW rows of the union tables into one
verification worklist, excluding anything already carrying a verdict.

The scan-verification sheet (detectors/gen_scanverify_sheet.py) is generated from
corrections_draft/file_first_verified.tsv, which holds only the RUN-1 population (122 rows).
The union-across-runs passes added net-new fileable candidates that are absent from it:
D7 (H1471, union_d7.tsv) and D9 (H1709, union_d9.tsv). Until those rows carry a verdict the
human gate covers only part of the queue.

This emits the worklist those rows need, with the Opus confirm/review evidence already
attached so the verification agents start from the triage's own reasoning rather than
re-deriving it.

    cd corrections_draft
    python build_netnew_worklist.py --out netnew_worklist.tsv
"""
import argparse
import csv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
UNIONS = [('D7', os.path.join(HERE, 'union_d7.tsv')),
          ('D9', os.path.join(HERE, 'union_d9.tsv'))]
VERIFIED = os.path.join(HERE, 'file_first_verified.tsv')


def load_verified_keys():
    """(dict, wrong) pairs that already carry a verdict -- never re-verify these."""
    keys = set()
    with open(VERIFIED, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if p[0] == 'dict' or len(p) < 4:
                continue
            keys.add((p[0], p[1]))
    return keys


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='netnew_worklist.tsv')
    args = ap.parse_args()

    verified = load_verified_keys()
    rows, skipped = [], 0
    for pass_id, path in UNIONS:
        if not os.path.exists(path):
            print('WARNING: %s missing -- skipping %s' % (path, pass_id))
            continue
        with open(path, encoding='utf-8') as f:
            for r in csv.DictReader(f, delimiter='\t'):
                if r.get('status') != 'NET_NEW':
                    continue
                key = (r['dict'], r['suspect'])
                if key in verified:
                    skipped += 1
                    continue
                rows.append({
                    'pass': pass_id,
                    'dict': r['dict'],
                    'wrong': r['suspect'],
                    'right': r['suggestion'],
                    'opus_confirm_reason': r.get('opus_confirm_reason', ''),
                    'opus_review': r.get('opus_review', ''),
                    'opus_review_reason': r.get('opus_review_reason', ''),
                })

    rows.sort(key=lambda x: (x['dict'], x['wrong']))
    out = args.out if os.path.isabs(args.out) else os.path.join(HERE, args.out)
    cols = ['pass', 'dict', 'wrong', 'right', 'opus_confirm_reason', 'opus_review',
            'opus_review_reason']
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

    per_dict = {}
    for r in rows:
        per_dict[r['dict']] = per_dict.get(r['dict'], 0) + 1
    print('wrote %s -- %d rows needing a verdict (%d already verified, skipped)'
          % (out, len(rows), skipped))
    for d in sorted(per_dict, key=lambda k: -per_dict[k]):
        print('  %-5s %3d' % (d, per_dict[d]))
    unrev = [r for r in rows if r['opus_review'] != 'fileable']
    if unrev:
        print('NOTE: %d row(s) carry no "fileable" review verdict -- flag for adjudication:'
              % len(unrev))
        for r in unrev:
            print('  %s %s -> %s (review=%s)' % (r['dict'], r['wrong'], r['right'],
                                                 r['opus_review'] or 'NONE'))


if __name__ == '__main__':
    main()
