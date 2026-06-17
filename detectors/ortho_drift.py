#!/usr/bin/env python3
"""ortho_drift.py -- Phase-0 pilot for the orthographic-drift study (see ../ORTHO_DRIFT_ROADMAP.md).

Scans a dictionary's GLOSS-language tokens (pilot: the German of PW) for spellings the
1901 / 1996 German orthographic reforms changed. Two signals:

  - REFORM MAP  -- a curated set of high-confidence pre-reform -> 2026 pairs (Thier->Tier,
                   daß->dass, Vocale->Vokale, ...). High precision. The headline result.
  - PATTERNS    -- recall regexes (any `th`, hard `c`, `-iren`, `ß`, `ey`). These OVER-flag
                   (Greek loans like "Theater" keep `th`; `ß` after a long vowel stays), so
                   they are written out as CANDIDATES needing a 2026 Duden/Hunspell wordlist
                   or the LLM classify pass to disambiguate -- not decided here.

This DOCUMENTS drift; it is a search-normalization / historical-linguistics layer and NEVER
edits csl-orig. Output -> ../ortho_drift/<DICT>_drift_report.txt + <DICT>_pattern_candidates.txt

The modern German reference is a Hunspell de_DE.dic (the 2006 reform ~= current Duden); see
load_modern_de() for the default path (Adobe InDesign's bundled dic) and the $ORTHO_DE_DIC
override. If it is absent the tool degrades to curated-map + patterns only.

Usage:
  cd detectors && python ortho_drift.py PW           # sampled (default ~2500 entries, by stride)
  cd detectors && python ortho_drift.py PW --full    # every entry (full PW)
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util

triage_util.reconfigure_stdio()
from collections import Counter, defaultdict

OUT = os.path.join(triage_util.ROOT, 'ortho_drift')
MAP_FILE = os.path.join(OUT, 'de_reform_map.tsv')   # persistent, expandable German reform map
SAMPLE_N = 2500

# --- German reform map: pre-reform spelling -> (2026 form, era) ------------------------------
# Conservative, textbook-certain pairs only. 1901 = II. Orthographische Konferenz; 1996 = the
# 1996/2004/2006 reform (ß->ss after a SHORT vowel only). Expand from DTA/RIDGES in the full build.
REFORM = {
    # 1901: etymological "th" -> "t" in German-origin words
    'thier': ('tier', '1901-th'), 'thiere': ('tiere', '1901-th'),
    'theil': ('teil', '1901-th'), 'theile': ('teile', '1901-th'), 'theils': ('teils', '1901-th'),
    'thal': ('tal', '1901-th'), 'thor': ('tor', '1901-th'), 'thür': ('tür', '1901-th'),
    'thurm': ('turm', '1901-th'), 'thau': ('tau', '1901-th'), 'thun': ('tun', '1901-th'),
    'gethan': ('getan', '1901-th'), 'muth': ('mut', '1901-th'), 'roth': ('rot', '1901-th'),
    'noth': ('not', '1901-th'), 'werth': ('wert', '1901-th'), 'rath': ('rat', '1901-th'),
    'wuth': ('wut', '1901-th'), 'blüthe': ('blüte', '1901-th'),
    # 1901: giebt->gibt; c->k/z in loans
    'giebt': ('gibt', '1901'), 'vocal': ('vokal', '1901-c'), 'vocale': ('vokale', '1901-c'),
    'capitel': ('kapitel', '1901-c'), 'cur': ('kur', '1901-c'), 'cultus': ('kultus', '1901-c'),
    'litteratur': ('literatur', '1901'), 'accent': ('akzent', '1901-c'),
    # archaic "ey" -> "ei"
    'seyn': ('sein', 'archaic-ey'), 'sey': ('sei', 'archaic-ey'), 'seyd': ('seid', 'archaic-ey'),
    # 1996: ß -> ss after a SHORT vowel (Straße/groß/Fuß keep ß -- not listed)
    'daß': ('dass', '1996-ss'), 'muß': ('muss', '1996-ss'), 'fluß': ('fluss', '1996-ss'),
    'schluß': ('schluss', '1996-ss'), 'genuß': ('genuss', '1996-ss'), 'nuß': ('nuss', '1996-ss'),
    'gewiß': ('gewiss', '1996-ss'), 'häßlich': ('hässlich', '1996-ss'), 'läßt': ('lässt', '1996-ss'),
    'paßt': ('passt', '1996-ss'), 'faßt': ('fasst', '1996-ss'),
    # period German that drifted (the "Dintenfass" gloss in PW)
    'dinte': ('tinte', '1901-th-adjacent'), 'dintenfass': ('tintenfass', '1996-ss'),
}


def load_reform_map(seed):
    """The curated seed merged with the persistent, corpus-accumulated map (MAP_FILE). The file
    is the expandable lexicon: each run folds its transform+dic-confirmed drift back into it, and
    DTA/RIDGES historical->modern pairs can be merged into it when available."""
    m = dict(seed)
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, encoding='utf-8') as f:
            for ln in f:
                if ln.startswith('#') or '\t' not in ln:
                    continue
                p = ln.rstrip('\n').split('\t')
                if len(p) >= 3 and p[0]:
                    m[p[0]] = (p[1], p[2])
    return m

# --- recall patterns (candidates only -- need wordlist/LLM to confirm) -----------------------
PATTERNS = [
    ('th', re.compile(r'th', re.I)),
    ('c-hard', re.compile(r'c[aoulr]', re.I)),
    ('-iren', re.compile(r'ir(?:en|t|te|st)$', re.I)),
    ('ss-eszett', re.compile(r'ß')),
    ('ey', re.compile(r'ey', re.I)),
]
# Greek/Latin-origin words that KEEP "th" in 2026 -> not drift (pilot stop-list; extend).
GREEK_TH = set((
    'theater thema themen theorie theologie theolog mathematik apotheke bibliothek rhythmus '
    'thron äther methode katholisch pathos epitheton mythos mythus orthographie sympathie '
    'theil'  # placeholder guard removed below
).split())
GREEK_TH.discard('theil')

# --- gloss tokenizer -------------------------------------------------------------------------
# Pilot finding: PW glosses embed editorial-correction records {{old->new||date|editor|url|}}
# and <bot>Latin species</bot> spans -- both leak non-German noise (github, editor names,
# botanical Latin) into the token stream, so strip them before tokenizing.
_SKT = re.compile(r'\{#.*?#\}|\{@.*?@\}', re.S)      # Sanskrit spans -> drop
_ANNO = re.compile(r'\{\{.*?\}\}', re.S)             # {{old->new||date|editor|github-url|}} -> drop
_BOT = re.compile(r'<bot>.*?</bot>', re.S | re.I)    # botanical Latin species names -> drop (not German)
_LS = re.compile(r'<ls>.*?</ls>', re.S | re.I)       # literary-source sigla -> drop
_ITAL = re.compile(r'\{%(.*?)%\}', re.S)             # italic (German glosses live here) -> unwrap
_TAG = re.compile(r'<[^>]+>')
_WORD = re.compile(r'[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß]{2,}')
# grammatical / source / editorial abbreviations that are not German lexical words
# (compared case-insensitively -- Latin abbrevs appear capitalised, e.g. "Caus.", "Comm.")
_ABBR = set('adj subst sing plur nom gen dat acc voc loc instr comp conj praep partic '
            'masc fem neutr vgl ibid cit seq fol vol cap caus comm com compar act med '
            'pass lexicon adv adj praet'.split())


def clean_gloss(body):
    t = _SKT.sub(' ', body)
    t = _ANNO.sub(' ', t)
    t = _BOT.sub(' ', t)
    t = _LS.sub(' ', t)
    t = _ITAL.sub(r' \1 ', t)
    return _TAG.sub(' ', t)


def german_tokens(body):
    out = []
    for w in _WORD.findall(clean_gloss(body)):
        if w.lower() in _ABBR or w.isupper():   # drop sigla (RV, AV, P) and grammatical abbrevs
            continue
        out.append(w)
    return out


# --- modern German word-list (Hunspell de_DE) + reform transforms --------------------------
# The 2006-reform Hunspell de_DE.dic ~= current Duden orthography. A LOCAL dependency (NOT
# committed; Adobe InDesign bundles it). Override the path with $ORTHO_DE_DIC. The Adobe
# "1901/1996/2006" variants are modern dicts differing only in the 1996 ss-rule -- they do NOT
# contain 19th-c. forms -- so drift is found by TRANSFORM-AND-CHECK: apply a reform rule to a
# token and accept it as drift iff the transformed form IS in the modern dic and the original is
# NOT (Thier->Tier is in the dic = drift; Theater->Teater is not = a Greek loan, not drift).
_DEFAULT_DE_DIC = (r'C:\Program Files\Adobe\Adobe InDesign 2026\Resources\Dictionaries\LILO'
                   r'\Linguistics\Providers\Plugins2\AdobeHunspellPlugin\Dictionaries\de_DE\de_DE.dic')


def load_modern_de(path=None):
    """Lowercased stem set of the modern German Hunspell dic; None if unavailable."""
    path = path or os.environ.get('ORTHO_DE_DIC') or _DEFAULT_DE_DIC
    if not os.path.exists(path):
        return None
    with open(path, encoding='latin-1') as f:
        lines = f.read().splitlines()
    return set(ln.split('/')[0].strip().lower() for ln in lines[1:] if ln.strip())


def reform_transforms(w):
    """(era, modern_candidate) pairs from applying each reform rule to a lowercased token."""
    out = []
    if 'th' in w:
        out.append(('1901-th', w.replace('th', 't')))
    if re.search(r'c[aoulr]', w):
        out.append(('1901-c', re.sub(r'c([aoulr])', r'k\1', w)))
    if re.search(r'c[eiy]', w):
        out.append(('1901-c', re.sub(r'c([eiy])', r'z\1', w)))
    if re.search(r'ir(en|t|te|st|end)$', w):
        out.append(('1901-iren', re.sub(r'ir(en|t|te|st|end)$', r'ier\1', w)))
    if 'ß' in w:
        out.append(('1996-ss', w.replace('ß', 'ss')))
    if 'ey' in w:
        out.append(('archaic-ey', w.replace('ey', 'ei')))
    if re.search(r'c[eiy]', w) and re.search(r'ir(en|t|te)$', w):   # combined (recitiren->rezitieren)
        t = re.sub(r'c([eiy])', r'z\1', w)
        out.append(('1901-c-iren', re.sub(r'ir(en|t|te)$', r'ier\1', t)))
    return out


def main():
    dict_code = triage_util.dict_arg('PW')
    full = '--full' in sys.argv[2:]
    idx = triage_util.build_entry_index(triage_util.csl_root(), dict_code)
    if idx is None:
        print('no csl-orig source for %s' % dict_code)
        sys.exit(1)
    entries = [e for lst in idx.by_k1.values() for e in lst]
    entries.sort(key=lambda e: int(e['lineno']))
    if full:
        sample = entries
    else:
        step = max(1, len(entries) // SAMPLE_N)
        sample = entries[::step]

    modern = load_modern_de()
    reform = load_reform_map(REFORM)
    drift = Counter()            # reform-map drift:     (old, new, era) -> count
    dicdrift = Counter()         # transform+dic drift:  (old, new, era) -> count
    drift_example = {}
    pat_cand = defaultdict(Counter)
    n_tokens = n_modern = 0

    for e in sample:
        for w in german_tokens(e['body']):
            n_tokens += 1
            lw = w.lower()
            if modern is not None and lw in modern:
                n_modern += 1                        # already 2026-modern German -> not drift
                continue
            if lw in reform:
                new, era = reform[lw]
                drift[(lw, new, era)] += 1
                drift_example.setdefault(lw, ' '.join(clean_gloss(e['body']).split())[:90])
                continue
            if modern is not None:
                hit = next(((c, era) for era, c in reform_transforms(lw) if c != lw and c in modern), None)
                if hit:
                    dicdrift[(lw, hit[0], hit[1])] += 1
                    drift_example.setdefault(lw, ' '.join(clean_gloss(e['body']).split())[:90])
                    continue
            for name, rx in PATTERNS:
                if name == 'th' and (lw in GREEK_TH or 'sch' in lw):
                    continue
                if name == 'c-hard' and ('ch' in lw or 'ck' in lw or 'sch' in lw):
                    continue
                if rx.search(w):
                    pat_cand[name][lw] += 1

    os.makedirs(OUT, exist_ok=True)
    rep = os.path.join(OUT, '%s_drift_report.txt' % dict_code)
    drift_total, dic_total = sum(drift.values()), sum(dicdrift.values())
    with open(rep, 'w', encoding='utf-8') as f:
        f.write('# %s orthographic-drift -- DOCUMENTATION ONLY (never edits csl-orig)\n' % dict_code)
        f.write('# %s\n' % ('FULL corpus' if full else 'SAMPLE: every %d-th entry (~%d of %d)'
                            % (max(1, len(entries) // SAMPLE_N), len(sample), len(entries))))
        f.write('# modern word-list: %s\n'
                % ('Hunspell de_DE 2006, %d stems' % len(modern) if modern is not None
                   else 'NOT WIRED (set $ORTHO_DE_DIC) -- curated map + patterns only'))
        f.write('# German gloss tokens: %d ; already-2026-modern: %d ; reform-drift: %d '
                '(dic-confirmed %d + map %d)\n'
                % (n_tokens, n_modern, drift_total + dic_total, dic_total, drift_total))
        f.write('#\n# ===== reform-drift CONFIRMED by transform + modern Hunspell dic =====\n')
        f.write('# pre-reform -> 2026             era          count  example entry\n')
        for (old, new, era), c in dicdrift.most_common():
            f.write('%-18s -> %-18s %-12s %4d  %s\n' % (old, new, era, c, drift_example.get(old, '')))
        f.write('\n# ===== reform-drift from the curated map (incl. inflected forms) =====\n')
        for (old, new, era), c in drift.most_common():
            f.write('%-18s -> %-18s %-12s %4d  %s\n' % (old, new, era, c, drift_example.get(old, '')))
        f.write('\n# ===== RESIDUAL pattern candidates (not modern, not transform-confirmable;\n')
        f.write('#       inflected drift / foreign / names / fragments -> the LLM pass) =====\n')
        for name, _ in PATTERNS:
            c = pat_cand[name]
            f.write('# -- %s: %d distinct (top 15) --\n' % (name, len(c)))
            for tok, n in c.most_common(15):
                f.write('   %-22s %4d\n' % (tok, n))

    cand = os.path.join(OUT, '%s_pattern_candidates.txt' % dict_code)
    with open(cand, 'w', encoding='utf-8') as f:
        f.write('# %s RESIDUAL pattern candidates (token<TAB>pattern<TAB>count) -- not modern + not '
                'transform-confirmable; feed to the LLM classify pass\n' % dict_code)
        seen = set()
        for name, _ in PATTERNS:
            for tok, n in pat_cand[name].most_common():
                if tok in seen:
                    continue
                seen.add(tok)
                f.write('%s\t%s\t%d\n' % (tok, name, n))

    # accumulate the discovered drift into the persistent map -- the expanded reform lexicon
    acc = dict(reform)
    for (old, new, era) in list(dicdrift) + list(drift):
        acc[old] = (new, era)
    with open(MAP_FILE, 'w', encoding='utf-8') as f:
        f.write('# German orthographic reform map:  old<TAB>2026<TAB>era\n')
        f.write('# Curated seed + drift mined from the corpus (transform + Hunspell-confirmed).\n')
        f.write('# Expandable -- merge DTA/RIDGES historical->modern pairs here. %d forms.\n' % len(acc))
        for old in sorted(acc):
            new, era = acc[old]
            f.write('%s\t%s\t%s\n' % (old, new, era))

    print('%s: %d German tokens in %d entries; modern-filtered %d%s'
          % (dict_code, n_tokens, len(sample), n_modern,
             '' if modern is not None else ' (Hunspell NOT wired)'))
    print('  reform-drift: %d  (dic-confirmed %d in %d forms + map %d in %d forms)'
          % (drift_total + dic_total, dic_total, len(dicdrift), drift_total, len(drift)))
    print('  top dic-confirmed: %s'
          % ', '.join('%s->%s(%d)' % (o, n, c) for (o, n, e), c in dicdrift.most_common(8)))
    print('  residual candidates: %d distinct -> %s' % (len(seen), os.path.relpath(cand, triage_util.ROOT)))
    print('  report -> %s' % os.path.relpath(rep, triage_util.ROOT))


if __name__ == '__main__':
    main()
