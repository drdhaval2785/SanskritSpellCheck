#!/usr/bin/env python3
"""entry_body_pilot.py -- H1535: extend the deterministic headword detectors
(charset_check, phonotactic_check, ngram) into a dictionary's ENTRY-BODY text.

The headword detectors (charset_check.py, phonotactic_check.py) and the ngram checker
(ngram/ngramspellcheck.py) all run on sanhw1.txt -- headwords only. This pilot builds a
body-token corpus from a dictionary's own csl-orig source (the Sanskrit spans inside entry
glosses, marked {#...#} or <s>...</s>) and reuses the SAME three detectors unmodified, so
"body scope" is a new INPUT, not a new algorithm.

Unlike raw corpus-attestation typo-detection (documented as a negative result in
body_xref/readme.md -- 79.9% of MW body forms are unattested inflected/compound forms, not
typos), charset_check and phonotactic_check are ABSOLUTE structural/rule checks: they do not
need a form to be a dictionary headword to judge it, so they should not hit the same
inflection wall.

A span is often a whole phrase (etymology, citation, grammatical note), not one word, so it
is split into individual words first. Two SHS-specific notation conventions are counted and
excluded rather than fabricated into false structural violations: a leading/embedded '-'
stands in for the previous stem (e.g. "-kaH" under headword "aMSaka"), and a bare '0' is
SHS's period-substitute abbreviation-dot for verb-class/pada/seT markers ("para0", "sa0",
"BvA0"), not a digit OCR-leak.

  cd detectors && python entry_body_pilot.py [DICT=SHS] [outdir=../corrections_draft/<DICT>/body_pilot]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util as tu
import charset_check
import phonotactic_check

tu.reconfigure_stdio()

_SPAN = re.compile(r'\{#([^#]+)#\}|<s>([^<]+)</s>')
# csl-orig's own change-tracker annotation ({{old->new||date|editor|issue-url|}}) sometimes
# leaks inside a {#...#} span (e.g. "see {#{{a->b||date|...|issues/225|}}#}"); it is metadata
# about an ALREADY-APPLIED correction, not dictionary content, so strip it before tokenizing
# rather than let its digits/URL fragments masquerade as body-text charset suspects.
_CHANGE_TRACKER = re.compile(r'\{\{.*?\}\}')
# a span is often a whole etymology/citation phrase, not one word -- split on the
# markup/punctuation separators the ngram tokenizer already treats as word breaks
# (ngram/ngramspellcheck.py's testwithcommonngrams strip set), plus the curly quotes SHS
# uses to bracket a quoted sutra/citation ('...' as U+2018/U+2019). The straight apostrophe
# is deliberately NOT a separator here -- SLP1 uses it for avagraha (u.ALPHABET includes it),
# so splitting on it would fragment a real word like "aDo'MSuka" into "aDo"+"MSuka".
_WORDSPLIT = re.compile(r'["‘’“”,.?!/*_()\[\]{}<>;:*–|#$+%^@=~`\s]+')


def extract_body_tokens(idx):
    """Walk every entry's body, split each Sanskrit span into individual words, yield
    (token, headword, lineno). Two SHS-specific notation conventions are excluded and
    counted separately, not fabricated into structural violations:
      - a leading/embedded '-' stands in for the previous stem (e.g. "-kaH" under "aMSaka")
      - a '0' is SHS's period-substitute abbreviation-dot (verb class/pada/seT markers:
        "para0"=parasmaipada, "sa0"=sakarmaka, "BvA0"=bhvadi, ...), not a digit OCR-leak.
    Returns (clean, stub_count, abbrev_count, total_words)."""
    clean = []
    stub = abbrev = total = 0
    for hw, entries in idx.by_k1.items():
        for e in entries:
            for m in _SPAN.finditer(e['body']):
                span = (m.group(1) or m.group(2) or '').strip()
                if not span:
                    continue
                span = _CHANGE_TRACKER.sub(' ', span)
                for word in _WORDSPLIT.split(span):
                    if not word:
                        continue
                    total += 1
                    if '-' in word:
                        stub += 1
                        continue
                    if '0' in word:
                        abbrev += 1
                        continue
                    clean.append((word, hw, e['lineno']))
    return clean, stub, abbrev, total


def write_token_file(clean, path):
    """One row per DISTINCT token (first occurrence's headword/lineno as provenance),
    in the 'word:dicts' shape charset_check/phonotactic_check already parse -- the
    'dicts' field here carries provenance (headword@lineno) instead of a dict list."""
    seen = {}
    order = []
    for tok, hw, lineno in clean:
        if tok not in seen:
            seen[tok] = (hw, lineno)
            order.append(tok)
    with open(path, 'w', encoding='utf-8') as f:
        for tok in order:
            hw, lineno = seen[tok]
            f.write("%s:%s@%s\n" % (tok, hw, lineno))
    return len(order)


def write_running_text(clean, path):
    """Whitespace-separated running text for ngramspellcheck.py (which tokenizes on
    whitespace) -- one distinct token per line is sufficient since it re-tokenizes anyway."""
    seen = set()
    with open(path, 'w', encoding='utf-8') as f:
        for tok, _hw, _lineno in clean:
            if tok not in seen:
                seen.add(tok)
                f.write(tok + '\n')
    return len(seen)


def headword_overlap(distinct_tokens, sanhw1_path):
    """How many distinct body tokens are ALREADY a headword somewhere in sanhw1.txt (so the
    headword-level detectors already had a chance to see them) vs genuinely NEW input."""
    hw_keys = set()
    with open(sanhw1_path, encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                hw_keys.add(line.split(':', 1)[0])
    already = sum(1 for t in distinct_tokens if t in hw_keys)
    return already, len(distinct_tokens) - already


def main():
    dict_code = tu.dict_arg('SHS')
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(tu.ROOT, 'corrections_draft', dict_code, 'body_pilot')
    os.makedirs(outdir, exist_ok=True)

    print("building %s entry index from csl-orig ..." % dict_code)
    idx = tu.build_entry_index(tu.csl_root(), dict_code)
    if idx is None:
        sys.exit('%s: no source (checked external_src/ and csl-orig)' % dict_code)
    print("  %d distinct headwords indexed" % len(idx.by_k1))

    clean, stub, abbrev, total = extract_body_tokens(idx)
    print("\nbody words: %d total (post word-split), %d '-'-stem-elision (excluded), "
          "%d '0'-abbreviation-dot (excluded), %d clean" % (total, stub, abbrev, len(clean)))
    single = sum(1 for t, _, _ in clean if len(t) < 2)
    clean = [row for row in clean if len(row[0]) >= 2]
    print("  %d single-character fragments also excluded (elision remnants) -> %d clean words"
          % (single, len(clean)))

    token_path = os.path.join(outdir, '%s_body_tokens.txt' % dict_code.lower())
    n_distinct = write_token_file(clean, token_path)
    print("  %d distinct clean tokens -> %s" % (n_distinct, token_path))

    distinct = sorted({t for t, _, _ in clean})
    already, new = headword_overlap(distinct, os.path.join(tu.ROOT, 'sanhw1.txt'))
    print("  of which already a headword somewhere in sanhw1.txt: %d ; genuinely new (body-only) surface: %d"
          % (already, new))

    running_path = os.path.join(outdir, '%s_body_running.txt' % dict_code.lower())
    write_running_text(clean, running_path)

    # --- run the three detectors, unmodified, against the body-token input --------------
    charset_out = os.path.join(outdir, '%s_body_charset_suspects.txt' % dict_code.lower())
    charset_check.main(token_path, charset_out)

    phono_out = os.path.join(outdir, '%s_body_phonotactic_suspects.txt' % dict_code.lower())
    phonotactic_check.main(token_path, phono_out)

    print("\nrunning_text -> %s (feed to ngram/ngramspellcheck.py separately: "
          "cd ../ngram && python ngramspellcheck.py %s <out> 2)" % (running_path, running_path))

    print("\n=== summary ===")
    print("dict=%s  total_spans=%d  stub_excluded=%d  clean_distinct=%d  new_vs_headwords=%d"
          % (dict_code, total, stub, n_distinct, new))


if __name__ == '__main__':
    main()
