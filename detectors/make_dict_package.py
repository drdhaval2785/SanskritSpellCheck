#!/usr/bin/env python3
"""make_dict_package.py -- build a per-dictionary tier-A candidate package from the
unified engine output, ready for the body-grounded triage.

Extracts the tier-A rows of `combined_candidates.txt` (run_all.py) in which the target
dictionary carries the suspect headword, and writes, under corrections_draft/<DICT>/:
  <DICT>_candidates.txt    ranked tier-A candidates  (score / wrong -> right / detectors / morph)
  <DICT>_draft.txt         updateByLine DRAFT change-file (via make_changefiles, locates
                           each entry in csl-orig and proposes the <k1>/<k2> edit)
  triage_work/<DICT>_sf.txt  intermediate DICT:wrong:right:n (gitignored)

Then run, in order:  triage_enrich.py -> triage_bodies.py -> triage_body_batches.py ->
the body-aware workflow -> triage_synthesize.py  (all take the same <DICT> argument).

Usage:  cd detectors && python make_dict_package.py PW   # (needs combined_candidates.txt)
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import make_changefiles

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    if len(sys.argv) < 2:
        print("usage: python make_dict_package.py <DICT>")
        sys.exit(1)
    dict_code = sys.argv[1]
    combined = os.path.join(HERE, 'combined_candidates.txt')
    if not os.path.exists(combined):
        print("combined_candidates.txt not found — run: python run_all.py ../sanhw1.txt")
        sys.exit(1)
    pkg = os.path.join(ROOT, 'corrections_draft', dict_code)
    work = os.path.join(pkg, 'triage_work')
    os.makedirs(work, exist_ok=True)

    rows = []
    with open(combined, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            p = line.split('\t')
            if len(p) < 5:
                continue
            tier, score, pair, dets, dicts = p[0], p[1], p[2], p[3], p[4]
            morph = len(p) > 5 and 'morph' in p[5]
            if tier != 'A':
                continue
            dlist = [d for d in dicts.strip('[]').split(',') if d]
            if dict_code not in dlist:
                continue
            m = re.match(r'(\S+)\s*->\s*(\S+)', pair)
            if not m:
                continue
            rows.append((int(score), m.group(1), m.group(2), dets, morph))

    cand = os.path.join(pkg, '%s_candidates.txt' % dict_code)
    with open(cand, 'w', encoding='utf-8') as f:
        f.write("# %s tier-A correction candidates (unified engine) — score\twrong -> right\tdetectors\tmorph\n" % dict_code)
        for sc, wsp, rsp, dets, mo in rows:
            f.write("%d\t%s -> %s\t%s\t%s\n" % (sc, wsp, rsp, dets, 'morph✓' if mo else ''))

    sf = os.path.join(work, '%s_sf.txt' % dict_code)
    with open(sf, 'w', encoding='utf-8') as f:
        for sc, wsp, rsp, dets, mo in rows:
            f.write("%s:%s:%s:n\n" % (dict_code, wsp, rsp))

    print("%s: %d tier-A candidates -> %s" % (dict_code, len(rows), os.path.relpath(cand, ROOT)))
    csl_root = os.path.join(ROOT, '..', 'csl-orig')
    make_changefiles.main(sf, csl_root, os.path.relpath(pkg, HERE))


if __name__ == '__main__':
    main()
