#!/usr/bin/env python3
"""build_spellcheck_dict.py — assemble the spell-check dictionary from the
A55 union headword index (+MWderivations): build, dedup, version stamp.

Sources (both live OUTSIDE this repo and are resolved like
detectors/union_attestation.py — env override, else sibling checkout):

  * A55 union headword index — dataset ``union-headwords`` of gasyoun/kosha
    (release data-v0.4.0, DOI 10.5281/zenodo.22102090; 323,422 rows; CC BY-SA 4.0).
    Canonical copy: sibling SanskritLexicography checkout,
    HeadwordLists/union/union_headwords.tsv (columns: slp1, iast, n_dicts, dicts,
    gender, fem_fold). Env override: SANSKRIT_UNION_HEADWORDS (the same variable
    detectors/union_attestation.py reads).
  * MWderivations — funderburkjim/MWderivations, step4/analysis2.txt
    (220,248 rows; columns: Hcode, L, key1, key2, gender, parse, status, method).
    Env override: MWDERIVATIONS_ANALYSIS2.

Assembly rules
  * union: the ``slp1`` column as-is (the union builder already strips accent
    marks and print-layer hyphenation).
  * MWderivations: every ``key1``, plus ``key2`` with hyphens and analysis-layer
    marks (``@ < > '`` and spaces) stripped — key2 components are taken only
    from rows whose parse RESOLVED (``status == DONE``), so unresolved
    placeholders never leak in. This is what lifts the dictionary past the
    union: derived and compound member spellings MW records but the fifteen
    CDSL key1 exports miss.
  * exact-string dedup, Sanskrit alphabetical order
    (detectors/slp1util.sanskrit_sort_key: M -> homorganic nasal normalization,
    so aMga sorts as aNga), UTF-8, LF, one word per line.

Output: HeadwordLists/spellcheck_union_mwderiv-v1.0.0.txt plus a .meta.json
manifest carrying the version, source versions, dedup counts and the artifact
sha256. Consumers load it with detectors/slp1util.load_spellcheck_dict().

  python tools/build_spellcheck_dict.py               # default locations
  python tools/build_spellcheck_dict.py --out DIR     # alternate output dir
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, "detectors"))
import slp1util  # noqa: E402  (repo-local shared util: sort key only)

DICT_VERSION = "1.0.0"
ARTIFACT_NAME = "spellcheck_union_mwderiv-v" + DICT_VERSION + ".txt"

# Marks the MWderivations analysis layer carries that the union key1 layer
# never does: accent markers, analysis brackets, quote/spaces. Hyphens are
# stripped separately (print-layer hyphenation, union-builder convention).
_MWD_STRIP = "@<>' \t-"


def default_union_path():
    env = os.environ.get("SANSKRIT_UNION_HEADWORDS")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "SanskritLexicography",
        "HeadwordLists", "union", "union_headwords.tsv"))


def default_mwderiv_path():
    env = os.environ.get("MWDERIVATIONS_ANALYSIS2")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "MWderivations", "step4", "analysis2.txt"))


def load_union_words(path):
    """slp1 column of the A55 union index (header skipped). Returns (words, rows)."""
    words = set()
    rows = 0
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        if not header or header[0] != "slp1":
            raise SystemExit("ERROR: %s does not look like union_headwords.tsv "
                             "(expected a 'slp1' first column)" % path)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0]:
                continue
            words.add(parts[0])
            rows += 1
    return words, rows


def clean_mwderiv_form(form):
    """Strip hyphens and analysis-layer marks; None when nothing survives."""
    cleaned = form.translate(str.maketrans("", "", _MWD_STRIP))
    return cleaned or None


def load_mwderiv_words(path):
    """key1 of every row + cleaned key2 of DONE rows. Returns (key1, key2, rows)."""
    key1 = set()
    key2 = set()
    rows = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            rows += 1
            if parts[2]:
                key1.add(parts[2])
            # key2 components only from rows whose parse resolved (DONE);
            # NTD/TODO/... key2 fields are placeholders, not spellings.
            if len(parts) > 6 and parts[6] == "DONE" and parts[3] \
                    and parts[3] != parts[2]:
                cleaned = clean_mwderiv_form(parts[3])
                if cleaned:
                    key2.add(cleaned)
    return key1, key2, rows


def build(union_path, mwderiv_path, out_dir):
    union, union_rows = load_union_words(union_path)
    mw_k1, mw_k2, mw_rows = load_mwderiv_words(mwderiv_path)

    combined_raw = union | mw_k1 | mw_k2
    deduped = sorted(combined_raw, key=slp1util.sanskrit_sort_key)

    os.makedirs(out_dir, exist_ok=True)
    artifact = os.path.join(out_dir, ARTIFACT_NAME)
    with open(artifact, "w", encoding="utf-8", newline="\n") as f:
        for w in deduped:
            f.write(w + "\n")
    sha256 = hashlib.sha256(open(artifact, "rb").read()).hexdigest()

    manifest = {
        "artifact": ARTIFACT_NAME,
        "version": DICT_VERSION,
        "built": __import__("datetime").date.today().isoformat(),
        "format": "plain text, UTF-8, LF, one SLP1 word per line, "
                  "Sanskrit alphabetical order (M->homorganic normalization)",
        "sha256": sha256,
        "counts": {
            "union_rows": union_rows,
            "union_words": len(union),
            "mwderiv_rows": mw_rows,
            "mwderiv_key1_words": len(mw_k1),
            "mwderiv_key2_words": len(mw_k2),
            "combined_raw": len(union) + len(mw_k1) + len(mw_k2),
            "deduped": len(deduped),
            "duplicates_removed": len(union) + len(mw_k1) + len(mw_k2)
                                  - len(deduped),
            "mwderiv_only": len((mw_k1 | mw_k2) - union),
            "union_only": len(union - mw_k1 - mw_k2),
        },
        "sources": {
            "union": {
                "dataset": "gasyoun/kosha union-headwords (A55)",
                "release": "data-v0.4.0",
                "doi": "10.5281/zenodo.22102090",
                "license": "CC BY-SA 4.0",
                "rows": 323422,
                "local_copy": "SanskritLexicography/HeadwordLists/union/"
                              "union_headwords.tsv",
                "env_override": "SANSKRIT_UNION_HEADWORDS",
            },
            "mwderivations": {
                "repo": "funderburkjim/MWderivations",
                "file": "step4/analysis2.txt",
                "rows": 220248,
                "env_override": "MWDERIVATIONS_ANALYSIS2",
            },
        },
        "builder": "tools/build_spellcheck_dict.py",
        "consumers": "detectors/slp1util.load_spellcheck_dict()",
    }
    meta_path = artifact + ".meta.json"
    with open(meta_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("union: %d rows -> %d words" % (union_rows, len(union)))
    print("mwderivations: %d rows -> %d key1 + %d cleaned key2 (DONE)"
          % (mw_rows, len(mw_k1), len(mw_k2)))
    print("combined raw: %d -> deduped: %d (removed %d)"
          % (len(union) + len(mw_k1) + len(mw_k2), len(deduped),
             len(union) + len(mw_k1) + len(mw_k2) - len(deduped)))
    print("mwderivations-only additions: %d"
          % len((mw_k1 | mw_k2) - union))
    print("wrote %s (v%s, sha256 %s)" % (artifact, DICT_VERSION, sha256[:16]))
    print("wrote %s" % meta_path)
    return artifact, meta_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--union", default=default_union_path(),
                    help="union_headwords.tsv (env SANSKRIT_UNION_HEADWORDS)")
    ap.add_argument("--mwderiv", default=default_mwderiv_path(),
                    help="MWderivations analysis2.txt (env MWDERIVATIONS_ANALYSIS2)")
    ap.add_argument("--out", default=os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, "HeadwordLists")),
        help="output directory (default HeadwordLists/)")
    args = ap.parse_args(argv)
    for p in (args.union, args.mwderiv):
        if not os.path.exists(p):
            ap.error("source not found: %s" % p)
    build(args.union, args.mwderiv, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
