#!/usr/bin/env python3
"""drift_dating.py -- O4: can the orthographic drift/1k rate DATE a dictionary?

Reads the per-language drift summaries (ortho_drift/<lang>_drift_summary.tsv, produced by
ortho_drift.py) and each dictionary's known publication year, then tests whether drift/1k
predicts the year. Three questions:

  1. Cross-language -- is a single drift->year calibration possible? (No: the rate is
     regime-stratified -- legislated reforms sit 1-3 orders of magnitude above convention drift,
     so a given rate means different epochs in different languages.)
  2. Within a language -- is drift/1k monotone with year, and how tight? (Spearman + linregress.)
  3. Dating power -- leave-one-out: predict each dict's year from a fit on the others; report the
     mean absolute error, and where the scalar rate fails vs the per-era composition.

Outputs: ortho_drift/drift_dating.png (scatter, symlog y) + console stats. DOCUMENTATION ONLY.
Caveat: the German absolute rate is reform-map-dependent (see O3) -- this uses the frozen
deterministic-pass summary; the per-era composition (th- vs ss-dominant) is the robust dater.

  cd detectors && python drift_dating.py
"""
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_util
triage_util.reconfigure_stdio()

OUT = os.path.join(triage_util.ROOT, 'ortho_drift')

# Known / accepted publication years (compilation midpoint where a range). AP ("modern" Apte,
# undated edition here) is held OUT as an undated test case. PD = Deccan College 1976-2009 (mid).
YEARS = {
    # English (convention drift)
    'WIL': 1832, 'GST': 1856, 'BEN': 1866, 'MW72': 1872, 'AP90': 1890, 'CAE': 1891,
    'MD': 1893, 'MW': 1899, 'SHS': 1900, 'VEI': 1912, 'BHS': 1953, 'IEG': 1966,
    'PE': 1975, 'PD': 1990,
    # German (legislated 1901 / 1996)
    'PW': 1865, 'PWG': 1865, 'GRA': 1873, 'CCS': 1887, 'SCH': 1928,
    # French (minor reform), Latin (none), Russian (legislated 1918)
    'BUR': 1866, 'STC': 1932, 'BOP': 1847, 'KOSSOVICH': 1885,
}
LANGS = ['en', 'de', 'fr', 'la', 'ru']
LANG_COLOR = {'en': '#1f77b4', 'de': '#d62728', 'fr': '#2ca02c', 'la': '#7f7f7f', 'ru': '#9467bd'}
LANG_NAME = {'en': 'English', 'de': 'German', 'fr': 'French', 'la': 'Latin', 'ru': 'Russian'}


def load(lang):
    """[(dict, year, drift_per_1k)] for dicts with a known year."""
    path = os.path.join(OUT, '%s_drift_summary.tsv' % lang)
    rows = []
    if not os.path.exists(path):
        return rows
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('#') or ln.startswith('dict\t') or '\t' not in ln:
            continue
        c = ln.rstrip('\n').split('\t')
        code, rate = c[0], float(c[4])
        if code in YEARS:
            rows.append((code, YEARS[code], rate))
    return rows


def exact_spearman_p(yrs, rate, rng_iters=100000):
    """Two-tailed permutation p for Spearman rho: fraction of year-permutations whose
    |rho| >= |observed|. scipy's default p is a t-approximation that is unreliable at
    small n (at n=5 it can report p<0.01, below the exact minimum of ~1/60) and with
    heavy ties -- so report the exact/Monte-Carlo permutation p alongside it.
    Exact enumeration for n<=8 (<=40320 perms); Monte-Carlo above."""
    from itertools import permutations
    obs = abs(stats.spearmanr(yrs, rate)[0])
    n = len(yrs)
    if n <= 8:
        seen, total, ge = set(), 0, 0
        for perm in permutations(yrs):
            if perm in seen:
                continue
            seen.add(perm)
            total += 1
            if abs(stats.spearmanr(perm, rate)[0]) >= obs - 1e-9:
                ge += 1
        return ge / total, total, 'exact'
    rng = np.random.default_rng(20260703)
    y = np.array(yrs, float)
    ge = 0
    for _ in range(rng_iters):
        if abs(stats.spearmanr(rng.permutation(y), rate)[0]) >= obs - 1e-9:
            ge += 1
    return ge / rng_iters, rng_iters, 'monte-carlo'


def fit_report(lang, rows):
    if len(rows) < 2:
        print('  %s: %d point(s) -- cannot fit (%s)'
              % (LANG_NAME[lang], len(rows), ', '.join('%s=%.2f' % (d, r) for d, _, r in rows)))
        return None
    yrs = np.array([y for _, y, _ in rows], float)
    rate = np.array([r for _, _, r in rows], float)
    rho, p = stats.spearmanr(yrs, rate)
    p_perm, n_perm, kind = exact_spearman_p([y for _, y, _ in rows], rate)
    print('  %s (n=%d): Spearman(year, drift/1k) = %+.3f (t-approx p=%.3f; %s permutation p=%.3f over %d) '
          '; rates %.2f..%.2f over %d..%d'
          % (LANG_NAME[lang], len(rows), rho, p, kind, p_perm, n_perm,
             rate.min(), rate.max(), int(yrs.min()), int(yrs.max())))
    return rho


