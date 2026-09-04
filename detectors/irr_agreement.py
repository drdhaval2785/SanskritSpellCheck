"""irr_agreement.py  (Python 3, stdlib-only)  -- H453 step 3 + H825 step 1 (D9):
Cohen's kappa, exact.

Computes inter-annotator agreement between the committed FILE-FIRST verdicts
(corrections_draft/file_first_verified.tsv, annotator A) and:
  - the blind within-family second annotation (irr/second_annotations.tsv,
    annotator B = Opus 4.8, same model family as A's Sonnet/Fable pass), and
  - if present, the blind CROSS-family second annotation
    (irr/cross_family_annotations.tsv, annotator C = a non-Anthropic judge,
    produced by detectors/irr_cross_family.py) -- ruling D9's self-enhancement-
    bias control (Zheng MT-Bench 2306.05685; Self-Preference Bias 2410.21819).
C is optional: this script degrades to the A-vs-B report alone when C hasn't been
run yet (e.g. no LLM_API_KEY configured on the host that ran this).

CAUTION (a real limit ruling D9 does not itself resolve): A-vs-B and A-vs-C are
both LLM-only inter-rater comparisons. Two annotators agreeing, even across model
families, shows consistency, not ground truth -- neither kappa here is licensed
against independent human judgment yet. See
corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md: a genuine ~30-row human-labelled
subset is a real gate for a human to fill, not something an agent session should
fabricate.

All arithmetic is exact (fractions.Fraction) -- no scipy, no float approximations
(the A37 lesson: scipy's t-approximation was invalid at small n; see
exact_spearman_p() in detectors/drift_dating.py). Decimals shown are exact
fractions rendered to 4 places.

Outputs:
  corrections_draft/irr/agreement_stats.md   (one section per available annotator
                                              pair: matrix, kappa overall + per
                                              class, percent agreement, binary
                                              collapse, disagreement list)
  and the same summary to stdout.

Usage: python detectors/irr_agreement.py
"""
import os
import sys
from fractions import Fraction

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
A_SRC = os.path.join(ROOT, 'corrections_draft', 'file_first_verified.tsv')
B_SRC = os.path.join(ROOT, 'corrections_draft', 'irr', 'second_annotations.tsv')
C_SRC = os.path.join(ROOT, 'corrections_draft', 'irr', 'cross_family_annotations.tsv')
OUT = os.path.join(ROOT, 'corrections_draft', 'irr', 'agreement_stats.md')

LABELS = ['PASS', 'SCAN-FIRST', 'EDITORIAL', 'DNF', 'DROP']


