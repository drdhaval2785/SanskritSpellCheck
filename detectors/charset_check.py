"""charset_check.py  (Python 3)  -- detector #3 (charset half)

Flag headwords containing any character that is not legal SLP1. Catches the
encoding-error class seen all over CORRECTIONS (Latin-with-diacritic like Ç/ç,
Greek-like letters, stray Devanagari, digits, whitespace, danda '|', IAST that
leaked into an SLP1 field). Pure structural check -- needs no base dictionary, so
it finds errors the pattern/cross-dict detectors are blind to.

Run on the merged headword list, or point it at any raw SLP1 file:
  python charset_check.py [input=../sanhw1.txt] [output=charset_suspects.txt]

Output line format matches faultfinder (so faultfinder3a-html.php / triage can
consume it):  X:CHS=<bad chars>:D
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()


def classify_char(ch):
    o = ord(ch)
    if ch.isspace():
        return "whitespace"
    if ch.isdigit():
        return "digit"
    if o < 128:
        return "ascii-punct"
    if 0x0900 <= o <= 0x097F:
        return "devanagari"
    if 0x0370 <= o <= 0x03FF:
        return "greek"
    if (0x00C0 <= o <= 0x024F) or (0x1E00 <= o <= 0x1EFF):
        return "latin-diacritic"
    return "other"


def main(infile, outfile):
    import collections
    cats = collections.Counter()
    n = total = 0
    with open(outfile, 'w', encoding='utf-8') as out:
        for line in u._read_words(infile):
            if not line:
                continue
            total += 1
            if ':' in line:
                hw, dicts = line.split(':', 1)
            else:
                hw, dicts = line, ''
            bad = [ch for ch in hw if ch not in u.ALPHABET]
            if bad:
                n += 1
                for ch in bad:
                    cats[classify_char(ch)] += 1
                detail = ''.join(sorted(set(bad)))
                out.write("%s:CHS=%s:%s\n" % (hw, detail, dicts))
    print("scanned %d headwords; %d with non-SLP1 chars -> %s" % (total, n, outfile))
    for k, v in cats.most_common():
        print("  %-16s %d" % (k, v))


if __name__ == "__main__":
    infile = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "charset_suspects.txt"
    main(infile, outfile)
