"""gen_vidyut_stems.py  (Python 3)  -- Phase 3.2: build the vidyut stem inventory

Extract the pratipadika (nominal stem) inventory from the vidyut kosha and write it as
a plain SLP1 stem list, so the detectors get a morphological-validity oracle WITHOUT a
runtime dependency on vidyut (mirrors how dcs_lemma_summary.json is vendored).

Run once where vidyut + its kosha data are available:
  python gen_vidyut_stems.py [kosha_dir=../../WhitneyRoots/scratch/vidyut_data/kosha] [out=vidyut_stems.txt]

Attribution: stems derived from vidyut (Arun Prasad / ambuda-org, MIT;
https://github.com/ambuda-org/vidyut) and its linguistic data.
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')


def main(kpath, out):
    from vidyut.kosha import Kosha
    k = Kosha(kpath)
    lemmas = sorted({p.lemma for p in k.pratipadikas() if getattr(p, 'lemma', None)})
    with open(out, 'w', encoding='utf-8') as f:
        for lem in lemmas:
            f.write(lem + '\n')
    print("%d distinct pratipadika stems -> %s" % (len(lemmas), out))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    here = os.path.dirname(os.path.abspath(__file__))
    kpath = args[0] if args else os.path.join(here, '..', '..', 'WhitneyRoots', 'scratch', 'vidyut_data', 'kosha')
    out = args[1] if len(args) > 1 else os.path.join(here, 'vidyut_stems.txt')
    if not os.path.isdir(kpath):
        print("kosha data not found at %s -- install vidyut data or pass the path" % kpath)
        sys.exit(1)
    main(kpath, out)
