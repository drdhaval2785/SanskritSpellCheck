#!/usr/bin/env python3
"""dump_refuted_typos.py -- emit the candidates a run classified TYPO and the source-confirm
gate then REFUTED, with the reason.

On a zero-fileable dictionary the union table is empty and carries no information. The
informative residue is this: which candidates looked like typos from the entry body alone, and
what the full entry said that killed them. That is do-not-file evidence -- per HYPOTHESES H3 the
durable deliverable of a mature dictionary's triage is the do-not-file list, not the typos.

    cd corrections_draft
    python dump_refuted_typos.py BHS SCH --out REFUTED_TYPO_CANDIDATES_PROBE22.tsv
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'detectors'))

import triage_util  # noqa: E402

triage_util.reconfigure_stdio()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dicts', nargs='+')
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    rows = []
    for d in args.dicts:
        work = triage_util.work_dir(d)
        cls = triage_util.load_verdicts(work, 'body_adj_*.json')
        conf = triage_util.load_verdicts(work, 'body_conf_*.json')
        refuted = [(s, v) for s, v in conf.items() if not v.get('is_typo')]
        confirmed = sum(1 for v in conf.values() if v.get('is_typo'))
        print('%-5s classify TYPO reaching confirm: %3d · refuted: %3d · confirmed: %d'
              % (d, len(conf), len(refuted), confirmed))
        for s, v in sorted(refuted):
            c = cls.get(s, {})
            rows.append([d, s, c.get('suggestion', ''), c.get('confidence', ''),
                         c.get('reason', ''), v.get('reason', '')])

    print('total refuted: %d' % len(rows))
    if not args.out:
        return
    out = args.out if os.path.isabs(args.out) else os.path.join(HERE, args.out)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('dict\tsuspect\tproposed\tcls_confidence\tclassify_reason\t'
                'opus_refutation_reason\n')
        for r in rows:
            f.write('\t'.join((c or '').replace('\t', ' ').replace('\n', ' ') for c in r) + '\n')
    print('wrote %s (%d rows)' % (out, len(rows)))


if __name__ == '__main__':
    main()
