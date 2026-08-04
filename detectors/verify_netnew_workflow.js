// Verification workflow for net-new FILE-FIRST candidates -- the union-pass twin of the
// July-2026 pass that produced corrections_draft/file_first_verified.tsv.
//
// The scan-verification sheet (gen_scanverify_sheet.py) is generated from
// file_first_verified.tsv, which holds only the RUN-1 population. Candidates found by the
// union-across-runs passes (D7/union_d7.tsv, D9/union_d9.tsv) carry Opus confirm + Opus
// review verdicts but NO verification verdict, so the human gate cannot see them. This
// assigns that verdict.
//
// Invoke via the Workflow tool with:
//   { scriptPath: ".../detectors/verify_netnew_workflow.js",
//     args: { dir } }        // dir = corrections_draft/verify_work (from build_verify_batches.py)
//
// Model split follows ruling D1 and the July pass: Sonnet 5 checks mechanically against the
// entry text; Fable 5 adjudicates every flag. The checker never issues a final verdict on a
// row it flags -- adjudication does, because the July pass measured the checkers
// over-flagging where the evidence is MORPHOLOGICAL rather than literal (satva/natva-certain
// forms restored to PASS by the judge) while never missing a reversed pair.
export const meta = {
  name: 'verify-netnew-filefirst',
  description: 'Verify net-new FILE-FIRST candidates against their entry text and assign PASS/SCAN-FIRST/EDITORIAL/DNF/DROP',
  phases: [
    { title: 'Discover', detail: 'list the verify_batch files on disk' },
    { title: 'Check', detail: 'Sonnet: locate the entry, quote evidence, check direction + collision + staleness' },
    { title: 'Adjudicate', detail: 'Fable: rule on every flagged row (D1 pins triage adjudication)' },
  ],
}

const A = (typeof args === 'string' ? JSON.parse(args) : (args || {}))
const DIR = A.dir
if (!DIR) throw new Error('verify-netnew: args must include {dir}')
const CHK_MODEL = A.chkModel || 'sonnet'
const ADJ_MODEL = A.adjModel || 'fable'

const SLP1 = 'SLP1: capitals are LONG vowels (A I U); f/F = vocalic r/rr; e/E = e/ai; o/O = o/au; z = retroflex s; S = palatal s; R = retroflex n; w/W = retroflex t/th; M = anusvara.'

const VERDICTS = ['PASS', 'SCAN-FIRST', 'EDITORIAL', 'DNF', 'DROP']

const CHK_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    required: ['dict', 'wrong', 'right', 'verdict', 'note', 'flag', 'flag_reason'],
    properties: {
      dict: { type: 'string' }, wrong: { type: 'string' }, right: { type: 'string' },
      verdict: { type: 'string', enum: VERDICTS },
      note: { type: 'string' },
      flag: { type: 'boolean' },
      flag_reason: { type: 'string' },
    } } } } }

const ADJ_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    required: ['dict', 'wrong', 'right', 'verdict', 'note'],
    properties: {
      dict: { type: 'string' }, wrong: { type: 'string' }, right: { type: 'string' },
      verdict: { type: 'string', enum: VERDICTS },
      note: { type: 'string' },
    } } } } }

const DISC_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['files'],
  properties: { files: { type: 'array', items: { type: 'string' } } } }

// The verdict vocabulary, verbatim from file_first_verified.tsv's own header.
const RUBRIC = `Assign exactly one verdict per row:

- PASS: file it. The entry's OWN text supports the correction — etymology, inflection,
  cross-reference, gloss, or an exceptionless grammatical rule (satva/natva, vrddhi vowel
  length, gender/stem agreement). A grammar-exceptionless rule COUNTS as evidence.
- SCAN-FIRST: file it, but marked "the scan is decisive". The correction is grammar-certain
  yet the entry is internally SILENT — no etymology, no inflection, no cross-reference that
  bears on the spelling. Use this rather than PASS when your only ground is outside the entry.
- EDITORIAL: NOT a plain correction. The \`right\` spelling ALREADY EXISTS as its own <k1>
  entry in this dictionary (respelling would create a duplicate headword), or the entry
  carries apparatus that a silent respell would clobber (errata note, "Idem" cross-listing,
  a constructed/starred form). The editor chooses merge vs respell vs leave.
- DNF: do-not-file. The suspect is a real distinct word, a documented variant, or a
  notational convention (e.g. Dhatupatha nopadesa root notation) — the triage was wrong.
- DROP: stale. The entry no longer reads as the triage saw it — already fixed upstream.`