def loo_dating(lang, rows):
    """Leave-one-out: predict year from drift/1k via linregress on the others. MAE in years."""
    if len(rows) < 3:
        print('    LOO dating: n=%d too small' % len(rows))
        return
    errs = []
    for i in range(len(rows)):
        tr = [rows[j] for j in range(len(rows)) if j != i]
        x = np.array([r for _, _, r in tr], float)   # drift/1k
        y = np.array([yr for _, yr, _ in tr], float)  # year
        if np.ptp(x) == 0:
            continue
        sl, ic, *_ = stats.linregress(x, y)
        pred = sl * rows[i][2] + ic
        errs.append(abs(pred - rows[i][1]))
    if errs:
        print('    LOO year-prediction MAE = %.0f years (n=%d, predicting year from rate)'
              % (np.mean(errs), len(errs)))


def main():
    data = {lang: load(lang) for lang in LANGS}

    print('=== O4: drift/1k as a dating signal ===')
    print('\n[1] Cross-language regime stratification (a given rate means different epochs):')
    for lang in LANGS:
        rs = data[lang]
        if rs:
            mx = max(r for _, _, r in rs)
            print('  %-8s %d dict(s), drift/1k up to %.2f' % (LANG_NAME[lang], len(rs), mx))

    print('\n[2] Within-language monotonicity (does the rate track the year?):')
    for lang in LANGS:
        fit_report(lang, data[lang])

    print('\n[3] Dating power -- leave-one-out year prediction from the rate:')
    for lang in ('de', 'en'):
        if len(data[lang]) >= 3:
            print('  %s:' % LANG_NAME[lang])
            loo_dating(lang, data[lang])

    print('\n[4] Where the SCALAR rate fails -- two concrete cases:')
    # (a) SCH: predict its year from the pre-1901 German fit (rate alone) vs its era composition.
    de = {d: (y, r) for d, y, r in data['de']}
    pre = [(y, r) for d, (y, r) in de.items() if d != 'SCH']
    x = np.array([r for _, r in pre], float)
    y = np.array([yr for yr, _ in pre], float)
    sl, ic, *_ = stats.linregress(x, y)
    sch_pred = sl * de['SCH'][1] + ic
    print('  (a) SCH (true 1928): pre-1901 rate-fit predicts %d (err %+d yr) -- the scalar rate'
          % (round(sch_pred), round(sch_pred) - 1928))
    print('      UNDER-dates it, reading its low th-drift as "near-modern". Its era COMPOSITION'
          '\n      (1996-ss DOMINANT over 1901-th) pins it post-1901/pre-1996 correctly -- O3/SCH control.')
    # (b) English saturation: how many dicts sit at exactly 0.00, and over what span?
    zeros = [(d, y) for d, y, r in data['en'] if r == 0.0]
    if zeros:
        ys = [y for _, y in zeros]
        print('  (b) English saturation: %d dicts read EXACTLY 0.00 drift/1k, spanning %d-%d (%d yr)'
              % (len(zeros), min(ys), max(ys), max(ys) - min(ys)))
        print('      -- the rate cannot order or date any of them; post-reform-completion it is flat.')

    # --- plot: drift/1k (symlog) vs year, per language ---
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for lang in LANGS:
        rs = data[lang]
        if not rs:
            continue
        xs = [y for _, y, _ in rs]
        ys = [r for _, _, r in rs]
        ax.scatter(xs, ys, c=LANG_COLOR[lang], label=LANG_NAME[lang], s=55, zorder=3,
                   edgecolors='white', linewidths=0.6)
        for code, y, r in rs:
            ax.annotate(code, (y, r), fontsize=7, color=LANG_COLOR[lang],
                        xytext=(3, 3), textcoords='offset points')
    # German linear fit line (the cleanest legislated gradient)
    de = data['de']
    if len(de) >= 2:
        xy = sorted((y, r) for _, y, r in de)
        xs = np.array([p[0] for p in xy], float)
        rr = np.array([p[1] for p in xy], float)
        sl, ic, rv, *_ = stats.linregress(xs, rr)
        gx = np.linspace(xs.min(), xs.max(), 50)
        ax.plot(gx, sl * gx + ic, '--', c=LANG_COLOR['de'], lw=1, alpha=0.6,
                label='German fit (R²=%.2f)' % (rv ** 2))
    ax.set_yscale('symlog', linthresh=0.01)
    ax.set_xlabel('publication year')
    ax.set_ylabel('reform-drift / 1k gloss tokens (symlog)')
    ax.set_title('O4 — orthographic drift rate vs publication year\n'
                 '(regime-stratified: legislated reforms ≫ convention drift)')
    ax.axhline(0, color='#ccc', lw=0.6, zorder=1)
    ax.grid(True, which='both', alpha=0.2)
    ax.legend(fontsize=8, loc='center right')
    fig.tight_layout()
    png = os.path.join(OUT, 'drift_dating.png')
    fig.savefig(png, dpi=130)
    print('\n  plot -> %s' % os.path.relpath(png, triage_util.ROOT))


if __name__ == '__main__':
    main()
