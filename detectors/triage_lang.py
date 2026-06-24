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
    'PD': 'en',                                          # Encyclopaedic Dict. of Sanskrit (Deccan College, Eng) -- external_src
    'PUI': 'en', 'INM': 'en', 'PE': 'en', 'YAT': 'en',   # Puranic/Mahabharata name indices, Yates (Eng)
    'ACC': 'en', 'IEG': 'en', 'MCI': 'en', 'PGN': 'en',  # Catalogus Cat., Epigraphical Gloss., name indices
    'VEI': 'en',                                          # Vedic Index of Names (Macdonell-Keith, Eng)
    'KRM': 'sa',                                          # Kramadisvara dhatupatha (Sanskrit root-list)
    'PW': 'de', 'PWG': 'de', 'SCH': 'de',                # Petersburg (Boehtlingk-Roth) + Schmidt Nachtraege
    'GRA': 'de', 'CCS': 'de',                            # Grassmann (Rigveda), Cappeller (German)
    'VCP': 'sa', 'SKD': 'sa',                            # Vacaspatyam, Sabdakalpadruma (Sanskrit-Sanskrit)
    'BUR': 'fr', 'STC': 'fr',                            # Burnouf 1866, Stchoupak-Nitti-Renou (French)
    'BOP': 'la',                                          # Bopp, Glossarium Sanscritum (Latin)
}
_LANG_NAME = {'en': 'English', 'de': 'German', 'sa': 'Sanskrit', 'fr': 'French', 'la': 'Latin'}

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
    'fr': {  # Burnouf 1866 / Stchoupak 1932 French-Sanskrit conventions
        # STC writes the correction directive as "lire <form>" (infinitive, e.g. valmi- "lire vallī-");
        # anchor on a following form-marker ({ or the ˚ ditto) so plain glosses ("action de lire") don't match.
        'wrong-reading':   r'faute pour|erreur pour|fautif|mauvaise le[çc]on|\blisez\b|\blire\s+[{˚]|à corriger|corrompu',
        'varia-lectio':    r'\bv\.\s?l\.|variante|autre le[çc]on',
        'in-composition':  r'en composition|en comp\.|pour \S+ devant|par sandhi|m[ée]tri',
        'cross-reference': r'\bvoyez\b|\bvoy\.|\bcf\.|\bq\.v\.|=\s*\{#|\bv\.\s*\{#',
    },
    'la': {  # Bopp 1847 Glossarium Sanscritum (Latin gloss)
        'wrong-reading':   r'vitiose|male pro|perperam|mendose|\blege\b|corrupt',
        'varia-lectio':    r'\bv\.\s?l\.|varia lectio|alii legunt|aliter',
        'in-composition':  r'in compositione|in comp\.|pro \S+ ante|metri causa',
        'cross-reference': r'\bvide\b|\bconf\.|\bcf\.|\bq\.v\.|=\s*\{#|\bv\.\s*\{#',
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
    'fr': ('French glosses (Burnouf / Stchoupak). Sanskrit forms appear in {#...#} (or inline IAST), '
           'French glosses in {%...%}. Intentional-spelling markers: "faute pour" / "erreur pour" / '
           '"lisez" / "mauvaise leçon" (error/false reading for); "v.l." / "variante"; "voyez" / '
           '"voy." / "cf." / "= {#X#}" (see/compare, cross-reference); "en composition". A normal '
           'French definition of the suspect itself means it is a real word. NOTE: BUR/STC inline '
           'their Sanskrit in IAST (not always {#..#}), so judge by meaning, not markup.'),
    'la': ('Latin glosses (Bopp, Glossarium). Sanskrit forms appear in {#...#} (or inline IAST), '
           'Latin glosses in {%...%}. Intentional-spelling markers: "vitiose" / "male pro" / '
           '"perperam" / "mendose" / "lege" (wrongly/read-for, an erroneous reading); "v.l." / '
           '"varia lectio" / "aliter"; "vide" / "cf." / "conf." / "= {#X#}" (see/compare); "in '
           'compositione". A normal Latin definition of the suspect itself means it is a real word.'),
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
