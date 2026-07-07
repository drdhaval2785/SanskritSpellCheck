"""meter_check.py  (Python 3) -- detector #7: batch chandas (meter) validation, H251

Flags dictionary headwords that co-occur with a metrically broken/ambiguous
GRETIL kavya verse (see meter/ for the three-way skrutable+chanda+vidyut-chandas
identifier and the word->headword bridge). A pAda that breaks its identified
meter is a suspect-text signal -- per the locked H251 decisions this is wired
in as a ranking-nudge evidence source (this detector is NOT in run_all.py's
HIGH_PRECISION set, so alone it stays tier C; it only promotes a candidate to
tier A in agreement with >=1 other detector, exactly like the existing 6
detectors' cross-agreement -- see run_all.py's ndet>=2 rule. No aggregation
logic in run_all.py was changed for this).

Reads the offline meter/meter_verdicts.jsonl (built once by
meter/build_meter_index.py -- NOT regenerated here; this script is cheap and
meant to run every run_all.py invocation) and the live sanhw1.txt, bridges
each non-clean verse's words to headwords via meter/headword_bridge.py, and
emits the standard flagger format:

  hw:MTR=<verdict>|<locus>[;<locus>...]:D

  python meter_check.py [sanhw1=../sanhw1.txt] [out=meter_suspects.txt]
"""
import sys
import os
import json
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meter'))
import slp1util as u          # noqa: E402
import headword_bridge as hb  # noqa: E402

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))
VERDICTS_PATH = os.path.join(HERE, 'meter', 'meter_verdicts.jsonl')


def main(sanhw1, outfile):
    if not os.path.exists(VERDICTS_PATH):
        sys.stderr.write("meter_check: %s not found -- run meter/build_meter_index.py first; "
                          "emitting empty output (not an error, the corpus index is a one-time "
                          "offline build, see meter/build_meter_index.py docstring)\n" % VERDICTS_PATH)
        open(outfile, 'w', encoding='utf-8').close()
        return

    idx = hb.load_headword_index(sanhw1)
    hits = collections.defaultdict(lambda: {'suspect': set(), 'review': set()})
    n_verses = n_nonclean = n_bridged = 0
    with open(VERDICTS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_verses += 1
            rec = json.loads(line)
            v = rec['verdict']
            if v == 'clean':
                continue
            n_nonclean += 1
            full_text = rec.get('full_text') or ' '.join(
                l['line'] for l in rec.get('chanda', []) if isinstance(l, dict) and l.get('line')) or ''
            if not full_text:
                continue
            verse_hits = hb.bridge_verse(full_text, idx)
            if verse_hits:
                n_bridged += 1
            locus = "%s#%s" % (rec['source'], rec['locus'])
            for hw in verse_hits:
                hits[hw][v].add(locus)

    with open(outfile, 'w', encoding='utf-8') as out:
        for hw in sorted(hits):
            dicts = idx.get(hw, '')
            for verdict_key in ('suspect', 'review'):
                loci = sorted(hits[hw][verdict_key])
                if not loci:
                    continue
                detail = "%s|%s" % (verdict_key, ';'.join(loci))
                out.write("%s:MTR=%s:%s\n" % (hw, detail, dicts))

    sys.stderr.write("meter_check: %d verses in index, %d non-clean, %d bridged to a headword, "
                      "%d distinct headwords flagged -> %s\n"
                      % (n_verses, n_nonclean, n_bridged, len(hits), outfile))


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sanhw1_arg = args[0] if len(args) > 0 else os.path.join(HERE, '..', 'sanhw1.txt')
    out_arg = args[1] if len(args) > 1 else os.path.join(HERE, 'meter_suspects.txt')
    main(sanhw1_arg, out_arg)
