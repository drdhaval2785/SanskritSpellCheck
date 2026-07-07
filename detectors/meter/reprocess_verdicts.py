"""reprocess_verdicts.py  (Python 3) -- recompute verdicts from a built index

`meter_verdicts.jsonl` stores each verse's raw `skrutable` / `chanda` / `vidyut`
tool outputs alongside the computed `verdict`. When only the VERDICT-COMPUTATION
logic changes (meter_ident.verdict()) -- as in the H277 recalibration -- the
verdicts can be recomputed from those stored raw outputs in seconds, WITHOUT
re-invoking skrutable/chanda/vidyut over the ~26k-verse corpus (~1 hour). Only a
change to the per-verse IDENTIFICATION logic (identify_skrutable/chanda/vidyut)
needs a full build_meter_index.py rerun.

Timeout records (verdict='review', empty `skrutable` + the 'processing timeout'
reason -- see build_meter_index.py) carry no raw tool output to recompute from and
are preserved verbatim.

  python reprocess_verdicts.py                # dry-run: print the old->new confusion matrix
  python reprocess_verdicts.py --apply        # rewrite meter_verdicts.jsonl in place
"""
import sys
import os
import json
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meter_ident as mi   # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def _is_timeout(rec):
    return not rec.get('skrutable') and 'timeout' in (rec.get('verdict_reason') or '')


def reprocess(path, apply):
    matrix = collections.Counter()          # (old, new) -> n
    samples = collections.defaultdict(list)  # (old, new) -> [(source, locus, meter)]
    out_lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            old = rec['verdict']
            if _is_timeout(rec):
                new, reason = old, rec.get('verdict_reason')
            else:
                new, reason = mi.verdict(rec.get('skrutable') or {},
                                         rec.get('chanda') or [],
                                         rec.get('vidyut') or {})
            matrix[(old, new)] += 1
            if old != new and len(samples[(old, new)]) < 4:
                samples[(old, new)].append(
                    (rec['source'], rec['locus'], (rec.get('skrutable') or {}).get('meter')))
            if apply:
                rec['verdict'] = new
                rec['verdict_reason'] = reason
                out_lines.append(json.dumps(rec, ensure_ascii=False))

    print("=== old -> new verdict confusion matrix ===")
    tot_new = collections.Counter()
    tot_old = collections.Counter()
    for (old, new), n in sorted(matrix.items()):
        tot_old[old] += n
        tot_new[new] += n
        flag = '' if old == new else '   <-- CHANGED'
        print("  %-8s -> %-8s  %6d%s" % (old, new, n, flag))
    total = sum(matrix.values())
    print("\n  totals OLD:", dict(tot_old))
    print("  totals NEW:", dict(tot_new))
    nonclean_new = total - tot_new['clean']
    print("  non-clean rate: OLD %.1f%%  ->  NEW %.1f%%"
          % (100.0 * (total - tot_old['clean']) / total, 100.0 * nonclean_new / total))
    print("\n=== samples of changed verdicts ===")
    for (old, new), rows in sorted(samples.items()):
        print("  [%s -> %s]" % (old, new))
        for src, loc, meter in rows:
            print("      %s %s   meter=%r" % (src, loc, meter))

    if apply:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(out_lines) + '\n')
        print("\n-> rewrote %d records to %s" % (len(out_lines), path))
    else:
        print("\n(dry-run; pass --apply to rewrite %s)" % path)


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    path = next((a for a in sys.argv[1:] if not a.startswith('--')),
                os.path.join(HERE, 'meter_verdicts.jsonl'))
    reprocess(path, apply)
