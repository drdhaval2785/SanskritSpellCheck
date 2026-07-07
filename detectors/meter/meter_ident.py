"""meter_ident.py  (Python 3) -- H251 build task 2: three-way meter identification + verdict

Wraps skrutable + chanda + vidyut-chandas behind one call per verse and computes
a clean|review|suspect verdict, extending the two-tool pilot scheme
(CHANDAS_ANUPRASA_PRIOR_ART.md #4) to the locked 3-way vote (decision 3):

  clean   -- skrutable perfect AND chanda exact-or-fuzzy(cost<=2, sim>=0.9) agrees
             on the meter (vidyut, when it returns a name, corroborates or is silent)
  review  -- tools disagree without a clear majority (e.g. chanda's near-tie
             mis-rank, pilot Finding 2; or vidyut names a 3rd meter with no
             majority)
  suspect -- skrutable reports imperfect scansion (a problem pAda) AND at least
             one other tool disagrees with it -- OR no tool agrees with any
             other at all

vidyut-chandas is a THIRD VOTE ON METER IDENTITY ONLY (per locked decision 3 /
the "don't over-trust vidyut-chandas" guard) -- it has no documented
error-localization, so it never contributes problem-syllable positions and a
`None` classification from it is not itself suspect evidence.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import sanskrit_util as su  # noqa: E402

_skrutable_mi = None
_vidyut_chandas = None


def _skrutable():
    global _skrutable_mi
    if _skrutable_mi is None:
        from skrutable.meter_identification import MeterIdentifier
        _skrutable_mi = MeterIdentifier()
    return _skrutable_mi


def _vidyut(data_path=None):
    global _vidyut_chandas
    if _vidyut_chandas is None:
        from vidyut.chandas import Chandas
        if data_path is None:
            data_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', '..', '..', 'WhitneyRoots', 'scratch', 'vidyut_data', 'chandas', 'meters.tsv')
        _vidyut_chandas = Chandas(data_path) if os.path.exists(data_path) else False
    return _vidyut_chandas or None


def identify_skrutable(full_text):
    """Run skrutable on a whole verse (its resplit_lite default needs the full
    verse to locate pAda boundaries -- see gretil_walker module docstring)."""
    try:
        v = _skrutable().identify_meter(full_text)
    except Exception as e:
        return {'meter': None, 'is_perfect': None, 'error': str(e)}
    diag = getattr(v, 'diagnostic', None)
    problem = {}
    if diag is not None:
        problem = getattr(diag, 'problem_syllables', None) or {}
    is_perfect = getattr(v, 'is_perfect', None)
    if is_perfect is None:
        is_perfect = (len(problem) == 0) if diag is not None else None
    return {'meter': getattr(v, 'meter_label', None), 'is_perfect': is_perfect, 'problem_padas': problem}


def identify_chanda(lines):
    """Run chanda per physical printed line (its pada-doubling detection
    resolves multi-pada lines on its own -- pilot Method note)."""
    import chanda
    results = []
    for line in lines:
        try:
            r = chanda.analyze_line(line, fuzzy=True, k=5)
        except Exception as e:
            results.append({'line': line, 'error': str(e)})
            continue
        if r.found and r.chanda:
            names = sorted({c[0] for c in r.chanda})
            results.append({'line': line, 'match': 'exact', 'meters': names})
        elif r.fuzzy:
            best = r.fuzzy[0]
            names = sorted({c[0] for c in best.get('chanda', [])})
            clean = best.get('cost', 99) <= 2 and best.get('similarity', 0) >= 0.9
            results.append({'line': line, 'match': 'fuzzy' if clean else 'fuzzy-weak',
                             'meters': names, 'cost': best.get('cost'), 'similarity': best.get('similarity')})
        else:
            results.append({'line': line, 'match': 'none', 'meters': []})
    return results


def identify_vidyut(full_text_iast):
    vc = _vidyut()
    if vc is None:
        return {'meter': None}
    try:
        slp1 = su.to_slp1(full_text_iast)
        r = vc.classify(slp1)
        name = getattr(r, 'name', None)
        return {'meter': name}
    except BaseException as e:
        # vidyut-chandas is a Rust extension; a malformed/edge-case SLP1 string
        # can trigger a Rust panic that PyO3 surfaces as pyo3_runtime.PanicException,
        # which does NOT subclass Exception (observed 07-07-2026: "index out of
        # bounds" on a corpus verse deep in the 26k-verse batch run, which killed
        # the whole build under a plain `except Exception`). vidyut is a
        # corroborating vote only (locked decision 3) -- silently degrade to "no
        # vidyut opinion" rather than let one verse abort the entire index.
        return {'meter': None, 'error': str(e)}


def _norm_name(n):
    """Normalize one meter name to a comparable IAST key: strip skrutable's
    trailing bracket detail (`vaṁśastha [12: jtjr]` -> `vaṁśastha`) and any
    parenthetical sub-variety note, transliterate chanda's Devanagari names."""
    n = (n or '').strip().split(' (')[0].split(' [')[0].strip()
    if n and ord(n[0]) >= 0x0900:            # Devanagari (chanda's meter names)
        n = su.deva_to_iast(n)
    return n.lower().replace('ṃ', 'ṁ').rstrip('.')


