"""dict_vs_corpus.py  (Python 3)  -- detector: dictionaries vs the corpus

The one detector that can catch a *collective* dictionary error -- a headword that
the dictionaries agree on but that the DCS corpus contradicts. Cross-dictionary
methods (o_vs_O, consensus, intra_dup) are blind to this: if every dictionary spells
a word the same (wrong) way there is no disagreement to exploit. An external corpus
breaks the tie.

For each headword whose normalized form is NOT an attested DCS lemma, generate its
confusion-neighbours; if a neighbour IS a DCS lemma of band >= MIN_BAND, flag the
headword as a likely error and suggest that lemma. Ranked by how many dictionaries
carry the suspect form (a high count = a genuinely collective error) and then by the
suggestion's corpus frequency band.

DCS data: vendored dcs_lemma_summary.json (DCS-2021, Oliver Hellwig, CC-BY).

PRECISION: this is the LOWEST-precision detector by design, because DCS-lemma
*absence* is a weak negative signal. The ranked output mixes genuine collective
errors with three kinds of false positive: (a) two distinct real words that are
confusion-neighbours (guha "Kārttikeya" vs guhA "cave"; magna vs nagna), (b)
citation-convention differences (dict ī-stem `sUcI` vs DCS lemma `sUci`), and (c)
real but rare/technical/prefix lexicon DCS simply does not list (dur, gu). Treat it
as a ranked *exploration* list that needs heavy human filtering, not a correction
feed. Its unique value is that it is the only detector that can see an error the
dictionaries make *unanimously*.

  python dict_vs_corpus.py [sanhw1=../sanhw1.txt] [out=dict_vs_corpus_corrections.txt]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

MIN_BAND = 4      # suggested DCS lemma must be "common" (>=100 occurrences) -- bias for precision
MIN_DICTS = 2     # suspect form must sit in >= this many dictionaries to count as collective


def main(sanhw1, outfile):
    root = os.path.dirname(sanhw1) or '.'
    dcs = u.load_dcs_lemmas(u.dcs_path())
    whitelist = u.load_whitelist(os.path.join(root, 'nochange', 'nochange.txt'))
    if not dcs:
        print("no DCS lemma summary found at %s -- nothing to do" % u.dcs_path())
        return
    print("DCS lemmas: %d" % len(dcs))

    flagged = []  # (n_dicts, band, wrong, suggest, dicts)
    for hw, dicts in u.parse_sanhw1(sanhw1):
        if hw in whitelist or len(dicts) < MIN_DICTS:
            continue
        if u.normalize_lemma(hw) in dcs:        # corpus attests the headword -> fine
            continue
        best, best_band = None, 0
        for c in u.confusion_candidates(hw):
            b = dcs.get(u.normalize_lemma(c), 0)
            if b > best_band:
                best, best_band = c, b
        if best and best_band >= MIN_BAND:
            flagged.append((len(dicts), best_band, hw, best, sorted(dicts)))

    flagged.sort(key=lambda r: (-r[0], -r[1], r[2]))
    with open(outfile, 'w', encoding='utf-8') as out:
        for _, _, wrong, sugg, dicts in flagged:
            for code in dicts:
                out.write("%s:%s:%s:n\n" % (code, wrong, sugg))

    collective = sum(1 for r in flagged if r[0] >= 5)
    print("flagged %d headwords absent from DCS with a common-DCS neighbour (%d in >=5 dicts) -> %s"
          % (len(flagged), collective, outfile))
    print("NOTE: lowest-precision detector -- mixes real collective errors with distinct")
    print("word-pairs, ī/i citation differences, and rare lexicon DCS omits. Filter heavily.")
    print("--- top 25 (suspect [in N dicts] -> DCS lemma [band]) ---")
    for ndicts, band, wrong, sugg, dicts in flagged[:25]:
        print("  %-20s [%2d dicts] -> %-20s [band %d]" % (wrong, ndicts, sugg, band))


if __name__ == "__main__":
    sanhw1 = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "dict_vs_corpus_corrections.txt"
    main(sanhw1, outfile)
