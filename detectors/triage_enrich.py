#!/usr/bin/env python3
"""triage_enrich.py -- attach deterministic evidence to tier-A correction candidates.

The unified engine's tier-A list mixes genuine typos with legitimate variant /
inflected / Vedic forms it cannot tell apart (e.g. `atrA`, `vAcas`, `prAvft`). This
script attaches, per candidate, the evidence a human (or an LLM adjudicator) needs to
separate the two -- WITHOUT looking at the scan:

  - k2 field         the dictionary's own key-2 (often accented): a `<k2>` carrying an
                     accent mark (/ \\ ^) on the disputed long vowel is editorial proof
                     the long spelling is intended -> the "correction" is likely wrong.
  - DCS bands        frequency band (0..5) of the SUSPECT and the SUGGESTION as DCS
                     lemmas. Suggestion attested + suspect not -> typo signal. Suspect
                     attested at band >=3 -> it is a real corpus word -> likely NOT a typo.
  - cross-dict count how many independent Cologne dicts carry the suspect form. Many
                     dicts agreeing on a spelling -> more likely a real variant.
  - confusion class  which single-char confusion (vowel-length / aspiration / sibilant /
                     retroflex-dental / nasal / v-b) + its empirical weight.
  - known-real flag  whether this exact pair is in the 3884 human-curated o_vs_O2 pairs
                     (historically confirmed real) -- a strong FILE prior + the
                     calibration ground truth.

Output: corrections_draft/MW/MW_evidence.jsonl (one JSON object per candidate) plus a
provisional deterministic bucket (FILE / DROP / GRAY) used only to prioritise -- the
LLM adjudication + adversarial verify + human scan check are the real decision.

Usage:
    cd detectors && python triage_enrich.py            # MW (default)
    cd detectors && python triage_enrich.py PW         # another dict, if a package exists
"""
import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import slp1util as u

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --- confusion classification ---------------------------------------------
_CLASS = {}
for _grp, _name in (
    ("aA iI uU fF xX", "vowel-length"),
    ("eE oO", "diphthong"),
    ("kK gG cC jJ wW qQ tT dD pP bB", "aspiration"),
    ("sS sz Sz", "sibilant"),
    ("tw TW dq DQ nR", "retroflex-dental"),
    ("nm nN nY mN mY mR NY NR YR", "nasal"),
    ("bv Bv", "v-b"),
):
    for _p in _grp.split():
        _CLASS[frozenset(_p)] = _name


def classify(a, b):
    """Return (confusion_class, pair_str) for suspect a vs suggestion b."""
    if len(a) != len(b):
        # an insertion/deletion: usually a trailing length/ending change
        return "length-change", None
    diff = [(x, y) for x, y in zip(a, b) if x != y]
    if len(diff) != 1:
        return "multi", None
    pr = diff[0]
    return _CLASS.get(frozenset(pr), "other"), ''.join(sorted(pr))


# --- k2 parsing ------------------------------------------------------------
_K2 = re.compile(r'<k2>([^<]*)')
_K1 = re.compile(r'<k1>([^<]*)')
_ACCENT = re.compile(r'[/\\^]')


def load_draft(path):
    """Map suspect headword -> {lineno, k1, k2, src} from an MW_draft.txt `old` line.

    Draft block:  `; Case N.  SUSPECT -> SUGG  scan=...`
                  `LINENO old <...>`
                  `LINENO new <...>`
    """
    out = {}
    cur = None
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r';\s*Case\s+\d+\.\s+(\S+)\s+->\s+(\S+)', line)
            if m:
                cur = m.group(1)
                continue
            m = re.match(r'(\d+)\s+old\s+(.*)', line)
            if m and cur is not None:
                src = m.group(2)
                k2 = _K2.search(src)
                k1 = _K1.search(src)
                out[cur] = {
                    'lineno': int(m.group(1)),
                    'k1': k1.group(1) if k1 else None,
                    'k2': k2.group(1) if k2 else None,
                    'src': src.strip(),
                }
                cur = None
    return out


# --- candidate parsing -----------------------------------------------------
def load_candidates(path):
    cands = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            score = int(parts[0])
            m = re.match(r'(\S+)\s+->\s+(\S+)', parts[1])
            if not m:
                continue
            suspect, sugg = m.group(1), m.group(2)
            dets = parts[2].strip('[]')
            detectors = [d for d in dets.split(',') if d]
            morph = len(parts) > 3 and 'morph' in parts[3]
            cands.append({'score': score, 'suspect': suspect,
                          'suggestion': sugg, 'detectors': detectors,
                          'morph': morph})
    return cands


def load_ndicts(sanhw_path):
    """suspect headword -> sorted list of dicts that contain it."""
    idx = {}
    for hw, dicts in u.parse_sanhw1(sanhw_path):
        idx[hw] = dicts
    return idx


def provisional(ev):
    """Conservative deterministic bucket -- a PRIOR for prioritisation, not a verdict."""
    s_band = ev['dcs_suspect_band']
    g_band = ev['dcs_sugg_band']
    nd = ev['ndicts']
    k2_conf = ev['k2_confirms_suspect']
    if ev['known_real']:
        return 'FILE', 'in the 3884 human-curated o_vs_O pairs (historically confirmed)'
    if k2_conf:
        return 'DROP', 'k2 markup (accent/hyphen) confirms the suspect long/disputed form is editorial'
    if s_band >= 3:
        return 'DROP', 'suspect is a DCS corpus lemma band>=%d (a real word)' % s_band
    if g_band >= 3 and s_band == 0 and nd <= 1:
        return 'FILE', 'suggestion is a DCS lemma band>=%d, suspect unattested, single dict' % g_band
    if nd >= 4 and s_band >= 1:
        return 'DROP', 'in %d dicts and DCS-attested -> likely a real variant' % nd
    return 'GRAY', 'mixed/weak signals -- needs lexical judgment'


