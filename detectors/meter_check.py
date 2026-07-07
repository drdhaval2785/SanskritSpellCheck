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

# DCS-rarity gate (H277): only surface a headword whose lemma is LOW-frequency in
# the DCS corpus. A common word (deva, rāja, ca, gam...) sitting in a metrically
# irregular kavya verse carries no signal -- kavya vocabulary overlaps enormously
# with ordinary dictionary headwords, so an un-gated bridge flags thousands of
# perfectly ordinary words by pure co-occurrence (7,925 pre-gate). A rare / unusual
# / unattested spelling near a metrical anomaly is the informative combination --
# mirrors run_all.py's CORROB_* reasoning (suspect + rare, not suspect + common)
# and headword_bridge's own STOPWORDS/MIN_LEMMA_LEN filter, extended to frequency.
# Bands (slp1util.load_dcs_lemmas): 1=hapax 2=rare(2-9) 3=uncommon 4=common 5=1000+;
# absent=0. Keep band <= RARE_BAND (0,1,2).
RARE_BAND = 2


def main(sanhw1, outfile):
    if not os.path.exists(VERDICTS_PATH):
        sys.stderr.write("meter_check: %s not found -- run meter/build_meter_index.py first; "
                          "emitting empty output (not an error, the corpus index is a one-time "
                          "offline build, see meter/build_meter_index.py docstring)\n" % VERDICTS_PATH)
        open(outfile, 'w', encoding='utf-8').close()
        return

    idx = hb.load_headword_index(sanhw1)
    dcs = u.load_dcs_lemmas(u.dcs_path())
    hits = collections.defaultdict(lambda: {'suspect': set(), 'review': set()})
    n_verses = n_nonclean = n_bridged = n_common_skipped = 0
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
            locus = "%s#%s" % (rec['source'], rec['locus'])
            bridged_here = False
            for hw in verse_hits:
                if dcs and dcs.get(u.normalize_lemma(hw), 0) > RARE_BAND:
                    n_common_skipped += 1        # common DCS word -> uninformative
                    continue
                hits[hw][v].add(locus)
                bridged_here = True
            if bridged_here:
                n_bridged += 1

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
                      "%d common-word bridge hits skipped (DCS band > %d), "
                      "%d distinct rare headwords flagged -> %s\n"
                      % (n_verses, n_nonclean, n_bridged, n_common_skipped, RARE_BAND,
                         len(hits), outfile))


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sanhw1_arg = args[0] if len(args) > 0 else os.path.join(HERE, '..', 'sanhw1.txt')
    out_arg = args[1] if len(args) > 1 else os.path.join(HERE, 'meter_suspects.txt')
    main(sanhw1_arg, out_arg)
