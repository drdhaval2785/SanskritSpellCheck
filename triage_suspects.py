"""triage_suspects.py  (Python 3)

Split a faultfinder AllvsXX.txt suspect list into a high-signal review list and a
low-value noise list, plus a tighter "gemination" subset, and print a summary.

Input line format (from faultfinder3a.php):  X:P=Y:D
  X = suspect headword (SLP1)
  P = pattern abbreviation (e.g. SCC, VV, CCE)
  Y = the offending substring (the actual flagged cluster)
  D = comma-separated dictionaries that contain X (never the base dict)

A line is NOISE if every dictionary in D is a specialized dictionary: such words are
domain-specific (Puranic/geographic/inscriptional proper names, Buddhist hybrid,
foreign names) and rarely real general-Sanskrit spelling errors. Otherwise SIGNAL.
The specialized set is sanhw2.py's `san_spc_dicts` (INM, VEI, PUI, ACC, KRM, IEG,
SNP, PE, PGN, MCI) plus PD/BHS/BUR, which README.md also calls "not worthwhile".

GEMINATION here means **post-repha doubling**: the offending substring Y has the
consonant `r` immediately followed by a doubled consonant (`r C C`, e.g. -rdd-,
-rjj-, -ryy-, -rmm-, -rRR-). This is the recurring real-error signature -- the
manuscript convention of doubling a consonant after `r` (dharma->dharmma,
surya->suryya, varNa->varRRa) that Cologne normalizes inconsistently across
dictionaries. Plain doubled consonants are NOT used, because most (-tt- in citta /
vRtta, -dd- in uddeSa) are perfectly legitimate Sanskrit geminates; restricting to
post-`r` doubling drops those false positives. Highest-precision view; most useful on
noisy (medium/small) bases where SIGNAL alone is still large.

PRIORITY is SIGNAL minus GEMINATION -- the non-post-repha anomalies, and the real
verify-first targets. faultfinder3a-html.php's own rcc() filter sets post-repha words
aside by default precisely because they are usually the faithful printed form, so the
genuinely-suspicious clusters are the non-rcc ones.

Signal/priority/gemination are sorted by headword length descending then alphabetically.

Usage:
  python triage_suspects.py <AllvsXX.txt> <signal_out.txt> <noise_out.txt>
  Also writes, alongside signal_out:
    *-priority.txt   = signal minus post-repha (non-rcc anomalies; VERIFY FIRST)
    *-gemination.txt = the post-repha subset (likely faithful print; low priority)
"""
import sys
import collections

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# sanhw2.py san_spc_dicts + PD/BHS/BUR (README "not worthwhile")
SPECIALIZED = {'INM', 'VEI', 'PUI', 'ACC', 'KRM', 'IEG', 'SNP', 'PE', 'PGN', 'MCI',
               'PD', 'BHS', 'BUR'}
CONSONANTS = set('kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSsh')


def parse(line):
    line = line.rstrip('\r\n')
    x = line[:line.index(':')]
    d = line[line.rindex(':') + 1:]
    mid = line[line.index(':') + 1:line.rindex(':')]
    p, _, y = mid.partition('=')
    dicts = [t for t in d.split(',') if t]
    return x, p, y, dicts, line


def has_gemination(y):
    # post-repha doubling: consonant 'r' followed by a doubled consonant (r C C)
    return any(y[i] == 'r' and y[i + 1] == y[i + 2] and y[i + 1] in CONSONANTS
               for i in range(len(y) - 2))


def write(path, recs):
    with open(path, 'w', encoding='utf-8') as f:
        for r in recs:
            f.write(r[4] + '\n')


def main(infile, signal_out, noise_out):
    signal, noise = [], []
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            rec = parse(line)
            if all(code in SPECIALIZED for code in rec[3]):
                noise.append(rec)
            else:
                signal.append(rec)

    signal.sort(key=lambda r: (-len(r[0]), r[0]))
    gem = [r for r in signal if has_gemination(r[2])]
    priority = [r for r in signal if not has_gemination(r[2])]

    def derive(name):
        return signal_out.replace('signal', name) if 'signal' in signal_out else signal_out + '.' + name

    gem_out = derive('gemination')
    priority_out = derive('priority')

    write(signal_out, signal)
    write(noise_out, noise)
    write(gem_out, gem)
    write(priority_out, priority)

    total = len(signal) + len(noise)
    print("total suspects        : %d" % total)
    print("signal (general)      : %d  -> %s" % (len(signal), signal_out))
    print("  priority (non-rcc)  : %d  -> %s   [VERIFY FIRST]" % (len(priority), priority_out))
    print("  gemination (post-r) : %d  -> %s   [likely faithful print, low priority]" % (len(gem), gem_out))
    print("noise (specialized)   : %d  -> %s" % (len(noise), noise_out))
    pats = collections.Counter(r[1] for r in priority)
    print("priority by pattern   : " + ", ".join("%s=%d" % (k, v) for k, v in pats.most_common()))
    print("--- top 12 priority suspects (longest first) ---")
    for r in priority[:12]:
        print("  " + r[4])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
