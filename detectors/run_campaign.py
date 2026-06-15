"""run_campaign.py  (Python 3)  -- Phase 2.4: per-dictionary campaigns

Splits the unified detector suite per dictionary so you can work one dictionary's
correction queue at a time (CORRECTIONS issues are filed per dictionary). Reuses
run_all's aggregation, scoring and review-HTML, then for each dictionary emits a
focused, tiered review package of the candidates that implicate it.

Outputs (gitignored, regenerable):
  campaigns/<DICT>/review.html      -- the dict's accept/reject review UI
  campaigns/<DICT>/candidates.txt   -- the dict's ranked candidate list
  campaigns/campaign_summary.txt    -- dashboard: per-dict A/B/C counts (campaign order)

  python run_campaign.py [--rerun] [sanhw1=../sanhw1.txt]
"""
import sys
import os
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import run_all as ra

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))


def main(sanhw1, rerun):
    ra.ensure_outputs(sanhw1, rerun)
    dcs = u.load_dcs_lemmas(u.dcs_path())
    weights = u.load_confusion_weights()
    cands = ra.aggregate()

    by_dict = collections.defaultdict(list)   # DICT -> [(score, tier, band, best, cand)]
    for c in cands.values():
        score, tier, best, band = ra.score_tier(c, dcs, weights)
        for d in c.dicts:
            by_dict[d].append((score, tier, best, band, c))

    base = os.path.join(HERE, 'campaigns')
    os.makedirs(base, exist_ok=True)
    summary = []
    for d, rows in by_dict.items():
        rows.sort(key=lambda r: (-r[0], r[4].suspect))
        tiers = collections.Counter(r[1] for r in rows)
        ddir = os.path.join(base, d)
        os.makedirs(ddir, exist_ok=True)
        with open(os.path.join(ddir, 'candidates.txt'), 'w', encoding='utf-8') as f:
            for score, tier, band, best, c in rows:
                f.write("%s\t%d\t%s -> %s\t[%s]\n"
                        % (tier, score, c.suspect, best or "(flag)", ",".join(sorted(c.detectors))))
        ra.write_review_html(rows, os.path.join(ddir, 'review.html'))
        summary.append((tiers['A'], tiers['B'], tiers['C'], len(rows), d))

    summary.sort(key=lambda s: (-s[0], -s[3]))   # campaign order: most tier-A first
    with open(os.path.join(base, 'campaign_summary.txt'), 'w', encoding='utf-8') as f:
        f.write("# per-dictionary campaign dashboard (work highest tier-A first)\n")
        f.write("# dict\ttierA\ttierB\ttierC\ttotal\n")
        for a, b, cc, tot, d in summary:
            f.write("%s\t%d\t%d\t%d\t%d\n" % (d, a, b, cc, tot))

    print("per-dictionary campaign packages -> campaigns/<DICT>/  (%d dicts)" % len(summary))
    print("dict   tierA  tierB  tierC  total   (campaign order)")
    for a, b, cc, tot, d in summary[:15]:
        print("  %-6s %5d  %5d  %5d  %5d" % (d, a, b, cc, tot))


if __name__ == "__main__":
    rerun = '--rerun' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    main(args[0] if args else "../sanhw1.txt", rerun)
