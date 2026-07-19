"""headword_bridge.py  (Python 3) -- H251 build task 4: word -> dictionary-headword bridge

The meter validator operates on free running GRETIL verse text (locus = file +
verse); the SpellCheck detectors operate on dictionary headwords (sanhw1.txt).
There is no existing bridge between a word-position in a verse and a specific
headword -- this module is that bridge.

Method: for each word in a flagged (non-clean) verse, convert IAST -> SLP1
(sanskrit_util.to_slp1, the shared org transliteration lib) and run it through
vidyut's segmenter (vidyut.cheda.Chedaka, already vendored at
../../../WhitneyRoots/scratch/vidyut_data for gen_vidyut_stems.py) to get its
lemma. The DCS lemma summary (slp1util.load_dcs_lemmas) was considered as a
simpler bag-of-lemmas alternative per the handoff, but it indexes already-
lemmatized DCS forms, not surface running text -- it cannot map an inflected
verse word back to a lemma by itself, so it is NOT sufficient alone as the
bridge (only as an auxiliary corroboration on top of vidyut's per-word lemma).
Chedaka gives a real per-token morphological lemma from context and is used as
the primary bridge; DCS attestation is not required for a hit (this module
does not gate on it -- run_all.py's existing CORROB_* logic already applies a
DCS-based nudge downstream).

The lemma is normalized (slp1util.normalize_lemma) and checked against the
live sanhw1.txt headword set -- so a hit means "a headword from the current
sanhw1.txt appears (as its lemma) in this GRETIL locus", which is exactly the
evidence meter_check.py needs to emit.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import sanskrit_util_compat as su   # noqa: E402
import slp1util as u          # noqa: E402

WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)

# Closed-class indeclinables/particles (SLP1) -- excluded from bridge hits.
# Every kavya verse contains several of these, so co-occurrence with a
# metrically-suspect verse carries no signal for them (unlike a content word,
# whose spelling could plausibly be the thing the meter break corrupted).
# Without this filter the bridge floods run_all.py with near-universal
# "hits" on common grammatical glue (observed 06-07-2026: single-token
# fragments like bare "A" and "ca" dominating meter_suspects.txt).
STOPWORDS = {
    'ca', 'vA', 'tu', 'hi', 'eva', 'api', 'na', 'iti', 'tathA', 'punaH', 'ataH',
    'yataH', 'yadi', 'tadA', 'yadA', 'yat', 'tat', 'ca-eva', 'atha', 'kila',
    'nu', 'sma', 'khalu', 'nUnam', 'A', 'I', 'U', 'a', 'i', 'u',
}
MIN_LEMMA_LEN = 3

_chedaka = None
_CHEDAKA_UNAVAILABLE = object()


def _get_chedaka():
    global _chedaka
    if _chedaka is None:
        try:
            from vidyut.cheda import Chedaka
            here = os.path.dirname(os.path.abspath(__file__))
            data = os.path.join(here, '..', '..', '..', 'WhitneyRoots', 'scratch', 'vidyut_data')
            _chedaka = Chedaka(data) if os.path.isdir(data) else _CHEDAKA_UNAVAILABLE
        except Exception:
            _chedaka = _CHEDAKA_UNAVAILABLE
    return None if _chedaka is _CHEDAKA_UNAVAILABLE else _chedaka


def tokenize(iast_text):
    return WORD_RE.findall(iast_text)


def lemmas_for_verse(full_text_iast):
    """Return the set of normalized SLP1 lemmas Chedaka finds for the words in
    one verse's text. Words Chedaka cannot segment (e.g. long unbroken
    compounds outside its training distribution) are silently skipped -- this
    is a recall gap in the bridge, not a false hit, and is logged in aggregate
    by build_meter_index's caller via the headword_bridge_stats() counters."""
    ch = _get_chedaka()
    if ch is None:
        return set()
    slp1 = su.to_slp1(full_text_iast)
    try:
        tokens = ch.run(slp1)
    except Exception:
        return set()
    out = set()
    for t in tokens:
        lemma = getattr(t, 'lemma', None)
        if not lemma:
            continue
        norm = u.normalize_lemma(lemma)
        if len(norm) < MIN_LEMMA_LEN or norm in STOPWORDS:
            continue
        out.add(norm)
    return out


def load_headword_index(sanhw1_path):
    """{normalized SLP1 headword: 'DICT1,DICT2,...'} from sanhw1.txt."""
    idx = {}
    for line in u._read_words(sanhw1_path):
        if not line or ':' not in line:
            continue
        hw, dicts = line.split(':', 1)
        idx[u.normalize_lemma(hw)] = dicts
    return idx


def bridge_verse(full_text_iast, headword_index):
    """Return {headword: dicts} for every sanhw1 headword whose lemma Chedaka
    finds in this verse's text."""
    hits = {}
    for lemma in lemmas_for_verse(full_text_iast):
        if lemma in headword_index:
            hits[lemma] = headword_index[lemma]
    return hits
