"""run_all.py  (Python 3)  -- Phase 1.1-1.3: unified runner + confidence tiers + review report

Runs every detector, parses their stable output formats, DEDUPLICATES across detectors
by suspect headword, assigns a confidence score + A/B/C tier (cross-detector agreement
is the main signal), and emits:

  combined_candidates.txt  -- the full ranked list (tier, score, suspect -> suggestion, evidence)
  combined_review.html     -- an accept/reject review UI with per-dictionary scan links
  combined_sf.txt          -- CORRECTIONS standard format (DICT:wrong:right:n) for the best suggestion

Detectors are consumed via their OUTPUT FILES (the X:CODE=Y:D and DICT:wrong:right:n
contracts), not their internals -- so this stays decoupled. Cached outputs are reused;
pass --rerun to regenerate them.

  python run_all.py [--rerun] [sanhw1=../sanhw1.txt]
"""
import sys
import os
import html
import json
import subprocess
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))

# (name, script, output file, kind). order_check needs source-order input -> excluded.
DETECTORS = [
    ('spell_correct',  'spell_correct.py',     'spell_correct_corrections.txt',  'corrector'),
    ('consensus',      'consensus.py',         'consensus_corrections.txt',      'corrector'),
    ('intra_dup',      'intra_dup.py',         'intra_dup_corrections.txt',      'corrector'),
    ('dict_vs_corpus', 'dict_vs_corpus.py',    'dict_vs_corpus_corrections.txt', 'corrector'),
    ('phonotactic',    'phonotactic_check.py', 'phonotactic_suspects.txt',       'flagger'),
    ('charset',        'charset_check.py',     'charset_suspects.txt',           'flagger'),
]
HIGH_PRECISION = {'phonotactic', 'charset'}
SCAN = "http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s"


class Cand:
    __slots__ = ('suspect', 'detectors', 'sugg_dets', 'sugg_dicts', 'reasons', 'dicts')

    def __init__(self, suspect):
        self.suspect = suspect
        self.detectors = set()
        self.sugg_dets = collections.defaultdict(set)   # suggestion -> {detectors}
        self.sugg_dicts = collections.defaultdict(set)  # suggestion -> {dicts that a corrector tied to it}
        self.reasons = []                               # (detector, code, detail)
        self.dicts = set()


