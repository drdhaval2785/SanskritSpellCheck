"""intra_dup.py  (Python 3)  -- detector #5: intra-dictionary self-contradiction

Flags a single dictionary that contains the SAME word spelled two confusable ways
-- e.g. both `kapila` and `kaPila`, or a compound entered twice with a vowel-length
difference (the "compounds stated twice" class in CORRECTIONS). This is a very
high-precision signal: the dictionary already attests the consensus spelling, so its
own near-variant is almost certainly an internal typo/duplicate.

Method: group all headwords by confusion_key, take the most-attested spelling as the
consensus, and for any near-variant (one confusion substitution) flag it in exactly
those dictionaries that ALSO contain the consensus spelling (intersection non-empty
== that dict holds the word twice). Skips whitelisted words.

The variant must also be RARE overall (<= MINORITY_MAX dicts) -- otherwise two
common real words that happen to be confusion-variants (anu/aRu, pAda/pada) get
flagged. With the rarity gate, a hit means "this dict has the widely-attested form
AND a rare near-variant of it" == a genuine internal typo.

  python intra_dup.py [sanhw1=../sanhw1.txt] [out=intra_dup_corrections.txt]
"""
import sys
import os
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

MINORITY_MAX = 2  # the variant must be attested in <= this many dicts overall


def main(sanhw1, outfile):
    whitelist = u.load_whitelist(os.path.join(os.path.dirname(sanhw1) or '.', 'nochange', 'nochange.txt'))
    groups = collections.defaultdict(dict)  # key -> {hw: set(dicts)}
    for hw, dicts in u.parse_sanhw1(sanhw1):
        groups[u.confusion_key(hw)][hw] = set(dicts)

    flagged = []  # (n_dicts_with_both, minority, consensus, [dicts with both])
    for members in groups.values():
        if len(members) < 2:
            continue
        cons = max(members, key=lambda h: len(members[h]))
        cons_d = members[cons]
        for hw, d in members.items():
            if hw == cons or hw in whitelist:
                continue
            if len(d) > MINORITY_MAX:
                continue
            if not u.confusion_sub(hw, cons):
                continue
            both = sorted(d & cons_d)  # dicts that have BOTH spellings
            if both:
                flagged.append((len(both), hw, cons, both))

    flagged.sort(key=lambda r: (-r[0], r[1]))
    with open(outfile, 'w', encoding='utf-8') as out:
        for _, wrong, right, both in flagged:
            for code in both:
                out.write("%s:%s:%s:n\n" % (code, wrong, right))

    print("intra-dictionary self-contradictions: %d  -> %s" % (len(flagged), outfile))
    print("--- top 25 (variant -> consensus  [dicts holding BOTH spellings]) ---")
    for _, wrong, right, both in flagged[:25]:
        print("  %-22s -> %-22s  [%s]" % (wrong, right, ",".join(both)))


if __name__ == "__main__":
    sanhw1 = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "intra_dup_corrections.txt"
    main(sanhw1, outfile)
