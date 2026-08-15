"""h454_gate_census.py — count :y / :n flags across FILE-FIRST queues.

H454 stop condition needs at least one :y before make_changefiles can emit
batch-1 drafts. Re-run anytime to reconfirm the human scan-verify gate.

  python corrections_draft/h454_gate_census.py
"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['SHS', 'YAT', 'ACC', 'PWG', 'MCI', 'MW', 'SKD', 'WIL', 'PW', 'VCP', 'GST']


def main():
    paths = sorted(glob.glob(os.path.join(HERE, '*', '*_file_first_sf.txt')))
    total_y = total_n = total_other = 0
    rows = []
    for path in paths:
        y = n = other = 0
        with open(path, encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith((';', '#')):
                    continue
                parts = s.split(':')
                if len(parts) >= 4:
                    flag = parts[-1].strip().lower()
                    if flag == 'y':
                        y += 1
                    elif flag == 'n':
                        n += 1
                    else:
                        other += 1
                else:
                    other += 1
        d = os.path.basename(os.path.dirname(path))
        if y or n or other:
            rows.append((d, y, n, other, path))
        total_y += y
        total_n += n
        total_other += other

    def sort_key(r):
        d = r[0]
        return (ORDER.index(d) if d in ORDER else 99, d)

    print('dict   y    n  other')
    for d, y, n, other, _path in sorted(rows, key=sort_key):
        print('%-6s %3d %4d %5d' % (d, y, n, other))
    print('TOTAL  y=%d n=%d other=%d' % (total_y, total_n, total_other))
    if total_y == 0:
        print('GATE: CLOSED — zero :y rows; vote the scanverify sheet before '
              'make_changefiles / cologne-correction-queue.')
        return 2
    print('GATE: OPEN — %d :y row(s) ready for make_changefiles.' % total_y)
    return 0


if __name__ == '__main__':
    sys.exit(main())
