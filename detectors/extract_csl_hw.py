"""extract_csl_hw.py  (Python 3)  -- Phase 1.4 helper

Extract headwords IN SOURCE ORDER from a raw csl-orig dictionary file. Each entry
begins with a header line of the form  <L>n<pc>...<k1>HEADWORD<k2>KEY2...  ; this
emits one headword per line, ready for order_check / charset_check / phonotactic_check
to run on the *raw* dictionary text rather than the cleaned sanhw1.txt.

Use --key k1 (default) or --key k2 — some dicts (e.g. MW) repeat k1 across sub-entries
and carry the distinguishing headword in k2.

  python extract_csl_hw.py <.../csl-orig/v02/DICT/DICT.txt> [out=DICT_hw.txt] [--key k1|k2]
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')


def main(infile, outfile, key):
    pat = re.compile('<%s>([^<]*)' % re.escape(key))
    n = 0
    with open(infile, 'r', encoding='utf-8') as f, open(outfile, 'w', encoding='utf-8') as out:
        for line in f:
            if '<L>' not in line:
                continue
            m = pat.search(line)
            if m and m.group(1).strip():
                out.write(m.group(1).strip() + '\n')
                n += 1
    print("%d headwords (source order) -> %s" % (n, outfile))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    key = 'k1'
    if '--key' in sys.argv:
        key = sys.argv[sys.argv.index('--key') + 1]
    if not args:
        print(__doc__)
        sys.exit(1)
    infile = args[0]
    outfile = args[1] if len(args) > 1 else os.path.splitext(os.path.basename(infile))[0] + "_hw.txt"
    main(infile, outfile, key)
