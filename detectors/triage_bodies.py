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
import os
import re
import json

import triage_lang
import triage_util

triage_util.reconfigure_stdio()
ROOT = triage_util.ROOT

_TAGS = re.compile(r'<[^>]+>')
_LEX = re.compile(r'<lex>')
# documented-intentional markers: default to English, overwritten per-dictionary in main()
# from triage_lang so the regex literals live in ONE place (triage_lang.py).
_WR, _VARIANT, _XREF = triage_lang.wr_re('MW'), triage_lang.variant_re('MW'), triage_lang.xref_re('MW')

# body-length thresholds for classify_one (chars of gloss, tags + the ¦ separator stripped):
_XREF_MAX_CHARS = 50      # a "See/cf." marker counts as a cross-reference only in a SHORT body
_REALWORD_MIN_CHARS = 12  # a body longer than this (or carrying a <lex> POS tag) is a real gloss
_THIN_MAX_CHARS = 3       # <= this is a bare key with no content -- what a genuine typo looks like
_BODY_TEXT_CAP = 500      # max chars of joined body text carried forward as body_text


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
    if _XREF.search(b) and len(plain) < _XREF_MAX_CHARS:
        return 'xref'
    if _LEX.search(b) or len(plain) > _REALWORD_MIN_CHARS:
        return 'realword'
    if len(plain) <= _THIN_MAX_CHARS:
        return 'thin'
    return 'realword'


def classify(bodies):
    """Return (kind, plain_text). Any intentional/real-word signal on ANY homograph entry
    wins over 'thin' (we must not 'fix' a key that another homograph proves is valid)."""
    if not bodies:
        return 'missing', ''
    kinds = [classify_one(b) for b in bodies]
    plains = [_TAGS.sub('', b).replace('¦', '').strip() for b in bodies]
    text = ' || '.join(p for p in plains if p)[:_BODY_TEXT_CAP]
    # precedence: documented-spelling/real-word beats thin
    for k in triage_util.INTENTIONAL_KINDS + ('realword',):
        if k in kinds:
            if len(bodies) > 1 and 'thin' in kinds:
                return 'multi-mixed', text
            return k, text
    return 'thin', text


def main():
    dict_code = triage_util.dict_arg()
    # select the documented-intentional markers for this dictionary's body language
    global _WR, _VARIANT, _XREF
    _WR, _VARIANT, _XREF = (triage_lang.wr_re(dict_code), triage_lang.variant_re(dict_code),
                            triage_lang.xref_re(dict_code))
    print("body language: %s (%s markers)" % (triage_lang.lang_name(dict_code), triage_lang.lang(dict_code)))
    pkg = triage_util.package_dir(dict_code)
    ev_path = os.path.join(pkg, '%s_evidence.jsonl' % dict_code)
    csl_root = triage_util.csl_root()

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
          % sum(c[k] for k in triage_util.NEEDS_JUDGMENT))
    print("  -> settled intentional (wr/variant/xref): %d ; unlocatable (missing): %d"
          % (sum(c[k] for k in triage_util.INTENTIONAL_KINDS), c['missing']))


if __name__ == '__main__':
    main()
