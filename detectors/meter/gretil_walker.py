"""gretil_walker.py  (Python 3) -- H251 build task 1: GRETIL kavya verse extractor

Parses the mass-converted "corpustei/transformations/plaintext" GRETIL files
(vendored locally under detectors/gretil_kavya_raw/, see
detectors/meter/README.md for the corpus-fetch step) into a flat list of verse
records: {file, locus, lines, full_text}.

Format observed across the 57-file Kavya section (checked 06-07-2026):
  - A header block, ending at a line that is exactly "# Text".
  - Verses are blank-line-separated paragraphs. Each paragraph is 1-2+ physical
    lines of running IAST text, optionally containing pada-boundary markers
    ("/", "//") and ending with a locus tag -- either bare (`KMgD_1`) or
    bracketed (`// valc_1.1 //`). Page-break markers `[[001]]` appear inline
    and are stripped.
  - Markup is NOT fully uniform (some texts mark padas with "/", others don't
    at all and rely on the tool's own resplit heuristics) -- this walker does
    not assume "/" is present; it hands whole verse text to skrutable (which
    resplits on its own) and hands physical printed lines to chanda (which
    resolves multi-pada lines itself), per the pilot's validated method
    (CHANDAS_ANUPRASA_PRIOR_ART.md #4).
"""
import os
import re
import glob

LOCUS_RE = re.compile(r'([A-Za-z][A-Za-z0-9]*_[0-9]+(?:[.,][0-9]+)*)')
PAGE_MARK_RE = re.compile(r'\[\[[^\]]*\]\]')

# A handful of "Kavya"-section texts are PROSE (campU / prose-romance, e.g.
# Dandin's Dasakumaracarita), not verse -- their locus-tagged paragraphs run
# to thousands of characters and both (a) produce meaningless meter verdicts
# (there is no meter to find) and (b) send skrutable's resplit_lite pAda-
# boundary search into a hang (observed 06-07-2026: a 19301-char "verse" in
# dazakumAracarita). The 99th percentile of ~26k genuinely-verse blocks in
# this corpus is 359 chars (even long meters like sragdharA/sardulavikridita
# stay well under this); blocks beyond MAX_VERSE_CHARS are prose and are
# skipped (counted, not silently dropped -- see walk_corpus's skip log).
MAX_VERSE_CHARS = 500


def _strip_page_marks(line):
    return PAGE_MARK_RE.sub(' ', line).strip()


def iter_blocks(path):
    """Yield (raw_lines) for each blank-line-separated paragraph in the '# Text'
    section of one GRETIL plaintext file."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == '# Text') + 1
    except StopIteration:
        start = 0
    block = []
    for raw in lines[start:]:
        line = _strip_page_marks(raw.rstrip('\n'))
        if not line:
            if block:
                yield block
                block = []
            continue
        block.append(line)
    if block:
        yield block


def parse_file(path):
    """Return a list of verse dicts for one GRETIL plaintext file.

    A block with no discoverable locus tag is skipped (front-matter stragglers,
    colophons without a citation) -- counted by the caller, not silently
    dropped from the log.
    """
    fname = os.path.splitext(os.path.basename(path))[0]
    verses = []
    skipped = 0
    skipped_prose = 0
    for block in iter_blocks(path):
        joined = ' '.join(block)
        m = None
        for cand in reversed(LOCUS_RE.findall(joined)):
            m = cand
        if not m:
            skipped += 1
            continue
        if len(joined) > MAX_VERSE_CHARS:
            skipped_prose += 1
            continue
        # strip the locus tag (and any surrounding // ... //) from the text
        text = LOCUS_RE.sub('', joined)
        text = text.replace('//', ' ').replace('/', ' / ')
        text = re.sub(r'\s+', ' ', text).strip(' /')
        lines_clean = [LOCUS_RE.sub(' ', re.sub(r'//?', ' ', l)) for l in block]
        lines_clean = [re.sub(r'\s+', ' ', l).strip() for l in lines_clean]
        verses.append({
            'file': fname,
            'locus': m,
            'lines': [l for l in lines_clean if l],
            'full_text': text,
        })
    return verses, skipped, skipped_prose


def walk_corpus(corpus_dir):
    """Yield (verse_dict) across every *.txt in corpus_dir, logging per-file
    skip counts to stderr (no silent caps)."""
    import sys
    total_v = total_skip = total_prose = 0
    for path in sorted(glob.glob(os.path.join(corpus_dir, '*.txt'))):
        verses, skipped, skipped_prose = parse_file(path)
        total_v += len(verses)
        total_skip += skipped
        total_prose += skipped_prose
        if skipped_prose:
            sys.stderr.write("gretil_walker: %s -- %d blocks over %d chars skipped as prose\n"
                              % (os.path.basename(path), skipped_prose, MAX_VERSE_CHARS))
        for v in verses:
            yield v
    sys.stderr.write("gretil_walker: %d verses parsed, %d blocks skipped (no locus tag), "
                      "%d blocks skipped (prose, >%d chars)\n"
                      % (total_v, total_skip, total_prose, MAX_VERSE_CHARS))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    here = os.path.dirname(os.path.abspath(__file__))
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'gretil_kavya_raw')
    n = 0
    for v in walk_corpus(d):
        n += 1
        if n <= 5:
            print(v['file'], v['locus'], '|', v['lines'])
    print("total verses:", n)
