"""gen_confusion_weights.py  (Python 3)  -- Phase 2.6: data-driven confusion model

Derive empirical single-character confusion weights from the real correction pairs in
o_vs_O/o_vs_O2.txt (the 2017 human-curated campaign), so candidate ranking can prefer
the *common* confusions (a/A) over rare ones, instead of the hand-set priors.

Emits confusion_weights.json: { "weights": {"<c1c2 sorted>": fraction}, ... } where
the fraction is that char-pair's share of all single-substitution pairs.

  python gen_confusion_weights.py [o_vs_O2=../o_vs_O/o_vs_O2.txt] [out=confusion_weights.json]
"""
import sys
import os
import json
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()


def main(infile, outfile):
    counts = collections.Counter()
    for line in u._read_words(infile):
        if ':' not in line:
            continue
        w1 = line.split(':', 1)[0]
        w2 = line.split(':', 1)[1].split('-', 1)[0]
        if not w1 or not w2 or len(w1) != len(w2):
            continue
        diff = [(a, b) for a, b in zip(w1, w2) if a != b]
        if len(diff) == 1:
            counts[''.join(sorted(diff[0]))] += 1
    total = sum(counts.values())
    weights = {k: round(v / total, 5) for k, v in counts.items()} if total else {}
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump({"source": os.path.basename(infile), "n_pairs": total,
                   "weights": weights, "counts": dict(counts)}, f, ensure_ascii=False, indent=1)
    print("derived %d char-pair weights from %d single-sub pairs -> %s" % (len(weights), total, outfile))
    for k, v in sorted(weights.items(), key=lambda x: -x[1])[:12]:
        print("  %-3s %5.1f%%  (%d)" % (k, v * 100, counts[k]))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    infile = args[0] if args else "../o_vs_O/o_vs_O2.txt"
    outfile = args[1] if len(args) > 1 else "confusion_weights.json"
    main(infile, outfile)
