"""Union-headword attestation signal (PROJECT_INTERLINKS feed).

Cross-dict attestation from SanskritLexicography's **union headword index**
(`HeadwordLists/union/union_headwords.tsv`, ~323k SLP1 headwords each tagged with
the number of dictionaries that attest it). A suspect that is itself attested
across many *independent* Cologne dictionaries is very likely a real Sanskrit
word, not a typo -- a ready-made "attested in N other dicts -> not a typo"
signal that lets run_all.py demote broadly-attested suspects out of tier A,
cutting the tier-A false-positive rate on mature dictionaries.

The index lives in a SIBLING repo and is large + licensed, so it is NOT
committed here. It is resolved like detectors/get_external_source.py: the env
override `SANSKRIT_UNION_HEADWORDS`, else the default sibling path. If the file
is absent, `load_union()` returns `{}` and every caller degrades to no-signal --
the pipeline's behaviour is then unchanged.

Keys are matched through slp1util.normalize_lemma (the same slp1_norm the union
builder uses), so the two sides join cleanly. SLP1 throughout.
"""
import os

import slp1util as u

_HERE = os.path.dirname(os.path.abspath(__file__))
# detectors/ -> repo root -> GitHub root -> SanskritLexicography sibling
DEFAULT_UNION = os.path.normpath(os.path.join(
    _HERE, "..", "..", "SanskritLexicography",
    "HeadwordLists", "union", "union_headwords.tsv"))

# Attested in >= this many dictionaries -> trust as a real word (conservative; the
# union spans ~12 general Cologne dicts). A maintainer tunable.
UNION_TRUST_DICTS = 5

_cache = None


def union_path():
    return os.environ.get("SANSKRIT_UNION_HEADWORDS", DEFAULT_UNION)


def load_union(path=None):
    """Return {normalized SLP1 headword: n_dicts}. Empty {} if the index is absent."""
    global _cache
    if path is None and _cache is not None:
        return _cache
    resolved = path or union_path()
    out = {}
    if os.path.exists(resolved):
        with open(resolved, "r", encoding="utf-8") as f:
            f.readline()  # header: slp1 \t iast \t n_dicts \t dicts \t ...
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 3:
                    continue
                try:
                    n = int(parts[2])
                except ValueError:
                    continue
                key = u.normalize_lemma(parts[0])
                if n > out.get(key, 0):
                    out[key] = n
    if path is None:
        _cache = out
    return out


def attestation(slp1, union=None):
    """Number of dictionaries attesting this SLP1 headword (0 if unknown/absent)."""
    idx = union if union is not None else load_union()
    return idx.get(u.normalize_lemma(slp1), 0)
