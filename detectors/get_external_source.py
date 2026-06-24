#!/usr/bin/env python3
"""get_external_source.py -- fetch a dictionary source that is NOT in the csl-orig merge
into external_src/<dict>/, so the body-grounded triage can read it like any csl-orig dict.

These sources are gitignored (see .gitignore): this repo hosts QA tooling and do-not-file
lists, not third-party dictionary text. Re-run this on a fresh clone to re-stage them.

  python get_external_source.py PD          # download + unzip the first PD source
  python get_external_source.py PD --list   # show what's registered, don't download

PD = "An Encyclopaedic Dictionary of Sanskrit on Historical Principles" (Deccan College,
Poona, 1976-2009; English glosses). Digital edition (c) 2014 The Sanskrit Library and
Thomas Malten, CC BY-NC-SA 3.0 -- non-commercial reuse with attribution + share-alike.
A SECOND PD source is expected; register it below as pd[1] when its URL is known.
"""
import io
import os
import sys
import zipfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util as tu

tu.reconfigure_stdio()

# dict code -> ordered list of sources. Each: (zip URL, member path inside the zip, output name).
# The FIRST entry whose download succeeds populates external_src/<dict>/<dict>.txt; extra
# members (meta/header) are saved alongside. Add the 2nd PD source as a new tuple here.
SOURCES = {
    'PD': [
        ("https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/downloads/pdtxt.zip",
         "txt/pd.txt", "pd.txt"),
    ],
}
# sibling members worth keeping (coding docs + license) when present in the same zip.
EXTRA_MEMBERS = {'txt/pd-meta2.txt': 'pd-meta2.txt', 'txt/pdheader.xml': 'pdheader.xml'}


def fetch(dict_code):
    d = dict_code.upper()
    if d not in SOURCES:
        sys.exit("no external source registered for %s (known: %s)" % (d, ', '.join(SOURCES)))
    out_dir = os.path.join(tu.EXTERNAL_SRC, d.lower())
    os.makedirs(out_dir, exist_ok=True)
    for url, member, outname in SOURCES[d]:
        print("downloading %s ..." % url)
        with urllib.request.urlopen(url) as r:                       # noqa: S310 (trusted Cologne host)
            blob = r.read()
        zf = zipfile.ZipFile(io.BytesIO(blob))
        with open(os.path.join(out_dir, outname), 'wb') as f:
            f.write(zf.read(member))
        for m, name in EXTRA_MEMBERS.items():
            if m in zf.namelist():
                with open(os.path.join(out_dir, name), 'wb') as f:
                    f.write(zf.read(m))
        path = tu.source_file(d)
        n = sum(1 for line in open(path, encoding='utf-8') if line.startswith('<L>'))
        print("staged %s  (%d entries)  -> %s" % (outname, n, os.path.relpath(path, tu.ROOT)))
        return
    sys.exit("all sources failed for %s" % d)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    code = args[0]
    if '--list' in sys.argv:
        for url, member, outname in SOURCES.get(code.upper(), []):
            print("%s  <-  %s (%s)" % (outname, url, member))
        return
    fetch(code)


if __name__ == '__main__':
    main()
