#!/usr/bin/env python3
"""triage_synthesize.py -- body-grounded review queue for a dictionary's tier-A
correction candidates.

The decisive evidence is the dictionary's OWN entry body (attached by triage_bodies.py):
a spelling-only detector cannot tell a typo from a real word, an intentional variant /
compounding form, or wrong-reading apparatus -- but the entry text can. This combines:

  - body_kind (deterministic, triage_bodies.py): wr / variant / xref = MW documents the
    spelling on purpose (NEVER file); missing = not in current source (unlocatable).
  - body-aware LLM classification (triage_work/body_adj_*.json) over the `realword` set:
    TYPO (gloss fits the suggestion, key misspelled) vs REALWORD (gloss fits the suspect,
    a distinct word) vs INTENTIONAL vs UNSURE.
  - source confirmation (triage_work/body_conf_*.json): each TYPO re-checked against the
    FULL csl-orig entry.

Buckets (best-first):
  1 FILE-FIRST   TYPO classified AND source-confirmed -> verify on the scan, then file
  2 TYPO-UNSURE  classified TYPO but source-confirm refuted -> needs eyes
  3 REVIEW       UNSURE / homograph -> undecidable without the page
  4 REAL-WORD    a distinct real word -> the "fix" would merge two words; do NOT file
  5 INTENTIONAL  MW documents the spelling (w.r./v.l./in-comp./xref) -> NEVER file
  6 UNLOCATABLE  not in the current MW source (stale sanhw1 / different key)

Usage:  cd detectors && python triage_synthesize.py [MW]
"""
import sys
import os
import re
import json
import glob

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import triage_lang
import triage_util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCAN = ("http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/"
        "servepdf.php?dict=%s&key=%s")
_CONF = {'high': 3, 'medium': 2, 'low': 1}


