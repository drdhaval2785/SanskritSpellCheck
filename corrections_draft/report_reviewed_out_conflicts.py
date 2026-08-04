#!/usr/bin/env python3
"""report_reviewed_out_conflicts.py -- list rows where run-1's review said DO-NOT-FILE but a
later pass says FILE.

These rows sit in <DICT>_file_first_sf.txt as COMMENTED-OUT ';DICT:wrong:right:n' lines: run-1's
Opus false-positive review ruled them not fileable. The union-across-runs passes re-found them
(union_across_runs.load_baseline skips comments, so a reviewed-out row counts as net-new) and the
H2274 verification pass assigned them PASS/SCAN-FIRST against the entry text.

That is a genuine editorial disagreement between two passes, NOT a plumbing gap, so nothing here
uncomments anything. The row stays reviewed-out; it appears in the scan sheet carrying the newer
verdict; and a human's vote is the arbiter. Note that approving one of these has no effect until
the row is activated -- apply_scanverify_decisions.py will report it as missing, which is the
intended, visible outcome rather than a silent flip.

    cd corrections_draft
    python report_reviewed_out_conflicts.py --out REVIEWED_OUT_VS_UNION_CONFLICTS.md
"""
import argparse
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import append_netnew_to_queues as A  # noqa: E402


def commented_keys(path):
    """wrong -> the raw commented line, for rows commented out of the queue."""
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s.startswith(';'):
                continue
            body = s.lstrip(';').strip()
            p = body.split(':')
            if len(p) >= 3 and p[0].isupper() and p[0].isalpha():
                out[p[1]] = body
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    netnew = A.load_netnew_keys()
    verified = {(r['dict'], r['wrong']): r for r in A.load_verified()}
    notes = {}
    with open(A.VERIFIED, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) >= 5 and p[0] != 'dict':
                notes[(p[0], p[1])] = p[4]

    conflicts = []
    for (d, w), r in sorted(verified.items()):
        if (d, w) not in netnew or r['verdict'] not in A.QUEUEABLE:
            continue
        com = commented_keys(A.queue_path(d))
        if w in com:
            conflicts.append((d, w, r['right'], r['verdict'], com[w], notes.get((d, w), '')))

    per = {}
    for c in conflicts:
        per[c[0]] = per.get(c[0], 0) + 1
    print('%d conflict row(s): %s' % (len(conflicts),
                                      ' · '.join('%s %d' % (k, per[k]) for k in sorted(per))))
    for d, w, right, verdict, com, _ in conflicts:
        print('  %-5s %-24s -> %-24s run2=%-10s run1=reviewed-out' % (d, w, right, verdict))

    if not args.out:
        return
    path = args.out if os.path.isabs(args.out) else os.path.join(HERE, args.out)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Reviewed-out vs union: %d rows two passes disagree about\n\n' % len(conflicts))
        f.write('_Created: 04-08-2026 · Last updated: 04-08-2026_\n\n')
        f.write('Run-1\'s Opus false-positive review ruled each of these **not fileable**, so it '
                'sits COMMENTED OUT in `<DICT>_file_first_sf.txt`. The union-across-runs passes '
                're-found it and the H2274 verification pass ruled it fileable against the '
                'entry\'s own text. Both judgements are recorded; neither has been silently '
                'overridden.\n\n')
        f.write('**Nothing here is activated.** The rows stay reviewed-out, they appear in the '
                'scan-verification sheet carrying the newer verdict, and a human\'s scan vote is '
                'the arbiter. Approving one has no effect until the row is uncommented — '
                '`apply_scanverify_decisions.py` reports it as missing, which is deliberate: a '
                'prior review decision should not be reversed by a silent flip.\n\n')
        f.write('Concentrated in **YAT**, whose b/v class was explicitly "held for scan" — '
                'exactly the population where the scan, not either pass, is the arbiter.\n\n')
        f.write('| dict | headword | proposed | H2274 verdict | run-1 | evidence |\n')
        f.write('|---|---|---|---|---|---|\n')
        for d, w, right, verdict, com, note in conflicts:
            f.write('| %s | `%s` | `%s` | **%s** | reviewed-out | %s |\n'
                    % (d, w, right, verdict, (note or '').replace('|', '\\|')[:180]))
        f.write('\n_Dr. Mārcis Gasūns_\n')
    print('wrote %s' % path)


if __name__ == '__main__':
    main()