def ensure_outputs(sanhw1, rerun):
    for name, script, out, kind in DETECTORS:
        path = os.path.join(HERE, out)
        if rerun or not os.path.exists(path) or os.path.getsize(path) == 0:
            print("running %s ..." % name)
            r = subprocess.run([sys.executable, os.path.join(HERE, script), sanhw1, path],
                               cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if r.returncode != 0:
                sys.stderr.write("ERROR: %s failed (exit %d):\n%s\n" % (name, r.returncode, (r.stderr or '')[-1500:]))
                raise SystemExit(1)
        else:
            print("using cached %s" % out)


def aggregate():
    cands = {}

    def get(hw):
        if hw not in cands:
            cands[hw] = Cand(hw)
        return cands[hw]

    for name, script, out, kind in DETECTORS:
        path = os.path.join(HERE, out)
        if not os.path.exists(path):
            continue
        for line in u._read_words(path):
            if not line:
                continue
            if kind == 'corrector':            # DICT:wrong:right:n
                parts = line.split(':')
                if len(parts) < 3:
                    continue
                code, wrong, right = parts[0], parts[1], parts[2]
                c = get(wrong)
                c.detectors.add(name)
                c.sugg_dets[right].add(name)
                c.sugg_dicts[right].add(code)
                c.dicts.add(code)
            else:                              # X:CODE=Y:D
                if ':' not in line:            # guard: skip malformed/colon-less lines
                    continue
                x = line[:line.index(':')]
                d = line[line.rindex(':') + 1:]
                mid = line[line.index(':') + 1:line.rindex(':')]
                rcode, _, detail = mid.partition('=')
                c = get(x)
                c.detectors.add(name)
                c.reasons.append((name, rcode, detail))
                c.dicts.update(t for t in d.split(',') if t)
    return cands


def score_tier(c, dcs):
    ndet = len(c.detectors)
    # best suggestion = most detector support, then highest DCS band
    best, best_band, best_supp = '', 0, -1
    for sugg, dets in c.sugg_dets.items():
        band = dcs.get(u.normalize_lemma(sugg), 0)
        if (len(dets), band) > (best_supp, best_band):
            best, best_band, best_supp = sugg, band, len(dets)
    hpf = bool(c.detectors & HIGH_PRECISION)
    score = ndet * 100 + best_band * 10 + (50 if hpf else 0) + len(c.dicts)
    if c.detectors == {'dict_vs_corpus'}:
        tier = 'C'                              # exploratory alone
    elif ndet >= 2 or hpf or best_band == 5:
        tier = 'A'
    elif best_band >= 3 or (c.detectors & {'consensus', 'intra_dup'}):
        tier = 'B'
    else:
        tier = 'C'
    return score, tier, best, best_band


def main(sanhw1, rerun):
    ensure_outputs(sanhw1, rerun)
    dcs = u.load_dcs_lemmas(u.dcs_path())
    cands = aggregate()

    rows = []
    for c in cands.values():
        score, tier, best, band = score_tier(c, dcs)
        rows.append((score, tier, band, best, c))
    rows.sort(key=lambda r: (-r[0], r[4].suspect))

    tiers = collections.Counter(r[1] for r in rows)
    multi = sum(1 for r in rows if len(r[4].detectors) >= 2)
    print("unified candidates: %d (deduped across %d detectors); multi-detector: %d"
          % (len(rows), len(DETECTORS), multi))
    print("tiers: A=%d  B=%d  C=%d" % (tiers['A'], tiers['B'], tiers['C']))

    # combined_candidates.txt -- full ranked list
    with open(os.path.join(HERE, 'combined_candidates.txt'), 'w', encoding='utf-8') as f:
        for score, tier, band, best, c in rows:
            dets = ",".join(sorted(c.detectors))
            f.write("%s\t%d\t%s -> %s\t[%s]\t[%s]\n"
                    % (tier, score, c.suspect, best or "(flag)", dets, ",".join(sorted(c.dicts))))

    # combined_sf.txt -- standard format; emit only the dicts a corrector tied to
    # the chosen suggestion (not flagger-contributed dicts with no correction evidence)
    with open(os.path.join(HERE, 'combined_sf.txt'), 'w', encoding='utf-8') as f:
        for score, tier, band, best, c in rows:
            if not best:
                continue
            for code in sorted(c.sugg_dicts.get(best, ())):
                f.write("%s:%s:%s:n\n" % (code, c.suspect, best))

    write_review_html(rows, os.path.join(HERE, 'combined_review.html'))
    print("-> combined_candidates.txt, combined_sf.txt, combined_review.html")
    print("--- top 15 ---")
    for score, tier, band, best, c in rows[:15]:
        print("  [%s] %-18s -> %-18s  {%s}" % (tier, c.suspect, best or "(flag)", ",".join(sorted(c.detectors))))


REVIEW_TEMPLATE = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>SanskritSpellCheck review</title>
<style>
 body{font-family:sans-serif;margin:1em}
 table{border-collapse:collapse;width:100%} th,td{border:1px solid #ccc;padding:4px 6px;font-size:14px}
 .A{background:#e7f5e7}.B{background:#fff7e0}.C{background:#fbeaea}
 .acc{background:#bdf5bd!important}.rej{background:#f5bdbd!important}
 button{margin:0 2px} .badge{background:#eee;border-radius:3px;padding:1px 4px;font-size:11px;margin-right:2px}
 #bar{position:sticky;top:0;background:#fff;padding:6px 0;border-bottom:1px solid #999}
</style></head><body>
<h2>SanskritSpellCheck &mdash; review queue</h2>
<div id="bar">
 Filter: <button onclick="filt('')">all</button>
 <button onclick="filt('A')">A</button><button onclick="filt('B')">B</button><button onclick="filt('C')">C</button>
 &nbsp;|&nbsp; <span id="counts"></span>
 &nbsp;|&nbsp; <button onclick="exp('y')">Export accepted (.txt)</button>
 <button onclick="exp('n')">Export rejected (.txt)</button>
 <span style="color:#666"> keys: a=accept r=reject s=skip</span>
</div>
@@CAPNOTE@@
<table id="t"><thead><tr><th>#</th><th>tier</th><th>suspect</th><th>&rarr; suggestion</th>
<th>detectors</th><th>evidence</th><th>scans</th><th>decision</th></tr></thead><tbody></tbody></table>
<script>
const DATA=JSON.parse(document.getElementById('payload').textContent);
const dec={}; let cur=0;
const BASE="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php";
function scanlinks(w,dicts){return dicts.map(d=>'<a target=_blank href="'+BASE+'?dict='+encodeURIComponent(d)+'&key='+encodeURIComponent(w)+'">'+d+'</a>').join(' ')}
function render(){const tb=document.querySelector('#t tbody');tb.innerHTML='';
 DATA.forEach((r,i)=>{const tr=document.createElement('tr');tr.className=r.tier+(dec[i]==='y'?' acc':dec[i]==='n'?' rej':'');tr.id='r'+i;
  tr.innerHTML='<td>'+(i+1)+'</td><td>'+r.tier+'</td><td><b>'+r.w+'</b></td><td>'+(r.s||'<i>(flag)</i>')+'</td>'+
   '<td>'+r.dets.map(d=>'<span class=badge>'+d+'</span>').join('')+'</td><td>'+(r.reason||'')+'</td>'+
   '<td>'+scanlinks(r.w,r.dicts)+'</td>'+
   '<td><button onclick="set('+i+",'y')\">&#10003;</button><button onclick=\"set("+i+",'n')\">&#10007;</button></td>';
  tb.appendChild(tr);});counts();}
function set(i,v){dec[i]=(dec[i]===v?undefined:v);const tr=document.getElementById('r'+i);
 tr.className=DATA[i].tier+(dec[i]==='y'?' acc':dec[i]==='n'?' rej':'');counts();
 localStorage.setItem('sscdec',JSON.stringify(dec));}
function counts(){const a=Object.values(dec).filter(x=>x==='y').length,r=Object.values(dec).filter(x=>x==='n').length;
 document.getElementById('counts').textContent='accepted '+a+' · rejected '+r+' · total '+DATA.length;}
function filt(t){document.querySelectorAll('#t tbody tr').forEach((tr,i)=>{tr.style.display=(!t||DATA[i].tier===t)?'':'none'});}
function exp(v){const out=[];DATA.forEach((r,i)=>{if(dec[i]===v&&r.s){r.dicts.forEach(d=>out.push(d+':'+r.w+':'+r.s+':'+v))}});
 const b=new Blob([out.join('\n')+'\n'],{type:'text/plain'});const a=document.createElement('a');
 a.href=URL.createObjectURL(b);a.download=(v==='y'?'accepted':'rejected')+'_sf.txt';a.click();}
document.addEventListener('keydown',e=>{if(e.key==='a')set(cur,'y');else if(e.key==='r')set(cur,'n');
 else if(e.key==='s'){}else return; cur=Math.min(cur+1,DATA.length-1);
 document.getElementById('r'+cur).scrollIntoView({block:'center'});});
try{Object.assign(dec,JSON.parse(localStorage.getItem('sscdec')||'{}'))}catch(e){}
render();
</script>
<script type="application/json" id="payload">@@PAYLOAD@@</script>
</body></html>"""


def write_review_html(rows, path, cap=1500):
    data = []
    for score, tier, band, best, c in rows[:cap]:
        reason = "; ".join("%s:%s" % (d, code) for d, code, _ in c.reasons)
        data.append({'w': c.suspect, 's': best, 'tier': tier, 'score': score,
                     'dets': sorted(c.detectors), 'dicts': sorted(c.dicts), 'reason': reason})
    payload = html.escape(json.dumps(data, ensure_ascii=False)).replace('</', '<\\/')
    capnote = ("" if len(rows) <= cap else
               "<p><b>Note:</b> showing top %d of %d by score; full list in combined_candidates.txt.</p>"
               % (cap, len(rows)))
    doc = REVIEW_TEMPLATE.replace('@@CAPNOTE@@', capnote).replace('@@PAYLOAD@@', payload)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)


if __name__ == "__main__":
    rerun = '--rerun' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sanhw1 = args[0] if args else "../sanhw1.txt"
    main(sanhw1, rerun)
