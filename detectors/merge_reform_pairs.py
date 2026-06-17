#!/usr/bin/env python3
"""merge_reform_pairs.py -- merge an EXTERNAL historical->modern pair file into a language's
orthographic reform map (`ortho_drift/<lang>_reform_map.tsv`), VALIDATED against the modern
Hunspell dic. The ingest format is the lowest common denominator for DTA/RIDGES exports,
WebFetch-harvested reform documentation, or hand-curated lists:

    old<TAB>new[<TAB>era]      ( '#' comment lines allowed )

A pair is accepted only if  old NOT in the modern dic  AND  new IN the modern dic  AND old!=new
-- the same transform-and-check guard ortho_drift.py uses, so hallucinations, dual-spellings and
rejected proposals are filtered out. DOCUMENTATION ONLY; never edits the dictionary sources.

    cd detectors && python merge_reform_pairs.py de ../ortho_drift/de_reform_web_candidates.tsv
"""
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortho_drift as od

od.triage_util.reconfigure_stdio()


def main():
    if len(sys.argv) < 3:
        print('usage: python merge_reform_pairs.py <lang> <pairs.tsv>')
        sys.exit(1)
    lang, infile = sys.argv[1], sys.argv[2]
    prof = od.PROFILES.get(lang)
    if prof is None:
        print('unknown lang %r (have %s)' % (lang, ', '.join(od.PROFILES)))
        sys.exit(1)
    modern = od.load_wordlist(prof)
    if modern is None:
        print('no modern wordlist for %s -- cannot validate external pairs; aborting' % lang)
        sys.exit(1)

    map_file = os.path.join(od.OUT, '%s_reform_map.tsv' % lang)
    rmap = od.load_reform_map(map_file, prof['seed'])
    before = len(rmap)
    accepted, rejected = [], []
    with open(infile, encoding='utf-8') as f:
        for ln in f:
            if ln.startswith('#') or '\t' not in ln:
                continue
            p = ln.rstrip('\n').split('\t')
            old, new = p[0].strip().lower(), p[1].strip().lower()
            era = p[2].strip() if len(p) > 2 and p[2].strip() else '1901'
            if old == new:
                rejected.append((old, new, 'same'))
            elif old in modern:
                rejected.append((old, new, 'old-in-dic'))
            elif new not in modern:
                rejected.append((old, new, 'new-not-in-dic'))
            elif old in rmap:
                rejected.append((old, new, 'already-mapped'))
            else:
                rmap[old] = (new, era)
                accepted.append((old, new, era))

    with open(map_file, 'w', encoding='utf-8') as f:
        f.write('# %s orthographic reform map:  old<TAB>2026<TAB>era\n' % prof['name'])
        f.write('# Curated seed + corpus-mined drift + dic-validated external pairs '
                '(DTA/RIDGES/web). %d forms.\n' % len(rmap))
        for o in sorted(rmap):
            n, e = rmap[o]
            f.write('%s\t%s\t%s\n' % (o, n, e))

    print('%s reform map: %d -> %d  (+%d accepted of %d input pairs)'
          % (lang, before, len(rmap), len(accepted), len(accepted) + len(rejected)))
    print('accepted: %s' % ', '.join('%s->%s' % (o, n) for o, n, e in accepted))
    print('rejected %d: %s' % (len(rejected), dict(Counter(r[2] for r in rejected))))
    for o, n, why in rejected:
        print('   reject %-16s -> %-16s (%s)' % (o, n, why))


if __name__ == '__main__':
    main()
