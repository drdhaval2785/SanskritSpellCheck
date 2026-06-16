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

# dict code -> language
_LANG = {'MW': 'en', 'PW': 'de', 'PWG': 'de', 'VCP': 'sa'}
_LANG_NAME = {'en': 'English', 'de': 'German', 'sa': 'Sanskrit'}

# language -> {sub-type: regex source}. Order matters (most specific first when sub-typing).
MARKERS = {
    'en': {
        'wrong-reading':   r'\bw\.\s?r\.|wrong reading|incorrect(?:ly)? for|wrongly',
        'varia-lectio':    r'\bv\.\s?l\.|\bvar\.|various reading',
        'in-composition':  r'in comp\.|before \S+ for|for \S+ before|\bsandhi\b|metric(?:ally)?\.? for',
        'cross-reference': r'¦\s*(See\b|cf\.|=)|\bq\.v\.|=\s*[˚\-<]',
    },
    'de': {  # Böhtlingk–Roth Petersburg conventions
        'wrong-reading':   r'fehlerhaft|verschrieben|verlesen|falsche?\s+(Lesart|Schreib\w*)|falsch f[üu]r|Druckfehler|\blies\b|verbessere|unrichtig|zu lesen|verdorben',
        'varia-lectio':    r'\bv\.\s?l\.|Nebenform|andere Lesart|Lesart',
        'in-composition':  r'im Compositum|in comp\.|metrisch|metri causa|am Ende eines',
        'cross-reference': r'¦\s*=|¦\s*<?ab>?s\.|¦\s*s\.\s|\bvgl\.|s\.\su\.',
    },
    'sa': {  # Vācaspatyam Sanskrit (SLP1 body)
        'wrong-reading':   r'aSudDa|apapAWa|asADu',
        'varia-lectio':    r'pAWAntara|iti pAWaH|\bpAWe\b|kvacit',
        'in-composition':  r'samAse|samAsa|samAsAnta',
        'cross-reference': r'drazwavya|draSyam|=\s',
    },
}
_SUBTYPE_ORDER = ['wrong-reading', 'varia-lectio', 'in-composition', 'cross-reference']


def lang(dictcode):
    return _LANG.get(dictcode.upper(), 'en')


def lang_name(dictcode):
    return _LANG_NAME[lang(dictcode)]


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


def subtype(body, dictcode):
    """Classify a documented-intentional spelling into a wrong-readings sub-type."""
    b = body or ''
    for name, rx in subtype_res(dictcode):
        if rx.search(b):
            return name
    return 'other-intentional'
