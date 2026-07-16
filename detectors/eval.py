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

  DETECTION-LEVEL METRICS (H825, ruling D11) -- against the held-out gold set in
    detectors/gold_corrections.tsv (build_gold_set.py, derived from the body-grounded
    triage's corrections_draft/file_first_verified.tsv -- never used to tune the
    detectors themselves): per-corrector precision / recall / F0.5 (beta=0.5,
    precision-weighted, Grundkiewicz D15-1052) against the 109 POSITIVE (fileable
    typo) rows, FPR against the large nochange whitelist, and a HARM metric = the
    fraction of the 13 HARM rows (EDITORIAL/DNF/DROP -- duplicate/apparatus
    collisions, do-not-file spellings, stale fixes) a corrector wrongly proposes to
    "fix". FP=0 on the nochange whitelist stays the shipping/filing gate (now a real
    gate: nonzero exit code on violation) -- the historical FALSE-POSITIVE sanity
    check above and this gate are the same measurement, not a conflict.

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
GOLD = os.path.join(HERE, 'gold_corrections.tsv')


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


def load_gold():
    """Held-out gold set (detectors/gold_corrections.tsv). Returns (positive_wrongs,
    harm_wrongs); empty sets (with a warning) if the file hasn't been generated yet."""
    positive, harm = set(), set()
    if not os.path.exists(GOLD):
        print("(no gold_corrections.tsv; run detectors/build_gold_set.py for detection metrics)")
        return positive, harm
    for line in u._read_words(GOLD):
        if line.startswith('#') or not line:
            continue
        cols = line.split('\t')
        if cols[0] == 'row_id':
            continue
        _row_id, _dict, wrong, _right, cls, _verdict = cols
        (positive if cls == 'POSITIVE' else harm).add(wrong)
    return positive, harm


def f_beta(precision, recall, beta=0.5):
    if precision == 0 and recall == 0:
        return 0.0
    b2 = beta * beta
    return (1 + b2) * precision * recall / (b2 * precision + recall)


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
    filing_gate_ok = True
    for name in CORRECTORS:
        fp = len(per_wrong[name] & nochange)
        print("  %-15s flags %d known-good words (want 0)" % (name, fp))
        if fp:
            filing_gate_ok = False

    gold_positive, gold_harm = load_gold()
    if gold_positive:
        print("=== DETECTION-LEVEL METRICS vs gold_corrections.tsv "
              "(%d POSITIVE, %d HARM) ===" % (len(gold_positive), len(gold_harm)))
        for name in CORRECTORS + ['ALL (union)']:
            wrongs = per_wrong[name] if name != 'ALL (union)' else set().union(*per_wrong.values())
            tp = wrongs & gold_positive
            fp_harm = wrongs & gold_harm
            fp_whitelist = wrongs & nochange
            precision_denom = len(tp) + len(fp_harm) + len(fp_whitelist)
            precision = len(tp) / precision_denom if precision_denom else 0.0
            recall = len(tp) / len(gold_positive) if gold_positive else 0.0
            fpr = len(fp_whitelist) / len(nochange) if nochange else 0.0
            harm = len(fp_harm) / len(gold_harm) if gold_harm else 0.0
            print("  %-15s P=%5.1f%% R=%5.1f%% F0.5=%5.3f  FPR=%.6f  harm=%5.1f%% "
                  "(tp=%d fp_whitelist=%d fp_harm=%d)"
                  % (name, 100 * precision, 100 * recall, f_beta(precision, recall),
                     fpr, 100 * harm, len(tp), len(fp_whitelist), len(fp_harm)))

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

    print("=== FILING GATE: %s ===" % ("PASS" if filing_gate_ok else "FAIL"))
    if not filing_gate_ok:
        sys.exit(1)


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