def main():
    dict_code = sys.argv[1] if len(sys.argv) > 1 else 'MW'
    pkg = os.path.join(ROOT, 'corrections_draft', dict_code)
    work = os.path.join(pkg, 'triage_work')

    ev = {}
    with open(os.path.join(pkg, '%s_evidence.jsonl' % dict_code), encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            ev[r['suspect']] = r
    bcls = triage_util.load_verdicts(work, 'body_adj_*.json')
    bconf = triage_util.load_verdicts(work, 'body_conf_*.json')
    brev = triage_util.load_verdicts(work, 'body_review_*.json')  # Opus false-positive gate

    buckets = {k: [] for k in ('FILE', 'TYPO_UNSURE', 'REVIEW', 'REALWORD', 'INTENTIONAL', 'UNLOCATABLE')}
    for s, e in ev.items():
        bk = e['body_kind']
        c = bcls.get(s)
        e = dict(e, _cls=c, _conf=bconf.get(s), _rev=brev.get(s))
        if bk == 'missing':
            buckets['UNLOCATABLE'].append(e)
        elif bk in ('wr', 'variant', 'xref'):
            buckets['INTENTIONAL'].append(e)
        elif c is None:
            buckets['REVIEW'].append(e)          # realword set but no body verdict -> eyes
        elif c['label'] == 'TYPO':
            cf, rv = e['_conf'], e['_rev']
            # FILE only if source-confirmed AND it survives the Opus false-positive review
            survives = (cf and cf.get('is_typo')) and (rv is None or rv.get('fileable'))
            buckets['FILE' if survives else 'TYPO_UNSURE'].append(e)
        elif c['label'] == 'REALWORD':
            buckets['REALWORD'].append(e)
        elif c['label'] == 'INTENTIONAL':
            buckets['INTENTIONAL'].append(e)
        else:
            buckets['REVIEW'].append(e)

    # fail-loud: a confirmed typo with no Opus review verdict means the false-positive gate did
    # not run for it (missing/unloadable body_review_*.json). Don't silently file it -- warn.
    unreviewed = [e for e in buckets['FILE'] if e.get('_rev') is None]
    if unreviewed:
        sys.stderr.write("  WARNING: %d FILE-FIRST candidate(s) have NO Opus review verdict -- the "
                         "false-positive gate was not applied to them%s; re-run the workflow's Review "
                         "phase (body_review_*.json) before filing.\n"
                         % (len(unreviewed), " (no body_review files found)" if not brev else ""))

    def conf_rank(e):
        c = e.get('_cls') or {}
        return (_CONF.get(c.get('confidence'), 0), e['dcs_sugg_band'], e['confusion_weight'])
    for k in buckets:
        buckets[k].sort(key=conf_rank, reverse=True)

    out = os.path.join(pkg, '%s_triaged.txt' % dict_code)
    with open(out, 'w', encoding='utf-8') as f:
        w = f.write
        nfile = len(buckets['FILE'])
        w("# %s tier-A -- BODY-GROUNDED triage  (DRAFT; verify every kept case against the scan)\n#\n" % dict_code)
        w("# The %d engine tier-A candidates were judged against MW's OWN entry text (csl-orig),\n" % len(ev))
        w("# not spelling alone. A spelling detector cannot tell a typo from a real word, an\n")
        w("# intentional variant / compounding form, or wrong-reading apparatus -- the entry can.\n")
        w("# Pipeline: deterministic body classification (triage_bodies.py) + a body-aware LLM\n")
        w("# pass over the 'realword' set + source confirmation of every TYPO verdict.\n#\n")
        w("# FINDING: of %d tier-A candidates, %d are body-confirmed fileable typos (%.1f%%).\n"
          % (len(ev), nfile, 100 * nfile / len(ev)))
        w("# %d are real distinct words, %d are spellings MW documents on purpose (w.r./v.l./\n"
          % (len(buckets['REALWORD']), len(buckets['INTENTIONAL'])))
        w("# in-comp./cross-ref -- filing them would CORRUPT MW), %d are not in the current\n"
          % len(buckets['UNLOCATABLE']))
        w("# source, and %d need eyes. 'Tier A' is high ENGINE confidence, NOT precision:\n"
          % (len(buckets['REVIEW']) + len(buckets['TYPO_UNSURE'])))
        w("# do NOT bulk-apply it. Start with bucket 1; a human confirms each on the scan.\n")

        def block(title, rows, detailed):
            w("\n# ===== %s (%d) =====\n" % (title, len(rows)))
            for e in rows:
                c, cf = e.get('_cls') or {}, e.get('_conf')
                head = "%-13s -> %-13s" % (e['suspect'], e['suggestion'])
                if detailed:
                    w("\n%s  [dcs=%d ndicts=%d body=%s%s]\n" % (
                        head, e['dcs_sugg_band'], e['ndicts'], e['body_kind'],
                        ' x%d' % e['body_count'] if e['body_count'] > 1 else ''))
                    if e['body_text']:
                        w("    %s: %s\n" % (dict_code, e['body_text'][:200]))
                    if c.get('reason'):
                        w("    judged: %s\n" % c['reason'])
                    if cf and cf.get('reason'):
                        w("    confirm: %s\n" % cf['reason'])
                    w("    scan: %s\n" % (SCAN % (dict_code, e['suspect'])))
                else:
                    note = (c.get('reason') or '')
                    w("%s | %s: %s | %s\n" % (head, dict_code, (e['body_text'] or '')[:90], note[:90]))
        block("BUCKET 1  FILE-FIRST -- body-confirmed typo (verify on scan, then file)", buckets['FILE'], True)
        block("BUCKET 2  TYPO-UNSURE -- classified typo but source-confirm refuted", buckets['TYPO_UNSURE'], True)
        block("BUCKET 3  REVIEW -- undecidable without the printed page", buckets['REVIEW'], True)
        block("BUCKET 4  REAL-WORD -- a distinct real word; the fix would merge two words", buckets['REALWORD'], False)
        block("BUCKET 5  INTENTIONAL -- MW documents the spelling on purpose; NEVER file", buckets['INTENTIONAL'], False)
        block("BUCKET 6  UNLOCATABLE -- not in the current MW source (stale/different key)", buckets['UNLOCATABLE'], False)

    sf = os.path.join(pkg, '%s_file_first_sf.txt' % dict_code)
    with open(sf, 'w', encoding='utf-8') as f:
        revout = [e for e in buckets['TYPO_UNSURE'] if e.get('_rev') and not e['_rev'].get('fileable')]
        f.write("; %s body-confirmed fileable typos -- CORRECTIONS standard format (DICT:wrong:right:n)\n" % dict_code)
        f.write("; %d fileable (classified TYPO + source-confirmed + survived the Opus false-positive review)" % len(buckets['FILE']))
        f.write((" + %d reviewed-out (commented below)\n" % len(revout)) if revout else "\n")
        f.write("; VERIFY each remaining case on the scan, flip trailing n->y for confirmed ones, then:\n")
        f.write(";   python chg_nchg_sep.py %s_file_first_sf.txt chg.txt nchg.txt\n" % dict_code)
        for e in buckets['FILE']:
            f.write("%s:%s:%s:n\n" % (dict_code, e['suspect'], e['suggestion']))
        for e in revout:   # auto-curated: the Opus review judged these intentional, not typos
            r = e['_rev']
            f.write("; REVIEWED-OUT (%s): %s\n;%s:%s:%s:n\n"
                    % (r.get('false_positive_type', '?'), (r.get('reason', '') or '')[:120],
                       dict_code, e['suspect'], e['suggestion']))

    # ---- the standing wrong-readings / do-not-file list -----------------
    # Every documented-intentional spelling MW carries on purpose: filing a
    # "correction" for any of these CORRUPTS the dictionary. Kept as a per-dict
    # reference so future runs (and humans) never re-flag them. Grouped by sub-type.
    from collections import defaultdict
    groups = defaultdict(list)
    for e in buckets['INTENTIONAL']:
        groups[triage_lang.subtype(e['body_text'], dict_code)].append(e)
    wr = os.path.join(pkg, '%s_wrong_readings.txt' % dict_code)
    order_sub = ['wrong-reading', 'varia-lectio', 'in-composition', 'cross-reference', 'other-intentional']
    with open(wr, 'w', encoding='utf-8') as f:
        f.write("# %s -- DOCUMENTED-INTENTIONAL spellings (NOT typos -- do NOT file corrections)\n#\n" % dict_code)
        f.write("# %d headwords that LOOK like misspellings but which %s records on purpose:\n"
                % (len(buckets['INTENTIONAL']), dict_code))
        f.write("# wrong-reading apparatus (w.r.), variae lectiones (v.l.), in-composition /\n")
        f.write("# sandhi forms (in comp. for...), cross-references (See / = X q.v.), and other\n")
        f.write("# grammatical/Vedic notes. Filing a 'correction' for any of these CORRUPTS %s.\n" % dict_code)
        f.write("# Use this as a suppression list: such headwords should not be re-flagged.\n")
        f.write("# Format per row:  headword -> would-be 'correction'  |  the %s entry text\n" % dict_code)
        for sub in order_sub:
            rows = sorted(groups.get(sub, []), key=lambda e: e['suspect'])
            if not rows:
                continue
            f.write("\n# ===== %s (%d) =====\n" % (sub.upper(), len(rows)))
            for e in rows:
                f.write("%-14s -> %-14s | %s\n" % (e['suspect'], e['suggestion'], (e['body_text'] or '')[:160]))

    print("triaged %d candidates -> %s" % (len(ev), os.path.relpath(out, ROOT)))
    order = [('FILE-FIRST', 'FILE'), ('TYPO-UNSURE', 'TYPO_UNSURE'), ('REVIEW', 'REVIEW'),
             ('REAL-WORD', 'REALWORD'), ('INTENTIONAL', 'INTENTIONAL'), ('UNLOCATABLE', 'UNLOCATABLE')]
    for name, k in order:
        print("  %-12s %5d" % (name, len(buckets[k])))
    print("  -> %s (%d rows)" % (os.path.relpath(sf, ROOT), len(buckets['FILE'])))
    print("  -> %s (%d documented-intentional, by sub-type: %s)" % (
        os.path.relpath(wr, ROOT), len(buckets['INTENTIONAL']),
        ', '.join('%s=%d' % (s, len(groups[s])) for s in order_sub if groups.get(s))))


if __name__ == '__main__':
    main()
