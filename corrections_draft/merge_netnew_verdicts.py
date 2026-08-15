#!/usr/bin/env python3
"""merge_netnew_verdicts.py -- assemble the net-new verification verdicts and append them
to file_first_verified.tsv.

Reads from BOTH durable channels and unions them, because neither is complete on its own
(Uprava FINDINGS §303): an agent can write its verdict file and fail in the return channel,
OR return its verdicts and never write the file. Observed in this very pass -- 3 of 13 check
batches returned without writing, and 3 different batches failed to return across two runs.

  channel 1: <work>/verify_chk_*.json + verify_adj_*.json   (what agents wrote)
  channel 2: the workflow journal.jsonl `result` records    (what agents returned)

Check verdicts carry a `flag` field; adjudication verdicts do not -- that is the discriminator.
An adjudicated verdict always wins over the checker's, per the July-2026 division of labour.

COVERAGE IS ASSERTED, not assumed: every row of the worklist must end with a verdict, and any
row whose two channels disagree is reported rather than silently resolved. Exits non-zero if
either check fails, so an incomplete merge cannot look like a complete one.

    cd corrections_draft
    python merge_netnew_verdicts.py --journal <path-to-journal.jsonl> --apply
"""
import argparse
import csv
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'verify_work')
WORKLIST = os.path.join(HERE, 'netnew_worklist.tsv')
VERIFIED = os.path.join(HERE, 'file_first_verified.tsv')
VALID = {'PASS', 'SCAN-FIRST', 'EDITORIAL', 'DNF', 'DROP'}


def key(d, w):
    return (d, w)


def load_json_array(path):
    """Tolerate a ```json fence or trailing prose, as triage_util.load_json_array does."""
    t = open(path, encoding='utf-8').read().strip()
    if t.startswith('```'):
        t = t.split('```')[1]
        if t.lstrip().startswith('json'):
            t = t.lstrip()[4:]
    return json.loads(t.strip())


def collect_from_disk():
    checks, adjs = {}, {}
    for p in sorted(glob.glob(os.path.join(WORK, 'verify_chk_*.json'))):
        for v in load_json_array(p):
            checks.setdefault(key(v['dict'], v['wrong']), []).append(('disk:' + os.path.basename(p), v))
    for p in sorted(glob.glob(os.path.join(WORK, 'verify_adj_*.json'))):
        for v in load_json_array(p):
            adjs.setdefault(key(v['dict'], v['wrong']), []).append(('disk:' + os.path.basename(p), v))
    return checks, adjs


def collect_from_journal(path):
    checks, adjs = {}, {}
    if not path or not os.path.exists(path):
        return checks, adjs
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get('type') != 'result' or not isinstance(rec.get('result'), dict):
            continue
        for v in rec['result'].get('verdicts', []):
            if not isinstance(v, dict) or 'dict' not in v or 'wrong' not in v:
                continue
            bucket = checks if 'flag' in v else adjs
            bucket.setdefault(key(v['dict'], v['wrong']), []).append(
                ('journal:' + str(rec.get('agentId'))[:8], v))
    return checks, adjs