def main():
    dict_code = sys.argv[1] if len(sys.argv) > 1 else 'MW'
    pkg = os.path.join(ROOT, 'corrections_draft', dict_code)
    cand_path = os.path.join(pkg, '%s_candidates.txt' % dict_code)
    draft_path = os.path.join(pkg, '%s_draft.txt' % dict_code)
    out_path = os.path.join(pkg, '%s_evidence.jsonl' % dict_code)

    cands = load_candidates(cand_path)
    draft = load_draft(draft_path) if os.path.exists(draft_path) else {}
    dcs = u.load_dcs_lemmas(u.dcs_path())
    weights = u.load_confusion_weights()
    ndicts = load_ndicts(os.path.join(ROOT, 'sanhw1.txt'))
    # historical ground-truth pairs (reuse eval.py's source)
    known = set()
    kp = os.path.join(ROOT, 'o_vs_O', 'o_vs_O2.txt')
    if os.path.exists(kp):
        for line in u._read_words(kp):
            if ':' in line:
                w1 = line.split(':', 1)[0]
                w2 = line.split(':', 1)[1].split('-', 1)[0]
                if w1 and w2 and w1 != w2:
                    known.add(frozenset((w1, w2)))

    def band(w):
        return dcs.get(u.normalize_lemma(w), 0)

    rows = []
    for c in cands:
        suspect, sugg = c['suspect'], c['suggestion']
        cls, pair = classify(suspect, sugg)
        d = draft.get(suspect, {})
        k2 = d.get('k2')
        k2_acc = bool(k2 and _ACCENT.search(k2))
        k2_clean = _ACCENT.sub('', k2).replace('-', '') if k2 else None
        ev = {
            'suspect': suspect,
            'suggestion': sugg,
            'score': c['score'],
            'detectors': c['detectors'],
            'n_detectors': len(c['detectors']),
            'morph_ok': c['morph'],
            'confusion_class': cls,
            'confusion_pair': pair,
            'confusion_weight': round(u.confusion_weight(suspect, sugg, weights), 4) if pair else 0.0,
            'dcs_suspect_band': band(suspect),
            'dcs_sugg_band': band(sugg),
            'ndicts': len(ndicts.get(suspect, [])),
            'dicts': ndicts.get(suspect, [])[:12],
            'k2_raw': k2,
            'k2_has_accent': k2_acc,
            'k2_has_hyphen': bool(k2 and '-' in k2),
            # k2 reduces to the suspect but carries extra editorial markup (accent
            # mark or a morpheme-boundary hyphen) -> the long/disputed spelling is
            # deliberate (e.g. a/-trA, prA-vft). A plain duplicate k2 == suspect is NOT.
            'k2_confirms_suspect': bool(k2 is not None and k2 != suspect and k2_clean == suspect),
            'lineno': d.get('lineno'),
            'located': suspect in draft,
            'known_real': frozenset((suspect, sugg)) in known,
        }
        bucket, reason = provisional(ev)
        ev['provisional'] = bucket
        ev['provisional_reason'] = reason
        rows.append(ev)

    with open(out_path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # split into small per-batch files so each adjudication agent reads one whole
    # file (no line-offset math, no giant args/returns).
    BATCH = 30
    work = os.path.join(pkg, 'triage_work')
    os.makedirs(work, exist_ok=True)
    nbatch = 0
    for i in range(0, len(rows), BATCH):
        with open(os.path.join(work, 'batch_%03d.jsonl' % (i // BATCH)), 'w', encoding='utf-8') as f:
            for r in rows[i:i + BATCH]:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        nbatch += 1

    # --- summary --------------------------------------------------------
    from collections import Counter
    prov = Counter(r['provisional'] for r in rows)
    cls = Counter(r['confusion_class'] for r in rows)
    print("%s tier-A candidates enriched: %d" % (dict_code, len(rows)))
    print("wrote %s" % os.path.relpath(out_path, ROOT))
    print("split into %d batch files of %d in %s" % (nbatch, BATCH, os.path.relpath(work, ROOT)))
    print("\nprovisional buckets (deterministic prior):")
    for b in ('FILE', 'GRAY', 'DROP'):
        print("  %-5s %5d" % (b, prov.get(b, 0)))
    print("\nconfusion classes:")
    for k, n in cls.most_common():
        print("  %-18s %5d" % (k, n))
    print("\nDCS evidence:")
    print("  suspect attested  (band>=1): %5d" % sum(1 for r in rows if r['dcs_suspect_band']))
    print("  suspect band>=3 (real word): %5d" % sum(1 for r in rows if r['dcs_suspect_band'] >= 3))
    print("  suggestion attested:         %5d" % sum(1 for r in rows if r['dcs_sugg_band']))
    print("  k2 confirms suspect:         %5d" % sum(1 for r in rows if r['k2_confirms_suspect']))
    print("  in historical o_vs_O pairs:  %5d" % sum(1 for r in rows if r['known_real']))


if __name__ == '__main__':
    main()
