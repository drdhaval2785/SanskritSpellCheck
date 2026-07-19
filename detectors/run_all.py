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
import json
import subprocess
import collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u
import union_attestation as ua

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
    ('meter_check',    'meter_check.py',       'meter_suspects.txt',             'flagger'),
    ('tied_field',     'tied_field_check.py',  'tied_field_suspects.txt',        'flagger'),
]
HIGH_PRECISION = {'phonotactic', 'charset', 'tied_field'}
SCAN = "http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s"

# Corpus-corroboration ranking nudge (score_tier). A candidate is corroborated when the
# suggestion is a frequent DCS lemma (band >= 4 of 5), the suspect is unattested (band 0), and
# the edit is a high-weight confusion class (CORROB_CW = 0.05, the elbow of the weight
# distribution: admits Aa .41 / Ii .25 / Uu .089 / Ss .078, excludes the Ww .042 tail).
#
# ⚠️ This is a SCORE nudge ONLY, deliberately NOT a tier promoter. A tier-C -> B promotion on this
# signal was tried and REJECTED: it surfaces real Sanskrit minimal pairs as if they were typos
# (patra=leaf vs pAtra=vessel, vata/rAtrI are real MW headwords) because (a) Sanskrit vowel-length
# pairs are exactly where spelling+corpus can't tell an error from a real word -- the reason the
# body-grounded triage exists -- and (b) suspect-band 0 is unreliable (DCS coverage gaps make
# common words look unattested). The single-detector pairs the corpus CAN vouch for (band >= 3)
# are already tier B; pushing further trades precision for nothing the body can't settle. So we
# only let corroboration raise a candidate's rank WITHIN its tier, never its tier. See the
# Task-2 write-up in HANDOFF_NEXT.md.
CORROB_SUGG_BAND = 4
CORROB_CW = 0.05


class Cand:
    __slots__ = ('suspect', 'detectors', 'sugg_dets', 'sugg_dicts', 'reasons', 'dicts',
                 'morph', 'corroborated', 'union_n', 'meter')

    def __init__(self, suspect):
        self.suspect = suspect
        self.detectors = set()
        self.sugg_dets = collections.defaultdict(set)   # suggestion -> {detectors}
        self.sugg_dicts = collections.defaultdict(set)  # suggestion -> {dicts that a corrector tied to it}
        self.reasons = []                               # (detector, code, detail)
        self.dicts = set()
        self.morph = False                              # vidyut: suggestion is a valid stem, suspect is not
        self.corroborated = False                       # corpus+confusion corroboration (ranking nudge)
        self.union_n = 0                                # union index: # of dicts attesting this suspect
        self.meter = None                               # meter_check corroboration level: 'suspect'|'review'|None


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
    # Whitelist = nochange.txt ∪ do_not_file_suppress.txt (the per-dict
    # documented-intentional spellings from the body-grounded triage). The
    # correctors already self-suppress, but the flaggers (phonotactic/charset)
    # do not -- filter here so no suppressed headword survives in any detector.
    whitelist = u.load_whitelist(os.path.join(HERE, '..', 'nochange', 'nochange.txt'))

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
                if wrong in whitelist:
                    continue
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
                if x in whitelist:
                    continue
                if name == 'meter_check':
                    # H277: meter_check is a pure CORROBORATION NUDGE, not a detector
                    # peer. It never INTRODUCES a candidate (an ordinary word merely
                    # co-occurring with an irregular kavya verse is coincidence, not a
                    # spelling signal -- kavya vocabulary overlaps ordinary headwords
                    # too much) and never joins c.detectors (so it can never lift ndet
                    # to 2 and promote a candidate to tier A on a coincidence -- the
                    # exact failure the CORROB_* block above rejected for a similar
                    # corpus signal). It only strengthens the RANK of a candidate an
                    # independent spelling detector already surfaced, via a small
                    # score nudge in score_tier keyed on c.meter. So: annotate an
                    # existing candidate; skip if none.
                    c = cands.get(x)
                    if c is None:
                        continue
                    level = 'suspect' if detail.startswith('suspect') else 'review'
                    if level == 'suspect' or c.meter is None:
                        c.meter = level
                    c.reasons.append((name, rcode, detail))
                    continue
                c = get(x)
                c.detectors.add(name)
                c.reasons.append((name, rcode, detail))
                c.dicts.update(t for t in d.split(',') if t)
    return cands


