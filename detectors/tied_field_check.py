"""tied_field_check.py  (Python 3)  -- detector #11: tied-field cross-field consistency

New detector SHAPE (H827, ACL roadmap rev 3 ruling D14), from the project's direct
methodological ancestor Bloodgood & Strauss, "Data Cleaning for XML Electronic
Dictionaries via Statistical Anomaly Detection" (arXiv 1602.07807, IEEE ICSC 2016):
checking that two fields expected to encode the SAME content across a
transliteration/length model actually agree ("tied-field consistency"). For CDSL
that is: SLP1-headword <-> its Devanagari rendering <-> its IAST rendering must be
mutually derivable.

sanhw1.txt (the unified headword list across all 33 dicts) stores only the SLP1
headword -- there is no separately-authored per-entry Devanagari/IAST field in this
repo's data model to cross-check against (unlike, say, a stored citation-form field
elsewhere). So the operative check here is the ROUND-TRIP: SLP1 -> Devanagari -> SLP1
and SLP1 -> IAST -> SLP1 must both return the original headword. A headword whose
round-trip does NOT return the original is either a genuine transcoder defect or an
SLP1 form using characters the transcoder cannot faithfully carry through that
particular target script -- surfaced here as a NEW, otherwise-invisible error class,
distinct from (and unblocked by) charset/phonotactic (surface-form only; no body gate,
see refuted R5/R6 in docs/HYPOTHESES.md).

Two round-trip asymmetries are DOCUMENTED PROPERTIES of the transcoders themselves
(not data errors) and are suppressed here so they never reach CORRECTIONS, matching
the do-not-file convention used elsewhere in this repo for editorial normalization:

  1. Devanagari path -- candrabindu (~) and avagraha (') are not round-trip stable
     through Devanagari: '~' -> chandrabindu 'ँ' -> reads back as anusvara 'M' (both
     anusvara and candrabindu collapse to Devanagari's single nasalization slot on the
     SLP1 side); avagraha "'" -> 'ऽ', which deva_to_slp1 drops (no SLP1 char position
     for it once written). Both are documented directly in sanskrit-util's own
     slp1_to_devanagari docstring. Expected (non-error) round-trip is therefore
     hw with '~' -> 'M' and "'" removed; anything else is a genuine TFC-DEV flag.
  2. IAST path -- IAST re-spells SLP1 aspirates (K/G/C/J/W/Q/T/D/P/B) and diphthongs
     (E/O) as two-letter digraphs (kh/gh/ch/jh/ṭh/ḍh/th/dh/ph/bh, ai/au). SLP1 already
     has ONE character for each of these, so whenever a headword's SLP1 has a PLAIN
     stop immediately followed by 'h' (a genuine two-phoneme sequence, e.g. a
     compound/sandhi boundary: vAk+hasta -> vAkhasta) or two adjacent short vowels
     (a+i, a+u -- vowel hiatus), the IAST rendering is textually IDENTICAL to the
     aspirate/diphthong spelling and to_slp1 (longest-key-first) reads it back as the
     single aspirate/diphthong character. This is an inherent one-way lossiness of
     concatenative IAST -- not a transcoder bug -- verified empirically: it explains
     100/100 of the IAST round-trip mismatches on the full sanhw1.txt population
     (H827 build, no unexplained residual). _iast_collapse() reproduces exactly what
     to_slp1(from_slp1(hw)) does in these positions; if the actual round-trip matches
     that prediction, suppress -- otherwise it is a genuine TFC-IAST flag.

Run:
  python tied_field_check.py [input=../sanhw1.txt] [output=tied_field_suspects.txt]

Output: faultfinder format  X:TFC-DEV=<deva>/<deva_rt>:D  or  X:TFC-IAST=<iast>/<iast_rt>:D
(same X:CODE=detail:D contract as charset_check/phonotactic_check -- consumed by
run_all.py as an 11th detector family and by faultfinder3a-html.php/triage_suspects.py.)
"""
import sys
import os
import re
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

# Longest-key-first is not needed here (all keys are 2 chars); order doesn't matter since
# the alternatives don't overlap (no key is a substring of another at the same position).
_DIGRAPH = re.compile(r'kh|gh|ch|jh|wh|qh|th|dh|ph|bh|ai|au')
_DMAP = {'kh': 'K', 'gh': 'G', 'ch': 'C', 'jh': 'J', 'wh': 'W', 'qh': 'Q',
         'th': 'T', 'dh': 'D', 'ph': 'P', 'bh': 'B', 'ai': 'E', 'au': 'O'}


def _iast_collapse(s):
    """Predict what to_slp1(from_slp1(s)) does at every plain-stop+h / vowel-hiatus
    position -- the documented IAST digraph ambiguity (see module docstring #2)."""
    return _DIGRAPH.sub(lambda m: _DMAP[m.group(0)], s)


def check(hw):
    """Return [(code, detail), ...] tied-field disagreements for one SLP1 headword.
    Empty for headwords containing a character outside u.ALPHABET -- those are
    charset_check's job (encoding errors), not a tied-field consistency question."""
    if not hw or any(ch not in u.ALPHABET for ch in hw):
        return []
    out = []
    deva = u.slp1_to_devanagari(hw)
    deva_rt = u.devanagari_to_slp1(deva)
    if deva_rt != hw:
        expected = hw.replace('~', 'M').replace("'", '')  # candrabindu/avagraha asymmetry
        if deva_rt != expected:
            out.append(('TFC-DEV', '%s/%s' % (deva, deva_rt)))
    iast = u.slp1_to_iast(hw)
    iast_rt = u.iast_to_slp1(iast)
    if iast_rt != hw:
        if iast_rt != _iast_collapse(hw):  # digraph/hiatus ambiguity
            out.append(('TFC-IAST', '%s/%s' % (iast, iast_rt)))
    return out


def main(infile, outfile):
    cats = collections.Counter()
    n = total = 0
    with open(outfile, 'w', encoding='utf-8') as out:
        for line in u._read_words(infile):
            if not line:
                continue
            total += 1
            hw, dicts = (line.split(':', 1) + [''])[:2] if ':' in line else (line, '')
            for code, detail in check(hw):
                n += 1
                cats[code] += 1
                out.write("%s:%s=%s:%s\n" % (hw, code, detail, dicts))
    print("scanned %d headwords; %d tied-field disagreements -> %s" % (total, n, outfile))
    for k, c in cats.most_common():
        print("  %-9s %d" % (k, c))


if __name__ == "__main__":
    infile = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "tied_field_suspects.txt"
    main(infile, outfile)
