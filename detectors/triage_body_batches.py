#!/usr/bin/env python3
"""triage_body_batches.py -- prepare body-aware verification batches.

The deterministic body classifier (triage_bodies.py) settles the wr/variant/xref
candidates (MW documents the spelling -> never file) and the missing ones (not in the
current source -> unlocatable). What it CANNOT settle is the `realword` set: an entry
with a real gloss might be a genuine distinct word (gloss fits the SUSPECT) OR a
misspelled key whose gloss actually belongs to the SUGGESTION (a real typo). That needs
semantic judgment, which an LLM does reliably once it can see MW's own entry text.

This writes triage_work/body_batch_NNN.jsonl (30 rows each) over the realword/thin/
multi-mixed candidates, each row carrying the entry body + the suggestion + the prior
adjudication, ready for the body-aware verification workflow.

Usage:  cd detectors && python triage_body_batches.py [MW]
"""
import os
import json

import triage_util

triage_util.reconfigure_stdio()
ROOT = triage_util.ROOT


def main():
    dict_code = triage_util.dict_arg()
    pkg = triage_util.package_dir(dict_code)
    work = triage_util.work_dir(dict_code)

    with open(os.path.join(pkg, '%s_evidence.jsonl' % dict_code), encoding='utf-8') as f:
        rows = [json.loads(l) for l in f]
    need = [r for r in rows if r['body_kind'] in triage_util.NEEDS_JUDGMENT]

    batch = []
    for r in need:
        batch.append({
            'suspect': r['suspect'],
            'suggestion': r['suggestion'],
            'body': r['body_text'],
            'body_count': r['body_count'],
            'dcs_sugg_band': r['dcs_sugg_band'],
        })

    BATCH = triage_util.BATCH_SIZE
    n = 0
    for i in range(0, len(batch), BATCH):
        with open(os.path.join(work, 'body_batch_%03d.jsonl' % (i // BATCH)), 'w', encoding='utf-8') as f:
            for r in batch[i:i + BATCH]:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        n += 1
    print("wrote %d body_batch files (%d candidates, %d/batch) in %s"
          % (n, len(batch), BATCH, os.path.relpath(work, ROOT)))
    print("settled deterministically -> intentional(wr/variant/xref)=%d  unlocatable(missing)=%d"
          % (sum(1 for r in rows if r['body_kind'] in triage_util.INTENTIONAL_KINDS),
             sum(1 for r in rows if r['body_kind'] == 'missing')))


if __name__ == '__main__':
    main()
