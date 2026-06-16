// Canonical body-aware triage workflow -- ONE script for every dictionary.
// Invoke via the Workflow tool with:
//   { scriptPath: ".../detectors/bodyaware_workflow.js",
//     args: { dict, dir, src, hint } }      // emit these with: python triage_dict.py <DICT>
// dict = dict code; dir = the <DICT>/triage_work dir; src = the csl-orig dict file;
// hint = triage_lang.marker_hint(dict) (the language-specific intentional-spelling markers).
// The batch count is DISCOVERED at runtime (no nbatch to pass wrong).
export const meta = {
  name: 'bodyaware-triage',
  description: 'Body-aware classification (TYPO/REALWORD/INTENTIONAL) of a dictionary realword candidates against its own entry text, then source-confirm the TYPO pile',
  phases: [
    { title: 'Discover', detail: 'list the body_batch files on disk' },
    { title: 'Classify', detail: 'judge each candidate from the dictionary entry body' },
    { title: 'Confirm', detail: 'read the full source entry to confirm each TYPO verdict' },
  ],
}

const A = (typeof args === 'string' ? JSON.parse(args) : (args || {}))
const DICT = A.dict || 'MW'
const DIR = A.dir
const SRC = A.src
const HINT = A.hint || ''
// Hybrid tiering: cheaper model for the bulk classify (+discover), stronger model for the
// small source-confirm gate. Pinned per-phase here -> no manual model toggling, one run.
const CLS_MODEL = A.clsModel || 'sonnet'
const CONF_MODEL = A.confModel || 'opus'
if (!DIR || !SRC) throw new Error('bodyaware-triage: args must include {dict, dir, src, hint}')

const CLS_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    required: ['suspect', 'suggestion', 'label', 'confidence', 'reason'],
    properties: {
      suspect: { type: 'string' }, suggestion: { type: 'string' },
      label: { type: 'string', enum: ['TYPO', 'REALWORD', 'INTENTIONAL', 'UNSURE'] },
      confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
      reason: { type: 'string' },
    } } } } }
const CONF_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: {
    type: 'object', additionalProperties: false,
    required: ['suspect', 'is_typo', 'reason'],
    properties: { suspect: { type: 'string' }, is_typo: { type: 'boolean' }, reason: { type: 'string' } },
  } } } }
const DISC_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['files'],
  properties: { files: { type: 'array', items: { type: 'string' } } } }

const SLP1 = 'SLP1: capitals are LONG vowels (A I U); f/F = vocalic r/rr; e/E = e/ai; o/O = o/au; z = retroflex s; S = palatal s; R = retroflex n; M = anusvara.'

const CLS_RUBRIC = `You are a Sanskrit lexicographer auditing ${DICT}. Each row is a headword \`suspect\` a spelling detector flagged as a possible misspelling of \`suggestion\` (one-letter difference). You are given ${DICT}'s OWN entry text in \`body\`. Decide:

- TYPO: the body definition/gloss plainly belongs to the SUGGESTION and the \`suspect\` key is just a misspelling. The error is in the key spelling; the content is the corrected word. FILE these.
- REALWORD: the body genuinely defines the SUSPECT as its own distinct word (its own gloss / derivation / a verbal root). Do NOT file.
- INTENTIONAL: the body documents the spelling ON PURPOSE. ${HINT} NEVER file these.
- UNSURE: body too terse/ambiguous, or a proper noun whose spelling you cannot judge.

${SLP1}
Be conservative: choose TYPO ONLY when the gloss clearly fits the suggestion and contradicts the suspect spelling. If the suspect could be its own word or a documented variant, choose REALWORD/INTENTIONAL/UNSURE. body_count>1 means homograph entries.
reason: <=150 chars; cite the gloss/marker and which spelling it fits.`

function idxOf(fn) { const m = fn.match(/(\d+)/); return m ? m[1] : '000' }

phase('Discover')
const disc = await agent(
  `List every file matching body_batch_*.jsonl in the directory:\n  ${DIR}\nUse the Glob tool (pattern "body_batch_*.jsonl", path "${DIR}"), or Bash ls. Return {"files":[...]} with ONLY the base filenames (e.g. "body_batch_000.jsonl"), sorted ascending.`,
  { label: 'discover', phase: 'Discover', schema: DISC_SCHEMA, model: CLS_MODEL })
