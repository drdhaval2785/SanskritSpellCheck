#!/usr/bin/env python3
"""triage_util.py -- shared helpers for the body-grounded triage pipeline.

Two things that were duplicated across triage_*.py / make_changefiles.py:

  load_json_array / load_verdicts -- read the JSON arrays the body-aware workflow
      agents write (tolerant of a stray ```json fence or trailing prose).

  EntryIndex / build_entry_index -- parse a csl-orig dictionary file ONCE into a
      headword -> [entries] index (each entry carries its line number, the raw <L>
      header line, the <k2> key, and the entry body), plus an L-number -> headword map
      so {{Lbody=N}} redirects (VCP) can be resolved to the headword they point at.
"""
import os
import re
import json
import glob


# --- workflow-output JSON ---------------------------------------------------
def load_json_array(path):
    """Load a JSON array an agent wrote, tolerating a ```json fence or trailing text."""
    t = open(path, encoding='utf-8').read().strip()
    if t.startswith('```'):
        t = t.split('```')[1]
        if t.lstrip().startswith('json'):
            t = t.lstrip()[4:]
    t = t.strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r'\[.*\]', t, re.S)   # last-ditch: grab the array
        return json.loads(m.group(0)) if m else []


def load_verdicts(workdir, pattern, key='suspect'):
    """{key: verdict} merged from every <pattern> file in workdir (later wins)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(workdir, pattern))):
        try:
            for v in load_json_array(p):
                if key in v:
                    out[v[key]] = v
        except Exception:
            pass
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
        return [e['body'] for e in self.by_k1.get(hw, [])]

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
