// Adjudicate an EXPLICIT list of flagged correction candidates.
//
// The companion to verify_netnew_workflow.js. That workflow derives its adjudication batch
// from whichever check batches succeeded in that run, so when a check batch fails and is
// resumed the flag set changes and a row can end up flagged in one run and never ruled in
// any. This takes the rows by name instead, so leftovers are ruled deterministically without
// re-running the checkers.
//
//   { scriptPath: ".../detectors/adjudicate_rows_workflow.js",
//     args: { rows: [{dict, wrong, right, checker_verdict, checker_note, flag_reason}], dir } }
//
// Fable 5 is pinned by ruling D1 (triage adjudication is Fable's).
export const meta = {
  name: 'adjudicate-flagged-rows',
  description: 'Rule PASS/SCAN-FIRST/EDITORIAL/DNF/DROP on an explicit list of flagged correction candidates',
  phases: [{ title: 'Adjudicate', detail: 'Fable: re-read each entry and rule' }],
}

const A = (typeof args === 'string' ? JSON.parse(args) : (args || {}))
const ROWS = A.rows || []
const DIR = A.dir
const ADJ_MODEL = A.adjModel || 'fable'
if (!ROWS.length) throw new Error('adjudicate-flagged-rows: args must include a non-empty {rows}')
if (!DIR) throw new Error('adjudicate-flagged-rows: args must include {dir}')

const SLP1 = 'SLP1: capitals are LONG vowels (A I U); f/F = vocalic r/rr; e/E = e/ai; o/O = o/au; z = retroflex s; S = palatal s; R = retroflex n; w/W = retroflex t/th; M = anusvara.'

const SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    required: ['dict', 'wrong', 'right', 'verdict', 'note'],
    properties: {
      dict: { type: 'string' }, wrong: { type: 'string' }, right: { type: 'string' },
      verdict: { type: 'string', enum: ['PASS', 'SCAN-FIRST', 'EDITORIAL', 'DNF', 'DROP'] },
      note: { type: 'string' },
    } } } } }

phase('Adjudicate')
const AB = 8
const batches = []
for (let i = 0; i < ROWS.length; i += AB) batches.push(ROWS.slice(i, i + AB))

const results = await parallel(batches.map((items, j) => () => {
  const list = items.map((r) =>
    `${r.dict}  ${r.wrong} -> ${r.right}\n   checker verdict: ${r.checker_verdict}\n   checker note: ${r.checker_note}\n   UNSURE BECAUSE: ${r.flag_reason}`).join('\n\n')
  return agent(
    `You are the adjudicating judge for proposed corrections to Cologne Sanskrit dictionaries. A mechanical checker examined each row below against the dictionary's own entry text and FLAGGED it as uncertain. Rule on each one.

Re-read each entry yourself before ruling: Grep tool, pattern "<k1>WRONG<" on the dictionary source at C:/Users/user/Documents/GitHub/csl-orig/v02/<lowercase-dict>/<lowercase-dict>.txt (output_mode "content", -n true), then Read the body to <LEND>. Also grep "<k1>RIGHT<" on the same file for the collision check.

Assign exactly one verdict:

- PASS: file it. The entry's OWN text supports the correction — etymology, inflection,
  cross-reference, gloss, or an exceptionless grammatical rule. A grammar-exceptionless rule
  COUNTS as evidence.
- SCAN-FIRST: file it, marked "the scan is decisive". Grammar-certain but the entry is
  internally SILENT on the spelling.
- EDITORIAL: the \`right\` spelling ALREADY EXISTS as its own <k1> entry (respelling would
  duplicate a headword), or apparatus would be clobbered.
- DNF: do-not-file — a real distinct word, a documented variant, or a notational convention.
- DROP: stale; the entry no longer reads as the triage saw it.

Decisive question for a row where the dictionary spells the form CONSISTENTLY across k1, k2
and the body: consistency is evidence of a HOUSE CONVENTION or of a systematic scan defect,
NOT of a one-off typo — and the two are distinguished by whether the spelling is defensible
Sanskrit. If the consistently-used form is a legitimate attested variant, that is DNF. If it
is not a possible form at all (violating an exceptionless rule) then consistency means the
defect is systematic, and the row is still fileable — but say which you concluded and why.

Process cautions carried from the July-2026 pass:
1. NEVER string-match the evidence. READ the entry.
2. Unicode trap: worklist ° (U+00B0) vs source ˚ (U+02DA) — never compare literally.
3. A \`k2\` that merely mirrors \`k1\` is NOT independent counter-evidence.
4. Morphological certainty is real evidence. This checker OVER-flags where the evidence is
   morphological rather than literal, and in the previous pass never once found a reversed
   pair the triage had missed — so expect to restore some to PASS. Do not rubber-stamp: a
   wrong PASS here edits a dictionary.
${SLP1}

Rows to adjudicate:

${list}

Write a JSON array (and nothing else) to:
  ${DIR}/verify_adj_extra_${String(j).padStart(3, '0')}.json
each {"dict":"..","wrong":"..","right":"..","verdict":"..","note":"<=240 chars quoting the entry text you read and giving the ruling"}
Then return the same verdicts as structured output.`,
    { label: `adj-extra:${String(j).padStart(3, '0')}`, phase: 'Adjudicate', schema: SCHEMA, model: ADJ_MODEL }
  )
}))

const verdicts = results.filter(Boolean).flatMap((r) => r.verdicts)
const failed = results.filter((r) => !r).length
return { rowsIn: ROWS.length, ruled: verdicts.length, batchesFailed: failed, verdicts }
