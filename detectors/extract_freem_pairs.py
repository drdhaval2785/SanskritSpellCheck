#!/usr/bin/env python3
"""extract_freem_pairs.py -- harvest historical->modern French spelling pairs from the FreEMnorm
parallel corpus (github.com/FreEM-corpora/FreEMnorm, 17th c. French, CC-licensed).

Each corpus/*.tsv row is  DIPLOMATIC<TAB>NORMALISED  (one sentence per line). We token-align the
two sides per row (difflib), take 1:1 'replace' spans where surface != norm, and emit
  old<TAB>new<TAB>count  (surface=old lowercased, norm=new) -- the same contract extract_dta_pairs.py
produces, i.e. the lowest-common-denominator input for merge_reform_pairs.py, which then dic-validates
(old NOT in fr_FR, new IN fr_FR). Letters-only [a-zà-ÿ] (this drops long-ſ U+017F typographic pairs
automatically); u/v and i/j letterform pairs DO pass and are classified downstream.

  cd detectors && python extract_freem_pairs.py ../external_src/freem/corpus ../external_src/freem/freem_fr_pairs.tsv [mincount=2]
"""
import os
import re
import sys
import glob
import difflib
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util
triage_util.reconfigure_stdio()

_WORD = re.compile(r'[A-Za-zÀ-ÖØ-öø-ÿ]+')       # French word; digits/punct excluded
_OK = re.compile(r'^[a-zà-öø-ÿ]+$')             # accepted token shape (post-lowercase)


def toks(s):
    # Long-ſ (U+017F) is purely TYPOGRAPHIC: fold it to s on BOTH sides BEFORE tokenizing, so
    # `ſon`/`son` align as equal (no pair) instead of truncating to a bogus `on`->`son`.
    s = s.replace('ſ', 's').replace('ﬅ', 'st').replace('ﬆ', 'st')
    return [w.lower() for w in _WORD.findall(s)]


def main():
    cdir = sys.argv[1] if len(sys.argv) > 1 else '../external_src/freem/corpus'
    out = sys.argv[2] if len(sys.argv) > 2 else '../external_src/freem/freem_fr_pairs.tsv'
    mincount = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    pairs = Counter()
    nfiles = nrows = 0
    for path in sorted(glob.glob(os.path.join(cdir, '*.tsv'))):
        nfiles += 1
        with open(path, encoding='utf-8') as f:
            for line in f:
                cols = line.rstrip('\n').split('\t')
                if len(cols) < 2:
                    continue
                nrows += 1
                a, b = toks(cols[0]), toks(cols[1])
                for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                    if op != 'replace' or (i2 - i1) != (j2 - j1):
                        continue                # only 1:1 substitutions (conservative)
                    for old, new in zip(a[i1:i2], b[j1:j2]):
                        if old != new and len(old) >= 2 and _OK.match(old) and _OK.match(new):
                            pairs[(old, new)] += 1

    kept = [(o, n, c) for (o, n), c in pairs.items() if c >= mincount]
    kept.sort(key=lambda r: (-r[2], r[0]))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('# FreEMnorm 17th-c.-French historical->modern pairs (surface<TAB>norm<TAB>count)\n')
        f.write('# %d files, %d aligned rows; %d distinct pairs, %d with count>=%d\n'
                % (nfiles, nrows, len(pairs), len(kept), mincount))
        for o, n, c in kept:
            f.write('%s\t%s\t%d\n' % (o, n, c))
    print('%d files, %d rows; %d distinct surface!=norm pairs; %d with count>=%d -> %s'
          % (nfiles, nrows, len(pairs), len(kept), mincount, os.path.relpath(out, triage_util.ROOT)))
    print('  top 20: %s' % ', '.join('%s->%s(%d)' % (o, n, c) for o, n, c in kept[:20]))


if __name__ == '__main__':
    main()
