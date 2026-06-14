"""phonotactic_check.py  (Python 3)  -- detector #4: phonotactic / anti-sandhi rules

Rule-based, ABSOLUTE validity check (unlike the statistical faultfinder, which only
knows "pattern absent from a base dict"). Flags SLP1 headwords that violate hard
Sanskrit phonotactic constraints, so it catches impossible forms even when they sit
in the base dictionary. Only high-confidence rules are used (anusvara/visarga/
candrabindu are vowel modifiers and MUST sit on a vowel; an anusvara cannot precede a
vowel; two identical vowels never sit adjacent):

  MAV  anusvara M immediately FOLLOWED by a vowel   (should be m / a nasal)
  MPC  anusvara M not sitting on a vowel            (consonant+M or word-initial M)
  HPC  visarga  H not sitting on a vowel            (consonant+H or word-initial H)
  TIL  candrabindu ~ mis-placed (not on a vowel, or before a vowel)
  VVD  two identical vowels adjacent                (aa/ii/uu... -> A/I/U)

  python phonotactic_check.py [input=../sanhw1.txt] [out=phonotactic_suspects.txt]

Output: faultfinder format  X:PH-<rule>=<detail>:D
"""
import sys
import os
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

VOW = u.VOWELS


def first_violation(w):
    for i, ch in enumerate(w):
        prev = w[i - 1] if i > 0 else ''
        nxt = w[i + 1] if i + 1 < len(w) else ''
        if ch == 'M':
            if nxt in VOW:
                return ('MAV', 'M' + nxt)
            if prev not in VOW:
                return ('MPC', (prev or '^') + 'M')
        elif ch == 'H':
            if prev not in VOW:
                return ('HPC', (prev or '^') + 'H')
        elif ch == '~':
            if prev not in VOW or nxt in VOW:
                return ('TIL', (prev or '^') + '~' + (nxt or '$'))
        if ch in VOW and prev == ch:
            return ('VVD', ch + ch)
    return None


def main(infile, outfile):
    cats = collections.Counter()
    n = total = 0
    with open(outfile, 'w', encoding='utf-8') as out:
        for line in u._read_words(infile):
            if not line:
                continue
            total += 1
            hw, dicts = (line.split(':', 1) + [''])[:2] if ':' in line else (line, '')
            v = first_violation(hw)
            if v:
                n += 1
                cats[v[0]] += 1
                out.write("%s:PH-%s=%s:%s\n" % (hw, v[0], v[1], dicts))
    print("scanned %d; phonotactic violations %d -> %s" % (total, n, outfile))
    for k, c in cats.most_common():
        print("  %-5s %d" % (k, c))


if __name__ == "__main__":
    infile = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "phonotactic_suspects.txt"
    main(infile, outfile)
