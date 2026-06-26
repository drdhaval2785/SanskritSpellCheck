"""ocr_verify.py  (Python 3)  -- Phase 2.1: OCR-assisted pre-verification

For each candidate (DICT:wrong:right), fetch the Cologne scanned page, get its text
(embedded PDF text layer if present, else OCR), and compare to the suspect vs the
suggested spelling to pre-label the candidate:

  CONFIRM    the print shows the SUGGESTED form -> the digital headword is a typo
  DENY       the print shows the CURRENT (suspect) form -> digital is faithful, not an error
  UNCERTAIN  neither found clearly (the common case on noisy old scans)

This is a TRIAGE PRIOR, never a verdict (OCR of old Devanagari scans is unreliable) --
it reorders the human review queue; a human still confirms against the scan.

Pipeline (all runnable here except OCR): servepdf.php -> parse the <object> PDF URL ->
fetch the page PDF -> pymupdf text/render. OCR uses tesseract + a Devanagari model
(`san`/`hin`) if present, else falls back to **easyocr** (`pip install easyocr`, neural
Devanagari, no system binary / admin needed); with neither, the page image is cached as a
review aid and the label is MANUAL. Polite: results are cached and fetches are rate-limited
-- run on small batches (e.g. a tier-A sample), not the whole corpus. (The Cologne servepdf
endpoint IP-throttles aggressively: a 429 burst means back off for a while, don't hammer it.)

  python ocr_verify.py [candidates=combined_sf.txt] [n=5] [--lang san]
"""
import sys
import os
import re
import io
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slp1util as u

u.reconfigure_stdio()
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'ocrcache')
SERVEPDF = "https://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=%s&key=%s"
UA = {'User-Agent': 'SanskritSpellCheck-ocr-verify/1.0 (research; gasyoun@gmail.com)'}
RATE_S = 3.0   # be polite -- the Cologne server returns 429 if hammered
LANG = 'san'

try:
    import pytesseract
    pytesseract.get_tesseract_version()
    OCR_OK = True
except Exception:
    OCR_OK = False

# Fallback OCR backend -- easyocr's neural Devanagari model needs NO system binary or admin
# (tesseract install is admin-gated on some machines). Used only when tesseract is absent.
try:
    import easyocr  # noqa: F401
    EASYOCR_OK = True
except Exception:
    EASYOCR_OK = False
_easyocr_reader = [None]


def easyocr_text(png_bytes):
    if _easyocr_reader[0] is None:
        import easyocr
        _easyocr_reader[0] = easyocr.Reader(['hi'], gpu=False, verbose=False)   # Devanagari script
    return ' '.join(_easyocr_reader[0].readtext(png_bytes, detail=0, paragraph=True))


_last_fetch = [0.0]


