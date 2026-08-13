# A44 — ARR Responsible NLP + reproducibility checklist

_Created: 10-08-2026 · Last updated: 10-08-2026_

Filled per the checklist gate in
[/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md)
Phase 3.5, under [H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md).

**Checklist source:** [aclrollingreview.org/responsibleNLPresearch](http://aclrollingreview.org/responsibleNLPresearch/),
fetched **10-08-2026**, page marked *"updated for the ARR October 2024 cycle"* (Anna Rogers,
from ARR board discussions; since February 2024 the checklist is filled in the submission form
rather than as a separate PDF).

**Subject:** [A44_body_grounded_triage_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md),
readiness 4/5, target **International Journal of Lexicography**.

**Venue calibration.** *IJL* is not ARR-governed, so this filled checklist is an **internal
quality bar, not a required submission artifact** — per the venue-calibration rule in the skill,
attach the formal file only for ACL/EMNLP/NAACL/LREC-family venues. It is worth filling anyway:
A44 is an LLM-method paper, so the C and E families are load-bearing for its credibility, and
the ISCLS demo track named in [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md)
as a secondary venue is closer to the ARR world than *IJL* is.

## A. For every submission

| Item | Status | Pointer |
|---|---|---|
| A1. Limitations | **yes** | Dedicated **§6 Limitations**, five substantive items: LLM stochasticity (the 122 figure is a floor under union-across-runs, not a point estimate); the reliability number is model-vs-model, not human IRR; queue decay ≈0.8 %/week against live `csl-orig`; PD read from a staged external source on one source only; the scan as final irreducible arbiter with 17 rows held at SCAN-FIRST. Scope-of-claims is explicit throughout. |
| A2. Risks | **yes** (§3.5, §4.7) | The paper's central risk *is* its subject: applying detector output would corrupt digitised editions. §4.7 quantifies it as a harm metric — raw detectors flag 77–100 % of rows verified as harmful to apply. §3.5 states the guardrail: the pipeline never edits a source; corrections route to the separate CORRECTIONS workflow ([#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)). No fairness/privacy/dual-use surface — the data is 19th–20th-c. public-domain dictionary text. |

## B. Scientific artifacts

Artifacts both **used** (33 CDSL dictionary editions) and **created** (triage queues, the
do-not-file catalogue, the suppression file, the gold set).

| Item | Status | Pointer |
|---|---|---|
| B1. Citation of creators | **yes** | The Cologne Digital Sanskrit Dictionaries corpus and per-dictionary editions are named with source identifiers; `csl-orig` cited as the live source with resolvable URLs. All 15 References URLs resolved and title/author-checked 12-07-2026. |
| B2. Licenses / terms | **no** — the one real B-family gap | No licence statement for the CDSL editions read as input, nor a declared licence for the **created** artifacts (`do_not_file_suppress.txt`, `file_first_verified.tsv`, `gold_corrections.tsv`). The suppression catalogue is the paper's principal deliverable and is offered for reuse, so it should carry an explicit licence. **Remaining work.** |
| B3. Intended use | **yes** | §3.5 states the intended use of the created artifacts precisely — a triage *prior*, never an auto-apply source; the entry and ultimately the scan are the arbiter. Consistent with scholarly use of public-domain lexicographic text. |
| B4. Personal info / offensive content | n/a | No personal data and no human-subject content; the corpus is historical dictionary text. |
| B5. Artifact documentation | **yes** | Language (Sanskrit), domain (lexicography), and per-dictionary provenance documented in [corrections_draft/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md) with a 33-dictionary status table; the do-not-file file carries per-class sections. Demographics are not applicable. |
| B6. Dataset statistics | **yes** | Exact counts throughout with as-of dates: 2,297 deduped do-not-file rows (2,549 gross), 122 confirmed fileable across 11 dicts, verdict split 92/17/11/1/1 as of 2026-07-02, MW precision 4/1,954 = 0.20 %, ~31k known-good headwords and 3,884 historical pairs in the eval harness, 13 HARM rows in the held-out gold set. |

## C. Computational experiments

| Item | Status | Pointer |
|---|---|---|
| C1. Model / infra details | **partial** | Per-phase **tier + exact version** is reported in §3.3 (Sonnet 4.6 `claude-sonnet-4-6` bulk classification; Opus 4.8 `claude-opus-4-8` source-confirm and adversarial review; four Sonnet 5 `claude-sonnet-5` checkers with Fable 5 `claude-fable-5` adjudication for the 2026-07-02 re-verification). Parameter counts and compute budget are **not reportable** — these are closed commercial APIs, not self-hosted models; that is a property of the setting, and the version pinning is the reproducibility substitute. State it that way rather than leaving C1 blank. |
| C2. Experimental setup | **yes** | §3.3 specifies the six-stage pipeline in order with the decision rubric for each stage (including the explicit keep/drop rubric of the adversarial gate); §3.2 defines the five-way decision. No hyperparameter search — prompts are the setup, and they live in the [/dict-triage](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.claude/commands/dict-triage.md) skill. |
| C3. Descriptive statistics | **partial, honestly stated** | §3.4 splits the outputs by epistemic status: the deterministic marker backbone and every count recompute bit-identically; the LLM typo pass is stochastic and the 122 is reported as a **floor under union-across-runs, not a point estimate**, with the disclosure that an MW re-run once refuted 4 previously confirmed typos. κ = 0.336 was computed once on the first blind run and reported as obtained, not iterated toward agreement. No confidence intervals on the percentages — the residual C3 gap. |
| C4. Package / tool versions | **partial** | The reproducing scripts are named and committed ([eval.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py), [gen_do_not_file_suppress.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_do_not_file_suppress.py), [irr_build_inputs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_build_inputs.py), [irr_agreement.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_agreement.py)) with the exact commands that regenerate each headline figure. No third-party NLP toolkit is used; κ is exact-arithmetic in-repo. Pinning a Python version in the reproducibility section would close this fully. |

## D. Human annotators and research participants

| Item | Status | Pointer |
|---|---|---|
| D1–D3, D5 | n/a | No crowdworkers, no recruited participants, no annotator population. The "human verification" stage of §3.3 is the author/editor performing normal editorial work on public-domain text, not human-subjects research. |
| D4. Ethics review | n/a | No human-subjects data collection protocol; nothing to approve or exempt. |

**Note against over-claiming:** the deferred *human anchor* of §6 — an independent human expert
annotator — would, if recruited, activate this whole family. It is currently tracked as future
work in [HUMAN_ANCHOR_NEEDED.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md), not performed.

## E. AI assistants

| Item | Status | Pointer |
|---|---|---|
| E1. Disclosure of AI use | **yes** | Unusually well satisfied: LLM use is the paper's object of study, not an aid to it. §3.3 gives per-phase tier + exact version for every model-mediated stage; §4.6 documents a blind second annotator of a different tier; §3.4 separates deterministic from stochastic output. The author-voice and referee passes on the manuscript itself are recorded in [SIGNOFF_A44_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A44_author_pass.md). |

## Verdict

**No blocker in the A-family.** A1 and A2 are both properly discharged — the failure mode this
gate most often catches (a missing Limitations section) does not apply.

Remaining work, in order:

1. **B2 — licence declaration** for the CDSL inputs and, more importantly, for the created
   do-not-file / suppression artifacts that the paper offers for reuse. This is the only
   outright `no`.
2. **C1 / C4 — state the closed-API constraint explicitly** (parameter counts and compute
   budget unavailable by construction; version pinning is the substitute) and pin a Python
   version in the reproducibility section.
3. **C3 — no confidence intervals**; the honest floor-not-estimate framing already covers the
   claim, so this is a refinement rather than a defect.

_Dr. Mārcis Gasūns_
