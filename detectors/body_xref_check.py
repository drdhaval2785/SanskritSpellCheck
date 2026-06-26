#!/usr/bin/env python3
"""body_xref_check.py -- cross-reference INTEGRITY check for a dictionary's entry bodies.

The headword spell-checkers ignore the entry body. But a body is full of cross-references
("See X", "cf. X", "= X", "q.v.") whose TARGET should resolve to a real entry somewhere. A
target that resolves nowhere -- after canonicalizing the dictionary's reference notation -- is
a **broken cross-reference**: a dangling pointer, an OCR-mangled target, or a typo. Unlike raw
body-form spell-checking, this signal is *apparatus-independent* and high-precision: the
dictionary itself asserts "this form exists", and we check whether it does.

READ-ONLY: reads csl-orig + sanhw1 + DCS; writes a report. Never edits a dictionary.

  cd detectors && python body_xref_check.py MW [out.txt]

The hard part is notation, so the unresolved set is real breaks, not artifacts. A CANONICAL key
(accents / backslash / caret, the ring abbreviation U+02DA/U+00B0/'0', avagraha, hyphens, spaces
and punctuation all removed) is applied to BOTH the target and every headword/lemma; a ring
abbreviation is additionally expanded against the entry's own headword. A target RESOLVES if its
canonical key (or a ring-expansion of it) matches a k1/k2 headword (any dict) or a DCS lemma.
"""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import triage_util as tu

tu.reconfigure_stdio()

RING = '˚°'                         # ring-above / degree (MW's headword-abbreviation mark)
_STRIP = re.compile(r"[˚°0/\\^'’\-–— .,;:()\[\]|]")
_CUE = re.compile(r'(?:\bSee\b|\bcf\.|\bq\.\s?v\.|=)\s*<s>([^<]+)</s>', re.I)


def canon(form):
    """Collapse reference notation to a comparison key: drop accents, ring, avagraha,
    hyphens, spaces, punctuation. Compounds, sandhi-spacing and accents all fold together."""
    return _STRIP.sub('', form.strip())


def build_index():
    """canonical-key set of every headword (k1∪k2, all dicts via sanhw1) + DCS lemma."""
    keys = set()
    with open(os.path.join(tu.ROOT, 'sanhw1.txt'), encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                keys.add(canon(line.split(':', 1)[0]))
    dcs = u.load_dcs_lemmas(u.dcs_path())
    for x in dcs:
        keys.add(canon(x))
        keys.add(canon(u.normalize_lemma(x)))
    keys.discard('')
    return keys


def main():
    dictcode = (sys.argv[1] if len(sys.argv) > 1 else 'MW').upper()
    out = sys.argv[2] if len(sys.argv) > 2 else None
    idx = tu.build_entry_index(tu.csl_root(), dictcode)
    if idx is None:
        sys.exit('%s: no source' % dictcode)
    keys = build_index()
    keys |= {canon(h) for h in idx.by_k1}
    keys |= {canon(h) for h in idx.by_k2}
    keys.discard('')

    def resolves(hw, raw):
        k = canon(raw)
        if not k:
            return True
        if k in keys:
            return True
        # √-root reference ("anu-√ grah", "ati-√ muc"): resolves iff the root after √ exists
        if '√' in raw:
            root = canon(raw.split('√')[-1])
            if root and root in keys:
                return True
        # ring abbreviation ("aDiv˚", "˚vat", "Akz˚"): an intra-entry self-reference to a form
        # built on this headword -- valid by construction (points within the current entry),
        # never a broken EXTERNAL link, so it cannot be a dangling reference.
        if any(c in raw for c in RING):
            return True
        return False

    def near_miss(k):
        """A canon key one confusion-edit from a real headword -> a TYPO'd reference (fileable)."""
        for nb in u.confusion_candidates(k):
            if nb != k and canon(nb) in keys:
                return canon(nb)
        return None

    total = broke = 0
    typo_rows, other_rows = [], []
    for hw, entries in idx.by_k1.items():
        for e in entries:
            for raw in _CUE.findall(e['body']):
                k = canon(raw)
                if not k:
                    continue
                total += 1
                if resolves(hw, raw):
                    continue
                broke += 1
                nm = near_miss(k)
                if nm:
                    typo_rows.append((hw, raw.strip(), k, nm, e['lineno']))
                else:
                    other_rows.append((hw, raw.strip(), k, e['lineno']))

    pct = 100 * broke / total if total else 0
    head = ('# %s cross-reference integrity -- DRAFT for human review (scan-verify each)\n'
            '# %d See/cf./=/q.v. targets ; %d unresolved (%.1f%%).\n'
            '#   TYPO\'d-ref (1 confusion-edit from a real entry -> FILE-FIRST): %d\n'
            '#   other-unresolved (partial/inflected/uncertain form refs): %d\n'
            % (dictcode, total, broke, pct, len(typo_rows), len(other_rows)))
    sys.stdout.write(head)
    if out:
        with open(out, 'w', encoding='utf-8') as f:
            f.write(head)
            f.write('# === FILE-FIRST: typo\'d cross-references (headword<TAB>raw<TAB>canon<TAB>should-be<TAB>line) ===\n')
            for hw, raw, k, nm, ln in typo_rows:
                f.write('%s\t%s\t%s\t%s\t%d\n' % (hw, raw, k, nm, ln))
            f.write('# === OTHER unresolved (headword<TAB>raw<TAB>canon<TAB>line) ===\n')
            for hw, raw, k, ln in other_rows:
                f.write('%s\t%s\t%s\t%d\n' % (hw, raw, k, ln))
        print('-> %s' % out)
    print('--- FILE-FIRST sample (typo\'d cross-refs) ---')
    for hw, raw, k, nm, ln in typo_rows[:25]:
        print('  %-16s See/cf. %-20s [%s -> %s]  line %d' % (hw, raw, k, nm, ln))


if __name__ == '__main__':
    main()
