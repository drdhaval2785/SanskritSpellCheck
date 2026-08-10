# Cover letter — submission to *Digital Scholarship in the Humanities*

_Created: 10-08-2026 · Last updated: 10-08-2026_

*(Skeleton, drafted under [H2406](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2406-Fable_SanskritSpellCheck_a37-plus5-camera-ready-pack_07.08.26.md). Every ⟦MG⟧ marker is a human decision, not a pending lookup.)*

---

To the Editors
*Digital Scholarship in the Humanities*
Oxford University Press

Dear Editors,

I should like to submit the enclosed article, **"Reading the Reform off the Gloss:
Orthographic Drift as a Dater of 19th–20th-Century Indological Dictionaries,"** for
consideration in *Digital Scholarship in the Humanities*.

The paper turns a familiar object of digital humanities — a marked-up corpus of historical
dictionaries — on an unfamiliar channel. A bilingual dictionary is written twice over: once
in the headword language it describes, and once in the *metalanguage* of its glosses and
prefaces. Measuring that second language against a pinned 2026 orthographic standard across
five gloss languages and nearly two centuries of sources (1832–2009), I show that the
magnitude and composition of orthographic drift are governed by the **type** of spelling
reform the metalanguage underwent, not merely by the dictionary's age: legislated reform
(Russian 1918 ≈ 358 drifted forms per 1,000 gloss tokens; German 1901/1996 ≈ 2.5–10),
convention drift (English and French ≈ 0–0.46), and none at all (Latin = 0, a negative
control) separate by nearly three orders of magnitude at the regime extremes.

The dating result is the part I would most want a DSH readership to weigh. The scalar drift
*rate* is a weak instrument; the **per-era composition** of the drift — which reform's forms
dominate — is a strong one. Schmidt's 1928 German supplement flips from a `th`-dominant
(pre-1901) to an `ß`-dominant (pre-1996) signature and lands in its true window, dated from
its own prose rather than its title page. Latin's zero confirms the tool manufactures no
drift where none exists.

I hope the article fits DSH on three counts. First, it is a **method contribution to corpus
philology**: the claim is not a new historical-spelling normaliser — that is a mature
subfield, and the paper says so — but the application of normalisation to a multilingual,
era-stratified *lexicographic* corpus, which yields a reproducible cross-decade drift
dataset and a metalanguage-dating instrument. Second, it reports its **negative result as
plainly as its positive one**: §4.8 fits the Ghanbarnejad et al. (2014) logistic S-curve to
the same data and finds the exogenous/endogenous mechanism ordering *inverted* (English
"abrupt" at 9.7 years against German "gradual" at 50.2), which I diagnose as a
cross-sectional sampling artifact rather than a finding about language change. Third, it is
**reproducible in the strict sense**: every figure recomputes from committed tables with the
commands given in the Data availability statement.

Two matters of scope I would rather state than have a referee infer. The corpus is the
Cologne Digital Sanskrit Dictionaries plus one external pre-revolutionary Russian source,
and two of the three regime cells rest on a single language each — so the paper reports a
stratification observed on this corpus, not a law. And the modern reference word-lists
(Hunspell `de_DE`, `en_GB`, `fr_FR`) are a local runtime dependency rather than committed
data, for licensing reasons; the statement names the exact snapshot identities against which
the published figures reproduce.

The manuscript runs to approximately **3,150 words** in the body, comfortably inside the
9,000-word limit for full papers, with one figure and 18 references. A companion short paper
developing the S-curve negative result on its own is intended for the LChange workshop
series and is **not** under consideration anywhere at present; I mention it so the overlap
is visible to the editors rather than discovered later. ⟦MG⟧ confirm whether to disclose the
companion in this letter or omit it.

The work is original, has not been published elsewhere, and is not under consideration by
another journal. ⟦MG⟧ funding statement: DSH requires a "Funding" section in the end matter
— confirm the intended wording (no external funding, if that is correct). Per the journal's
AI disclosure policy I note here that large language models were used in drafting and
revising the manuscript — not in producing the measurements, which come from a deterministic
detector committed in the repository; the manuscript's AI Disclosure Statement names the
tools, versions, and the extent of that use, and I have verified all generated content.

I am happy to adapt length, apparatus, and citation style to Oxford HUMSOC house
conventions.

With thanks for your consideration, and kind regards,

Mārcis Gasūns
Independent scholar
gasyoun@ya.ru · ORCID: [0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)

---

## ⟦MG⟧ decisions before this letter is sent

| # | Decision | Why it is a human's |
|---|---|---|
| 1 | **Addressee** — the letter opens "To the Editors" rather than naming the current Editor. Confirm the name from the journal masthead before sending. | A name invented from memory is a defect; the masthead is the only source. |
| 2 | **Funding statement wording** — DSH mandates a "Funding" end-matter section; "no external funding" is presumed but not confirmed. | A factual claim about the author's funding. |
| 3 | **Disclose the LChange companion, or not** — the draft letter discloses it. The overlap is one section (§4.8) reframed; disclosure is the conservative choice, silence the simpler one. | Editorial positioning, and a dual-submission judgement. |
| 4 | **Article type** — submitted as a full paper. At ~3,150 words the body is short for the category and would also fit DSH's "shorter articles" class (5,000 words, "material of a more general nature") — but that class is framed for general-interest pieces, and this is a primary research result. | Editorial positioning. |
| 5 | **Read-through for register** — the standing gate from [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md), still open; on sign-off A37 bumps to 5/5. | The author's public voice. |
| 6 | **Editorial "we" for a sole-author byline** — the author-voice pass declined to flip ~20 instances to first-person singular unasked. DSH prints both. | A register change the author should choose. |

_Dr. Mārcis Gasūns_
