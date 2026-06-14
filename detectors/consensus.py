"""consensus.py  (Python 3)  -- detector #2: cross-dictionary consensus voting

Generalizes the pairwise o_vs_O method to N-way voting. Headwords are grouped by
confusion_key (so confusable spellings land together); within a group the spelling
attested in the MOST dictionaries is the "consensus", and any near-variant attested
in far fewer dictionaries is flagged as a likely error, with the consensus spelling
as the suggested correction.

Two gates keep precision high (the confusion_key alone over-merges distinct words
like ata/aTa, and a trailing case ending like aNgaH vs aNga must NOT count as a
"typo"):
  * the minority differs from the consensus by exactly ONE confusion substitution
    (same length: a/A, k/K, s/S, o/O, v/b, t/w ... -- not an added/dropped ending),
    and
  * the consensus is attested in at least MARGIN more dictionaries than the
    minority, and the minority itself sits in <= MINORITY_MAX dictionaries.

Reads sanhw1.txt. Writes the CORRECTIONS standard format (DICT:wrong:right:n) plus
a ranked human-readable list. Skips whitelisted (nochange.txt) words.

  python consensus.py [sanhw1=../sanhw1.txt] [out=consensus_corrections.txt]
"""
import sys
import os
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()

MINORITY_MAX = 2    # only flag spellings attested in <= this many dictionaries
MARGIN = 3          # consensus must have >= MINORITY count + MARGIN dictionaries


def main(sanhw1, outfile):
    whitelist = u.load_whitelist(os.path.join(os.path.dirname(sanhw1) or '.', 'nochange', 'nochange.txt'))
    dcs = u.load_dcs_lemmas(u.dcs_path())  # suppress minorities that are real attested words
    groups = collections.defaultdict(list)
    for hw, dicts in u.parse_sanhw1(sanhw1):
        groups[u.confusion_key(hw)].append((hw, set(dicts)))

    flagged = []  # (margin, minority, consensus, minority_dicts, consensus_dicts)
    for members in groups.values():
        if len(members) < 2:
            continue
        members.sort(key=lambda m: -len(m[1]))
        cons_hw, cons_d = members[0]
        for hw, d in members[1:]:
            if hw == cons_hw or hw in whitelist:
                continue
            if u.normalize_lemma(hw) in dcs:   # the "minority" is an attested DCS lemma -> a real word
                continue
            if len(d) > MINORITY_MAX:
                continue
            if len(cons_d) - len(d) < MARGIN:
                continue
            if not u.confusion_sub(hw, cons_hw):
                continue
            flagged.append((len(cons_d) - len(d), hw, cons_hw, sorted(d), sorted(cons_d)))

    flagged.sort(key=lambda r: (-r[0], r[1]))
    with open(outfile, 'w', encoding='utf-8') as out:
        for _, wrong, right, wd, _cd in flagged:
            for code in wd:
                out.write("%s:%s:%s:n\n" % (code, wrong, right))

    print("groups: %d   flagged minority spellings: %d  -> %s"
          % (sum(1 for g in groups.values() if len(g) > 1), len(flagged), outfile))
    print("(gates: one confusion substitution, minority in <=%d dicts, consensus >= minority+%d dicts)"
          % (MINORITY_MAX, MARGIN))
    print("--- top 20 by margin (wrong -> consensus  [minority dicts | consensus dicts]) ---")
    for margin, wrong, right, wd, cd in flagged[:20]:
        print("  %-22s -> %-22s  [%s | %d dicts]" % (wrong, right, ",".join(wd), len(cd)))


if __name__ == "__main__":
    sanhw1 = sys.argv[1] if len(sys.argv) > 1 else "../sanhw1.txt"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "consensus_corrections.txt"
    main(sanhw1, outfile)
