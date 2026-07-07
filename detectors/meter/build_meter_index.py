"""build_meter_index.py  (Python 3) -- H251 build task: one-time GRETIL kavya meter index

Runs the three-way meter identifier (meter_ident.py) over every verse the
walker (gretil_walker.py) extracts from detectors/gretil_kavya_raw/*.txt and
writes one JSON record per verse to meter_verdicts.jsonl.

This is the expensive, corpus-scale, OFFLINE step (~0.14 s/verse, ~26k verses
-> ~1 hour) -- separate from meter_check.py (the run_all.py-facing flagger),
which only reads this file plus the live sanhw1.txt at each invocation. Rerun
this script when the corpus changes (new GRETIL texts) or a tool is upgraded;
NOT on every run_all.py invocation.

Per-verse TIMEOUT guard: a handful of long, pAda-marker-less verses (observed
06-07-2026: sa_bhallaTa-bhallaTazataka Bhall_86, a ~21-syllable-pAda meter
with no '/' hints at all) send skrutable's resplit_lite pAda-boundary search
into a combinatorial blowup and hang indefinitely. Each verse runs in a
worker thread with a wall-clock timeout; on timeout it is recorded with
verdict='review' (not silently dropped) and the run moves on. The stuck
worker thread itself cannot be killed (CPython has no safe thread-kill) and
is simply abandoned -- harmless since it's a handful of verses out of ~26k,
not a resource leak that matters at this scale.

RESUME: if out_path already exists, verses already recorded (by
source+locus) are skipped so a restart after a kill/crash does not redo the
whole corpus -- appends new records rather than starting over.

  python build_meter_index.py [corpus_dir=../gretil_kavya_raw] [out=meter_verdicts.jsonl]
"""
import sys
import os
import json
import time
import concurrent.futures as cf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gretil_walker as gw   # noqa: E402
import meter_ident as mi     # noqa: E402

PER_VERSE_TIMEOUT_S = 8


def _already_done(out_path):
    done = set()
    counts = {'clean': 0, 'review': 0, 'suspect': 0}
    if os.path.exists(out_path):
        with open(out_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue        # last line may be truncated by a kill -- drop it
                done.add((rec['source'], rec['locus']))
                counts[rec['verdict']] = counts.get(rec['verdict'], 0) + 1
    return done, counts


def main(corpus_dir, out_path):
    t0 = time.time()
    done, counts = _already_done(out_path)
    n = len(done)
    n_timeout = 0
    if done:
        sys.stderr.write("build_meter_index: resuming, %d verses already recorded\n" % len(done))
    with open(out_path, 'a', encoding='utf-8') as out, \
            cf.ThreadPoolExecutor(max_workers=1) as pool:
        for v in gw.walk_corpus(corpus_dir):
            key = ('GRETIL:%s' % v['file'], v['locus'])
            if key in done:
                continue
            fut = pool.submit(mi.identify_verse, v)
            try:
                rec = fut.result(timeout=PER_VERSE_TIMEOUT_S)
            except cf.TimeoutError:
                n_timeout += 1
                rec = {'source': key[0], 'locus': key[1], 'full_text': v['full_text'],
                        'skrutable': {}, 'chanda': [], 'vidyut': {},
                        'verdict': 'review',
                        'verdict_reason': 'processing timeout (>%ds, likely a long pAda-marker-less '
                                           'verse blowing up resplit enumeration)' % PER_VERSE_TIMEOUT_S}
                pool = cf.ThreadPoolExecutor(max_workers=1)  # abandon the stuck worker, get a fresh one
            counts[rec['verdict']] = counts.get(rec['verdict'], 0) + 1
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
            out.flush()
            n += 1
            if n % 1000 == 0:
                sys.stderr.write("  %d verses (%.0fs) clean=%d review=%d suspect=%d timeouts=%d\n"
                                  % (n, time.time() - t0, counts['clean'], counts['review'],
                                     counts['suspect'], n_timeout))
    sys.stderr.write("build_meter_index: %d verses -> %s in %.0fs (clean=%d review=%d suspect=%d, "
                      "%d timeouts, %.1f%% suspect+review)\n"
                      % (n, out_path, time.time() - t0, counts['clean'], counts['review'], counts['suspect'],
                         n_timeout, 100.0 * (counts['review'] + counts['suspect']) / n if n else 0))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    here = os.path.dirname(os.path.abspath(__file__))
    args = sys.argv[1:]
    corpus_dir = args[0] if len(args) > 0 else os.path.join(here, '..', 'gretil_kavya_raw')
    out_path = args[1] if len(args) > 1 else os.path.join(here, 'meter_verdicts.jsonl')
    main(corpus_dir, out_path)
