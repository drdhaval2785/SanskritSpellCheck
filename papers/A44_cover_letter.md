# Cover letter — submission to the *International Journal of Lexicography*

_Created: 10-08-2026 · Last updated: 10-08-2026_

*(Skeleton, drafted under [H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md). Every ⟦MG⟧ marker is a human decision, not a pending lookup.)*

---

To the Editor
*International Journal of Lexicography*
Dr Robert Lew (Editor)

Dear Dr Lew,

I should like to submit the enclosed article, **"The Dictionary Body as Ground Truth:
Body-Grounded LLM Triage and the Precision-Collapse Result,"** for consideration in the
*International Journal of Lexicography*.

The paper reports a negative result and the method that survives it. On mature digitised
dictionaries, headword-level spelling-anomaly detection collapses to near-zero precision —
4 of 1,954 flags in Monier-Williams, 0.20 % — and no refinement of the spelling statistics
escapes the collapse, because the information that separates a genuine typo from an
intentional orthographic variant, a rare-but-real word, or editorial apparatus is simply not
present in the headword. It is in the entry body. The article shows that a staged pipeline
which reads the body — classify, confirm against the entry, re-verify, human-verify —
recovers the real errors where they concentrate (poorly digitised sources: SHS ≈ 15 %,
YAT ≈ 11 %), and exposes a *collision* class that no headword-level check can see at all.

The more durable contribution is the inverse artifact. Across 33 dictionaries of the Cologne
Digital Sanskrit Dictionaries corpus, the pipeline produced a **2,297-entry deduplicated
do-not-file catalogue** (2,549 gross) — a reusable record of what must *not* be "corrected",
which is what prevents a well-intentioned bulk pass from corrupting a digitised edition. A
detection-level harm metric quantifies that risk directly: raw detectors flag 77–100 % of the
rows independently verified as harmful to apply.

I hope the piece will interest the readership of the *IJL* on three counts. First, as a
**methodological result for digital lexicography**: the entry body, not spelling or corpus
frequency, is the reliable ground truth for the typo-vs-variant decision, and that claim is
stated as a measurement rather than an intuition. Second, as a **reproducibility study**: a
blind second annotator of a different model family re-derived the taxonomy from the entry
bodies alone (κ = 0.336 five-way; 99.2 % binary defect recognition), reported as obtained
rather than iterated toward agreement, with the remaining human-anchor gap stated plainly in
the Limitations rather than papered over. Third, as **editorial practice**: the workflow never
edits its sources — confirmed corrections are reported to the separate Cologne CORRECTIONS
workflow — so the paper doubles as a description of a non-destructive correction discipline.

The article runs to approximately **6,500 words** including apparatus, with 15 references in
APA (7th ed.) style. All underlying artifacts — the per-dictionary triage queues, the
re-verification table, the deduplicated suppression file, and the evaluation harness that
reproduces every headline figure — are openly available in the project repository and are
listed in the Data and reproducibility section; they can accompany the article as supplements
or be cited as datasets, as the editors prefer.

The work is original, has not been published elsewhere, and is not under consideration by
another journal. I have no competing interests to declare. ⟦MG⟧ funding statement: the
*IJL* requires funding sources to be named in the manuscript — confirm the intended wording
(no external funding, if that is correct). The analysis was carried out with the assistance of
large language models, which is not incidental but the object of study; the paper documents
per-phase model attribution in its method section.

I am happy to adapt length, apparatus, and citation style to the journal's house conventions.

With thanks for your consideration, and kind regards,

Mārcis Gasūns
Independent scholar
gasyoun@ya.ru · ORCID: [0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)

---

## ⟦MG⟧ decisions before this letter is sent

| # | Decision | Why it is a human's |
|---|---|---|
| 1 | **Funding statement wording** — *IJL* requires funding sources named in the manuscript; "no external funding" is presumed but not confirmed. | A factual claim about the author's funding. |
| 2 | **Supplement vs. dataset citation** — offer the artifacts as supplementary files, or cite them as `[dataset]` entries with a DOI (which requires minting one, e.g. Zenodo). | Changes the References list and commits to a DOI. |
| 3 | **Article-type framing** — submitted as a full research article; the negative-result spine could also suit a shorter format. | Editorial positioning. |
| 4 | **Read-through for register** — the standing gate from [SIGNOFF_A44_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A44_author_pass.md), still open. | The author's public voice. |

_Dr. Mārcis Gasūns_
