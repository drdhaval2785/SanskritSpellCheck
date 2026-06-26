#!/usr/bin/env python3
"""ortho_drift.py -- orthographic-drift scan over a dictionary's GLOSS language (see
../ORTHO_DRIFT_ROADMAP.md). Multi-language, profile-driven:

  de  German  (PW/PWG/GRA/CCS/SCH, csl-orig) -- 1901 th->t / c->k|z / -iren, 1996 ss; Hunspell de_DE.
  fr  French  (BUR/STC, csl-orig)            -- minor (pre-1935 / 1990); Hunspell fr_FR membership.
  la  Latin   (BOP, csl-orig)                -- NEGATIVE CONTROL: no reform, no wordlist -> ~0 drift.
  ru  Russian (Kossovich, SamudraManthanam jsonl) -- 1918 reform; WORDLIST-FREE (the abolished
              letters i/yat/fita/izhitsa + word-final hard-sign are pre-1918 by definition).

Drift is found by TRANSFORM-AND-CHECK: apply a reform rule to a flagged token and accept it as
drift iff the transformed form is in the modern wordlist and the original is not (Thier->Tier in
the dic = drift; Theater->Teater not = a Greek loan). For wordlist-free languages (ru) the rule is
definitional, so any token a transform changes is drift. DOCUMENTATION ONLY; never edits sources.

Outputs -> ../ortho_drift/<DICT>_drift_report.txt + <DICT>_pattern_candidates.txt;
the per-language reform lexicon accumulates in <lang>_reform_map.tsv; cross-dict comparison in
<lang>_drift_summary.tsv. Hunspell dics are LOCAL deps (Adobe InDesign bundle / $ORTHO_<L>_DIC),
not committed; if absent the tool degrades to curated-map + patterns only.

Usage:
  cd detectors && python ortho_drift.py PW            # sampled (default ~2500 entries, by stride)
  cd detectors && python ortho_drift.py BUR --full    # every entry (BUR=French, BOP=Latin, ...)
  cd detectors && python ortho_drift.py KOSSOVICH --full   # Russian (jsonl source)
"""
import sys
import os
import re
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util

triage_util.reconfigure_stdio()
from collections import Counter, defaultdict

OUT = os.path.join(triage_util.ROOT, 'ortho_drift')
SAMPLE_N = 2500

# Typographic substitutions that are NOT orthographic reform: the æ/œ ligature
# (mediæval->medieval, æther->ether) is a print-shop convention, not a dated/legislated
# spelling change. It is still counted + reported as its own era column, but it is
# EXCLUDED from the headline reform-drift/1k rate so it doesn't inflate the gradient
# (it dominated several EN dicts: SHS 109, MW72 92, AP90 39). See ORTHO_DRIFT_FINDINGS.md.
NONREFORM_ERAS = {'ligature'}
_ADOBE = (r'C:\Program Files\Adobe\Adobe InDesign 2026\Resources\Dictionaries\LILO'
          r'\Linguistics\Providers\Plugins2\AdobeHunspellPlugin\Dictionaries')


# Hunspell .dic resolution: $ORTHO_<L>_DIC env var (checked in load_wordlist) wins; else the
# Adobe InDesign bundle if present; else a locally-staged copy under external_src/hunspell/
# (gitignored — e.g. en_GB.dic from github.com/ropensci/hunspell inst/dict). All local deps.
_HUNSPELL_LOCAL = os.path.join(triage_util.ROOT, 'external_src', 'hunspell')


def _dic(lang):
    adobe = os.path.join(_ADOBE, lang, lang + '.dic')
    if os.path.exists(adobe):
        return adobe
    return os.path.join(_HUNSPELL_LOCAL, lang + '.dic')


# --- csl-orig gloss tokenizer (shared by de/fr/la) -------------------------------------------
# PW-style glosses embed editorial-correction records {{old->new||date|editor|url|}} and
# <bot>Latin species</bot> spans -- strip them so they don't leak into the token stream.
_SKT = re.compile(r'\{#.*?#\}|\{@.*?@\}', re.S)      # Sanskrit spans -> drop
_ANNO = re.compile(r'\{\{.*?\}\}', re.S)             # {{old->new||date|editor|github-url|}} -> drop
_BOT = re.compile(r'<bot>.*?</bot>', re.S | re.I)    # botanical Latin species -> drop
_LS = re.compile(r'<ls>.*?</ls>', re.S | re.I)       # literary-source sigla -> drop
_S = re.compile(r'<s>.*?</s>', re.S | re.I)          # <s>SLP1</s> Sanskrit (MW etc.) -> drop
_ITAL = re.compile(r'\{%(.*?)%\}', re.S)             # italic gloss -> unwrap
_TAG = re.compile(r'<[^>]+>')
_DEVA = re.compile(r'[ऀ-ॿ]+')              # Devanagari -> drop (ru jsonl carries it)


