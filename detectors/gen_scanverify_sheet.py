"""Generate the H454 scan-verification review sheet (interactive HTML).

Items = EVERY fileable row of corrections_draft/file_first_verified.tsv (verdict PASS or
SCAN-FIRST), enriched with entry bodies from corrections_draft/irr/irr_inputs.tsv and a
Cologne scan deep-link per row.
Output: <repo>/review/sanskritspellcheck-filefirst-scanverify_review.html
(review/ is gitignored -- the sheet is a personal voting artifact, regenerable).
Votes are consumed by corrections_draft/apply_scanverify_decisions.py.

The row count is DERIVED from the TSV, and both the filename and the headings are
count-free/interpolated. Until 04-08-2026 this script asserted `len(items) == 109` and
carried "109rows" in its own output filename -- the run-1 population. That made the sheet
un-regenerable the moment the fileable population legitimately grew: the union-across-runs
passes (D7/H1471, D9/H1709) added 73 PASS/SCAN-FIRST rows and the generator simply crashed,
so the human gate silently kept covering only the original 109 (~58%). A hardcoded expected
count turns "there is more to review" into "the tool is broken".
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, 'corrections_draft', 'file_first_verified.tsv')
IRR = os.path.join(ROOT, 'corrections_draft', 'irr', 'irr_inputs.tsv')
OUT_DIR = os.path.join(ROOT, 'review')
# Count-free by design: the old name embedded "109rows", so a sheet regenerated after the
# fileable population grew would either lie in its own filename or silently orphan the
# previous decisions file under a different name.
SHEET_NAME = 'sanskritspellcheck-filefirst-scanverify_review'
OUT = os.path.join(OUT_DIR, SHEET_NAME + '.html')
SCAN_URL = 'http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s'
GENERATED = datetime.date.today().strftime('%d-%m-%Y')
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

# Entry bodies: irr_inputs.tsv first, then the dictionary source itself.
# irr_inputs.tsv was built for the run-1 IRR study, so it covers ONLY those rows -- every row
# added later (the 73 union-pass rows) had no body and rendered as a bare correction with no
# entry text to judge it against, which is unvotable. The fallback reads the entry through
# triage_util.build_entry_index, the same resolver the triage and make_changefiles use, so a
# dict staged in external_src/ works identically. Indices are built lazily, one per dict.
_idx_cache = {}


def body_for(dictcode, hw):
    """The entry body for a headword: IRR inputs if present, else read from the source."""
    cached = bodies.get((dictcode, hw))
    if cached:
        return cached
    if dictcode not in _idx_cache:
        _idx_cache[dictcode] = triage_util.build_entry_index(triage_util.csl_root(), dictcode)
    idx = _idx_cache[dictcode]
    if idx is None:
        return ''
    got = idx.bodies(hw)
    return ' ⟪//⟫ '.join(b for b in got if b) if got else ''

items = []
for r in rows:
    items.append({
        'id': '%s:%s:%s' % (r['dict'], r['wrong'], r['right']),
        'dict': r['dict'],
        'wrong': r['wrong'],
        'right': r['right'],
        'verdict': r['verdict'],
        'note': r['note'],
        'body': body_for(r['dict'], r['wrong']),
        'scan': SCAN_URL % (r['dict'].lower(), r['wrong']),
    })

# The row count is DERIVED, never asserted against a literal. It was pinned at 109 (the
# run-1 population) which meant that every time the fileable population legitimately grew,
# regenerating the sheet CRASHED instead of covering the new rows -- so the gate silently
# stayed at its old coverage. The union-across-runs passes (D7/H1471, D9/H1709) added 73
# PASS/SCAN-FIRST rows and hit exactly that. Guard against an EMPTY sheet instead, which is
# the failure that actually matters.
if not items:
    sys.exit('no PASS/SCAN-FIRST rows found in %s -- refusing to write an empty sheet' % TSV)
print('sheet covers %d fileable row(s): %s'
      % (len(items), ' · '.join('%s %d' % (v, sum(1 for i in items if i['verdict'] == v))
                                for v in ('PASS', 'SCAN-FIRST'))))

payload = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')

page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>SanskritSpellCheck — FILE-FIRST scan verification (%COUNT% rows) — H454 batch 1</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f5f4f0;color:#222}
header{position:sticky;top:0;background:#2b3a4a;color:#fff;padding:10px 16px;z-index:5}
header h1{font-size:16px;margin:0 0 4px 0}
#tally{font-size:13px}
#tally b{margin-right:10px}
.hint{font-size:12px;opacity:.8}
main{max-width:980px;margin:0 auto;padding:12px}
.item{background:#fff;border:1px solid #ddd;border-radius:6px;margin:10px 0;padding:10px 14px}
.item.cur{outline:3px solid #4a90d9}
.item h3{margin:0 0 6px 0;font-size:15px}
.pair{font-family:Consolas,monospace;font-size:15px}
.pair .w{color:#b00020;text-decoration:line-through}
.pair .r{color:#0a7a2f;font-weight:bold}
.verdict{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;margin-left:8px;vertical-align:middle}
.verdict.PASS{background:#e2f2e5;color:#0a7a2f}
.verdict.SCAN-FIRST{background:#fdeeda;color:#a05a00}
.body{font-size:13px;background:#fafaf5;border-left:3px solid #cbc9bd;padding:6px 9px;margin:7px 0;max-height:110px;overflow:auto}
.note{font-size:12px;color:#555;margin:5px 0}
.links a{font-size:13px;margin-right:14px}
.btns{margin-top:8px}
.btns button{font-size:13px;padding:5px 13px;margin-right:7px;border-radius:5px;border:1px solid #bbb;background:#fff;cursor:pointer}
.item.approve{border-color:#0a7a2f;background:#f3faf4}
.item.reject{border-color:#b00020;background:#fdf4f5}
.item.defer{border-color:#a05a00;background:#fdf9f2}
.item.approve .b-a,.item.reject .b-r,.item.defer .b-d{outline:2px solid #333;font-weight:bold}
.item input.usernote{width:96%;font-size:12px;margin-top:6px;padding:3px 6px}
#dl{background:#0a7a2f;color:#fff;border:none;padding:6px 14px;border-radius:5px;cursor:pointer;margin-left:16px}
.dicthead{margin:18px 0 4px 0;font-size:14px;color:#2b3a4a;border-bottom:2px solid #2b3a4a}
</style></head><body>
<header>
<h1>SanskritSpellCheck — FILE-FIRST scan verification · %COUNT% rows · H454 batch 1 · %DATE%</h1>
<div id="tally"></div>
<div class="hint">✅ approve = the scanned page confirms the correction (row flips n→y, enters the batch) ·
❌ reject = the scan shows the digitization is faithful (stays n, feeds do-not-file) ·
⏸ defer = unclear / scan unreadable. Keys: a / r / d, ↑↓ or j/k to move. Votes persist locally.
<button id="dl">Download %NAME%_decisions.json</button></div>
</header>
<main id="list"></main>
<script>
const SHEET_ID = "%NAME%";
const ITEMS = %PAYLOAD%;
const store = () => JSON.parse(localStorage.getItem(SHEET_ID) || "{}");
const save = s => localStorage.setItem(SHEET_ID, JSON.stringify(s));
let cur = 0;
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function render(){
  const s = store(); const list = document.getElementById('list'); list.innerHTML='';
  let lastDict = null;
  ITEMS.forEach((it,i)=>{
    if(it.dict!==lastDict){const h=document.createElement('div');h.className='dicthead';
      h.textContent=it.dict+' — '+ITEMS.filter(x=>x.dict===it.dict).length+' rows';list.appendChild(h);lastDict=it.dict;}
    const v = s[it.id] || {};
    const div = document.createElement('div');
    div.className = 'item' + (v.decision? ' '+v.decision : '') + (i===cur? ' cur':'');
    div.id = 'it'+i;
    div.innerHTML = '<h3>'+(i+1)+'. <span class="pair"><span class="w">'+esc(it.wrong)+
      '</span> → <span class="r">'+esc(it.right)+'</span></span>'+
      '<span class="verdict '+it.verdict+'">'+it.verdict+'</span></h3>'+
      (it.body? '<div class="body">'+esc(it.body)+'</div>':'')+
      '<div class="note">'+esc(it.note)+'</div>'+
      '<div class="links"><a href="'+it.scan+'" target="_blank">scanned page ('+esc(it.dict)+' : '+esc(it.wrong)+')</a></div>'+
      '<div class="btns"><button class="b-a">✅ approve (y)</button>'+
      '<button class="b-r">❌ reject</button><button class="b-d">⏸ defer</button></div>'+
      '<input class="usernote" placeholder="note (optional)" value="'+esc(v.note||'')+'">';
    div.querySelector('.b-a').onclick = ()=>vote(i,'approve');
    div.querySelector('.b-r').onclick = ()=>vote(i,'reject');
    div.querySelector('.b-d').onclick = ()=>vote(i,'defer');
    div.querySelector('.usernote').onchange = e=>{const st=store();st[it.id]=st[it.id]||{};st[it.id].note=e.target.value;save(st);};
    div.onclick = ()=>{cur=i;mark();};
    list.appendChild(div);
  });
  tally();
}
function mark(){document.querySelectorAll('.item').forEach((d,i)=>d.classList.toggle('cur',i===cur));}
function vote(i,d){const st=store();const it=ITEMS[i];st[it.id]=st[it.id]||{};
  st[it.id].decision = (st[it.id].decision===d? null : d); save(st);
  cur = Math.min(i+1, ITEMS.length-1); render();
  const el=document.getElementById('it'+cur); if(el) el.scrollIntoView({block:'center'});}
function tally(){const s=store();let a=0,r=0,d=0;
  ITEMS.forEach(it=>{const v=(s[it.id]||{}).decision; if(v==='approve')a++;else if(v==='reject')r++;else if(v==='defer')d++;});
  document.getElementById('tally').innerHTML='<b>✅ '+a+'</b><b>❌ '+r+'</b><b>⏸ '+d+
    '</b><b>⬜ '+(ITEMS.length-a-r-d)+' unvoted</b> of '+ITEMS.length;}
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  if(e.key==='a')vote(cur,'approve'); else if(e.key==='r')vote(cur,'reject');
  else if(e.key==='d')vote(cur,'defer');
  else if(e.key==='ArrowDown'||e.key==='j'){cur=Math.min(cur+1,ITEMS.length-1);mark();document.getElementById('it'+cur).scrollIntoView({block:'center'});e.preventDefault();}
  else if(e.key==='ArrowUp'||e.key==='k'){cur=Math.max(cur-1,0);mark();document.getElementById('it'+cur).scrollIntoView({block:'center'});e.preventDefault();}
});
document.getElementById('dl').onclick=()=>{
  const s=store();
  const out={sheet_id:SHEET_ID,generated:"2026-07-10",decided:new Date().toISOString(),
    items:ITEMS.map(it=>({id:it.id,decision:(s[it.id]||{}).decision||null,note:(s[it.id]||{}).note||""}))};
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));
  a.download=SHEET_ID.replace('_review','')+'_decisions.json';
  a.click();};
render();
</script></body></html>
"""
page = (page.replace('%PAYLOAD%', payload)
            .replace('%NAME%', SHEET_NAME.replace('_review', ''))
            .replace('%COUNT%', str(len(items)))
            .replace('%DATE%', GENERATED))
os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(page)
print('%d items -> %s (%.0f KB)' % (len(items), OUT, os.path.getsize(OUT) / 1024))
