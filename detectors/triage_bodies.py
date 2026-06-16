#!/usr/bin/env python3
"""triage_bodies.py -- attach each candidate's MW entry BODY (from csl-orig) to the
evidence, and classify it. The dictionary's OWN entry text is the decisive signal a
spelling-only detector is blind to:

  - w.r.   `<s>marga</s> ¦ <ab>w.r.</ab> for <s>mArga</s>` -- an INTENTIONAL wrong-reading
           apparatus entry. "Correcting" it deletes MW's scholarship. NEVER file.
  - xref   `<s>kiriwa</s> ¦ See <s>ati-kir°</s>.` -- a cross-reference entry. Intentional.
  - gloss  `<s>muka</s> ¦ <lex>m.</lex> the smell of cow-dung` -- a real headword with a
           definition. It is a real word, not a typo, even if it looks like mUka.
  - thin   no gloss / cross-ref -- a bare key; THIS is what a real typo looks like.

We discovered an adversarial-verify miss (muka confirmed as a typo though MW glosses it
'the smell of cow-dung'): the verifier reasoned from memory, not the source. This module
makes the body explicit so the re-verify and the synthesis decide from MW's own text.

Builds a {headword -> [entry bodies]} index from csl-orig MW in one pass, augments
<DICT>_evidence.jsonl in place with body fields, and reports how the FILE-labeled set
classifies. Usage:  cd detectors && python triage_bodies.py [MW]
"""
import sys
import os
import re
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import triage_lang
import triage_util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GITHUB = os.path.dirname(ROOT)

_TAGS = re.compile(r'<[^>]+>')
_LEX = re.compile(r'<lex>')
# documented-intentional markers: default to English, overwritten per-dictionary in main()
# from triage_lang so the regex literals live in ONE place (triage_lang.py).
_WR, _VARIANT, _XREF = triage_lang.wr_re('MW'), triage_lang.variant_re('MW'), triage_lang.xref_re('MW')


def classify_one(b):
    """Classify a single entry body.
    wr/variant/xref = MW deliberately documents this spelling -> NEVER file.
    realword        = a normal definition -> suspect is its own word -> not a typo.
    thin            = a bare key with no content -> what a genuine typo looks like.
    """
    plain = _TAGS.sub('', b).replace('¦', '').strip()
    if _WR.search(b):
        return 'wr'
    if _VARIANT.search(b):
        return 'variant'
    if _XREF.search(b) and len(plain) < 50:
        return 'xref'
    if _LEX.search(b) or len(plain) > 12:
        return 'realword'
    if len(plain) <= 3:
        return 'thin'
    return 'realword'


def classify(bodies):
    """Return (kind, plain_text). Any intentional/real-word signal on ANY homograph entry
    wins over 'thin' (we must not 'fix' a key that another homograph proves is valid)."""
    if not bodies:
        return 'missing', ''
    kinds = [classify_one(b) for b in bodies]
    plains = [_TAGS.sub('', b).replace('¦', '').strip() for b in bodies]
    text = ' || '.join(p for p in plains if p)[:500]
    # precedence: documented-spelling/real-word beats thin
    for k in ('wr', 'variant', 'xref', 'realword'):
        if k in kinds:
            if len(bodies) > 1 and 'thin' in kinds:
                return 'multi-mixed', text
            return k, text
    return 'thin', text


def main():
    dict_code = sys.argv[1] if len(sys.argv) > 1 else 'MW'
    # select the documented-intentional markers for this dictionary's body language
    global _WR, _VARIANT, _XREF
    _WR, _VARIANT, _XREF = (triage_lang.wr_re(dict_code), triage_lang.variant_re(dict_code),
                            triage_lang.xref_re(dict_code))
    print("body language: %s (%s markers)" % (triage_lang.lang_name(dict_code), triage_lang.lang(dict_code)))
    pkg = os.path.join(ROOT, 'corrections_draft', dict_code)
    ev_path = os.path.join(pkg, '%s_evidence.jsonl' % dict_code)
    csl_root = os.path.join(GITHUB, 'csl-orig')

    print("building %s entry index from csl-orig/v02/%s ..." % (dict_code, dict_code.lower()))
    idx = triage_util.build_entry_index(csl_root, dict_code)
    print("  %d distinct headwords indexed" % (len(idx.by_k1) if idx else 0))

    with open(ev_path, encoding='utf-8') as f:
        rows = [json.loads(l) for l in f]
    for r in rows:
        bodies = idx.bodies(r['suspect']) if idx else []
        kind, text = classify(bodies)
        r['body_kind'] = kind
        r['body_count'] = len(bodies)
        r['body_text'] = triage_util.resolve_redirect(text, idx)
    with open(ev_path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print("augmented %s with body_kind/body_count/body_text" % os.path.relpath(ev_path, ROOT))

    # body_kind distribution (drives the triage)
    from collections import Counter
    c = Counter(r['body_kind'] for r in rows)
    print("\nbody_kind across all %d tier-A:" % len(rows))
    for k, n in c.most_common():
        print("  %-12s %4d" % (k, n))
    print("  -> need body-aware judgment (realword/thin/multi): %d"
          % sum(c[k] for k in ('realword', 'thin', 'multi-mixed')))
    print("  -> settled intentional (wr/variant/xref): %d ; unlocatable (missing): %d"
          % (sum(c[k] for k in ('wr', 'variant', 'xref')), c['missing']))


if __name__ == '__main__':
    main()