def read_a():
    rows = []
    with open(A_SRC, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if p[0] == 'dict':
                continue
            rows.append({'dict': p[0], 'wrong': p[1], 'right': p[2], 'a': p[3]})
    for i, r in enumerate(rows, 1):
        r['row_id'] = '%03d' % i
    return rows


def read_second(path):
    """{row_id: {'label':..., 'reason':...}} from a second_annotations.tsv-shaped file
    (row_id, <label col>, <reason col>) -- the column name varies (a2_label/c_label)
    but the position is always col 1/2."""
    out = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if p[0] == 'row_id':
                continue
            out[p[0]] = {'label': p[1], 'reason': p[2] if len(p) > 2 else ''}
    return out


def kappa(pairs):
    """Exact Cohen's kappa over (a,b) label pairs -> (po, pe, kappa) Fractions."""
    n = len(pairs)
    po = Fraction(sum(1 for a, b in pairs if a == b), n)
    pe = Fraction(0)
    for lab in LABELS:
        na = sum(1 for a, _ in pairs if a == lab)
        nb = sum(1 for _, b in pairs if b == lab)
        pe += Fraction(na, n) * Fraction(nb, n)
    if pe == 1:
        return po, pe, Fraction(1)
    return po, pe, (po - pe) / (1 - pe)


def binary_kappa(pairs, lab):
    """Kappa for one class vs rest."""
    bp = [(a == lab, b == lab) for a, b in pairs]
    n = len(bp)
    po = Fraction(sum(1 for a, b in bp if a == b), n)
    pe = Fraction(0)
    for v in (True, False):
        na = sum(1 for a, _ in bp if a == v)
        nb = sum(1 for _, b in bp if b == v)
        pe += Fraction(na, n) * Fraction(nb, n)
    if pe == 1:
        return Fraction(1)
    return (po - pe) / (1 - pe)


def dec(fr, places=4):
    return ('%.*f' % (places, float(fr)))


def report_section(w, a_rows, other_map, other_name, other_desc):
    """Emit one full agreement section (matrix, kappas, binary collapse,
    disagreements) for annotator A vs `other_map` (keyed by row_id).

    Coverage rule (H4075 fix 2): stats are computed over the COVERED overlap
    (rows present in both A and the second annotation), with the uncovered
    rows reported explicitly — a partially-grown file_first_verified.tsv must
    not stub the whole section (the F2 lesson: 122-row annotations + a 200-row
    A file used to erase the kappas entirely). Stub only on zero overlap.
    """
    covered = [r for r in a_rows if r['row_id'] in other_map]
    missing = [r['row_id'] for r in a_rows if r['row_id'] not in other_map]
    if not covered:
        w('**SKIPPED — no %s annotations at all; %d A rows uncovered.**' % (other_name, len(missing)))
        w('')
        return
    if missing:
        w('_Coverage: %d of %d A rows have a %s annotation; stats below cover the '
          'overlap only. Unannotated rows (%d): %s._'
          % (len(covered), len(a_rows), other_name, len(missing), ', '.join(missing)))
        w('')

    pairs = [(r['a'], other_map[r['row_id']]['label']) for r in covered]
    n = len(pairs)
    po, pe, k = kappa(pairs)

    mat = {la: {lb: 0 for lb in LABELS} for la in LABELS}
    for a, b in pairs:
        mat[a][b] += 1

    w('## Annotator A (FILE-FIRST verdicts) vs annotator %s (%s)' % (other_name, other_desc))
    w('')
    w('| metric | exact | decimal |')
    w('|---|---|---|')
    w('| observed agreement p_o | %s | %s |' % (po, dec(po)))
    w('| chance agreement p_e | %s | %s |' % (pe, dec(pe)))
    w("| Cohen's kappa | %s | %s |" % (k, dec(k)))
    w('')
    w('### Confusion matrix (rows = A; cols = %s)' % other_name)
    w('')
    w('| A \\ %s | ' % other_name + ' | '.join(LABELS) + ' | total |')
    w('|---|' + '---|' * (len(LABELS) + 1))
    for la in LABELS:
        row = [str(mat[la][lb]) for lb in LABELS]
        w('| **%s** | %s | %d |' % (la, ' | '.join(row), sum(mat[la].values())))
    w('| **total** | ' + ' | '.join(str(sum(mat[la][lb] for la in LABELS)) for lb in LABELS) + ' | %d |' % n)
    w('')
    w('### Per-class kappa (class vs rest)')
    w('')
    w('| class | A count | %s count | binary kappa |' % other_name)
    w('|---|---|---|---|')
    for lab in LABELS:
        na = sum(1 for a, _ in pairs if a == lab)
        nb = sum(1 for _, b in pairs if b == lab)
        w('| %s | %d | %d | %s |' % (lab, na, nb, dec(binary_kappa(pairs, lab))))
    w('')
    w('### Secondary statistic: binary defect-recognized collapse')
    w('')
    w('Labels collapsed to ACT = {PASS, SCAN-FIRST, EDITORIAL} (a genuine defect needing')
    w('action) vs NOACT = {DNF, DROP}. Pre-registered secondary view (filing *policy*')
    w('removed, defect *recognition* kept); not selected post hoc.')
    w('')
    bmap = lambda x: 'ACT' if x in ('PASS', 'SCAN-FIRST', 'EDITORIAL') else 'NOACT'  # noqa: E731
    bpairs = [(bmap(a), bmap(b)) for a, b in pairs]
    bn = len(bpairs)
    bpo = Fraction(sum(1 for a, b in bpairs if a == b), bn)
    bpe = Fraction(0)
    for v in ('ACT', 'NOACT'):
        na = sum(1 for a, _ in bpairs if a == v)
        nb = sum(1 for _, b in bpairs if b == v)
        bpe += Fraction(na, bn) * Fraction(nb, bn)
    bk = Fraction(1) if bpe == 1 else (bpo - bpe) / (1 - bpe)
    w('| metric | exact | decimal |')
    w('|---|---|---|')
    w('| observed agreement p_o | %s | %s |' % (bpo, dec(bpo)))
    w("| Cohen's kappa (binary) | %s | %s |" % (bk, dec(bk)))
    w('')
    w('### Disagreements')
    w('')
    w('| row | dict | wrong | right | A | %s | %s reason |' % (other_name, other_name))
    w('|---|---|---|---|---|---|---|')
    for r in covered:
        b = other_map[r['row_id']]
        if r['a'] != b['label']:
            w('| %s | %s | %s | %s | %s | %s | %s |' % (
                r['row_id'], r['dict'], r['wrong'], r['right'], r['a'], b['label'],
                b['reason'].replace('|', '/')))
    w('')


def main():
    a_rows = read_a()
    b_map = read_second(B_SRC)

    lines = []
    w = lines.append
    w('# IRR agreement statistics — FILE-FIRST verdicts vs blind second annotator(s)')
    w('')
    w('_Generated by [detectors/irr_agreement.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_agreement.py); exact arithmetic (fractions), n=%d._' % len(a_rows))
    w('')

    report_section(w, a_rows, b_map, 'B', 'within-family, Opus 4.8 (claude-opus-4-8), blind')

    if os.path.exists(C_SRC):
        c_map = read_second(C_SRC)
        report_section(w, a_rows, c_map, 'C',
                        'cross-family (H825/D9), non-Anthropic judge, blind — '
                        'see detectors/irr_cross_family.py')
    else:
        w('## Annotator C (cross-family, ruling D9)')
        w('')
        w('_Not yet run — %s absent. Run `python detectors/irr_cross_family.py` with a '
          'non-Anthropic LLM_API_KEY configured (DeepSeek or any OpenAI-compatible '
          'endpoint), then re-run this script._' % os.path.relpath(C_SRC, ROOT).replace('\\', '/'))
        w('')

    w('## Human anchor (ruling D9 residual gate)')
    w('')
    w('Both sections above are LLM-only inter-rater comparisons; agreement between two (or '
      'three) model families is evidence of consistency, not of correctness against the '
      'physical scan. See '
      '[corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md) '
      'for the outstanding ~30-row human-labelled seed set that licenses citing these kappas '
      'as validated inter-annotator reliability rather than mutual LLM consistency.')
    w('')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:20]))
    print('...')
    print('-> %s' % OUT)


if __name__ == '__main__':
    main()
