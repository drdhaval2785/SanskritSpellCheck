#!/usr/bin/env python3
"""triage_util.py -- shared helpers for the body-grounded triage pipeline.

The triage core. Stdlib-only (no dependency on the SLP1 confusion model in slp1util.py),
so every triage_*.py step can import it cheaply. Collects what was otherwise copy-pasted
across the steps:

  paths / CLI / tunables -- HERE/ROOT/GITHUB, reconfigure_stdio(), dict_arg(),
      package_dir() / work_dir(), csl_root() / csl_dict_file(), and the shared constants
      (BATCH_SIZE, INTENTIONAL_KINDS, NEEDS_JUDGMENT) that several steps must agree on.

  load_json_array / load_verdicts -- read the JSON arrays the body-aware workflow
      agents write (tolerant of a stray ```json fence or trailing prose).

  EntryIndex / build_entry_index -- parse a csl-orig dictionary file ONCE into a
      headword -> [entries] index (each entry carries its line number, the raw <L>
      header line, the <k2> key, and the entry body), plus an L-number -> headword map
      so {{Lbody=N}} redirects (VCP) can be resolved to the headword they point at.
"""
import os
import re
import sys
import json
import glob


# --- shared paths, CLI, and tunables ---------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))   # detectors/
ROOT = os.path.dirname(HERE)                         # repo root
GITHUB = os.path.dirname(ROOT)                       # GitHub/ (sibling checkout: csl-orig/)

# Rows per agent batch. The body-aware workflow spawns one agent per batch file, so this
# trades agent count against per-agent context. Shared by triage_enrich (batch_*.jsonl) and
# triage_body_batches (body_batch_*.jsonl) so the two stay in lockstep.
BATCH_SIZE = 30

# body_kind values (set by triage_bodies.classify) that mean the dictionary documents the
# spelling ON PURPOSE -> never file. Used by triage_bodies + triage_synthesize + triage_body_batches.
INTENTIONAL_KINDS = ('wr', 'variant', 'xref')

# body_kind values that a deterministic pass cannot settle -> hand to the body-aware LLM.
NEEDS_JUDGMENT = ('realword', 'thin', 'multi-mixed')

# Cologne scanned-page deep-link template: SCAN_URL % (dict_code, headword_key).
SCAN_URL = ("http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/"
            "servepdf.php?dict=%s&key=%s")


def reconfigure_stdio():
    """Force UTF-8 on stdout/stderr (Windows consoles default to cp1252)."""
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def dict_arg(default='MW'):
    """The <DICT> code shared by every triage step's CLI: argv[1], defaulting to MW."""
    return sys.argv[1] if len(sys.argv) > 1 else default


def package_dir(dict_code):
    """corrections_draft/<DICT>/ -- the per-dictionary triage package."""
    return os.path.join(ROOT, 'corrections_draft', dict_code)


def work_dir(dict_code, create=False):
    """<package>/triage_work/ -- gitignored intermediates (batch files, agent verdicts)."""
    w = os.path.join(package_dir(dict_code), 'triage_work')
    if create:
        os.makedirs(w, exist_ok=True)
    return w


def csl_root():
    """The csl-orig checkout (a sibling of this repo): GitHub/csl-orig."""
    return os.path.join(GITHUB, 'csl-orig')


def csl_dict_file(dict_code):
    """csl-orig/v02/<dict>/<dict>.txt -- the canonical source text for a dictionary."""
    d = dict_code.lower()
    return os.path.join(csl_root(), 'v02', d, d + '.txt')


# --- workflow-output JSON ---------------------------------------------------
def load_json_array(path):
    """Load a JSON array an agent wrote, tolerating a ```json fence or trailing prose."""
    with open(path, encoding='utf-8') as f:
        t = f.read().strip()
    if t.startswith('```'):
        t = t.split('```')[1]
        if t.lstrip().startswith('json'):
            t = t.lstrip()[4:]
    t = t.strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        # Parse the FIRST valid JSON array, scanning '[' candidates. A greedy first-'[' to
        # last-']' span over-captures when surrounding prose also contains brackets.
        dec, start = json.JSONDecoder(), 0
        while True:
            i = t.find('[', start)
            if i < 0:
                return []
            try:
                obj, _ = dec.raw_decode(t, i)
                if isinstance(obj, list):
                    return obj
            except json.JSONDecodeError:
                pass
            start = i + 1