def score_tier(c, dcs, weights, stems, union=None):
    ndet = len(c.detectors)
    # best suggestion = most detector support, then highest DCS band
    best, best_band, best_supp = '', 0, -1
    for sugg, dets in c.sugg_dets.items():
        band = dcs.get(u.normalize_lemma(sugg), 0)
        if (len(dets), band) > (best_supp, best_band):
            best, best_band, best_supp = sugg, band, len(dets)
    hpf = bool(c.detectors & HIGH_PRECISION)
    cw = u.confusion_weight(c.suspect, best, weights) if best else 0.0  # common confusion -> rank up
    # vidyut morphology signal: the correction yields a valid stem the suspect lacks.
    # WEAK on dictionary headwords (most aren't pratipadikas, and an inflected suspect
    # looks "not a stem"), so it is a ranking nudge + tag only -- NOT a tier promoter.
    c.morph = bool(best) and (best in stems) and (c.suspect not in stems)
    # corpus corroboration (ranking nudge only -- see CORROB_* note above; NOT a tier promoter):
    # suggestion is a frequent DCS lemma, suspect is unattested, edit is a high-weight confusion.
    suspect_band = dcs.get(u.normalize_lemma(c.suspect), 0)
    c.corroborated = (best_band >= CORROB_SUGG_BAND and suspect_band == 0 and cw >= CORROB_CW)
    # union attestation: the suspect itself is a headword in c.union_n dictionaries.
    # Broad cross-dict attestation is strong evidence it is a real word, not a typo
    # (the "attested in N other dicts -> not a typo" signal). It ranks a candidate
    # DOWN within its tier and, when broadly attested, demotes tier A -> B -- but
    # NEVER below B and NEVER for the high-precision flaggers (a charset/phonotactic
    # violation is a real error even if a shared digitization mistake is attested
    # in several dicts). When the union index is absent, c.union_n is 0 -> no effect.
    c.union_n = ua.attestation(c.suspect, union) if union is not None else 0
    # meter corroboration (H277): a small RANK nudge only -- suspect verse a touch
    # more than review. Never a tier promoter (see aggregate()'s meter_check note);
    # c.meter is not in c.detectors, so it does not touch ndet/tier below.
    meter_nudge = 8 if c.meter == 'suspect' else 4 if c.meter == 'review' else 0
    score = (ndet * 100 + best_band * 10 + (50 if hpf else 0) + len(c.dicts)
             + round(cw * 20) + (15 if c.morph else 0) + (5 if c.corroborated else 0)
             + meter_nudge - min(c.union_n, 12))
    if c.detectors == {'dict_vs_corpus'}:
        tier = 'C'                              # exploratory alone (corroboration ranks it up in C)
    elif ndet >= 2 or hpf or best_band == 5:
        tier = 'A'
    elif best_band >= 3 or (c.detectors & {'consensus', 'intra_dup'}):
        tier = 'B'
    else:
        tier = 'C'
    if tier == 'A' and not hpf and c.union_n >= ua.UNION_TRUST_DICTS:
        tier = 'B'                              # broadly attested -> real word, demote out of tier A
    return score, tier, best, best_band


