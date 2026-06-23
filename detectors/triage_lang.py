#!/usr/bin/env python3
"""triage_lang.py -- per-dictionary language profiles for the body-grounded triage.

The "documented-intentional spelling" markers that distinguish a real entry from an
editorial wrong-reading / variant / cross-reference are LANGUAGE-SPECIFIC: MW glosses in
English ("w.r. for", "in comp. for", "See"), the Petersburg dictionaries PW/PWG in German
("fehlerhaft für", "verschrieben", "lies", "s.", "vgl."), Vācaspatyam VCP in Sanskrit
("aSudDa", "pAWAntara"). One place to keep them, keyed by the four sub-types the
wrong-readings list groups by.
"""
import re

# dict code -> language (the ONE place to register a dictionary; unknown codes default to 'en')
_LANG = {
    'MW': 'en', 'MW72': 'en', 'AP': 'en', 'AP90': 'en',   # Monier-Williams 1899/1872, Apte 1957/1890
    'WIL': 'en', 'BEN': 'en', 'GST': 'en', 'CAE': 'en',   # Wilson, Benfey, Goldstuecker, Cappeller (Eng)
    'MD': 'en', 'SHS': 'en',                              # Macdonell, Shabda-Sagara
    'BHS': 'en',                                          # Edgerton, Buddhist Hybrid Sanskrit Dict (Eng)
    'PUI': 'en', 'INM': 'en', 'PE': 'en', 'YAT': 'en',   # Puranic/Mahabharata name indices, Yates (Eng)
    'ACC': 'en', 'IEG': 'en', 'MCI': 'en', 'PGN': 'en',  # Catalogus Cat., Epigraphical Gloss., name indices
    'VEI': 'en',                                          # Vedic Index of Names (Macdonell-Keith, Eng)
    'KRM': 'sa',                                          # Kramadisvara dhatupatha (Sanskrit root-list)
    'PW': 'de', 'PWG': 'de', 'SCH': 'de',                # Petersburg (Boehtlingk-Roth) + Schmidt Nachtraege
    'GRA': 'de', 'CCS': 'de',                            # Grassmann (Rigveda), Cappeller (German)
    'VCP': 'sa', 'SKD': 'sa',                            # Vacaspatyam, Sabdakalpadruma (Sanskrit-Sanskrit)
}
_LANG_NAME = {'en': 'English', 'de': 'German', 'sa': 'Sanskrit'}

# language -> {sub-type: regex source}. Order matters (most specific first when sub-typing).
MARKERS = {
    'en': {
        'wrong-reading':   r'\bw\.\s?r\.|wrong reading|incorrect(?:ly)? for|wrongly',
        'varia-lectio':    r'\bv\.\s?l\.|\bvar\.|various reading',
        'in-composition':  r'in comp\.|before \S+ for|for \S+ before|\bsandhi\b|metric(?:ally)?\.? for',
        # ¦-independent: body_text has the ¦ separator stripped, so markers must not need it
        # (classify_one guards body_kind with len<50 so a bare "See" can't mislabel a long body).
        'cross-reference': r'\bSee\b|\bcf\.|\bq\.v\.|=\s*[˚\-<]',
    },
    'de': {  # Böhtlingk–Roth Petersburg conventions
        # incl. PW correction-note apparatus: "Richtig {#X#}" / "lies {#X#}" (the headword is the
        # form-as-found, X is PW's noted correct form -> intentional apparatus, do NOT file).
        'wrong-reading':   r'fehlerhaft|verschrieben|verlesen|falsche?\s+(Lesart|Schreib\w*)|falsch f[üu]r|Druckfehler|\blies\b|verbessere|unrichtig|zu lesen|verdorben|Richtig \{#|richtiger \{#',
        'varia-lectio':    r'\bv\.\s?l\.|Nebenform|andere Lesart|Lesart',
        'in-composition':  r'im Compositum|in comp\.|metrisch|metri causa|am Ende eines',
        'cross-reference': r'\bs\.\su\.|\bs\.\s+\{#|\bvgl\.|=\s*\{#|<ab>s\.',
    },
    'sa': {  # Vācaspatyam Sanskrit (SLP1 body)
        'wrong-reading':   r'aSudDa|apapAWa|asADu',
        'varia-lectio':    r'pAWAntara|iti pAWaH|\bpAWe\b|kvacit pAWaH',
        'in-composition':  r'samAse|samAsAnta|samAsfta',
        # {{Lbody=N}} = VCP redirect (a variant/cross-ref headword sharing another entry's
        # body, e.g. vrAhmaRa -> brAhmaRa); draSya/drazwavya = "is to be seen" (see X).
        'cross-reference': r'\{\{Lbody=|drazwavya|draSyam|tatra draSyam',
    },
}
_SUBTYPE_ORDER = ['wrong-reading', 'varia-lectio', 'in-composition', 'cross-reference']
_SUBTYPE_FALLBACK = 'other-intentional'   # an intentional spelling matching no specific marker


