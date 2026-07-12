"""irr_cross_family.py  (Python 3)  -- H825 step 1 (ruling D9): cross-family blind
second annotation for the IRR sample, via a non-Anthropic judge (DeepSeek/any
OpenAI-compatible endpoint by default).

Why: A44's existing IRR (corrections_draft/irr/second_annotations.tsv) uses Opus 4.8
as annotator B against Sonnet-derived verdicts (annotator A) -- both Anthropic, the
self-enhancement-bias confound the LLM-as-judge literature flags (Zheng MT-Bench
2306.05685; Self-Preference Bias 2410.21819). This script re-runs the SAME blind
5-way classification (PASS / SCAN-FIRST / EDITORIAL / DNF / DROP) over the SAME
122-row evidence-only input (corrections_draft/irr/irr_inputs.tsv) with a
different-family judge, so detectors/irr_agreement.py can report a cross-family
kappa alongside the existing within-family one.

Blind: the model sees ONLY the (dict, wrong, right, wrong_entry_text,
right_entry_text) columns of irr_inputs.tsv -- no verdicts, no notes, no
information about which pass (A/B) produced anything, and no knowledge that this is
a "second opinion" (anchoring/position control, same as the original H453 design).

Backend config (env, same convention as CommentaryStrategies/scripts/annotate_batch.py
-- reuse over reinvent, see [[feedback-no-anthropic-key-use-deepseek]]):
  LLM_API_KEY   (or OPENAI_API_KEY)  -- required
  LLM_BASE_URL  -- e.g. https://api.deepseek.com  (omit for api.openai.com)
  LLM_MODEL     -- e.g. deepseek-chat             (or pass --model)

Output: corrections_draft/irr/cross_family_annotations.tsv
        row_id \t c_label \t c_reason   (same shape as second_annotations.tsv's
        a2_label/a2_reason, so irr_agreement.py can consume both uniformly)

Usage:
    export LLM_API_KEY=...
    export LLM_BASE_URL=https://api.deepseek.com
    export LLM_MODEL=deepseek-chat
    python detectors/irr_cross_family.py --limit 5      # smoke test
    python detectors/irr_cross_family.py                # full 122-row run

    python detectors/irr_cross_family.py --dry-run       # no API call, no key needed
"""
import sys
import os
import re
import json
import time
import argparse

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IRR_DIR = os.path.join(ROOT, 'corrections_draft', 'irr')
INPUTS = os.path.join(IRR_DIR, 'irr_inputs.tsv')
OUTPUT = os.path.join(IRR_DIR, 'cross_family_annotations.tsv')

LABELS = ['PASS', 'SCAN-FIRST', 'EDITORIAL', 'DNF', 'DROP']

SYSTEM_PROMPT = """You are verifying a proposed spelling correction in a Sanskrit \
dictionary (Cologne Digital Sanskrit Dictionaries corpus, SLP1 transliteration) \
against that dictionary's OWN entry text. You are told a headword ("wrong") and a \
proposed corrected spelling ("right"), plus the entry text found under each \
spelling (if any exists at all -- one side is often "[no separate entry under this \
headword]").

Judge ONLY from the entry text evidence given below -- do not use outside \
knowledge of what the "correct" Sanskrit spelling should be beyond what the entry \
itself states (etymology, cross-references, inflected forms, glosses).

Classify into exactly one of these five labels:
  PASS        -- entry evidence (etymology, inflection, cross-reference, or \
                 quoted citation) directly supports treating "wrong" as a \
                 typo of "right"; a plain in-place correction is warranted.
  SCAN-FIRST  -- grammatically/etymologically plausible but the entry text \
                 itself is silent or too terse to decide; only the original \
                 printed page (scan) can settle it.
  EDITORIAL   -- both "wrong" and "right" (or a close variant) already exist as \
                 SEPARATE, independently attested/cited headwords -- this is a \
                 duplicate-pair / apparatus-collision decision (merge vs respell \
                 vs leave both), not a plain correction.
  DNF         -- do-not-file: entry evidence suggests "wrong" is a deliberate, \
                 intentional spelling (e.g. a technical grammatical notation, an \
                 editorial convention, or an attested variant), not an error.
  DROP        -- the correction is stale: "right" already exists as its own \
                 correctly-spelled entry, i.e. this has already been fixed \
                 upstream.

Reply with ONLY a JSON object: {"label": "<one of the five>", "reason": "<one \
sentence citing the specific entry evidence you used>"}. No other text.
"""