def clean_gloss(body):
    t = _SKT.sub(' ', body)
    t = _ANNO.sub(' ', t)
    t = _BOT.sub(' ', t)
    t = _LS.sub(' ', t)
    t = _S.sub(' ', t)
    t = _ITAL.sub(r' \1 ', t)
    t = _TAG.sub(' ', t)
    return _DEVA.sub(' ', t)


# ============================ German (de) ============================
DE_REFORM = {
    'thier': ('tier', '1901-th'), 'thiere': ('tiere', '1901-th'),
    'theil': ('teil', '1901-th'), 'theile': ('teile', '1901-th'), 'theils': ('teils', '1901-th'),
    'thal': ('tal', '1901-th'), 'thor': ('tor', '1901-th'), 'thür': ('tür', '1901-th'),
    'thurm': ('turm', '1901-th'), 'thau': ('tau', '1901-th'), 'thun': ('tun', '1901-th'),
    'gethan': ('getan', '1901-th'), 'muth': ('mut', '1901-th'), 'roth': ('rot', '1901-th'),
    'noth': ('not', '1901-th'), 'werth': ('wert', '1901-th'), 'rath': ('rat', '1901-th'),
    'wuth': ('wut', '1901-th'), 'blüthe': ('blüte', '1901-th'),
    'giebt': ('gibt', '1901'), 'vocal': ('vokal', '1901-c'), 'vocale': ('vokale', '1901-c'),
    'capitel': ('kapitel', '1901-c'), 'cur': ('kur', '1901-c'), 'cultus': ('kultus', '1901-c'),
    'litteratur': ('literatur', '1901'), 'accent': ('akzent', '1901-c'),
    'seyn': ('sein', 'archaic-ey'), 'sey': ('sei', 'archaic-ey'), 'seyd': ('seid', 'archaic-ey'),
    'daß': ('dass', '1996-ss'), 'muß': ('muss', '1996-ss'), 'fluß': ('fluss', '1996-ss'),
    'schluß': ('schluss', '1996-ss'), 'genuß': ('genuss', '1996-ss'), 'nuß': ('nuss', '1996-ss'),
    'gewiß': ('gewiss', '1996-ss'), 'häßlich': ('hässlich', '1996-ss'), 'läßt': ('lässt', '1996-ss'),
    'paßt': ('passt', '1996-ss'), 'faßt': ('fasst', '1996-ss'),
    'dinte': ('tinte', '1901-th-adjacent'), 'dintenfass': ('tintenfass', '1996-ss'),
}
DE_GREEK_TH = set(('theater thema themen theorie theologie theolog mathematik apotheke bibliothek '
                   'rhythmus thron äther methode katholisch pathos epitheton mythos mythus '
                   'orthographie sympathie').split())


def de_transforms(w):
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
    if re.search(r'c[eiy]', w) and re.search(r'ir(en|t|te)$', w):
        t = re.sub(r'c([eiy])', r'z\1', w)
        out.append(('1901-c-iren', re.sub(r'ir(en|t|te)$', r'ier\1', t)))
    return out


def de_pattern_skip(name, lw):
    if name == 'th':
        return lw in DE_GREEK_TH or 'sch' in lw
    if name == 'c-hard':
        return 'ch' in lw or 'ck' in lw or 'sch' in lw
    return False


# ============================ French (fr) ============================
FR_REFORM = {
    'poëte': ('poète', 'trema'), 'poëme': ('poème', 'trema'), 'poësie': ('poésie', 'trema'),
    'phantaisie': ('fantaisie', 'ph-f'), 'rhythme': ('rythme', 'ph-f'),
    'étoit': ('était', 'oi-ai'), 'étoient': ('étaient', 'oi-ai'), 'avoit': ('avait', 'oi-ai'),
    'françois': ('français', 'oi-ai'), 'connoit': ('connaît', 'oi-ai'),
}


