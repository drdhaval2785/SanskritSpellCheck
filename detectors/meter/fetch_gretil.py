"""fetch_gretil.py  (Python 3) -- H289 Phase-2: fetch + sample a GRETIL section text

Downloads a GRETIL "corpustei/transformations/plaintext" file by its basename and
writes it (optionally SAMPLED to a bounded verse count) into a raw corpus dir the
existing walker/build_meter_index pipeline consumes unchanged. Large sections
(Epics/Purāṇa are 10k-100k+ verses) must be SAMPLED, not fetched-and-built whole
(handoff H289 guard); --cap keeps the first N blank-line-separated verse blocks
(a representative contiguous opening slice) plus the header, preserving the
'# Text' marker gretil_walker.iter_blocks keys on.

Raw output is gitignored (CC BY-NC-SA third-party verse text; detectors/gretil_*_raw/).

  python fetch_gretil.py <out_raw_dir> <plaintext_basename> [--cap=N]

e.g.
  python fetch_gretil.py ../gretil_purana_raw sa_mArkaNDeyapurANa1-93.txt --cap=1500
"""
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE = "https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/plaintext/"


def sample_text(raw, cap):
    """Keep the header up to and including the '# Text' line, then the first `cap`
    blank-line-separated blocks. cap<=0 means no cap (whole file)."""
    if cap is None or cap <= 0:
        return raw
    lines = raw.splitlines(keepends=True)
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == '# Text')
    except StopIteration:
        return raw          # no marker -> can't sample structurally; keep whole
    head = lines[:start + 1]
    body = lines[start + 1:]
    kept = []
    blocks = 0
    in_block = False
    for l in body:
        if l.strip():
            in_block = True
            kept.append(l)
        else:
            if in_block:
                blocks += 1
                in_block = False
            kept.append(l)
            if blocks >= cap:
                break
    return ''.join(head) + ''.join(kept)


def main(out_dir, basename, cap):
    os.makedirs(out_dir, exist_ok=True)
    url = BASE + basename
    sys.stderr.write("fetching %s ...\n" % url)
    raw = urllib.request.urlopen(url, timeout=60).read().decode('utf-8', 'replace')  # noqa: S310
    sampled = sample_text(raw, cap)
    out_path = os.path.join(out_dir, basename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(sampled)
    note = ("sampled to first %d blocks" % cap) if cap and cap > 0 else "whole file"
    sys.stderr.write("wrote %s  (%d -> %d chars, %s)\n"
                     % (out_path, len(raw), len(sampled), note))


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        sys.exit(__doc__)
    cap = next((int(a.split('=', 1)[1]) for a in sys.argv[1:] if a.startswith('--cap=')), None)
    main(args[0], args[1], cap)
