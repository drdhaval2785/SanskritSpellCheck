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
import glob

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import triage_lang

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GITHUB = os.path.dirname(ROOT)

_K1 = re.compile(r'<k1>([^<]*)')
_TAGS = re.compile(r'<[^>]+>')
_LEX = re.compile(r'<lex>')
# MW's own text says the spelling is a wrong reading -> intentional error apparatus
_WR = re.compile(r'\bw\.\s?r\.|wrong reading|incorrect(?:ly)? for|wrongly (?:for|written)', re.I)
# MW documents the spelling as a deliberate variant / sandhi / compounding form
_VARIANT = re.compile(
    r'\bv\.\s?l\.|in comp\. for|metric(?:ally)?\.? for|\bq\.v\.|for \S+ before|'
    r'=\s*[˚\-]|=\s*<s>|\bvar\.|prā\b', re.I)
# pure cross-reference pointer
_XREF = re.compile(r'¦\s*(See\b|cf\.|=)', re.I)


def build_index(mw_path):
    """headword (k1) -> list of raw body strings (text between the <L> line and <LEND>)."""
    idx = {}
    cur_k1 = None
    buf = []
    with open(mw_path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('<L>'):
                m = _K1.search(line)
                cur_k1 = m.group(1) if m else None
                buf = []
            elif line.startswith('<LEND>'):
                if cur_k1 is not None:
                    idx.setdefault(cur_k1, []).append(' '.join(buf).strip())
                cur_k1 = None
            elif cur_k1 is not None:
                buf.append(line.rstrip('\n'))
    return idx


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
    mw_path = os.path.join(GITHUB, 'csl-orig', 'v02', dict_code.lower(),
                           '%s.txt' % dict_code.lower())

    print("building %s entry index from %s ..." % (dict_code, os.path.relpath(mw_path, GITHUB)))
    idx = build_index(mw_path)
    print("  %d distinct headwords indexed" % len(idx))

    rows = [json.loads(l) for l in open(ev_path, encoding='utf-8')]
    for r in rows:
        bodies = idx.get(r['suspect'], [])
        kind, text = classify(bodies)
        r['body_kind'] = kind
        r['body_count'] = len(bodies)
        r['body_text'] = text
    with open(ev_path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print("augmented %s with body_kind/body_count/body_text" % os.path.relpath(ev_path, ROOT))

    # body_kind distribution (drives the triage)
    from collections import Counter
    by = {r['suspect']: r for r in rows}
    c = Counter(r['body_kind'] for r in rows)
    print("\nbody_kind across all %d tier-A:" % len(rows))
    for k, n in c.most_common():
        print("  %-12s %4d" % (k, n))
    print("  -> need body-aware judgment (realword/thin/multi): %d"
          % sum(c[k] for k in ('realword', 'thin', 'multi-mixed')))
    print("  -> settled intentional (wr/variant/xref): %d ; unlocatable (missing): %d"
          % (sum(c[k] for k in ('wr', 'variant', 'xref')), c['missing']))

    # optional cross-check vs a first-pass FILE-labeled set, if one exists (MW only)
    adj = {}
    for p in sorted(glob.glob(os.path.join(pkg, 'triage_work', 'adj_*.json'))):
        try:
            t = open(p, encoding='utf-8').read().strip()
            if t.startswith('```'):
                t = t.split('```')[1].lstrip('json').strip()
            for v in json.loads(t):
                adj[v['suspect']] = v
        except Exception:
            pass
    if adj:
        ver = {}
        for p in sorted(glob.glob(os.path.join(pkg, 'triage_work', 'verify_*.json'))):
            try:
                t = open(p, encoding='utf-8').read().strip()
                if t.startswith('```'):
                    t = t.split('```')[1].lstrip('json').strip()
                for v in json.loads(t):
                    ver[v['suspect']] = v
            except Exception:
                pass
        confirmed = [s for s, v in adj.items() if v['label'] == 'FILE' and ver.get(s, {}).get('real_typo')]
        bad = [s for s in confirmed if by[s]['body_kind'] not in ('thin', 'missing')]
        print("\n(first-pass cross-check) %d FILE-confirmed -> %d have a real/intentional %s body "
              "(false positives the body catches)" % (len(confirmed), len(bad), dict_code))


if __name__ == '__main__':
    main()
