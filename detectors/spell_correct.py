"""spell_correct.py  (Python 3)  -- detector #1: noisy-channel correction

For each headword that is NOT in a trusted lexicon (MW + PW + VCP stems), generate
its confusion-neighbours and, if a neighbour IS a trusted headword, flag the word as
a likely misspelling of it. Unlike consensus (which votes by dict count), this uses a
curated ground-truth lexicon, so it catches a word that is wrong in several minor
dicts at once.

Grounded in the DCS corpus (vendored dcs_lemma_summary.json, 83k SLP1 lemmas with
frequency bands 1..5, DCS-2021 / Oliver Hellwig, CC-BY):
  * SUPPRESS -- a headword that is itself an attested DCS lemma is a real word, not a
    typo, so it is skipped (big false-positive cut for rare words absent from MW/PW/VCP).
  * RANK -- suggestions are ordered by the suggested lemma's DCS frequency band, so
    "wrong -> very-common word" surfaces first. The raw CountVowels texts give a
    secondary surface-form corpus signal.

Confusion neighbours = one same-length confusion substitution (a/A, k/K, s/S, o/O,
v/b, t/w, nasal ...) PLUS the vocalic-r spelling variants f <-> ri / ru (the
SfNg/SriNg class), which the same-length confusion_sub cannot express.

  python spell_correct.py [sanhw1=../sanhw1.txt] [out=spell_correct_corrections.txt]
"""
import sys
import os
import glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()


def main(sanhw1, outfile):
    root = os.path.dirname(sanhw1) or '.'
    lex = u.load_lexicon([os.path.join(root, f) for f in ('MWslp.txt', 'PWslp.txt', 'VCPslp.txt')])
    corpus = u.load_corpus(glob.glob(os.path.join(root, 'CountVowels', '*-CVC-SLP1.txt')))
    dcs = u.load_dcs_lemmas(u.dcs_path())
    whitelist = u.load_whitelist(os.path.join(root, 'nochange', 'nochange.txt'))
    print("trusted lexicon: %d   corpus tokens: %d   DCS lemmas: %d" % (len(lex), len(corpus), len(dcs)))

    def band(c):
        return dcs.get(u.normalize_lemma(c), 0)

    flagged = []   # (dcs_band, in_corpus, wrong, suggest, dicts)
    suppressed = 0
    for hw, dicts in u.parse_sanhw1(sanhw1):
        if hw in lex or hw in whitelist:
            continue
        if u.normalize_lemma(hw) in dcs:        # attested DCS lemma -> a real word, not a typo
            suppressed += 1
            continue
        hits = [c for c in u.confusion_candidates(hw) if c in lex]
        if not hits:
            continue
        hits.sort(key=lambda c: (-band(c), c not in corpus, c))
        best = hits[0]
        flagged.append((band(best), best in corpus, hw, best, dicts))

    flagged.sort(key=lambda r: (-r[0], not r[1], r[2]))   # highest DCS band first
    with open(outfile, 'w', encoding='utf-8') as out:
        for bnd, incorp, wrong, sugg, dicts in flagged:
            for code in dicts:
                out.write("%s:%s:%s:n\n" % (code, wrong, sugg))
    hi = sum(1 for r in flagged if r[0] >= 4)
    print("flagged %d (%d suppressed as DCS-attested real words); %d suggest a common DCS lemma (band>=4) -> %s"
          % (len(flagged), suppressed, hi, outfile))
    print("--- top 25 by DCS frequency (wrong -> suggestion  [DCS band, dicts]) ---")
    for bnd, incorp, wrong, sugg, dicts in flagged[:25]:
        print("  %-20s -> %-20s  [band %d%s | %s]"
              % (wrong, sugg, bnd, '+corpus' if incorp else '', ",".join(dicts)))


if __name__ == "__main__":
    sanhw1 = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "spell_correct_corrections.txt"
    main(sanhw1, outfile)
