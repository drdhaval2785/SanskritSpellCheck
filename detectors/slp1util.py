"""slp1util.py  (Python 3) -- shared SLP1 helpers for the detectors/ spell-checkers.

One place for the SLP1 alphabet, the confusion model (derived from the real
o_vs_O correction distribution: vowel-length 75%, aspiration 13%, sibilant 8%,
diphthong 4%, plus v/b and retroflex/dental/nasal from the CORRECTIONS history),
and loaders for the trusted lexicons / corpus / whitelist that ship with the repo.

SLP1 quick reference (the chars actually used in sanhw1.txt headwords):
  vowels      a A i I u U f F x X e E o O      (f/F = vocalic r/rr, x/X = vocalic l/ll, E = ai, O = au)
  marks       M (anusvara)  H (visarga)  ~ (candrabindu)
  consonants  k K g G N | c C j J Y | w W q Q R | t T d D n | p P b B m | y r l v | S z s h | L (Vedic l-bar)
"""
import sys
import os
import collections

VOWELS = set("aAiIuUfFxXeEoO")
MARKS = set("MH~")
CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL")
# legal characters in a well-formed SLP1 headword (avagraha ' is allowed too)
ALPHABET = VOWELS | MARKS | CONSONANTS | {"'"}

# --- confusion model -------------------------------------------------------
# Collapse every char to a representative so that spellings that differ only by
# a common scribal/OCR confusion map to the SAME key. Single pass: each ORIGINAL
# char -> its final representative.
_COLLAPSE = str.maketrans({
    # vowels: long -> short, diphthong -> simple
    'A': 'a', 'I': 'i', 'U': 'u', 'F': 'f', 'X': 'x', 'E': 'e', 'O': 'o',
    # velar
    'K': 'k', 'G': 'g',
    # palatal (Y = nasal ny -> n)
    'C': 'c', 'J': 'j', 'Y': 'n',
    # retroflex -> dental representative (R = nasal n. -> n)
    'w': 't', 'W': 't', 'q': 'd', 'Q': 'd', 'R': 'n',
    # dental (N = velar nasal -> n)
    'T': 't', 'D': 'd', 'N': 'n',
    # labial (b/B/v merge -- the v<->b confusion; m -> nasal n)
    'P': 'p', 'b': 'v', 'B': 'v', 'm': 'n',
    # sibilants -> s
    'S': 's', 'z': 's',
    # semivowels
    'L': 'l',
})
_DROP = set("MH~'")  # diacritics that frequently vary; dropped from the key


def confusion_key(w):
    """Aggressive normalization for grouping confusable spellings.
    Collapses vowel length, aspiration, retroflex/dental, sibilants, nasals,
    b/v, drops anusvara/visarga/candrabindu, and degeminates (collapses runs of
    the same resulting consonant)."""
    w = w.translate(_COLLAPSE)
    w = ''.join(ch for ch in w if ch not in _DROP)
    out = []
    for ch in w:
        if not out or out[-1] != ch:
            out.append(ch)
    return ''.join(out)


# Unordered single-character confusion pairs (the real classes: vowel-length,
# diphthong, retroflex/dental, sibilant, aspiration, v/b, nasal). Used to confirm
# that two same-length spellings differ by ONE genuine confusion -- which excludes
# morphological endings (a trailing visarga/anusvara is an indel, not a confusion).
CONFUSION_PAIRS = {frozenset(p) for p in (
    "aA iI uU fF xX eE oO "
    "tw TW dq DQ nR "
    "sS sz Sz "
    "kK gG cC jJ wW qQ tT dD pP bB "
    "bv Bv "
    "nm nN nY mN mY mR NY NR YR"
).split()}


def confusion_sub(a, b):
    """True iff a and b are the same length and differ in exactly one position by a
    known confusion pair (so a/A, k/K, s/S, o/O, v/b, t/w ... but NOT a trailing
    case ending, which is a length difference)."""
    if len(a) != len(b):
        return False
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    return len(diff) == 1 and frozenset(diff[0]) in CONFUSION_PAIRS


# Sanskrit collation key (mirrors sanhw1.py's slp_cmp1): map SLP1 to a sort
# alphabet, and treat anusvara M before a varga consonant as the homorganic nasal
# (so aMga sorts as aNga).
import re as _re
_SORT_TAB = str.maketrans(
    "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw")
_HOMORGANIC = {c: n for n, grp in
               (('N', 'kKgGN'), ('Y', 'cCjJY'), ('R', 'wWqQR'),
                ('n', 'tTdDn'), ('m', 'pPbBm')) for c in grp}
_M_BEFORE_VARGA = _re.compile('(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])')


def sanskrit_sort_key(w):
    w = _M_BEFORE_VARGA.sub(lambda m: _HOMORGANIC[m.group(2)] + m.group(2), w)
    return w.translate(_SORT_TAB)


# char -> confusion partners, for generating correction candidates
_PARTNERS = collections.defaultdict(set)
for _pair in CONFUSION_PAIRS:
    _a, _b = tuple(_pair)
    _PARTNERS[_a].add(_b)
    _PARTNERS[_b].add(_a)