def load_verdicts(workdir, pattern, key='suspect'):
    """{key: verdict} merged from every <pattern> file in workdir (later wins)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(workdir, pattern))):
        try:
            for v in load_json_array(p):
                if key in v:
                    out[v[key]] = v
        except Exception as e:
            # Do NOT swallow silently -- a dropped verdict file skews the downstream buckets
            # (and can silently disable the review gate). Make the loss visible.
            print("  WARNING: could not load %s: %s" % (os.path.basename(p), str(e)[:80]), file=sys.stderr)
    return out


# --- csl-orig entry index ---------------------------------------------------
_L = re.compile(r'<L>([0-9.]+)')
_K1 = re.compile(r'<k1>([^<]*)')
_K2 = re.compile(r'<k2>([^<]*)')


class EntryIndex:
    """headword -> [entry dicts]; each entry = {lnum, lineno, line, k1, k2, body}."""

    def __init__(self):
        self.by_k1 = {}
        self.by_k2 = {}
        self.by_l = {}   # L-number string -> k1 (for {{Lbody=N}} redirects)

    def entries(self, hw):
        return self.by_k1.get(hw, [])

    def bodies(self, hw):
        # mirror first(): prefer k1, fall back to k2 so a k2-only headword still yields its body
        return [e['body'] for e in (self.by_k1.get(hw) or self.by_k2.get(hw) or [])]

    def first(self, hw):
        """First entry under k1 (or k2) for hw, preferring k1; None if absent."""
        lst = self.by_k1.get(hw) or self.by_k2.get(hw)
        return lst[0] if lst else None

    def k1_for_l(self, lnum):
        return self.by_l.get(str(lnum))


def _finalize(idx, cur, buf):
    cur['body'] = ' '.join(buf).strip()
    if cur['k1']:
        idx.by_k1.setdefault(cur['k1'], []).append(cur)
    if cur['k2']:
        idx.by_k2.setdefault(cur['k2'], []).append(cur)
    if cur['lnum']:
        idx.by_l.setdefault(cur['lnum'], cur['k1'])


def build_entry_index(csl_root, dictcode):
    """Parse csl-orig/v02/<dict>/<dict>.txt into an EntryIndex; None if the file is absent."""
    path = os.path.join(csl_root, 'v02', dictcode.lower(), dictcode.lower() + '.txt')
    if not os.path.exists(path):
        return None
    idx = EntryIndex()
    cur, buf = None, []
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if line.startswith('<L>'):
                if cur is not None:           # entry without an explicit <LEND>
                    _finalize(idx, cur, buf)
                s = line.rstrip('\n')
                lm, m1, m2 = _L.search(s), _K1.search(s), _K2.search(s)
                cur = {'lnum': lm.group(1) if lm else None, 'lineno': i, 'line': s,
                       'k1': m1.group(1).strip() if m1 else '',
                       'k2': m2.group(1).strip() if m2 else ''}
                buf = []
            elif line.startswith('<LEND>'):
                if cur is not None:
                    _finalize(idx, cur, buf)
                    cur, buf = None, []
            elif cur is not None:
                buf.append(line.rstrip('\n'))
        if cur is not None:
            _finalize(idx, cur, buf)
    return idx


_LBODY = re.compile(r'\{\{Lbody=([0-9.]+)\}\}')


def resolve_redirect(body, idx):
    """If body is a VCP {{Lbody=N}} redirect, annotate it with the target headword."""
    m = _LBODY.search(body or '')
    if not m:
        return body
    target = idx.k1_for_l(m.group(1)) if idx else None
    return ('%s  (redirect -> %s)' % (body, target)) if target else body
