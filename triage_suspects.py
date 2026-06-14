"""triage_suspects.py  (Python 3)

Split a faultfinder AllvsXX.txt suspect list into a high-signal review list and a
low-value noise list, and print a summary.

Input line format (from faultfinder3a.php):  X:P=Y:D
  X = suspect headword (SLP1)
  P = pattern abbreviation (e.g. SCC, VV, CCE)
  Y = the offending substring
  D = comma-separated dictionaries that contain X (never the base dict)

A line is NOISE if every dictionary in D is a specialized dictionary: such words are
domain-specific (Puranic/geographic/inscriptional proper names, Buddhist hybrid,
foreign names) and rarely real general-Sanskrit spelling errors. Otherwise SIGNAL.
The specialized set is sanhw2.py's `san_spc_dicts` (INM, VEI, PUI, ACC, KRM, IEG,
SNP, PE, PGN, MCI) plus PD/BHS/BUR, which README.md also calls "not worthwhile".

Signal is sorted by headword length descending then alphabetically -- longer words
are higher-probability real errors (the o_vs_O method uses the same heuristic).

Usage:
  python triage_suspects.py <AllvsXX.txt> <signal_out.txt> <noise_out.txt>
"""
import sys
import collections

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# sanhw2.py san_spc_dicts + PD/BHS/BUR (README "not worthwhile")
SPECIALIZED = {'INM', 'VEI', 'PUI', 'ACC', 'KRM', 'IEG', 'SNP', 'PE', 'PGN', 'MCI',
               'PD', 'BHS', 'BUR'}


def parse(line):
    line = line.rstrip('\r\n')
    x = line[:line.index(':')]
    d = line[line.rindex(':') + 1:]
    mid = line[line.index(':') + 1:line.rindex(':')]
    p = mid.split('=')[0]
    dicts = [t for t in d.split(',') if t]
    return x, p, dicts, line


def main(infile, signal_out, noise_out):
    signal, noise = [], []
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            x, p, dicts, raw = parse(line)
            if all(code in SPECIALIZED for code in dicts):
                noise.append((x, p, dicts, raw))
            else:
                signal.append((x, p, dicts, raw))

    signal.sort(key=lambda r: (-len(r[0]), r[0]))

    with open(signal_out, 'w', encoding='utf-8') as f:
        for _, _, _, raw in signal:
            f.write(raw + '\n')
    with open(noise_out, 'w', encoding='utf-8') as f:
        for _, _, _, raw in noise:
            f.write(raw + '\n')

    total = len(signal) + len(noise)
    print("total suspects : %d" % total)
    print("signal (review): %d  -> %s" % (len(signal), signal_out))
    print("noise (special): %d  -> %s" % (len(noise), noise_out))
    pats = collections.Counter(p for _, p, _, _ in signal)
    print("signal by pattern: " + ", ".join("%s=%d" % (k, v) for k, v in pats.most_common()))
    gdicts = collections.Counter(c for _, _, dd, _ in signal for c in dd if c not in SPECIALIZED)
    print("signal by dict   : " + ", ".join("%s=%d" % (k, v) for k, v in gdicts.most_common(10)))
    print("--- top 12 signal suspects (longest first) ---")
    for _, _, _, raw in signal[:12]:
        print("  " + raw)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