def confusion_candidates(w):
    """Spelling neighbours of w: one confusion substitution at each position, plus
    the two-character vocalic-r variants f <-> ri / ru (and rI/rU -> F)."""
    cs = set()
    for i, ch in enumerate(w):
        for p in _PARTNERS.get(ch, ()):
            cs.add(w[:i] + p + w[i + 1:])
        if ch == 'f':
            cs.add(w[:i] + 'ri' + w[i + 1:])
            cs.add(w[:i] + 'ru' + w[i + 1:])
    for i in range(len(w) - 1):
        if w[i] == 'r' and w[i + 1] in 'iu':
            cs.add(w[:i] + 'f' + w[i + 2:])
        if w[i] == 'r' and w[i + 1] in 'IU':
            cs.add(w[:i] + 'F' + w[i + 2:])
    cs.discard(w)
    return cs


# --- Devanagari -> SLP1 (delegated to the shared sanskrit-util package) -----------


def devanagari_to_slp1(s):
    """Devanagari -> SLP1 via the shared sanskrit-util package (single source of truth),
    then map danda / double-danda to spaces so OCR page text splits into word tokens.
    Used only by ocr_verify; needs the sanskrit-util sibling (or the pip-installed pkg)."""
    from sanskrit_util import to_slp1, deva_to_iast
    return to_slp1(deva_to_iast(s)).replace('।', ' ').replace('॥', ' ')


def edit_distance(a, b, cap=3):
    """Levenshtein distance, short-circuited once it exceeds `cap`."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        best = i
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
            best = min(best, cur[-1])
        if best > cap:
            return cap + 1
        prev = cur
    return min(prev[-1], cap + 1)   # honor the documented cap+1 ceiling


# --- loaders ---------------------------------------------------------------
def _read_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.lstrip('﻿').strip()  # tolerate UTF-8 BOM (MWslp.txt has one)


def load_lexicon(paths):
    """Trusted dictionary headword (stem) set from SLP1 dumps like MWslp.txt."""
    s = set()
    for p in paths:
        for w in _read_words(p):
            if w:
                s.add(w)
    return s


def load_corpus(paths):
    """Attested inflected word-forms from whitespace-tokenized SLP1 corpus files
    (CountVowels/*-CVC-SLP1.txt). Trailing verse numbers are dropped."""
    s = set()
    for p in paths:
        with open(p, 'r', encoding='utf-8') as f:
            for line in f:
                for tok in line.split():
                    if tok.isdigit():
                        continue
                    if tok:
                        s.add(tok)
    return s


def normalize_lemma(w):
    """Normalize an SLP1 headword to the DCS join key (per VisualDCS consumption
    contract): strip accents (/ \\ ^ ~) and trailing homonym digits; SLP1 case is
    preserved (it is phonemic)."""
    w = w.translate(str.maketrans('', '', '/\\^~'))
    return w.rstrip('0123456789')


def load_dcs_lemmas(path):
    """Return {normalized SLP1 lemma: freqBand 1..5} for the attested lemmas in a
    vendored dcs_lemma_summary.json (VisualDCS / DCS-2021, Oliver Hellwig, CC-BY).
    freqBand: 1=hapax, 2=rare(2-9), 3=uncommon(10-99), 4=common(100-999), 5=1000+.
    Returns {} if the file is absent (the summary is an optional enrichment)."""
    import json
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {k: v.get('freqBand', 1) for k, v in data['lemmas'].items() if v.get('attested')}


def dcs_path():
    """Default path to the vendored DCS lemma summary, next to this module."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dcs_lemma_summary.json')


def vidyut_stems_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vidyut_stems.txt')


def load_vidyut_stems(path=None):
    """Set of morphologically-valid SLP1 nominal stems (pratipadikas) from vidyut,
    vendored by gen_vidyut_stems.py. {} if absent. A *sparse* oracle for dictionary
    headwords (many are compounds/names/Vedic, not stems), so use stem PRESENCE as a
    grammar signal, never absence as proof of error."""
    if path is None:
        path = vidyut_stems_path()
    if not os.path.exists(path):
        return set()
    with open(path, 'r', encoding='utf-8') as f:
        return {ln.strip() for ln in f if ln.strip()}


def load_confusion_weights(path=None):
    """{'<c1c2 sorted>': fraction} empirical single-char confusion weights from
    gen_confusion_weights.py. Returns {} if absent."""
    import json
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'confusion_weights.json')
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f).get('weights', {})


def confusion_weight(a, b, weights):
    """Empirical weight (0..1) of the single confusion edit turning a into b; 0 if a,b
    differ by more than one character or the pair is unknown."""
    if len(a) != len(b):
        return 0.0
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    if len(diff) != 1:
        return 0.0
    return weights.get(''.join(sorted(diff[0])), 0.0)


def load_whitelist(path='nochange/nochange.txt'):
    try:
        return {w for w in _read_words(path) if w}
    except OSError:
        return set()


def parse_sanhw1(path='sanhw1.txt'):
    """Yield (headword, [dict_codes]) from a sanhw1.txt-format file."""
    for line in _read_words(path):
        if not line or ':' not in line:
            continue
        hw, dicts = line.split(':', 1)
        yield hw, [d for d in dicts.split(',') if d]


def reconfigure_stdio():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
