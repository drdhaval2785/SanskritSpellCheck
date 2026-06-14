"""order_check.py  (Python 3)  -- detector #6: alphabetic-order checker

Reads a dictionary's headwords IN SOURCE ORDER (one per line, SLP1) and reports
adjacent pairs that are out of Sanskrit collation order -- the "alphabetic
misordering" class (e.g. AP90 sub-headword misordering in CORRECTIONS). Collation
uses the repo's own ordering (slp1util.sanskrit_sort_key, mirroring sanhw1.py:
SLP1 alphabet + anusvara-before-varga sorts as the homorganic nasal).

NOTE on input: this needs the dictionary's headwords in *source* order. The
HeadwordLists/*.txt in this repo are already sorted/deduped, so a real run takes a
source-order list extracted from the dictionary text in the csl-orig sibling repo.
The logic is verified here with --selftest.

  python order_check.py <source_order_headwords.txt> [out=order_suspects.txt]
  python order_check.py --selftest
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()


def check(words):
    """Return list of (index, prev, cur) where cur sorts before prev."""
    out = []
    for i in range(1, len(words)):
        if u.sanskrit_sort_key(words[i]) < u.sanskrit_sort_key(words[i - 1]):
            out.append((i, words[i - 1], words[i]))
    return out


def selftest():
    # correctly Sanskrit-sorted (note aMga sorts as aNga, between aNkura and the
    # k-words; agni sorts first):
    good = ["agni", "aNka", "aNkura", "aMga", "kala", "kAla"]
    assert check(good) == [], "sorted list flagged: %r" % check(good)
    # move 'agni' (which sorts first) to the end -> exactly one violation:
    bad = good[1:] + [good[0]]
    v = check(bad)
    assert len(v) == 1 and v[0][2] == "agni", v
    print("selftest OK: sorted list -> 0 violations; planted 'agni' at end -> flagged")


def main(infile, outfile):
    words = [w for w in u._read_words(infile) if w]
    bad = check(words)
    with open(outfile, 'w', encoding='utf-8') as out:
        for i, prev, cur in bad:
            out.write("%s:ORD=after_%s:line%d\n" % (cur, prev, i + 1))
    print("headwords: %d   order violations: %d -> %s" % (len(words), len(bad), outfile))
    for i, prev, cur in bad[:25]:
        print("  line %d: %s should not follow %s" % (i + 1, cur, prev))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
        selftest()
    elif len(sys.argv) >= 2:
        main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "order_suspects.txt")
    else:
        print(__doc__)
        sys.exit(1)
