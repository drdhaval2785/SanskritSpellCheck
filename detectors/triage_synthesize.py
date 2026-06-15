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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCAN = ("http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/"
        "servepdf.php?dict=%s&key=%s")
_CONF = {'high': 3, 'medium': 2, 'low': 1}


def load_dir(pattern):
    out = {}
    for p in sorted(glob.glob(pattern)):
        try:
            t = open(p, encoding='utf-8').read().strip()
            if t.startswith('```'):
                t = t.split('```')[1].lstrip('json').strip()
            try:
                data = json.loads(t)
            except json.JSONDecodeError:
                m = re.search(r'\[.*\]', t, re.S)
                data = json.loads(m.group(0)) if m else []
            for v in data:
                out[v['suspect']] = v
        except Exception as e:
            print("  WARN: %s: %s" % (os.path.basename(p), str(e)[:60]))
    return out


def main():
    dict_code = sys.argv[1] if len(sys.argv) > 1 else 'MW'
    pkg = os.path.join(ROOT, 'corrections_draft', dict_code)
    work = os.path.join(pkg, 'triage_work')

    ev = {}
    with open(os.path.join(pkg, '%s_evidence.jsonl' % dict_code), encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            ev[r['suspect']] = r
    bcls = load_dir(os.path.join(work, 'body_adj_*.json'))
    bconf = load_dir(os.path.join(work, 'body_conf_*.json'))

    buckets = {k: [] for k in ('FILE', 'TYPO_UNSURE', 'REVIEW', 'REALWORD', 'INTENTIONAL', 'UNLOCATABLE')}
    for s, e in ev.items():
        bk = e['body_kind']
        c = bcls.get(s)
        e = dict(e, _cls=c, _conf=bconf.get(s))
        if bk == 'missing':
            buckets['UNLOCATABLE'].append(e)
        elif bk in ('wr', 'variant', 'xref'):
            buckets['INTENTIONAL'].append(e)
        elif c is None:
            buckets['REVIEW'].append(e)          # realword set but no body verdict -> eyes
        elif c['label'] == 'TYPO':
            cf = bconf.get(s)
            buckets['FILE' if (cf and cf.get('is_typo')) else 'TYPO_UNSURE'].append(e)
        elif c['label'] == 'REALWORD':
            buckets['REALWORD'].append(e)
        elif c['label'] == 'INTENTIONAL':
            buckets['INTENTIONAL'].append(e)
        else:
            buckets['REVIEW'].append(e)

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
                        w("    MW: %s\n" % e['body_text'][:200])
                    if c.get('reason'):
                        w("    judged: %s\n" % c['reason'])
                    if cf and cf.get('reason'):
                        w("    confirm: %s\n" % cf['reason'])
                    w("    scan: %s\n" % (SCAN % (dict_code, e['suspect'])))
                else:
                    note = (c.get('reason') or '')
                    w("%s | MW: %s | %s\n" % (head, (e['body_text'] or '')[:90], note[:90]))
        block("BUCKET 1  FILE-FIRST -- body-confirmed typo (verify on scan, then file)", buckets['FILE'], True)
        block("BUCKET 2  TYPO-UNSURE -- classified typo but source-confirm refuted", buckets['TYPO_UNSURE'], True)
        block("BUCKET 3  REVIEW -- undecidable without the printed page", buckets['REVIEW'], True)
        block("BUCKET 4  REAL-WORD -- a distinct real word; the fix would merge two words", buckets['REALWORD'], False)
        block("BUCKET 5  INTENTIONAL -- MW documents the spelling on purpose; NEVER file", buckets['INTENTIONAL'], False)
        block("BUCKET 6  UNLOCATABLE -- not in the current MW source (stale/different key)", buckets['UNLOCATABLE'], False)

    sf = os.path.join(pkg, '%s_file_first_sf.txt' % dict_code)
    with open(sf, 'w', encoding='utf-8') as f:
        f.write("; %s body-confirmed fileable typos -- CORRECTIONS standard format (DICT:wrong:right:n)\n" % dict_code)
        f.write("; %d candidates: classified TYPO from MW's entry body AND source-confirmed.\n" % len(buckets['FILE']))
        f.write("; VERIFY each on the scan, flip trailing n->y for confirmed ones, then:\n")
        f.write(";   python chg_nchg_sep.py %s_file_first_sf.txt chg.txt nchg.txt\n" % dict_code)
        for e in buckets['FILE']:
            f.write("%s:%s:%s:n\n" % (dict_code, e['suspect'], e['suggestion']))

    print("triaged %d candidates -> %s" % (len(ev), os.path.relpath(out, ROOT)))
    order = [('FILE-FIRST', 'FILE'), ('TYPO-UNSURE', 'TYPO_UNSURE'), ('REVIEW', 'REVIEW'),
             ('REAL-WORD', 'REALWORD'), ('INTENTIONAL', 'INTENTIONAL'), ('UNLOCATABLE', 'UNLOCATABLE')]
    for name, k in order:
        print("  %-12s %5d" % (name, len(buckets[k])))
    print("  -> %s (%d rows)" % (os.path.relpath(sf, ROOT), len(buckets['FILE'])))


if __name__ == '__main__':
    main()
