#!/usr/bin/env python3
"""union_across_runs.py -- measure the recall gain of a SECOND body-aware triage run.

Roadmap ruling D7 (ROADMAP_2026_2027.md, Q3 2026 item 5): the LLM TYPO pass is
stochastic, so recall may grow by *unioning* independent runs rather than by
re-running and overwriting. D7 cut that experiment to three high-yield dicts
(SHS/YAT/ACC) and required the gain to be **measured**, not assumed.

This script performs the union and the measurement. It NEVER writes into the
committed package -- `triage_synthesize.py` would overwrite `<DICT>_file_first_sf.txt`
with the second run's verdicts, silently discarding first-run finds. Instead the
second run's FILE-FIRST set is reconstructed here directly from the gitignored
agent verdicts in `triage_work/`, using the SAME rule triage_synthesize.py line 73
applies:

    survives = confirm.is_typo AND (review is None OR review.fileable)

so run-1 (committed) and run-2 (reconstructed) are compared like for like.

    cd detectors
    python union_across_runs.py SHS YAT ACC --out ../corrections_draft/union_d7.tsv

Every net-new candidate carries the Opus confirm reason AND the Opus review
verdict + reason, which is the adjudication gate D7 requires for new candidates.
"""
import os
import re
import sys
import glob
import json
import argparse

import triage_util

triage_util.reconfigure_stdio()


def load_baseline(dict_code):
    """The committed run-1 FILE-FIRST set: {suspect: suggestion} from <DICT>_file_first_sf.txt.

    Format is the CORRECTIONS standard `DICT:wrong:right:flag`; `;` comments (which
    include the reviewed-out rows) are skipped, so the baseline is the fileable set only.
    """
    path = os.path.join(triage_util.package_dir(dict_code),
                        '%s_file_first_sf.txt' % dict_code)
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            parts = line.split(':')
            if len(parts) >= 3 and parts[0] == dict_code:
                out[parts[1]] = parts[2]
    return out


def load_pool(dict_code):
    """The CURRENT tier-A pool: {suspect: body_kind} from <DICT>_evidence.jsonl.

    Needed to keep the measurement honest. The tier-A pool shrank between run 1 and
    run 2 (the ledger's H2 records YAT 27/247 and ACC 22/174 against today's 219/144),
    because later engine work -- union-attestation demotion, do-not-file suppression --
    removed candidates. So a run-1 find that run 2 does not reproduce is NOT
    automatically stochastic variance: it may simply no longer be a candidate, or may
    now be settled deterministically before the LLM ever sees it. Only a suspect that
    is still routed to the body-aware pass and comes back different is real run-to-run
    variance, and only that number belongs in the D7 verdict.
    """
    path = os.path.join(triage_util.package_dir(dict_code),
                        '%s_evidence.jsonl' % dict_code)
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r['suspect']] = r.get('body_kind', '')
    return out


