"""monthly_loop.py  (Python 3)  -- H1533: monthly hybrid detection-loop driver

Runs the full detector suite (run_all.py) against sanhw1.txt, then diffs the
resulting tier-A candidates against the last committed baseline
(monthly_loop/tier_a_baseline.txt) to compute what's NEW since the previous
cycle. The suppression layer itself (nochange.txt + do_not_file_suppress.txt)
is already applied inside run_all.aggregate() -- this script only adds the
across-runs delta on top of that per-run filtering.

Writes a dated report (monthly_loop/reports/<date>.md) and rewrites the
baseline to the current tier-A set. Meant to be invoked by
.github/workflows/monthly-detection-loop.yml on a monthly cron (or
workflow_dispatch for manual verification) -- that workflow uploads the
report/combined_candidates.txt as run artifacts and opens a PR with the
updated baseline+report when this run reports a delta. Safe to run locally:

  python monthly_loop.py [--rerun] [sanhw1=../sanhw1.txt] [date=YYYY-MM]
"""
import sys
import os
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import run_all

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))
LOOP_DIR = os.path.join(HERE, 'monthly_loop')
BASELINE_PATH = os.path.join(LOOP_DIR, 'tier_a_baseline.txt')
REPORTS_DIR = os.path.join(LOOP_DIR, 'reports')
CANDIDATES_PATH = os.path.join(HERE, 'combined_candidates.txt')
REPORT_TABLE_CAP = 200  # keep the report skimmable; full set always lives in the baseline file


def load_tier_a(path):
    """suspect -> full row, tier-A rows only. Shared by combined_candidates.txt
    (run_all's native output) and tier_a_baseline.txt (a verbatim copy of the
    prior run's tier-A rows) -- both use the identical "A\\t<score>\\t<suspect>
    -> <suggestion>\\t..." format, so one parser covers both."""
    rows = {}
    if not os.path.exists(path):
        return rows
    for line in u._read_words(path):
        if not line or not line.startswith('A\t'):
            continue
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        suspect = parts[2].split(' -> ', 1)[0]
        rows.setdefault(suspect, line)
    return rows


def write_baseline(path, tier_a):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for suspect in sorted(tier_a):
            f.write(tier_a[suspect] + '\n')


def _row_line(row):
    # "A\t465\tnarA -> nara\t[dets]\t[dicts]..." -> "narA -> nara  {dets}"
    parts = row.split('\t')
    arrow = parts[2] if len(parts) > 2 else ''
    dets = parts[3] if len(parts) > 3 else ''
    return "`%s`  %s" % (arrow, dets)


def write_report(path, date_str, tier_a, new, resolved):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Monthly detection loop -- %s\n\n" % date_str)
        f.write("Tier-A candidates this run: **%d**  ·  new: **%d**  ·  resolved: **%d**\n\n"
                % (len(tier_a), len(new), len(resolved)))
        if new:
            shown = sorted(new)[:REPORT_TABLE_CAP]
            f.write("## New tier-A candidates (%d)\n\n" % len(new))
            for suspect in shown:
                f.write("- %s\n" % _row_line(tier_a[suspect]))
            if len(new) > len(shown):
                f.write("\n_...and %d more; full set in `monthly_loop/tier_a_baseline.txt`._\n"
                        % (len(new) - len(shown)))
        else:
            f.write("No new tier-A candidates since the last run.\n")
        f.write("\n")
        if resolved:
            f.write("## Resolved / dropped out of tier A (%d)\n\n" % len(resolved))
            f.write("Suppressed, corrected upstream, or no longer flagged at tier A.\n\n")
            for suspect in sorted(resolved):
                f.write("- `%s`\n" % suspect)
            f.write("\n")


def _write_github_output(changed, new_count, resolved_count, report_path):
    gha_out = os.environ.get('GITHUB_OUTPUT')
    if not gha_out:
        return
    with open(gha_out, 'a', encoding='utf-8') as f:
        f.write('changed=%s\n' % ('true' if changed else 'false'))
        f.write('new_count=%d\n' % new_count)
        f.write('resolved_count=%d\n' % resolved_count)
        f.write('report_path=%s\n' % os.path.relpath(report_path, os.path.join(HERE, '..')).replace(os.sep, '/'))


def main(sanhw1, rerun, date_str):
    run_all.main(sanhw1, rerun)
    tier_a = load_tier_a(CANDIDATES_PATH)
    baseline = load_tier_a(BASELINE_PATH)
    new = set(tier_a) - set(baseline)
    resolved = set(baseline) - set(tier_a)

    report_path = os.path.join(REPORTS_DIR, '%s.md' % date_str)
    write_report(report_path, date_str, tier_a, new, resolved)
    write_baseline(BASELINE_PATH, tier_a)

    changed = bool(new or resolved)
    print("monthly_loop: tier-A total=%d new=%d resolved=%d -> %s"
          % (len(tier_a), len(new), len(resolved), report_path))
    _write_github_output(changed, len(new), len(resolved), report_path)


if __name__ == "__main__":
    rerun = '--rerun' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sanhw1 = args[0] if args else os.path.join(HERE, '..', 'sanhw1.txt')
    date_str = args[1] if len(args) > 1 else datetime.date.today().strftime('%Y-%m')
    main(sanhw1, rerun, date_str)