class OpenAIBackend:
    name = "openai"

    def __init__(self):
        try:
            import openai
        except ImportError:
            print("ERROR: openai package not installed. Run: pip install openai")
            sys.exit(1)
        self._sdk = openai
        api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("LLM_BASE_URL") or None
        if not api_key:
            print("ERROR: no API key. Set LLM_API_KEY (or OPENAI_API_KEY); for "
                  "non-OpenAI providers also set LLM_BASE_URL (e.g. DeepSeek: "
                  "https://api.deepseek.com). Never use ANTHROPIC_API_KEY here -- "
                  "the whole point is a non-Anthropic judge (ruling D9).")
            sys.exit(2)
        self.base_url = base_url or "https://api.openai.com/v1"
        self.client = (openai.OpenAI(api_key=api_key, base_url=base_url)
                       if base_url else openai.OpenAI(api_key=api_key))

    def complete(self, system_prompt, user_content, model):
        resp = self.client.chat.completions.create(
            model=model,
            max_tokens=300,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        return (resp.choices[0].message.content or "").strip()

    def preflight(self, model):
        o = self._sdk
        try:
            self.client.chat.completions.create(
                model=model, max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
            return None
        except o.AuthenticationError:
            return f"API key rejected (401) at {self.base_url}."
        except o.NotFoundError:
            return f"model {model!r} not found at {self.base_url}. Set --model / $LLM_MODEL."
        except o.APIError as e:
            print(f"WARNING: preflight inconclusive ({type(e).__name__}: {e}); proceeding.")
            return None
        except Exception as e:
            print(f"WARNING: preflight could not run ({type(e).__name__}: {e}); proceeding.")
            return None

    def is_fatal(self, exc):
        return isinstance(exc, (self._sdk.AuthenticationError, self._sdk.PermissionDeniedError))


def read_inputs():
    rows = []
    with open(INPUTS, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if p[0] == 'row_id':
                continue
            row_id, dictc, wrong, right, wrong_entry, right_entry = (p + [''] * 6)[:6]
            rows.append({'row_id': row_id, 'dict': dictc, 'wrong': wrong, 'right': right,
                         'wrong_entry_text': wrong_entry, 'right_entry_text': right_entry})
    return rows


def classify(backend, row, model):
    user_content = (
        "dict: %s\nwrong: %s\nright: %s\n\n"
        "entry text under \"wrong\":\n%s\n\n"
        "entry text under \"right\":\n%s\n"
    ) % (row['dict'], row['wrong'], row['right'],
         row['wrong_entry_text'], row['right_entry_text'])
    text = backend.complete(SYSTEM_PROMPT, user_content, model)
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if not m:
        raise ValueError("no JSON in reply: %s" % text[:200])
    obj = json.loads(m.group())
    label = obj.get('label', '').strip().upper()
    if label not in LABELS:
        raise ValueError("invalid label %r" % label)
    return label, obj.get('reason', '').strip()


def load_existing():
    done = {}
    if not os.path.exists(OUTPUT):
        return done
    with open(OUTPUT, encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if p[0] == 'row_id':
                continue
            done[p[0]] = (p[1], p[2] if len(p) > 2 else '')
    return done


def write_output(rows, results, backend_name, model):
    os.makedirs(IRR_DIR, exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# H825 cross-family blind second annotation (ruling D9). '
                'Annotator C = %s/%s, non-Anthropic judge.\n' % (backend_name, model))
        f.write('# Evidence = irr_inputs.tsv rows only (dict, wrong, right, '
                'wrong_entry_text, right_entry_text) -- NO access to annotator A/B\n'
                '# verdicts, notes, or the fact this is a re-annotation. Same five-way\n'
                '# taxonomy as file_first_verified.tsv / second_annotations.tsv:\n'
                '# PASS | SCAN-FIRST | EDITORIAL | DNF | DROP.\n')
        f.write('row_id\tc_label\tc_reason\n')
        for r in rows:
            if r['row_id'] not in results:
                continue
            label, reason = results[r['row_id']]
            f.write('%s\t%s\t%s\n' % (r['row_id'], label, reason.replace('\t', ' ').replace('\n', ' ')))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--backend', default=os.environ.get('LLM_BACKEND', 'openai'),
                     choices=['openai'])
    ap.add_argument('--model', default=os.environ.get('LLM_MODEL'))
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--sleep', type=float, default=0.3)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    rows = read_inputs()
    if args.limit:
        rows = rows[:args.limit]
    print("Loaded %d rows from %s" % (len(rows), INPUTS))

    if args.dry_run:
        print("[DRY RUN] backend=%s model=%s -- would classify %d rows (no API call)."
              % (args.backend, args.model, len(rows)))
        for r in rows[:3]:
            print("  [%s] %s -> %s" % (r['row_id'], r['wrong'], r['right']))
        return

    model = args.model
    if not model:
        print("ERROR: no model. Pass --model or set $LLM_MODEL (e.g. deepseek-chat).")
        sys.exit(1)

    backend = OpenAIBackend()
    print("Backend: %s   model: %s   base_url: %s" % (args.backend, model, backend.base_url))
    err = backend.preflight(model)
    if err:
        print("ERROR: %s" % err)
        sys.exit(2)

    done = load_existing()
    results = dict(done)
    errors = 0
    for i, r in enumerate(rows, 1):
        if r['row_id'] in done:
            continue
        print("  [%d/%d] row %s (%s -> %s)..." % (i, len(rows), r['row_id'], r['wrong'], r['right']),
              end=' ', flush=True)
        try:
            label, reason = classify(backend, r, model)
            results[r['row_id']] = (label, reason)
            print(label)
        except Exception as e:
            if backend.is_fatal(e):
                print("\nFATAL: %s: %s" % (type(e).__name__, e))
                print("Aborting -- fix credentials/permissions, then re-run (resumable).")
                break
            errors += 1
            print("ERROR: %s" % e)
        if results and i % 20 == 0:
            write_output(rows, results, args.backend, model)
        time.sleep(args.sleep)

    if results:
        write_output(rows, results, args.backend, model)
        print("\nComplete: %d/%d rows classified, %d errors -> %s"
              % (len(results), len(rows), errors, OUTPUT))
    else:
        print("\nNo rows classified (%d errors); output file not written." % errors)


if __name__ == '__main__':
    main()
