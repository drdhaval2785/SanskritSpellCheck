#!/usr/bin/env python3
"""append_netnew_to_queues.py -- put the verified net-new rows into the per-dict FILE-FIRST
queues so a scan-verification vote on them can actually be applied.

The gap this closes: the scan sheet is generated from file_first_verified.tsv, but
apply_scanverify_decisions.py flips ':n' -> ':y' in corrections_draft/<DICT>/<DICT>_file_first_sf.txt.
The net-new rows from the union passes (D7/H1471, D9/H1709) were verified into the former and
never existed in the latter, so approving one had nothing to flip -- the vote would be
reported 'missing' and lost. A 182-row sheet whose votes only land for 109 rows is worse than
a 109-row sheet, because the loss is invisible at voting time.

APPEND-ONLY BY CONSTRUCTION. Existing rows are never rewritten, reordered or re-flagged --
this is exactly the guardrail the union passes exist to honour ("union, never overwrite":
triage_synthesize.py would have replaced these files and destroyed run 1's finds). Rows are
added with the trailing ':n', so nothing becomes fileable without the human scan vote; the
H454 gate stays closed until a human votes.

EDITORIAL rows are deliberately NOT appended. They are not plain corrections -- the corrected
spelling already exists as its own <k1>, so a silent respell would create a duplicate headword.
They stay editor decisions, which is the entire point of the class.

    cd corrections_draft
    python append_netnew_to_queues.py            # dry run
    python append_netnew_to_queues.py --apply
"""
import argparse
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFIED = os.path.join(HERE, 'file_first_verified.tsv')
WORKLIST = os.path.join(HERE, 'netnew_worklist.tsv')
QUEUEABLE = ('PASS', 'SCAN-FIRST')
MARKER = '; --- net-new from the union-across-runs passes (D7/H1471 + D9/H1709), verified'


def load_netnew_keys():
    """(dict, wrong) of every row that came from a union pass -- i.e. is not run-1."""
    keys = set()
    with open(WORKLIST, encoding='utf-8') as f:
        header = f.readline().rstrip('\n').split('\t')
        di, wi = header.index('dict'), header.index('wrong')
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) > max(di, wi):
                keys.add((p[di], p[wi]))
    return keys


def load_verified():
    rows = []
    with open(VERIFIED, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) < 4 or p[0] == 'dict':
                continue
            rows.append({'dict': p[0], 'wrong': p[1], 'right': p[2], 'verdict': p[3]})
    return rows


def queue_path(dictcode):
    return os.path.join(HERE, dictcode, '%s_file_first_sf.txt' % dictcode)


def existing_keys(path):
    """Every wrong-headword already present, INCLUDING commented-out rows -- a row that was
    deliberately commented out must not be resurrected by an append."""
    keys = set()
    if not os.path.exists(path):
        return keys
    with open(path, encoding='utf-8') as f:
        for line in f:
            s = line.strip().lstrip(';').strip()
            parts = s.split(':')
            if len(parts) >= 3:
                keys.add(parts[1])
    return keys


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--date', default='04-08-2026', help='provenance date for the marker line')
    args = ap.parse_args()

    netnew = load_netnew_keys()
    rows = [r for r in load_verified()
            if (r['dict'], r['wrong']) in netnew and r['verdict'] in QUEUEABLE]
    skipped = [r for r in load_verified()
               if (r['dict'], r['wrong']) in netnew and r['verdict'] not in QUEUEABLE]

    by_dict = {}
    for r in rows:
        by_dict.setdefault(r['dict'], []).append(r)

    total_new, total_dup = 0, 0
    for d in sorted(by_dict):
        path = queue_path(d)
        if not os.path.exists(path):
            print('  %-5s NO QUEUE FILE at %s — skipping %d row(s)' % (d, path, len(by_dict[d])))
            continue
        have = existing_keys(path)
        fresh = [r for r in by_dict[d] if r['wrong'] not in have]
        dup = len(by_dict[d]) - len(fresh)
        total_new += len(fresh)
        total_dup += dup
        print('  %-5s +%2d row(s)%s' % (d, len(fresh), '  (%d already present)' % dup if dup else ''))
        if not args.apply or not fresh:
            continue
        with open(path, 'a', encoding='utf-8', newline='\n') as f:
            f.write('%s %s. Verified: Sonnet 5 (claude-sonnet-5) check vs the entry text,\n'
                    % (MARKER, args.date))
            f.write(';     Fable 5 (claude-fable-5) adjudication of flags. Evidence per row in\n')
            f.write(';     file_first_verified.tsv; EDITORIAL rows deliberately excluded (they are\n')
            f.write(';     headword collisions, not plain corrections). All ":n" — vote the scan sheet.\n')
            for r in sorted(fresh, key=lambda x: x['wrong']):
                f.write('%s:%s:%s:n\n' % (r['dict'], r['wrong'], r['right']))

    print('%s %d row(s) across %d dict(s)%s'
          % ('appended' if args.apply else 'would append', total_new, len(by_dict),
             '; %d already present' % total_dup if total_dup else ''))
    if skipped:
        print('excluded %d non-queueable row(s) (correct — these are editor decisions):' % len(skipped))
        for r in skipped:
            print('  %-5s %s -> %s  [%s]' % (r['dict'], r['wrong'], r['right'], r['verdict']))
    if not args.apply:
        print('(dry run — pass --apply)')


if __name__ == '__main__':
    main()