def lang(dictcode):
    return _LANG.get(dictcode.upper(), 'en')


def lang_name(dictcode):
    return _LANG_NAME[lang(dictcode)]


# human-readable marker hint for the body-aware workflow rubric (ONE source of truth, so
# the unified workflow builds its language-specific rubric from here, not hand-copied prose)
_HINT = {
    'en': ('English glosses. Intentional-spelling markers: "w.r. for" (wrong reading), '
           '"v.l." (varia lectio), "in comp. for" / "for X before Y" (sandhi/compounding), '
           '"= X" / "See X" / "q.v." (cross-reference). A real definition (a <lex> POS tag + '
           'meaning) means the suspect is a real word.'),
    'de': ('German glosses (Boehtlingk-Roth Petersburg). Sanskrit forms appear in {#...#}, '
           'German glosses in {%...%}. Intentional-spelling markers: "fehlerhaft fuer" / '
           '"verschrieben fuer" / "falsche/schlechte Lesart" / "verlesen" (erroneous/false '
           'reading for); "v.l." / "Nebenform"; "lies" / "verbessere" (read!/correct to); '
           '"s." / "s. u." / "vgl." (see/compare, cross-reference); "= {#X#}"; "im Compositum". '
           'A normal German gloss describing the suspect itself means it is a real word.'),
    'sa': ('Sanskrit glosses (Vacaspatyam, SLP1, abbreviated with "0": pu0=masc, strI=fem, '
           'tri0=adj, n0=neut; a ROOT entry = meaning + gana (BvA0/ada0/tu0/cu0...) + '
           'para0/Atma0 + saka0 + sew, then conjugation -> a real distinct word). A '
           '{{Lbody=N}} body is a REDIRECT (variant headword sharing entry N) = intentional '
           'cross-reference; aSudDa/apapAWa = wrong reading; pAWAntara/iti pAWaH = variant.'),
}


def marker_hint(dictcode):
    """One-paragraph description of this dictionary's documented-intentional markers,
    for the body-aware workflow rubric."""
    return _HINT[lang(dictcode)]


def _src(dictcode):
    return MARKERS[lang(dictcode)]


def subtype_res(dictcode):
    """Ordered [(sub-type, compiled regex)] for grouping the wrong-readings list."""
    m = _src(dictcode)
    return [(k, re.compile(m[k], re.I)) for k in _SUBTYPE_ORDER]


def wr_re(dictcode):
    return re.compile(_src(dictcode)['wrong-reading'], re.I)


def variant_re(dictcode):
    m = _src(dictcode)
    return re.compile('(?:%s)|(?:%s)' % (m['varia-lectio'], m['in-composition']), re.I)


def xref_re(dictcode):
    return re.compile(_src(dictcode)['cross-reference'], re.I)


def subtype_order():
    """The wrong-readings sub-types in display order, plus the catch-all that subtype()
    returns for an intentional spelling matching no specific marker. ONE source of truth
    for the do-not-file list's grouping (triage_synthesize)."""
    return _SUBTYPE_ORDER + [_SUBTYPE_FALLBACK]


def subtype(body, dictcode):
    """Classify a documented-intentional spelling into a wrong-readings sub-type."""
    b = body or ''
    for name, rx in subtype_res(dictcode):
        if rx.search(b):
            return name
    return _SUBTYPE_FALLBACK