def fr_transforms(w):
    out = []
    if 'oë' in w:
        out.append(('trema', w.replace('oë', 'oè')))
    if 'aë' in w:
        out.append(('trema', w.replace('aë', 'aé')))
    if re.search(r'oi(s|t|ent|x)?$', w):                 # archaic imperfect/cond. -oi- -> -ai-
        out.append(('oi-ai', re.sub(r'oi((?:s|t|ent|x)?)$', r'ai\1', w)))
    if w.startswith('ph'):
        out.append(('ph-f', 'f' + w[2:]))
    return out


# ============================ English (en) -- convention drift, no legislated reform =========
# Reference = en_GB (British: these are British/Indian-English dicts, so honour/-ise/-re are
# CORRECT, not drift). Curated map = irregular archaic forms; transforms = rule-derivable classes,
# all dic-guarded (e.g. complexion->complection is rejected; connexion->connection kept).
EN_REFORM = {
    'shew': ('show', 'archaic'), 'shews': ('shows', 'archaic'), 'shewn': ('shown', 'archaic'),
    'shewing': ('showing', 'archaic'), 'gulph': ('gulf', 'archaic'), 'cloathing': ('clothing', 'archaic'),
    'controul': ('control', 'archaic'), 'compleat': ('complete', 'archaic'), 'ancle': ('ankle', 'archaic'),
    'chace': ('chase', 'archaic'), 'cyder': ('cider', 'archaic'), 'sceptic': ('sceptic', 'archaic'),
}
EN_REFORM.pop('sceptic', None)   # sceptic is current British -- guard against accidental entry


def en_transforms(w):
    out = []
    if w.endswith('xion'):                       # connexion->connection, inflexion->inflection
        out.append(('xion', w[:-4] + 'ction'))
    if 'æ' in w:                                 # mediæval -> medieval / mediaeval
        out.append(('ligature', w.replace('æ', 'e')))
        out.append(('ligature', w.replace('æ', 'ae')))
    if 'œ' in w:
        out.append(('ligature', w.replace('œ', 'e')))
        out.append(('ligature', w.replace('œ', 'oe')))
    if w.endswith('ick') and len(w) > 4:         # musick->music (brick->bric rejected by the dic)
        out.append(('ick', w[:-3] + 'ic'))
    return out


# ============================ Russian (ru) -- 1918, WORDLIST-FREE ============================
_RU_1918 = [('ѣ', 'е'), ('Ѣ', 'Е'), ('і', 'и'), ('І', 'И'), ('ѳ', 'ф'), ('Ѳ', 'Ф'),
            ('ѵ', 'и'), ('Ѵ', 'И')]


def ru_transforms(w):
    m = w
    for old, new in _RU_1918:
        m = m.replace(old, new)
    m = re.sub(r'ъ$', '', m)            # word-final hard sign abolished (домъ -> дом)
    if m == w:
        return []
    # tag by the letter that drove it (for the summary)
    era = ('1918-yat' if ('ѣ' in w or 'Ѣ' in w) else '1918-i' if ('і' in w or 'І' in w)
           else '1918-fita' if ('ѳ' in w or 'Ѳ' in w) else '1918-izhitsa' if ('ѵ' in w or 'Ѵ' in w)
           else '1918-hardsign')
    return [(era, m)]