const CAUTIONS = `Process cautions carried from the July-2026 pass — these caused real errors:

1. NEVER string-match the evidence. READ the entry body. Naive substring matching produced
   ~33 spurious flags across two agents in the previous pass.
2. Unicode trap: the degree sign differs between worklist (U+00B0 °) and source (U+02DA ˚).
   Never compare them literally.
3. A \`k2\` field that merely mirrors \`k1\` is NOT independent counter-evidence.
4. Morphological certainty is real evidence, not a reason to doubt. If satva/natva, vrddhi
   vowel length, or gender/stem agreement makes the correction exceptionless, that is PASS
   (or SCAN-FIRST if the entry itself says nothing) — do not flag it merely for being
   grammatical rather than literal.`

function idxOf(fn) { const m = fn.match(/(\d+)/); return m ? m[1] : '000' }

phase('Discover')
const disc = await agent(
  `List every file matching verify_batch_*.jsonl in the directory:\n  ${DIR}\nUse the Glob tool (pattern "verify_batch_*.jsonl", path "${DIR}"), or Bash ls. Return {"files":[...]} with ONLY the base filenames, sorted ascending.`,
  { label: 'discover', phase: 'Discover', schema: DISC_SCHEMA, model: CHK_MODEL })
const files = ((disc && disc.files) || []).filter((f) => /verify_batch_\d+\.jsonl/.test(f)).sort()
if (!files.length) throw new Error('no verify_batch_*.jsonl files found in ' + DIR)
log(`discovered ${files.length} batch files`)

phase('Check')
const chkResults = await parallel(files.map((fn) => () =>
  agent(
    `You are verifying proposed spelling corrections to a Cologne Sanskrit dictionary BEFORE they are filed. Each row was already judged a probable typo by two prior passes; your job is the independent pre-filing gate.

STEP 1 — read your batch with the Read tool:
  ${DIR}/${fn}
Each line (ignore the line-number gutter) is JSON: {pass, dict, wrong, right, opus_confirm_reason, opus_review_reason, src}. \`src\` is the dictionary source file. \`wrong\` is the current headword; \`right\` is the proposed correction. The two opus_* fields are the PRIOR passes' reasoning — useful context, but you must verify independently, not restate them.

STEP 2 — for EVERY row, do all four checks against the source file \`src\`:

  (a) LOCATE. Grep tool, pattern "<k1>WRONG<" on \`src\` (output_mode "content", -n true), then
      Read the entry body that follows, up to <LEND>. If the entry is absent -> DROP.
  (b) EVIDENCE. Quote the exact text bearing on the spelling — etymology (E. / vyutpatti),
      inflection, gloss, cross-reference. This quote goes in \`note\`.
  (c) DIRECTION. Does the evidence support \`right\` over \`wrong\`? If the entry actually
      defines \`wrong\` as its own word, or documents the spelling on purpose -> DNF.
  (d) COLLISION. Grep "<k1>RIGHT<" on the SAME \`src\`. If \`right\` already exists as its own
      entry, respelling would create a duplicate headword -> EDITORIAL. Also EDITORIAL if the
      entry carries apparatus (errata, "Idem" cross-listing, a starred/constructed form) that
      a silent respell would clobber.

${RUBRIC}

${CAUTIONS}
${SLP1}

STEP 3 — set \`flag\` = true for any row where you are NOT confident, where the checks
disagree with each other, or where the prior passes' reasoning conflicts with what you read.
A flagged row goes to a stronger judge, so flagging is cheap and guessing is not. Still record
your best-guess \`verdict\`, and put WHY you are unsure in \`flag_reason\` (empty string if not flagged).
\`note\`: <=240 chars, lead with the quoted entry text you actually read.

STEP 4 — write your verdicts as a JSON array (and nothing else) to:
  ${DIR}/verify_chk_${idxOf(fn)}.json
one element per input row, same order. Then return the same verdicts as structured output.`,
    { label: `chk:${idxOf(fn)}`, phase: 'Check', schema: CHK_SCHEMA, model: CHK_MODEL }
  )
))
const allChk = chkResults.filter(Boolean).flatMap((r) => r.verdicts)
const chkFailed = chkResults.filter((r) => !r).length
const flagged = allChk.filter((v) => v.flag)
log(`checked ${allChk.length} row(s) across ${files.length - chkFailed}/${files.length} batches; flagged ${flagged.length}`)
if (chkFailed) log(`WARNING: ${chkFailed} check batch(es) FAILED — the counts above are a lower bound, not a total`)

