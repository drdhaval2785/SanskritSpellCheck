#!/usr/bin/env python3
"""Regenerate nochange/do_not_file_suppress.txt from the per-dict do-not-file lists.

The body-grounded triage (see corrections_draft/) emits, for every triaged
dictionary, a ``<DICT>_wrong_readings.txt`` -- the standing do-not-file list of
spellings the dictionary documents on purpose (wrong-reading ``w.r.`` apparatus,
``v.l.``, in-composition / sandhi forms, cross-references, other grammatical /
Vedic notes). Filing a "correction" for any of these CORRUPTS the source.

This script collects the headword (left column, before ``->``) from every such
file, dedups, and writes them to a single suppression file that
``slp1util.load_whitelist`` unions with the human-curated ``nochange.txt`` so the
detectors never re-surface them. Provenance stays separate from nochange.txt.

Re-run this whenever more dictionaries are triaged:

    cd detectors && python gen_do_not_file_suppress.py
"""
import glob
import os

from triage_util import GITHUB, ROOT, reconfigure_stdio

reconfigure_stdio()

OUT = os.path.join(ROOT, 'nochange', 'do_not_file_suppress.txt')


def headwords_from(path):
    """Yield the SLP1 headword (left of '->') from each data row of a
    *_wrong_readings.txt file. Skips comments, section headers and blanks."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.lstrip('﻿').rstrip('\n')
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            if '->' not in s:
                continue
            hw = s.split('->', 1)[0].strip()
            if hw:
                yield hw


def main():
    pattern = os.path.join(ROOT, 'corrections_draft', '*', '*_wrong_readings.txt')
    files = sorted(glob.glob(pattern))
    words = {}
    per_file = []
    for path in files:
        hws = set(headwords_from(path))
        per_file.append((os.path.relpath(path, GITHUB), len(hws)))
        for hw in hws:
            words.setdefault(hw, None)

    out = sorted(words)
    header = [
        '# do_not_file_suppress.txt -- detector suppression list (auto-generated)',
        '#',
        '# Headwords that LOOK like misspellings but which a dictionary documents on',
        '# purpose (wrong-reading apparatus, variae lectiones, in-composition / sandhi',
        '# forms, cross-references, grammatical / Vedic notes). Collected from the left',
        "# column of every corrections_draft/<DICT>/<DICT>_wrong_readings.txt produced by",
        '# the body-grounded triage. slp1util.load_whitelist() unions these with the',
        '# human-curated nochange.txt so the detectors never re-flag them.',
        '#',
        '# DO NOT hand-edit -- regenerate with detectors/gen_do_not_file_suppress.py',
        '# after triaging more dictionaries.',
        '#',
        f'# {len(out)} unique headwords from {len(files)} dictionaries:',
    ]
    for rel, n in per_file:
        header.append(f'#   {rel}: {n}')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(header) + '\n')
        for hw in out:
            f.write(hw + '\n')

    print(f'{len(files)} files -> {len(out)} unique suppressed headwords')
    print(f'wrote {os.path.relpath(OUT, GITHUB)}')


if __name__ == '__main__':
    main()
