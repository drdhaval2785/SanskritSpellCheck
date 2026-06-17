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

Usage:
  cd detectors && python ortho_drift.py PW           # sampled (default ~2500 entries, by stride)
  cd detectors && python ortho_drift.py PW --full    # every entry
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util

triage_util.reconfigure_stdio()
from collections import Counter, defaultdict

OUT = os.path.join(triage_util.ROOT, 'ortho_drift')
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

    drift = Counter()            # (old_lower, new, era) -> count
    drift_example = {}           # old_lower -> a short body excerpt
    pat_cand = defaultdict(Counter)   # pattern -> Counter(token -> count)
    n_tokens = 0

    for e in sample:
        toks = german_tokens(e['body'])
        n_tokens += len(toks)
        for w in toks:
            lw = w.lower()
            if lw in REFORM:
                new, era = REFORM[lw]
                drift[(lw, new, era)] += 1
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
    drift_total = sum(drift.values())
    with open(rep, 'w', encoding='utf-8') as f:
        f.write('# %s orthographic-drift pilot -- DOCUMENTATION ONLY (never edits csl-orig)\n' % dict_code)
        f.write('# %s\n' % ('FULL corpus' if full else 'SAMPLE: every %d-th entry (~%d of %d)'
                            % (max(1, len(entries) // SAMPLE_N), len(sample), len(entries))))
        f.write('# German gloss tokens scanned: %d\n' % n_tokens)
        f.write('# REFORM-MAP drift occurrences: %d (%.2f%% of tokens) in %d distinct forms\n'
                % (drift_total, 100.0 * drift_total / max(1, n_tokens), len(drift)))
        f.write('#\n# ===== CONFIRMED reform-drift (curated map; high precision) =====\n')
        f.write('# pre-reform -> 2026          era         count   example entry\n')
        for (old, new, era), c in drift.most_common():
            f.write('%-14s -> %-14s %-12s %5d   %s\n' % (old, new, era, c, drift_example.get(old, '')))
        f.write('\n# ===== PATTERN candidates (need 2026 Duden/Hunspell or the LLM pass to confirm;\n')
        f.write('#       OVER-flags: Greek "th" loans, long-vowel "ß", etc. -> NOT decided here) =====\n')
        for name, _ in PATTERNS:
            c = pat_cand[name]
            f.write('# -- %s: %d distinct candidate tokens (top 15) --\n' % (name, len(c)))
            for tok, n in c.most_common(15):
                f.write('   %-22s %4d\n' % (tok, n))

    cand = os.path.join(OUT, '%s_pattern_candidates.txt' % dict_code)
    with open(cand, 'w', encoding='utf-8') as f:
        f.write('# %s pattern candidates (token<TAB>pattern<TAB>count) -- feed to the LLM classify pass\n' % dict_code)
        seen = set()
        for name, _ in PATTERNS:
            for tok, n in pat_cand[name].most_common():
                if tok in seen:
                    continue
                seen.add(tok)
                f.write('%s\t%s\t%d\n' % (tok, name, n))

    print('%s: scanned %d German tokens in %d entries' % (dict_code, n_tokens, len(sample)))
    print('  CONFIRMED reform-drift: %d occurrences, %d distinct forms' % (drift_total, len(drift)))
    print('  top: %s' % ', '.join('%s->%s(%d)' % (o, n, c) for (o, n, e), c in drift.most_common(8)))
    print('  pattern candidates: %d distinct -> %s' % (len(seen), os.path.relpath(cand, triage_util.ROOT)))
    print('  report -> %s' % os.path.relpath(rep, triage_util.ROOT))


if __name__ == '__main__':
    main()
