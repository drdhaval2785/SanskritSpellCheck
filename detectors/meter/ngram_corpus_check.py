"""ngram_corpus_check.py  (Python 3) -- H289 Phase-3 stream 2: in-corpus GRETIL typo finder

Runs the bigram spell-check over the RUNNING TEXT of a GRETIL section (not
dictionary headwords) to surface words whose SLP1 bigrams are absent from the
MW∩PW headword bigram model -- i.e. OCR / encoding / transcription slips inside
the e-text itself. This is a DIFFERENT deliverable from the dictionary-headword
QA: these are GRETIL/e-text errors, reported upstream to GRETIL, not to the
Cologne CORRECTIONS queue (handoff H289 Phase 3, stream 2).

It reuses the canonical model + suppression assets of
[`ngram/ngramspellcheck.py`](../../ngram/ngramspellcheck.py) verbatim --
`ngram/data/2grams.txt` (bigrams common to MW *and* PW headwords),
`whitelist.txt`, `whiteends.txt` (visarga/anusvāra sandhi + a/ā-split endings) --
and the same `whiteterm` inflection guard, `spaceignore`, `artisplitignore`
defaults. The one thing it adds is what a running-text tool needs and the
headword-oriented CLI lacks: it walks verses via `gretil_walker`, transliterates
each verse IAST→SLP1 with the canonical `sanskrit_util.to_slp1`, and keeps the
**locus** of every flagged word so the output is an actionable per-locus list a
human (or GRETIL) can jump to.

Output: `<out>` = one row per (flagged word), tab-separated:
    word <TAB> offending-bigrams <TAB> count <TAB> loci(up to LOCI_CAP)
sorted by descending count (a slip that recurs is likelier real than a hapax).

  python ngram_corpus_check.py <section_raw_dir> <out.tsv> [--n=2]

NOTE the method is intentionally high-recall / low-precision on running text
(inflected + sandhi'd + compounded words legitimately contain bigrams no headword
has), so the list is a HUMAN-REVIEW queue, never an auto-fix source.
"""
import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import gretil_walker as gw       # noqa: E402
import sanskrit_util_compat as su       # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
NGRAM_DATA = os.path.join(HERE, '..', '..', 'ngram', 'data')
LOCI_CAP = 8
# same token-cleaning character class as ngramspellcheck.testwithcommonngrams
_PUNCT_RE = re.compile('[\'",.?0-9!/*_\\(\\)\\[\\]\\{\\}<>;:*’#$+%^@–=“”|॒]')


def _load(name):
    with open(os.path.join(NGRAM_DATA, name), encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip()]


def ngrams(word, n):
    return [word[i:i + n] for i in range(len(word) - n + 1)] if n < len(word) else []


def whiteterm(ends, word, diff, basengrams, n):
    """Verbatim port of ngramspellcheck.whiteterm -- suppress a flagged word whose
    only anomaly is an inflectional visarga/anusvāra/a-ā ending."""
    for end in ends:
        pre, post = end.split(':')
        word1 = ''
        if word.endswith(pre):
            word1 = word.rstrip(pre) + post
        if diff <= set(pre) and set(ngrams(word, n)) < set(basengrams):
            return True
        elif word1 != '' and set(ngrams(word1, n)) < set(basengrams):
            return True
    return False


def main(raw_dir, out_path, n):
    basengrams = set(_load('2grams.txt'))
    whitelist = set(_load('whitelist.txt'))
    whiteends = list(set(_load('whiteends.txt') + ['AY:a', 'FY:f', 'IY:i', 'UY:u']))  # artisplitignore
    spaceignore = True

    flagged = collections.defaultdict(lambda: {'bigrams': set(), 'loci': [], 'count': 0})
    n_verses = n_tokens = 0
    for v in gw.walk_corpus(raw_dir):
        locus = '%s#%s' % (v['file'], v['locus'])
        n_verses += 1
        slp1 = su.to_slp1(v['full_text'])
        for tok in slp1.replace('-', ' ').split():
            tok = tok.replace('’', '')
            tok = _PUNCT_RE.sub('', tok)
            if not tok:
                continue
            n_tokens += 1
            tg = ngrams(tok, n)
            diff = set(tg) - basengrams
            if not diff:
                continue
            if diff <= whitelist or whiteterm(whiteends, tok, diff, basengrams, n):
                continue
            dl = sorted(diff)
            if spaceignore and dl[0][0] == 'n':   # anusvāra-class noise, per ngramspellcheck
                continue
            rec = flagged[tok]
            rec['bigrams'] |= diff
            rec['count'] += 1
            if len(rec['loci']) < LOCI_CAP:
                rec['loci'].append(locus)

    rows = sorted(flagged.items(), key=lambda kv: (-kv[1]['count'], kv[0]))
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write('# word\tbigrams_absent_from_MW∩PW\tcount\tloci\n')
        for word, rec in rows:
            out.write('%s\t%s\t%d\t%s\n'
                      % (word, ','.join(sorted(rec['bigrams'])), rec['count'], ';'.join(rec['loci'])))
    sys.stderr.write("ngram_corpus_check: %d verses, %d tokens, %d distinct flagged words -> %s\n"
                     % (n_verses, n_tokens, len(flagged), out_path))


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        sys.exit(__doc__)
    n = next((int(a.split('=', 1)[1]) for a in sys.argv[1:] if a.startswith('--n=')), 2)
    main(args[0], args[1], n)
