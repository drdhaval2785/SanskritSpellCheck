#!/usr/bin/env python3
"""build_verify_batches.py -- deterministic prep for the net-new verification pass.

Splits netnew_worklist.tsv into per-dictionary batch files the verification workflow
reads. Batching is grouped BY DICT so each agent greps a single source file, and the
source path is resolved once here (via triage_util.source_file) rather than by each
agent -- the same resolver make_changefiles.py and the triage steps use, so a dict
staged in external_src/ is handled identically.

    cd corrections_draft
    python build_verify_batches.py                # -> verify_work/verify_batch_NNN.jsonl

Each line: {pass, dict, wrong, right, opus_confirm_reason, opus_review_reason, src}
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'detectors'))

import triage_util  # noqa: E402

triage_util.reconfigure_stdio()

BATCH_SIZE = 10


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--worklist', default=os.path.join(HERE, 'netnew_worklist.tsv'))
    ap.add_argument('--out', default=os.path.join(HERE, 'verify_work'))
    args = ap.parse_args()

    with open(args.worklist, encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))

    by_dict = {}
    for r in rows:
        by_dict.setdefault(r['dict'], []).append(r)

    os.makedirs(args.out, exist_ok=True)
    for stale in os.listdir(args.out):
        if stale.startswith('verify_batch_') and stale.endswith('.jsonl'):
            os.remove(os.path.join(args.out, stale))

    n = 0
    missing_src = []
    for d in sorted(by_dict):
        src = triage_util.source_file(d)
        if not os.path.exists(src):
            missing_src.append((d, src))
        items = by_dict[d]
        for i in range(0, len(items), BATCH_SIZE):
            chunk = items[i:i + BATCH_SIZE]
            path = os.path.join(args.out, 'verify_batch_%03d.jsonl' % n)
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                for r in chunk:
                    f.write(json.dumps({
                        'pass': r['pass'], 'dict': d,
                        'wrong': r['wrong'], 'right': r['right'],
                        'opus_confirm_reason': r['opus_confirm_reason'],
                        'opus_review_reason': r['opus_review_reason'],
                        'src': src.replace('\\', '/'),
                    }, ensure_ascii=False) + '\n')
            print('  %-5s batch %03d: %2d rows' % (d, n, len(chunk)))
            n += 1

    print('wrote %d batch files (%d rows) in %s' % (n, len(rows), args.out))
    if missing_src:
        print('ERROR: source text missing for %d dict(s) -- verification cannot read the entry:'
              % len(missing_src))
        for d, p in missing_src:
            print('  %s -> %s' % (d, p))
        sys.exit(1)


if __name__ == '__main__':
    main()
