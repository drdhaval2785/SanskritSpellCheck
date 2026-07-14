"""Generate the H454 scan-verification review sheet (interactive HTML).

Items = the 109 fileable rows of corrections_draft/file_first_verified.tsv
(verdict PASS or SCAN-FIRST), enriched with entry bodies from
corrections_draft/irr/irr_inputs.tsv and a Cologne scan deep-link per row.
Output: <repo>/review/sanskritspellcheck-filefirst-scanverify_109rows_review.html
(review/ is gitignored -- the sheet is a personal voting artifact, regenerable).
Votes are consumed by corrections_draft/apply_scanverify_decisions.py.

Calls the shared csl_pyutil.render_review_sheet() emitter (H925/H931) instead of
hand-writing the HTML/JS shell -- this generator's own decision vocabulary
(approve/reject/defer) and export shape ({id, decision, note}) already matched
the shared contract exactly, so this was a clean, lossless port (unlike the two
other pass-2 candidates, which had real contract mismatches -- see H931).
Needs `pip install "csl-pyutil @ git+https://github.com/sanskrit-lexicon/csl-pyutil@main"`.
"""
import os
import sys

from csl_pyutil import render_review_sheet, esc

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'corrections_draft', 'file_first_verified.tsv')
IRR = os.path.join(ROOT, 'corrections_draft', 'irr', 'irr_inputs.tsv')
OUT_DIR = os.path.join(ROOT, 'review')
SHEET_NAME = 'sanskritspellcheck-filefirst-scanverify_109rows_review'
OUT = os.path.join(OUT_DIR, SHEET_NAME + '.html')
SCAN_URL = 'http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s'
ORDER = ['SHS', 'YAT', 'ACC', 'PWG', 'MCI', 'MW', 'SKD', 'WIL', 'PW', 'VCP', 'GST']

bodies = {}
with open(IRR, encoding='utf-8') as f:
    for line in f:
        p = line.rstrip('\n').split('\t')
        if p[0] in ('row_id',) or line.startswith('#'):
            continue
        bodies[(p[1], p[2])] = p[4]

rows = []
with open(TSV, encoding='utf-8') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        p = line.rstrip('\n').split('\t')
        if p[0] == 'dict':
            continue
        if p[3] in ('PASS', 'SCAN-FIRST'):
            rows.append({'dict': p[0], 'wrong': p[1], 'right': p[2],
                         'verdict': p[3], 'note': p[4] if len(p) > 4 else ''})

rows.sort(key=lambda r: (ORDER.index(r['dict']) if r['dict'] in ORDER else 99))
items = []
for r in rows:
    items.append({
        'id': '%s:%s:%s' % (r['dict'], r['wrong'], r['right']),
        'dict': r['dict'],
        'wrong': r['wrong'],
        'right': r['right'],
        'verdict': r['verdict'],
        'note': r['note'],
        'body': bodies.get((r['dict'], r['wrong']), ''),
        'scan': SCAN_URL % (r['dict'].lower(), r['wrong']),
    })

assert len(items) == 109, 'expected 109 fileable rows, got %d' % len(items)

sheet_items = []
for it in items:
    panels = []
    if it['body']:
        panels.append(('Entry body', '<div>%s</div>' % esc(it['body'])))
    if it['note']:
        panels.append(('Dataset note', esc(it['note'])))
    panels.append(('Scan', '<a href="%s" target="_blank" rel="noopener">scanned page (%s : %s)</a>'
                   % (esc(it['scan']), esc(it['dict']), esc(it['wrong']))))
    sheet_items.append({
        'id': it['id'],
        'filt': it['dict'],
        'title': '%s → %s' % (it['wrong'], it['right']),
        'badges': [it['dict'], it['verdict']],
        'question': ('<span style="color:#b00020;text-decoration:line-through">%s</span> '
                     '→ <span style="color:#0a7a2f;font-weight:bold">%s</span>'
                     % (esc(it['wrong']), esc(it['right']))),
        'panels': panels,
        'note_placeholder': 'note (optional)',
    })

config = {
    'sheet_id': SHEET_NAME.replace('_review', ''),
    'title': 'SanskritSpellCheck — FILE-FIRST scan verification (109 rows) — H454 batch 1',
    'subtitle': ('approve = the scanned page confirms the correction (row flips n→y, enters the batch) · '
                 'reject = the scan shows the digitization is faithful (stays n, feeds do-not-file) · '
                 'defer = unclear / scan unreadable.'),
    'footer': 'SanskritSpellCheck FILE-FIRST scan verification · 109 rows · H454 batch 1 · 10-07-2026.',
    'approve_label': 'Approve', 'reject_label': 'Reject',
    'filters': [(d, d) for d in ORDER if any(it['dict'] == d for it in items)],
    'generated': '2026-07-10',
}
page = render_review_sheet(sheet_items, config, extras=True)
os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(page)
print('%d items -> %s (%.0f KB)' % (len(items), OUT, os.path.getsize(OUT) / 1024))
