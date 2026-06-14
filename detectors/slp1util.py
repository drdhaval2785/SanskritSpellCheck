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
    return prev[-1]


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