def merge(a, b):
    out = {k: list(vs) for k, vs in a.items()}
    for k, vs in b.items():
        out.setdefault(k, []).extend(vs)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--journal', nargs='*', default=[],
                    help='workflow journal.jsonl file(s) — the return channel. Pass one per '
                         'workflow run (checkers, adjudication, any resume): each run has its '
                         'own journal, and no single channel is complete (FINDINGS §303).')
    ap.add_argument('--apply', action='store_true', help='append rows to file_first_verified.tsv')
    args = ap.parse_args()

    with open(WORKLIST, encoding='utf-8') as f:
        worklist = list(csv.DictReader(f, delimiter='\t'))

    dchk, dadj = collect_from_disk()
    checks, adjs = dchk, dadj
    jtot_c, jtot_a = 0, 0
    for jp in args.journal:
        jchk, jadj = collect_from_journal(jp)
        jtot_c, jtot_a = jtot_c + len(jchk), jtot_a + len(jadj)
        checks, adjs = merge(checks, jchk), merge(adjs, jadj)
    print('channels: disk chk=%d adj=%d rows · %d journal(s) chk=%d adj=%d rows'
          % (len(dchk), len(dadj), len(args.journal), jtot_c, jtot_a))

    rows, missing, disagree, bad, unruled = [], [], [], [], []
    for r in worklist:
        k = key(r['dict'], r['wrong'])
        chosen, source = None, None
        if k in adjs:
            chosen, source = adjs[k][0][1], 'adjudicated'
        elif k in checks:
            chosen, source = checks[k][0][1], 'checker'
        if chosen is None:
            missing.append(r)
            continue
        # A row the checker FLAGGED must be ruled by the judge. Falling back to the
        # checker's own best guess is precisely what the July-2026 pass forbids: that
        # checker over-flags on morphological evidence and its guess on a flagged row
        # carries no authority. Treat an unruled flag as unresolved, not as a verdict.
        if source == 'checker' and any(v.get('flag') for _, v in checks.get(k, [])):
            why = next((v.get('flag_reason') for _, v in checks.get(k, []) if v.get('flag')), '')
            unruled.append((r, chosen['verdict'], why))
            continue
        seen = {v['verdict'] for _, v in checks.get(k, [])} | {v['verdict'] for _, v in adjs.get(k, [])}
        if len(seen) > 1:
            disagree.append((r, sorted(seen), chosen['verdict'], source))
        if chosen['verdict'] not in VALID:
            bad.append((r, chosen['verdict']))
            continue
        if chosen.get('right') and chosen['right'] != r['right']:
            disagree.append((r, ['right:%s' % chosen['right']], chosen['verdict'], source))
        rows.append({'dict': r['dict'], 'wrong': r['wrong'], 'right': r['right'],
                     'verdict': chosen['verdict'],
                     'note': (chosen.get('note') or '').replace('\t', ' ').replace('\n', ' '),
                     'source': source, 'pass': r['pass']})

    tally = {}
    for r in rows:
        tally[r['verdict']] = tally.get(r['verdict'], 0) + 1
    print('resolved %d/%d rows — %s' % (len(rows), len(worklist),
                                        ' · '.join('%s %d' % (k, tally[k]) for k in sorted(tally))))
    print('  adjudicated: %d · checker-only: %d'
          % (sum(1 for r in rows if r['source'] == 'adjudicated'),
             sum(1 for r in rows if r['source'] == 'checker')))
    per_pass = {}
    for r in rows:
        per_pass[r['pass']] = per_pass.get(r['pass'], 0) + 1
    print('  by union pass: %s' % (' · '.join('%s %d' % (k, per_pass[k]) for k in sorted(per_pass))))

    for r, seen, took, src in disagree:
        print('  DISAGREEMENT %s %s: channels=%s -> took %s (%s)'
              % (r['dict'], r['wrong'], seen, took, src))
    for r, v in bad:
        print('  INVALID VERDICT %s %s: %r' % (r['dict'], r['wrong'], v))
    for r in missing:
        print('  NO VERDICT %s %s -> %s' % (r['dict'], r['wrong'], r['right']))
    for r, guess, why in unruled:
        print('  FLAGGED, NEVER ADJUDICATED %s %s -> %s (checker guessed %s; unsure: %s)'
              % (r['dict'], r['wrong'], r['right'], guess, why[:100]))

    if missing or bad or unruled:
        print('REFUSING to apply: %d unresolved · %d invalid · %d flagged-but-unruled — '
              'resume the workflow so the judge rules those'
              % (len(missing), len(bad), len(unruled)))
        sys.exit(1)

    if not args.apply:
        print('(dry run — pass --apply to append to file_first_verified.tsv)')
        return

    existing = open(VERIFIED, encoding='utf-8').read()
    if not existing.endswith('\n'):
        existing += '\n'
    with open(VERIFIED, 'w', encoding='utf-8', newline='\n') as f:
        f.write(existing)
        f.write('# --- net-new FILE-FIRST rows from the union-across-runs passes, verified '
                '04-08-2026 (H2274). Mechanical verification: Sonnet 5 (claude-sonnet-5) against '
                'the entry text (locate/evidence/direction/collision); adjudication of flags: '
                'Fable 5 (claude-fable-5). Sources: union_d7.tsv (D7/H1471), union_d9.tsv (D9/H1709).\n')
        for r in sorted(rows, key=lambda x: (x['dict'], x['wrong'])):
            f.write('\t'.join([r['dict'], r['wrong'], r['right'], r['verdict'], r['note']]) + '\n')
    print('appended %d row(s) to %s' % (len(rows), VERIFIED))


if __name__ == '__main__':
    main()
