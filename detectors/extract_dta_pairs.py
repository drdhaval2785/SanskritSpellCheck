#!/usr/bin/env python3
"""extract_dta_pairs.py -- harvest historical->modern German spelling pairs from a DTA
lingattr-TEI corpus zip (dta-lingattr-tei_*.zip from deutschestextarchiv.de/download).

Each token is `<w ... norm="MODERN">SURFACE</w>`; the DTA::CAB `norm` is the modern
orthographic form, the element text is the historical surface form. A pair where
surface != norm is an orthographic drift candidate. We emit  old<TAB>new<TAB>count
(surface=old, norm=new), letter-only, deduped, sorted by frequency -- the lowest-common-
denominator input for merge_reform_pairs.py, which then dic-validates (old NOT in de_DE,
new IN de_DE) so inflection/OCR noise that isn't a real historical->modern pair drops out.

Streams the zip (no multi-GB unpack) and skips any corrupt member (a resume glitch left one).

  cd detectors && python extract_dta_pairs.py ../external_src/dta/dta_lingattr.zip ../external_src/dta/dta_de_pairs.tsv
"""
import io
import re
import sys
import zipfile
from collections import Counter

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import triage_util
triage_util.reconfigure_stdio()

# <w ...norm="NORM"...>SURFACE</w> -- NORM may sit before/after other attrs; SURFACE is plain text.
_W = re.compile(r'<w\b[^>]*\bnorm="([^"]*)"[^>]*>([^<]*)</w>')
_LETTERS = re.compile(r'^[A-Za-zÀ-ÿäöüÄÖÜß]+$')   # drop punctuation / numerals / mixed tokens


def main():
    if len(sys.argv) < 3:
        sys.exit('usage: python extract_dta_pairs.py <lingattr.zip> <out.tsv> [min_count=2]')
    zippath, outpath = sys.argv[1], sys.argv[2]
    min_count = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    pairs = Counter()
    files = ok = bad = 0
    zf = zipfile.ZipFile(zippath)
    names = [n for n in zf.namelist() if n.endswith('.xml')]
    print('lingattr TEI files: %d' % len(names))
    for n in names:
        files += 1
        try:
            data = zf.read(n).decode('utf-8', 'replace')
            ok += 1
        except Exception:           # corrupt member (resume glitch): zlib.error / BadZipFile / etc.
            bad += 1
            continue
        for norm, surf in _W.findall(data):
            norm = norm.strip()
            surf = surf.strip()
            if surf and norm and surf != norm and _LETTERS.match(surf) and _LETTERS.match(norm):
                pairs[(surf, norm)] += 1
        if files % 500 == 0:
            print('  %d/%d files, %d distinct drift pairs so far' % (files, len(names), len(pairs)))

    kept = [(s, n, c) for (s, n), c in pairs.items() if c >= min_count]
    kept.sort(key=lambda r: -r[2])
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('# DTA lingattr-TEI historical->modern pairs (surface != CAB norm); old<TAB>new<TAB>count\n')
        f.write('# %d files read (%d unreadable); %d distinct pairs, %d with count >= %d\n'
                % (ok, bad, len(pairs), len(kept), min_count))
        for s, n, c in kept:
            f.write('%s\t%s\t%d\n' % (s, n, c))
    print('read %d files (%d corrupt skipped); %d distinct drift pairs, %d kept (count >= %d) -> %s'
          % (ok, bad, len(pairs), len(kept), min_count, outpath))
    print('top 15:', ['%s->%s(%d)' % (s, n, c) for s, n, c in kept[:15]])


if __name__ == '__main__':
    main()
