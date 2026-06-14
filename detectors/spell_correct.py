"""spell_correct.py  (Python 3)  -- detector #1: noisy-channel correction

For each headword that is NOT in a trusted lexicon (MW + PW + VCP stems), generate
its confusion-neighbours and, if a neighbour IS a trusted headword, flag the word as
a likely misspelling of it. Scored/ranked by whether the suggested form is attested
in a real Sanskrit corpus (the CountVowels/*-CVC-SLP1.txt texts). Unlike consensus
(which votes by dict count), this uses a curated ground-truth lexicon + corpus, so it
catches a word that is wrong in several minor dicts at once.

Confusion neighbours = one same-length confusion substitution (a/A, k/K, s/S, o/O,
v/b, t/w, nasal ...) PLUS the vocalic-r spelling variants f <-> ri / ru (the
SfNg/SriNg class), which the same-length confusion_sub cannot express.

  python spell_correct.py [sanhw1=../sanhw1.txt] [out=spell_correct_corrections.txt]
"""
import sys
import os
import glob
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

# char -> set of confusion partners, derived from the shared confusion-pair table
PARTNERS = collections.defaultdict(set)
for _pair in u.CONFUSION_PAIRS:
    _a, _b = tuple(_pair)
    PARTNERS[_a].add(_b)
    PARTNERS[_b].add(_a)


def candidates(w):
    cs = set()
    for i, ch in enumerate(w):
        for p in PARTNERS.get(ch, ()):
            cs.add(w[:i] + p + w[i + 1:])
        if ch == 'f':                         # vocalic r written as ri / ru
            cs.add(w[:i] + 'ri' + w[i + 1:])
            cs.add(w[:i] + 'ru' + w[i + 1:])
    for i in range(len(w) - 1):               # ri / ru / rI / rU written for vocalic r
        if w[i] == 'r' and w[i + 1] in 'iu':
            cs.add(w[:i] + 'f' + w[i + 2:])
        if w[i] == 'r' and w[i + 1] in 'IU':
            cs.add(w[:i] + 'F' + w[i + 2:])
    cs.discard(w)
    return cs


def main(sanhw1, outfile):
    root = os.path.dirname(sanhw1) or '.'
    lex = u.load_lexicon([os.path.join(root, f) for f in ('MWslp.txt', 'PWslp.txt', 'VCPslp.txt')])
    corpus = u.load_corpus(glob.glob(os.path.join(root, 'CountVowels', '*-CVC-SLP1.txt')))
    whitelist = u.load_whitelist(os.path.join(root, 'nochange', 'nochange.txt'))
    print("trusted lexicon: %d stems   corpus tokens: %d" % (len(lex), len(corpus)))

    flagged = []  # (corpus_support, wrong, suggest, dicts)
    for hw, dicts in u.parse_sanhw1(sanhw1):
        if hw in lex or hw in whitelist:
            continue
        hits = [c for c in candidates(hw) if c in lex]
        if not hits:
            continue
        # prefer a suggestion that is also attested in the corpus
        hits.sort(key=lambda c: (c not in corpus, c))
        best = hits[0]
        support = (best in corpus) and (hw not in corpus)
        flagged.append((support, hw, best, dicts))

    flagged.sort(key=lambda r: (not r[0], r[1]))  # corpus-supported first
    with open(outfile, 'w', encoding='utf-8') as out:
        for support, wrong, sugg, dicts in flagged:
            tag = 'corpus' if support else 'lex'
            for code in dicts:
                out.write("%s:%s:%s:n\n" % (code, wrong, sugg))
    corpus_n = sum(1 for r in flagged if r[0])
    print("flagged %d misspellings (%d corpus-corroborated) -> %s" % (len(flagged), corpus_n, outfile))
    print("--- top 25 corpus-corroborated (wrong -> suggestion [dicts]) ---")
    shown = 0
    for support, wrong, sugg, dicts in flagged:
        if not support:
            continue
        print("  %-20s -> %-20s  [%s]" % (wrong, sugg, ",".join(dicts)))
        shown += 1
        if shown >= 25:
            break


if __name__ == "__main__":
    sanhw1 = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "spell_correct_corrections.txt"
    main(sanhw1, outfile)