PROFILES = {
    'de': dict(name='German', source='csl', wordlist=_dic('de_DE'), wordlist_env='ORTHO_DE_DIC',
               enc='latin-1', seed=DE_REFORM, transforms=de_transforms, skip=de_pattern_skip,
               word=re.compile(r'[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß]{2,}'),
               abbr=set('adj subst sing plur nom gen dat acc voc loc instr comp conj praep partic '
                        'masc fem neutr vgl ibid cit seq fol vol cap caus comm com compar act med '
                        'pass lexicon adv praet'.split()),
               patterns=[('th', re.compile(r'th', re.I)), ('c-hard', re.compile(r'c[aoulr]', re.I)),
                         ('-iren', re.compile(r'ir(?:en|t|te|st)$', re.I)), ('ss-eszett', re.compile(r'ß')),
                         ('ey', re.compile(r'ey', re.I))],
               canon=['1901-th', '1901-c', '1901-c-iren', '1901-iren', '1996-ss', 'archaic-ey'],
               wordlist_free=False),
    'fr': dict(name='French', source='csl', wordlist=_dic('fr_FR'), wordlist_env='ORTHO_FR_DIC',
               enc='utf-8', seed=FR_REFORM, transforms=fr_transforms, skip=None,
               word=re.compile(r'[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ]{2,}'),
               abbr=set('adj subst masc fem pron nom acc gén dat voc sm sf adv conj prép part '
                        'litt fig pop voy cf ibid sanscr védique'.split()),
               patterns=[('trema', re.compile(r'[ëï]')), ('oi', re.compile(r'oi(s|t|ent|x)?$')),
                         ('ph', re.compile(r'^ph'))],
               canon=['oi-ai', 'trema', 'ph-f'], wordlist_free=False),
    'en': dict(name='English', source='csl', wordlist=_dic('en_GB'), wordlist_env='ORTHO_EN_DIC',
               enc='latin-1', seed=EN_REFORM, transforms=en_transforms, skip=None,
               word=re.compile(r'[A-Za-zÆæŒœ][A-Za-zÆæŒœ]{2,}'),
               abbr=set('adj mfn nom acc voc gen dat loc abl ibid cf viz etc fig lit comp '
                        'masc fem neut sing plur du adv pron'.split()),
               patterns=[('xion', re.compile(r'xion$', re.I)), ('ligature', re.compile(r'[æœ]')),
                         ('ick', re.compile(r'ick$', re.I)), ('shew', re.compile(r'shew', re.I))],
               canon=['xion', 'ligature', 'ick', 'archaic'], wordlist_free=False),
    'la': dict(name='Latin', source='csl', wordlist=None, wordlist_env='ORTHO_LA_DIC', enc='utf-8',
               seed={}, transforms=lambda w: [], skip=None,
               word=re.compile(r'[A-Za-zæœÆŒ][A-Za-zæœÆŒ]{2,}'), abbr=set(),
               patterns=[], canon=[], wordlist_free=False),
    'ru': dict(name='Russian', source='jsonl',
               jsonl=os.path.join(triage_util.GITHUB, 'SamudraManthanam', 'web', 'corpus_builder',
                                  'jsonl', 'kossovich.jsonl'),
               jsonl_field='text', wordlist=None, wordlist_env='ORTHO_RU_DIC', enc='utf-8',
               seed={}, transforms=ru_transforms, skip=None,
               word=re.compile(r'[А-Яа-яЁёІіѢѣѲѳѴѵ]{2,}'), abbr=set(),
               patterns=[('yat', re.compile(r'[ѣѲ]')), ('i-dec', re.compile(r'[іІ]')),
                         ('hardsign', re.compile(r'ъ$'))],
               canon=['1918-yat', '1918-i', '1918-hardsign', '1918-fita', '1918-izhitsa'],
               wordlist_free=True),
}
LANG_OF = {'PW': 'de', 'PWG': 'de', 'GRA': 'de', 'CCS': 'de', 'SCH': 'de',
           'BUR': 'fr', 'STC': 'fr', 'BOP': 'la', 'KOSSOVICH': 'ru', 'KOCHERGINA': 'ru',
           'MW': 'en', 'MW72': 'en', 'AP': 'en', 'AP90': 'en', 'WIL': 'en', 'BEN': 'en',
           'GST': 'en', 'CAE': 'en', 'MD': 'en', 'SHS': 'en',
           # modern-EN recency-control anchors (PD = Deccan College 1976-2009, the most modern;
           # BHS/IEG/PE/VEI = 20th-c. glossaries). Expect ~0 drift vs the 19th-c. cluster.
           'PD': 'en', 'BHS': 'en', 'IEG': 'en', 'PE': 'en', 'VEI': 'en'}


def load_wordlist(prof):
    path = os.environ.get(prof['wordlist_env']) or prof['wordlist']
    if not path or not os.path.exists(path):
        return None
    for enc in (prof['enc'], 'utf-8', 'latin-1'):
        try:
            with open(path, encoding=enc) as f:
                lines = f.read().splitlines()
            return set(ln.split('/')[0].strip().lower() for ln in lines[1:] if ln.strip())
        except UnicodeDecodeError:
            continue
    return None


def load_reform_map(map_file, seed):
    m = dict(seed)
    if os.path.exists(map_file):
        with open(map_file, encoding='utf-8') as f:
            for ln in f:
                if ln.startswith('#') or '\t' not in ln:
                    continue
                p = ln.rstrip('\n').split('\t')
                if len(p) >= 3 and p[0]:
                    m[p[0]] = (p[1], p[2])
    return m


def tokens(prof, text):
    out = []
    for w in prof['word'].findall(clean_gloss(text)):
        if w.lower() in prof['abbr'] or w.isupper():
            continue
        out.append(w)
    return out