// --- Adjudicate: Fable-pinned (ruling D1) judgment over every flagged row.
let adjudicated = []
if (flagged.length) {
  phase('Adjudicate')
  const AB = 8
  const ab = []
  for (let i = 0; i < flagged.length; i += AB) ab.push(flagged.slice(i, i + AB))
  const adjResults = await parallel(ab.map((items, j) => () => {
    const list = items.map((v) =>
      `${v.dict}  ${v.wrong} -> ${v.right}\n   checker verdict: ${v.verdict}\n   checker note: ${v.note}\n   UNSURE BECAUSE: ${v.flag_reason}`).join('\n\n')
    return agent(
      `You are the adjudicating judge for proposed corrections to Cologne Sanskrit dictionaries. A mechanical checker examined each row below against the dictionary's own entry text and FLAGGED it as uncertain. Rule on each one.

Re-read each entry yourself before ruling: Grep tool, pattern "<k1>WRONG<" on the dictionary source, then Read the body to <LEND>. Sources are under C:/Users/user/Documents/GitHub/csl-orig/v02/<lowercase-dict>/<lowercase-dict>.txt.

${RUBRIC}

${CAUTIONS}
${SLP1}

The previous pass measured this checker's failure mode precisely: it OVER-flags where the
evidence is morphological rather than literal (satva/natva-certain forms, vrddhi vowel length,
gender/stem agreement were all wrongly flagged and correctly restored to PASS by the judge),
and it did NOT once find a reversed pair the triage had missed. So expect to restore several
of these to PASS. But do NOT rubber-stamp: the checker's collision finds (EDITORIAL) and
genuine real-word finds (DNF) are exactly the cases worth keeping, and a wrong PASS here
edits a dictionary.

Rows to adjudicate:

${list}

Write a JSON array (and nothing else) to:
  ${DIR}/verify_adj_${String(j).padStart(3, '0')}.json
each {"dict":"..","wrong":"..","right":"..","verdict":"PASS|SCAN-FIRST|EDITORIAL|DNF|DROP","note":"<=240 chars quoting the entry text you read and giving the ruling"}
Then return the same verdicts as structured output.`,
      { label: `adj:${String(j).padStart(3, '0')}`, phase: 'Adjudicate', schema: ADJ_SCHEMA, model: ADJ_MODEL }
    )
  }))
  adjudicated = adjResults.filter(Boolean).flatMap((r) => r.verdicts)
  const adjFailed = adjResults.filter((r) => !r).length
  if (adjFailed) log(`WARNING: ${adjFailed} adjudication batch(es) FAILED — ${flagged.length - adjudicated.length} flagged row(s) have NO ruling`)
}

// Final verdict per row: the judge's ruling wins wherever one exists.
const adjBy = {}
for (const v of adjudicated) adjBy[`${v.dict}\u0000${v.wrong}`] = v
const final = allChk.map((v) => {
  const a = adjBy[`${v.dict}\u0000${v.wrong}`]
  return a ? { ...v, verdict: a.verdict, note: a.note, adjudicated: true }
           : { ...v, adjudicated: false }
})

const tally = {}
for (const v of final) tally[v.verdict] = (tally[v.verdict] || 0) + 1

return {
  rowsIn: allChk.length,
  checkBatches: files.length,
  checkBatchesFailed: chkFailed,
  flagged: flagged.length,
  adjudicated: adjudicated.length,
  unruledFlags: flagged.length - adjudicated.length,
  tally,
  final,
}