def _flatten_chanda_names(raw_names):
    """chanda groups metrically-identical synonym names in one string joined
    by ' = ' (e.g. 'vasantatilakā = siṁhonnatā = uddharṣiṇī' are ALL names for
    the same pattern) and lists genuinely distinct candidates comma-separated
    by the caller's set. Splitting on '=' before normalizing means a match on
    ANY synonym counts as agreement -- comparing the raw joined string (the
    bug this replaced) made skrutable's single canonical name never match
    chanda's synonym-group string even when the first synonym was identical."""
    out = set()
    for raw in raw_names:
        for part in raw.split('='):
            norm = _norm_name(part)
            if norm:
                out.add(norm)
    return out


def verdict(skr, cha, vid):
    """3-way vote per the locked scheme (see module docstring)."""
    skr_name = _norm_name(skr.get('meter'))
    skr_ok = bool(skr.get('is_perfect'))
    cha_names = set()
    cha_clean = True
    for r in cha:
        if r.get('match') == 'exact':
            cha_names |= _flatten_chanda_names(r.get('meters', []))
        elif r.get('match') == 'fuzzy':
            cha_names |= _flatten_chanda_names(r.get('meters', []))
        elif r.get('match') == 'fuzzy-weak':
            cha_names |= _flatten_chanda_names(r.get('meters', []))
            cha_clean = False
        else:
            cha_clean = False
    vid_name = _norm_name(vid.get('meter'))

    votes = [n for n in (skr_name, vid_name) if n]
    cha_agrees = (not cha_names) or (skr_name in cha_names) if skr_name else False
    vid_agrees = (not vid_name) or (vid_name == skr_name)

    if skr_ok and cha_agrees and vid_agrees:
        return 'clean', 'skrutable perfect; chanda/vidyut agree or silent'
    if not skr_ok:
        others_disagree = (cha_names and skr_name not in cha_names) or (vid_name and vid_name != skr_name)
        if others_disagree or not cha_names:
            return 'suspect', 'skrutable imperfect scansion (%s)' % (skr.get('problem_padas') or {})
        return 'review', 'skrutable imperfect but no other tool contradicts the meter'
    if skr_name and cha_names and skr_name not in cha_names:
        return 'review', "chanda's best candidate (%s) never matches skrutable (%s)" % (
            ','.join(sorted(cha_names)), skr_name)
    if not cha_clean:
        return 'review', 'chanda needed a weak/near-tie fuzzy match (pilot Finding 2)'
    return 'clean', 'skrutable perfect; chanda/vidyut agree'


def identify_verse(verse):
    """verse: {file, locus, lines, full_text} from gretil_walker. Returns the
    full per-verse record (pilot's proposed JSON shape, extended to 3 tools)."""
    skr = identify_skrutable(verse['full_text'])
    cha = identify_chanda(verse['lines'])
    vid = identify_vidyut(verse['full_text'])
    verd, reason = verdict(skr, cha, vid)
    return {
        'source': 'GRETIL:%s' % verse['file'],
        'locus': verse['locus'],
        'full_text': verse['full_text'],
        'skrutable': skr,
        'chanda': cha,
        'vidyut': vid,
        'verdict': verd,
        'verdict_reason': reason,
    }


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    import gretil_walker as gw
    here = os.path.dirname(os.path.abspath(__file__))
    n = 0
    for v in gw.walk_corpus(os.path.join(here, '..', 'gretil_kavya_raw')):
        rec = identify_verse(v)
        print(rec['source'], rec['locus'], '->', rec['verdict'], '|', rec['verdict_reason'])
        n += 1
        if n >= 15:
            break