def main(sanhw1, rerun):
    ensure_outputs(sanhw1, rerun)
    dcs = u.load_dcs_lemmas(u.dcs_path())
    weights = u.load_confusion_weights()
    stems = u.load_vidyut_stems()
    union = ua.load_union()
    if union:
        print("union attestation: %d headwords from %s" % (len(union), ua.union_path()))
    else:
        print("union attestation: index absent (%s) -- signal off" % ua.union_path())
    cands = aggregate()

    rows = []
    for c in cands.values():
        score, tier, best, band = score_tier(c, dcs, weights, stems, union)
        rows.append((score, tier, band, best, c))
    rows.sort(key=lambda r: (-r[0], r[4].suspect))
    demoted = sum(1 for r in rows if r[4].union_n >= ua.UNION_TRUST_DICTS
                  and not (r[4].detectors & HIGH_PRECISION))

    tiers = collections.Counter(r[1] for r in rows)
    multi = sum(1 for r in rows if len(r[4].detectors) >= 2)
    print("unified candidates: %d (deduped across %d detectors); multi-detector: %d"
          % (len(rows), len(DETECTORS), multi))
    print("tiers: A=%d  B=%d  C=%d" % (tiers['A'], tiers['B'], tiers['C']))
    if union:
        print("union-attested suspects (>=%d dicts, demoted A->B unless high-precision): %d"
              % (ua.UNION_TRUST_DICTS, demoted))

    # combined_candidates.txt -- full ranked list
    with open(os.path.join(HERE, 'combined_candidates.txt'), 'w', encoding='utf-8') as f:
        for score, tier, band, best, c in rows:
            dets = ",".join(sorted(c.detectors))
            f.write("%s\t%d\t%s -> %s\t[%s]\t[%s]%s%s%s\n"
                    % (tier, score, c.suspect, best or "(flag)", dets, ",".join(sorted(c.dicts)),
                       "\tmorph" if c.morph else "",
                       "\tmeter=%s" % c.meter if c.meter else "",
                       "\tunion=%d" % c.union_n if c.union_n else ""))

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
<script type="application/json" id="payload">@@PAYLOAD@@</script>
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
function exp(v){const out=[];DATA.forEach((r,i)=>{if(dec[i]===v&&r.s){r.export_dicts.forEach(d=>out.push(d+':'+r.w+':'+r.s+':'+v))}});
 const b=new Blob([out.join('\n')+'\n'],{type:'text/plain'});const a=document.createElement('a');
 a.href=URL.createObjectURL(b);a.download=(v==='y'?'accepted':'rejected')+'_sf.txt';a.click();}
document.addEventListener('keydown',e=>{if(e.key==='a')set(cur,'y');else if(e.key==='r')set(cur,'n');
 else if(e.key==='s'){}else return; cur=Math.min(cur+1,DATA.length-1);
 document.getElementById('r'+cur).scrollIntoView({block:'center'});});
try{Object.assign(dec,JSON.parse(localStorage.getItem('sscdec')||'{}'))}catch(e){}
render();
</script>
</body></html>"""


def _json_for_script(value):
    """Serialize JSON safely inside a script data block without corrupting quotes."""
    payload = json.dumps(value, ensure_ascii=False)
    for char, escaped in (('&', r'\u0026'), ('<', r'\u003c'), ('>', r'\u003e'),
                          ('\u2028', r'\u2028'), ('\u2029', r'\u2029')):
        payload = payload.replace(char, escaped)
    return payload


def write_review_html(rows, path, cap=1500, dict_scope=None):
    scope = set(dict_scope) if dict_scope is not None else None
    data = []
    for score, tier, band, best, c in rows[:cap]:
        reason = "; ".join("%s:%s" % (d, code) for d, code, _ in c.reasons)
        if c.morph:
            reason = (reason + " morph✓").strip()
        if c.meter:
            reason = (reason + " meter:%s" % c.meter).strip()
        scan_dicts = c.dicts if scope is None else c.dicts & scope
        supported = c.sugg_dicts.get(best, ()) if best else ()
        export_dicts = set(supported) if scope is None else set(supported) & scope
        data.append({'w': c.suspect, 's': best, 'tier': tier, 'score': score,
                     'dets': sorted(c.detectors), 'dicts': sorted(scan_dicts),
                     'export_dicts': sorted(export_dicts), 'reason': reason})
    payload = _json_for_script(data)
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