def load_run2(dict_code):
    """Reconstruct the second run's FILE-FIRST set from the triage_work verdicts.

    Returns (file_first, detail) where file_first is {suspect: suggestion} and detail
    carries the per-suspect evidence trail (classify reason, Opus confirm verdict/reason,
    Opus review verdict/type/reason) for the ones that survive.
    """
    work = triage_util.work_dir(dict_code)
    bcls = triage_util.load_verdicts(work, 'body_adj_*.json')
    bconf = triage_util.load_verdicts(work, 'body_conf_*.json')
    brev = triage_util.load_verdicts(work, 'body_review_*.json')

    file_first, detail = {}, {}
    for suspect, cf in bconf.items():
        if not cf.get('is_typo'):
            continue
        rv = brev.get(suspect)
        if rv is not None and not rv.get('fileable'):
            continue
        cl = bcls.get(suspect, {})
        file_first[suspect] = cl.get('suggestion', '')
        detail[suspect] = {
            'suggestion': cl.get('suggestion', ''),
            'cls_reason': cl.get('reason', ''),
            'cls_confidence': cl.get('confidence', ''),
            'conf_reason': cf.get('reason', ''),
            'review_seen': rv is not None,
            'review_fileable': (rv or {}).get('fileable'),
            'review_type': (rv or {}).get('false_positive_type', ''),
            'review_reason': (rv or {}).get('reason', ''),
        }
    counts = {'classified': len(bcls), 'confirmed_typo': sum(1 for v in bconf.values() if v.get('is_typo')),
              'reviewed': len(brev),
              'reviewed_out': sum(1 for v in brev.values() if not v.get('fileable'))}
    return file_first, detail, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dicts', nargs='+', help='dictionary codes, e.g. SHS YAT ACC')
    ap.add_argument('--out', default=None, help='TSV path for the union table')
    args = ap.parse_args()

    rows = []
    summary = []
    for d in args.dicts:
        base = load_baseline(d)
        pool = load_pool(d)
        run2, detail, counts = load_run2(d)
        both = sorted(set(base) & set(run2))
        net_new = sorted(set(run2) - set(base))
        not_refound = sorted(set(base) - set(run2))

        for s in net_new:
            dt = detail[s]
            rows.append([d, s, dt['suggestion'] or run2[s], 'NET_NEW',
                         dt['cls_confidence'], dt['conf_reason'],
                         ('fileable' if dt['review_fileable'] else
                          ('UNREVIEWED' if not dt['review_seen'] else 'reviewed_out')),
                         dt['review_type'], dt['review_reason']])
        for s in both:
            dt = detail[s]
            rows.append([d, s, base[s], 'BOTH_RUNS', dt['cls_confidence'],
                         dt['conf_reason'],
                         ('fileable' if dt['review_fileable'] else
                          ('UNREVIEWED' if not dt['review_seen'] else 'reviewed_out')),
                         dt['review_type'], dt['review_reason']])
        # Decompose the run-1-only rows: out of the pool / settled before the LLM /
        # genuinely re-judged. Only the last class is run-to-run variance.
        dropped_pool, settled_pre_llm, variance = [], [], []
        for s in not_refound:
            kind = pool.get(s)
            if kind is None:
                dropped_pool.append(s)
                why = 'RUN1_ONLY_POOL_DROPPED'
            elif kind not in triage_util.NEEDS_JUDGMENT:
                settled_pre_llm.append(s)
                why = 'RUN1_ONLY_SETTLED_%s' % kind.upper()
            else:
                variance.append(s)
                why = 'RUN1_ONLY_LLM_VARIANCE'
            rows.append([d, s, base[s], why, '', '', '', '', ''])

        summary.append({
            'dict': d, 'run1': len(base), 'run2': len(run2),
            'both': len(both), 'net_new': len(net_new), 'not_refound': len(not_refound),
            'run1_only_pool_dropped': len(dropped_pool),
            'run1_only_settled_pre_llm': len(settled_pre_llm),
            'run1_only_llm_variance': len(variance),
            'union': len(set(base) | set(run2)),
            'unreviewed_in_run2': sum(1 for s in run2 if not detail[s]['review_seen']),
            **counts,
        })

    cols = ('run1', 'run2', 'both', 'net_new', 'not_refound',
            'run1_only_pool_dropped', 'run1_only_settled_pre_llm',
            'run1_only_llm_variance', 'union')
    hdr = ('run1', 'run2', 'both', 'NET-NEW', 'r1-only', 'r1:pool', 'r1:settled',
           'r1:VAR', 'union')
    print('%-5s' % 'dict' + ''.join('%11s' % h for h in hdr))
    for s in summary:
        print('%-5s' % s['dict'] + ''.join('%11d' % s[c] for c in cols))
    tot = {k: sum(s[k] for s in summary) for k in cols}
    print('%-5s' % 'TOTAL' + ''.join('%11d' % tot[c] for c in cols))

    gain = (tot['net_new'] / tot['run1'] * 100.0) if tot['run1'] else 0.0
    print('\nmeasured recall gain from the union: +%d fileable candidates '
          '(+%.1f%% over the committed %d)' % (tot['net_new'], gain, tot['run1']))
    unrev = sum(s['unreviewed_in_run2'] for s in summary)
    if unrev:
        print('WARNING: %d run-2 survivors carry NO review verdict -- they did not pass the '
              'Opus false-positive gate and must not be filed as-is.' % unrev)

    if args.out:
        out = args.out if os.path.isabs(args.out) else os.path.join(triage_util.HERE, args.out)
        with open(out, 'w', encoding='utf-8') as f:
            f.write('dict\tsuspect\tsuggestion\tstatus\tcls_confidence\t'
                    'opus_confirm_reason\topus_review\treview_fp_type\topus_review_reason\n')
            for r in rows:
                f.write('\t'.join((c or '').replace('\t', ' ').replace('\n', ' ')
                                  for c in r) + '\n')
        print('\nwrote %s (%d rows)' % (out, len(rows)))

    print('\n' + json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
