"""eval.py  (Python 3)  -- Phase 1.5 + 1.6: evaluation harness

Measures the detector suite against the data we actually have:

  RECALL vs the 2017 campaign -- o_vs_O/o_vs_O2.txt holds 3884 human-curated
    single-letter confusion pairs. How many does each corrector re-discover? (A
    real recall number against a historical candidate set; <100% is expected, since
    the new detectors suppress pairs where both spellings are attested real words.)

  FALSE-POSITIVE sanity vs known-good -- nochange/nochange.txt holds ~31k words
    confirmed correct. A detector flagging one of those is a false positive; the
    count should be ~0 (the detectors suppress the whitelist).

  NOVELTY -- how many corrector candidates are NEW (not in the 2017 pairs), i.e. what
    the suite finds beyond the old single-letter cross-dict method.

  TIER CHECK -- of the recovered known pairs, what run_all tier did they land in?
    (Known-real pairs should concentrate in tier A/B.)

  SPOT-CHECK SAMPLE (1.5) -- writes the top-N tier-A candidates with scan links to
    spotcheck_sample.txt for human precision verification (true precision needs eyes
    on the scans), and reports an automated proxy.

  python eval.py   (reads the *_corrections.txt the detectors already produced; run
                    run_all.py first if they are missing)
"""
import sys
import os
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORRECTORS = ['spell_correct', 'consensus', 'intra_dup', 'dict_vs_corpus']
SCAN = "http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s"


def load_corrector_pairs(name):
    """{frozenset({wrong,right})} and {wrong} from a *_corrections.txt."""
    path = os.path.join(HERE, name + '_corrections.txt')
    pairs, wrongs = set(), set()
    if not os.path.exists(path):
        return pairs, wrongs
    for line in u._read_words(path):
        p = line.split(':')
        if len(p) >= 3 and p[1] != p[2]:
            pairs.add(frozenset((p[1], p[2])))
            wrongs.add(p[1])
    return pairs, wrongs


def load_known_pairs():
    known = set()
    path = os.path.join(ROOT, 'o_vs_O', 'o_vs_O2.txt')
    for line in u._read_words(path):
        if ':' not in line:
            continue
        w1 = line.split(':', 1)[0]
        w2 = line.split(':', 1)[1].split('-', 1)[0]
        if w1 and w2 and w1 != w2:
            known.add(frozenset((w1, w2)))
    return known


def load_tiers():
    tier = {}
    path = os.path.join(HERE, 'combined_candidates.txt')
    if not os.path.exists(path):
        return tier
    for line in u._read_words(path):
        cols = line.split('\t')
        if len(cols) >= 3 and ' -> ' in cols[2]:
            tier[cols[2].split(' -> ', 1)[0]] = cols[0]
    return tier


def main():
    known = load_known_pairs()
    nochange = u.load_whitelist(os.path.join(ROOT, 'nochange', 'nochange.txt'))
    per_pairs, per_wrong = {}, {}
    for name in CORRECTORS:
        per_pairs[name], per_wrong[name] = load_corrector_pairs(name)
    union = set().union(*per_pairs.values()) if per_pairs else set()

    print("=== RECALL vs %d historical o_vs_O pairs ===" % len(known))
    for name in CORRECTORS:
        rec = len(known & per_pairs[name])
        print("  %-15s recovers %5d / %d = %5.1f%%   (emits %d pairs)"
              % (name, rec, len(known), 100 * rec / len(known) if known else 0, len(per_pairs[name])))
    urec = len(known & union)
    print("  %-15s recovers %5d / %d = %5.1f%%" % ("ALL (union)", urec, len(known),
                                                   100 * urec / len(known) if known else 0))
    novel = len(union - known)
    print("  novelty: %d corrector candidate-pairs are NEW (not in the 2017 set)" % novel)

    print("=== FALSE-POSITIVE sanity vs %d known-good (nochange) words ===" % len(nochange))
    for name in CORRECTORS:
        fp = len(per_wrong[name] & nochange)
        print("  %-15s flags %d known-good words (want 0)" % (name, fp))

    tier = load_tiers()
    if tier:
        rec_tiers = collections.Counter()
        for pr in (known & union):
            for w in pr:
                if w in tier:
                    rec_tiers[tier[w]] += 1
                    break
        print("=== recovered known pairs by run_all tier ===  " +
              ", ".join("%s=%d" % (t, rec_tiers[t]) for t in 'ABC'))

    write_spotcheck(tier)


def write_spotcheck(tier, n=100):
    """Top-N tier-A candidates from combined_candidates.txt for human verification."""
    path = os.path.join(HERE, 'combined_candidates.txt')
    if not os.path.exists(path):
        print("(no combined_candidates.txt; run run_all.py for the spot-check sample)")
        return
    rows = []
    for line in u._read_words(path):
        c = line.split('\t')
        if len(c) >= 5 and c[0] == 'A':
            sus = c[2].split(' -> ', 1)[0]
            sug = c[2].split(' -> ', 1)[1] if ' -> ' in c[2] else ''
            dets = c[3].strip('[]')
            dicts = c[4].strip('[]')
            rows.append((sus, sug, dets, dicts))
        if len(rows) >= n:
            break
    out = os.path.join(HERE, 'spotcheck_sample.txt')
    with open(out, 'w', encoding='utf-8') as f:
        f.write("# top %d tier-A candidates for human precision verification\n" % len(rows))
        f.write("# suspect -> suggestion | detectors | dicts | scan\n")
        for sus, sug, dets, dicts in rows:
            d0 = dicts.split(',')[0] if dicts else 'MW'
            f.write("%s -> %s | %s | %s | %s\n" % (sus, sug, dets, dicts, SCAN % (d0, sus)))
    multi = sum(1 for r in rows if ',' in r[2])
    print("=== SPOT-CHECK (1.5): %d tier-A rows -> %s ===" % (len(rows), out))
    print("  auto-proxy: %d/%d (%.0f%%) flagged by >=2 detectors; verify against scans for true precision"
          % (multi, len(rows), 100 * multi / len(rows) if rows else 0))


if __name__ == "__main__":
    main()