def iter_texts(prof, dict_code, full):
    """Yield (text, full_count) over the source -- csl-orig entries or jsonl rows."""
    if prof['source'] == 'jsonl':
        path = prof['jsonl']
        if not os.path.exists(path):
            print('jsonl source missing: %s' % path)
            sys.exit(1)
        rows = [json.loads(l) for l in open(path, encoding='utf-8') if l.strip()]
        texts = [r.get(prof['jsonl_field'], '') for r in rows]
    else:
        idx = triage_util.build_entry_index(triage_util.csl_root(), dict_code)
        if idx is None:
            print('no csl-orig source for %s' % dict_code)
            sys.exit(1)
        entries = sorted((e for lst in idx.by_k1.values() for e in lst), key=lambda e: int(e['lineno']))
        texts = [e['body'] for e in entries]
    n = len(texts)
    if not full:
        texts = texts[::max(1, n // SAMPLE_N)]
    return texts, n


def main():
    dict_code = triage_util.dict_arg('PW')
    full = '--full' in sys.argv[2:]
    lang = LANG_OF.get(dict_code.upper(), 'de')
    prof = PROFILES[lang]
    map_file = os.path.join(OUT, '%s_reform_map.tsv' % lang)
    summ_file = os.path.join(OUT, '%s_drift_summary.tsv' % lang)

    texts, n_src = iter_texts(prof, dict_code, full)
    modern = None if prof['wordlist_free'] else load_wordlist(prof)
    reform = load_reform_map(map_file, prof['seed'])

    drift = Counter()       # reform-map drift
    dicdrift = Counter()    # transform-confirmed drift
    drift_example = {}
    pat_cand = defaultdict(Counter)
    n_tokens = n_modern = 0

    for text in texts:
        for w in tokens(prof, text):
            n_tokens += 1
            lw = w.lower()
            if modern is not None and lw in modern:
                n_modern += 1
                continue
            if lw in reform:
                new, era = reform[lw]
                drift[(lw, new, era)] += 1
                drift_example.setdefault(lw, ' '.join(clean_gloss(text).split())[:90])
                continue
            # transform-and-check (wordlist) OR definitional (wordlist-free, e.g. ru 1918)
            hit = None
            for era, cand in prof['transforms'](lw):
                if cand != lw and (prof['wordlist_free'] or (modern is not None and cand in modern)):
                    hit = (cand, era)
                    break
            if hit:
                dicdrift[(lw, hit[0], hit[1])] += 1
                drift_example.setdefault(lw, ' '.join(clean_gloss(text).split())[:90])
                continue
            for name, rx in prof['patterns']:
                if prof['skip'] and prof['skip'](name, lw):
                    continue
                if rx.search(w):
                    pat_cand[name][lw] += 1

    os.makedirs(OUT, exist_ok=True)
    drift_total, dic_total = sum(drift.values()), sum(dicdrift.values())
    total = drift_total + dic_total
    era_occ = Counter()
    for (o, nw, era), c in list(drift.items()) + list(dicdrift.items()):
        era_occ[era] += c
    # split the typographic (ligature) class out of the headline reform rate
    nonreform = sum(era_occ.get(e, 0) for e in NONREFORM_ERAS)
    reform_total = total - nonreform

    rep = os.path.join(OUT, '%s_drift_report.txt' % dict_code)
    with open(rep, 'w', encoding='utf-8') as f:
        f.write('# %s (%s) orthographic-drift -- DOCUMENTATION ONLY (never edits the source)\n'
                % (dict_code, prof['name']))
        f.write('# %s\n' % ('FULL corpus' if full else 'SAMPLE: every %d-th of %d'
                            % (max(1, n_src // SAMPLE_N), n_src)))
        f.write('# modern word-list: %s\n'
                % ('%s, %d stems' % (prof['wordlist_env'], len(modern)) if modern is not None
                   else ('wordlist-free (1918 rule is definitional)' if prof['wordlist_free']
                         else 'NONE (control / not wired) -- map + patterns only')))
        f.write('# gloss tokens: %d ; already-modern: %d ; drift occurrences: %d (transform %d + map %d)\n'
                % (n_tokens, n_modern, total, dic_total, drift_total))
        f.write('# reform-drift: %d (%.2f/1k) ; non-reform/ligature (excluded from rate): %d\n'
                % (reform_total, 1000.0 * reform_total / max(1, n_tokens), nonreform))
        f.write('# drift occurrences by era: %s\n'
                % (', '.join('%s=%d' % (e, era_occ[e]) for e in sorted(era_occ, key=lambda k: -era_occ[k])) or '(none)'))
        f.write('#\n# ===== reform-drift CONFIRMED by transform (+ wordlist, where available) =====\n')
        for (old, new, era), c in dicdrift.most_common():
            f.write('%-22s -> %-22s %-14s %4d  %s\n' % (old, new, era, c, drift_example.get(old, '')))
        f.write('\n# ===== reform-drift from the curated/accumulated map =====\n')
        for (old, new, era), c in drift.most_common():
            f.write('%-22s -> %-22s %-14s %4d  %s\n' % (old, new, era, c, drift_example.get(old, '')))
        f.write('\n# ===== RESIDUAL pattern candidates (-> LLM pass) =====\n')
        for name, _ in prof['patterns']:
            c = pat_cand[name]
            f.write('# -- %s: %d distinct (top 15) --\n' % (name, len(c)))
            for tok, k in c.most_common(15):
                f.write('   %-24s %4d\n' % (tok, k))

    cand = os.path.join(OUT, '%s_pattern_candidates.txt' % dict_code)
    seen = set()
    with open(cand, 'w', encoding='utf-8') as f:
        f.write('# %s RESIDUAL pattern candidates (token<TAB>pattern<TAB>count) -> LLM classify pass\n' % dict_code)
        for name, _ in prof['patterns']:
            for tok, k in pat_cand[name].most_common():
                if tok in seen:
                    continue
                seen.add(tok)
                f.write('%s\t%s\t%d\n' % (tok, name, k))

    # accumulate the per-language reform lexicon
    acc = dict(reform)
    for (old, new, era) in list(dicdrift) + list(drift):
        acc[old] = (new, era)
    with open(map_file, 'w', encoding='utf-8') as f:
        f.write('# %s orthographic reform map:  old<TAB>2026<TAB>era\n' % prof['name'])
        f.write('# Curated seed + corpus-mined drift. Expandable. %d forms.\n' % len(acc))
        for old in sorted(acc):
            new, era = acc[old]
            f.write('%s\t%s\t%s\n' % (old, new, era))

    # cross-dictionary comparison (per language)
    CANON = prof['canon']
    summ = {}
    if os.path.exists(summ_file):
        for ln in open(summ_file, encoding='utf-8'):
            if not ln.startswith('#') and '\t' in ln and not ln.startswith('dict\t'):
                summ[ln.split('\t', 1)[0]] = ln.rstrip('\n')
    cols = ([dict_code, str(n_tokens), '%.0f' % (100.0 * n_modern / max(1, n_tokens)),
             str(reform_total), '%.2f' % (1000.0 * reform_total / max(1, n_tokens))]
            + [str(era_occ.get(e, 0)) for e in CANON])
    summ[dict_code] = '\t'.join(cols)
    with open(summ_file, 'w', encoding='utf-8') as f:
        f.write('# %s orthographic-drift across dictionaries -- DOCUMENTATION ONLY\n' % prof['name'])
        f.write('# drift/1k = reform-drift per 1000 gloss tokens; EXCLUDES typographic eras %s\n'
                % (sorted(NONREFORM_ERAS),))
        f.write('dict\ttokens\tmodern%%\tdrift\tdrift/1k\t%s\n' % '\t'.join(CANON))
        for k in sorted(summ):
            f.write(summ[k] + '\n')

    print('%s (%s): %d gloss tokens; modern-filtered %d%s'
          % (dict_code, prof['name'], n_tokens, n_modern,
             '' if (modern is not None or prof['wordlist_free']) else ' (no wordlist)'))
    print('  reform-drift: %d (%.2f/1k); non-reform/ligature excluded: %d; by era: %s'
          % (reform_total, 1000.0 * reform_total / max(1, n_tokens), nonreform,
             ', '.join('%s=%d' % (e, era_occ[e]) for e in CANON if era_occ.get(e)) or '(none)'))
    print('  transform %d in %d forms + map %d in %d forms; residual %d -> %s'
          % (dic_total, len(dicdrift), drift_total, len(drift), len(seen),
             os.path.relpath(cand, triage_util.ROOT)))
    print('  report -> %s ; map -> %s' % (os.path.relpath(rep, triage_util.ROOT),
                                          os.path.relpath(map_file, triage_util.ROOT)))


if __name__ == '__main__':
    main()