const files = ((disc && disc.files) || []).filter((f) => /body_batch_\d+\.jsonl/.test(f)).sort()
if (!files.length) throw new Error('no body_batch_*.jsonl files found in ' + DIR)
log(`discovered ${files.length} batch files`)

phase('Classify')
const clsResults = await parallel(files.map((fn) => () =>
  agent(
    `You audit ${DICT} spelling-correction candidates using ${DICT}'s own entry text.

STEP 1 - read your batch with the Read tool:
  ${DIR}/${fn}
Each line (ignore the line-number gutter) is a JSON object {suspect, suggestion, body, body_count, dcs_sugg_band}.

STEP 2 - classify EVERY row with this rubric:
${CLS_RUBRIC}

STEP 3 - write your verdicts as a JSON array (and nothing else) to:
  ${DIR}/body_adj_${idxOf(fn)}.json
one element per input row, same order: {"suspect":"..","suggestion":"..","label":"TYPO|REALWORD|INTENTIONAL|UNSURE","confidence":"high|medium|low","reason":".."}
Then return the same verdicts as structured output.`,
    { label: `cls:${idxOf(fn)}`, phase: 'Classify', schema: CLS_SCHEMA, model: CLS_MODEL }
  )
))
const allCls = clsResults.filter(Boolean).flatMap((r) => r.verdicts)
const typoPile = allCls.filter((v) => v.label === 'TYPO')
log(`classified ${allCls.length}; TYPO=${typoPile.length} REALWORD=${allCls.filter((v) => v.label === 'REALWORD').length} INTENTIONAL=${allCls.filter((v) => v.label === 'INTENTIONAL').length} UNSURE=${allCls.filter((v) => v.label === 'UNSURE').length}`)

phase('Confirm')
const VB = 15
const vb = []
for (let i = 0; i < typoPile.length; i += VB) vb.push(typoPile.slice(i, i + VB))
const confResults = await parallel(vb.map((items, j) => () => {
  const list = items.map((v) => `${v.suspect} -> ${v.suggestion}  [classified TYPO: ${v.reason}]`).join('\n')
  return agent(
    `Each line is a candidate TYPO: a ${DICT} headword \`suspect\` proposed as a misspelling of \`suggestion\`. CONFIRM each by reading ${DICT}'s FULL entry from the source.

Find each entry: use the Grep tool with pattern "<k1>SUSPECT<" on the file
  ${SRC}
(output_mode "content", -n true). Then Read those line(s) and the entry body that follows (up to <LEND>). ${HINT}

Set is_typo=true ONLY if the gloss/definition clearly belongs to \`suggestion\` and the suspect key is a bare spelling error, AND the body does NOT document the spelling and does NOT define the suspect as its own word. Set is_typo=false if the suspect is a real distinct word, a documented variant/redirect/wrong-reading, the entry is absent, or you cannot confirm. DEFAULT false when uncertain.
${SLP1}

Candidates:
${list}

Write your verdicts as a JSON array (and nothing else) to:
  ${DIR}/body_conf_${String(j).padStart(3, '0')}.json
each {"suspect":"..","is_typo":true|false,"reason":"<=150 chars citing the entry text you read"}
Then return the same verdicts as structured output.`,
    { label: `confirm:${String(j).padStart(3, '0')}`, phase: 'Confirm', schema: CONF_SCHEMA, model: CONF_MODEL }
  )
}))
const allConf = confResults.filter(Boolean).flatMap((r) => r.verdicts)
const confirmed = allConf.filter((v) => v.is_typo)

return {
  dict: DICT,
  classified: allCls.length,
  typo: typoPile.length,
  realword: allCls.filter((v) => v.label === 'REALWORD').length,
  intentional: allCls.filter((v) => v.label === 'INTENTIONAL').length,
  unsure: allCls.filter((v) => v.label === 'UNSURE').length,
  confirmedTypos: confirmed.length,
  confirmedSuspects: confirmed.map((v) => v.suspect),
}