def http_get(url, tries=3):
    """Cached (disk), rate-limited and retrying GET. Cache-read spares the server on
    re-runs; the throttle bounds the REAL request rate (every network hit, not just
    once per candidate); retries cover 429 and transient connection/timeout errors."""
    os.makedirs(CACHE, exist_ok=True)
    cache = os.path.join(CACHE, 'net_' + hashlib.md5(url.encode('utf-8')).hexdigest())
    if os.path.exists(cache):
        with open(cache, 'rb') as f:
            return f.read()
    for k in range(tries):
        try:
            wait = RATE_S - (time.time() - _last_fetch[0])
            if wait > 0:
                time.sleep(wait)
            _last_fetch[0] = time.time()
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
            with open(cache, 'wb') as f:
                f.write(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and k < tries - 1:
                time.sleep(5 * (k + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if k < tries - 1:
                time.sleep(2 * (k + 1))
                continue
            raise


def resolve_scan_url(dictcode, key):
    """The scan URL from servepdf's HTML -- either <object data='...'> (PDF dicts) or
    <img src='...'> (jpg/png dicts: WIL, MD, CCS, PWKVN, FRI)."""
    html = http_get(SERVEPDF % (dictcode, urllib.parse.quote(key))).decode('utf-8', 'replace')
    m = re.search(r"""(?:data|src)=['"]([^'"]+\.(?:pdf|jpe?g|png))['"]""", html, re.I)
    if not m:
        return None
    url = m.group(1)
    return ('https:' + url) if url.startswith('//') else url


def page_slp1(url, pngpath):
    """Fetch the scan (PDF or image) and return (source, slp1_text). source in
    {pdftext, ocr, image}. Caches the page PNG as a review aid."""
    data = http_get(url)
    if url.lower().endswith('.pdf'):
        import fitz
        pg = fitz.open(stream=data, filetype='pdf').load_page(0)
        txt = pg.get_text().strip()
        if txt:
            return 'pdftext', u.devanagari_to_slp1(txt)
        png = pg.get_pixmap(dpi=200).tobytes('png')
    else:
        png = data   # already a raster scan (jpg/png)
    with open(pngpath, 'wb') as f:
        f.write(png)
    if OCR_OK:
        from PIL import Image
        raw = pytesseract.image_to_string(Image.open(io.BytesIO(png)), lang=LANG)
        return 'ocr', u.devanagari_to_slp1(raw)
    if EASYOCR_OK:
        return 'easyocr', u.devanagari_to_slp1(easyocr_text(png))
    return 'image', ''


def _min_dist(tokens, word):
    return min((u.edit_distance(t, word, 2) for t in tokens), default=99)


def verify(page, suspect, suggestion):
    """Decide by which form a page token is CLOSER to -- suspect and suggestion are
    one confusion edit apart, so a plain fuzzy match would hit both; the closest-match
    rule distinguishes them while tolerating one OCR slip on the winning form."""
    toks = page.split()
    dsp, dsg = _min_dist(toks, suspect), _min_dist(toks, suggestion)
    if dsg < dsp and dsg <= 1:
        return 'CONFIRM'     # print is closer to the suggested (corrected) form
    if dsp < dsg and dsp <= 1:
        return 'DENY'        # print is closer to the current (suspect) form -> faithful
    return 'UNCERTAIN'


def main(infile, n):
    os.makedirs(CACHE, exist_ok=True)
    cands = []
    for line in u._read_words(infile):
        p = line.split(':')
        if len(p) >= 3 and p[1] != p[2]:
            cands.append((p[0], p[1], p[2]))
        if len(cands) >= n:
            break
    engine = ('tesseract:' + LANG if OCR_OK else 'easyocr:Devanagari' if EASYOCR_OK
              else 'NONE -> scan-prefetch aid only')
    print("OCR engine: %s; processing %d candidates (rate-limited %.1fs)" % (engine, len(cands), RATE_S))
    out = open(os.path.join(HERE, 'ocr_verify_report.txt'), 'w', encoding='utf-8')
    labels = {}
    for i, (dictc, wrong, right) in enumerate(cands):
        png = os.path.join(CACHE, "%s_%s.png" % (dictc, re.sub(r'[^A-Za-z0-9]', '_', wrong)))
        try:
            url = resolve_scan_url(dictc, wrong)   # http_get throttles+caches internally
            if not url:
                label, src = 'NO-SCAN', '-'
            else:
                src, page = page_slp1(url, png)
                label = verify(page, wrong, right) if src != 'image' else 'MANUAL'
        except Exception as e:
            label, src = 'ERROR', repr(e)[:60]
        labels[label] = labels.get(label, 0) + 1
        img = png if os.path.exists(png) else '-'
        out.write("%s\t%s -> %s\t%s\t%s\t%s\n" % (label, wrong, right, dictc, src, img))
    out.close()
    print("labels: " + ", ".join("%s=%d" % kv for kv in sorted(labels.items())))
    print("-> ocr_verify_report.txt  (scan images cached in ocrcache/)")
    if not OCR_OK and not EASYOCR_OK:
        print("install tesseract + a Devanagari model (san/hin), or `pip install easyocr`, "
              "to enable auto CONFIRM/DENY.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--lang' in sys.argv:
        LANG = sys.argv[sys.argv.index('--lang') + 1]
    infile = args[0] if args else "combined_sf.txt"
    n = int(args[1]) if len(args) > 1 else 5
    if not os.path.exists(infile):
        print("input %s not found (run run_all.py, or pass a DICT:wrong:right file)" % infile)
        sys.exit(1)
    main(infile, n)
