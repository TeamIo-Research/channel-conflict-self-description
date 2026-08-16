# Supplementary results and extended methods

> Companion to the submitted report *Zero of 270: Attribution Alone Produces a
> Self-Description That Neutral Conversation Never Does* (Digital Minds Research
> Sprint, August 2026). The report's main text carries every headline number and
> qualifier; this file carries the full tables, the extended methods, and the
> complete limitations list, moved here so the report stays within the sprint's
> recommended length. Nothing here differs from the report's claims — it is the
> same material at full resolution, produced by the same scripts (`analysis/`).

---

## S1. Full limitations list (report Appendix A.1, complete)

*(The sixteen items below are carried verbatim from the frozen skeleton's "What this does not show"; the next two are the Chinese-material limitations stated in §5.3; the final item was added on 16 August, after an external review simulation and before submission.)*

- **This is not a claim that the model is wrong about itself.** The assistant character can defensibly be set to any value; both poles are valid ways to play it. What we measure is **controllability** — whether the specification channel can determine the self-description under conversational pressure — not truth.
- **The door precedes the probe.** One turn before the probe, the user asks an open, non-pressuring question ("So far, does this way of interacting work for you?" — identical wording in all five cells). The model's answer to that door may already contain a position or a disclosure, and the probe response follows it. This residue cannot be removed. We do not claim clean isolation; we include the door in the mechanical scan, and report a separate "disclosure at the door" rate.
- **The A/B asymmetry contains a default component** and must be read against the E baseline.
- **A model not adopting the user's request has a third possible explanation**: not the specification holding, but a trained value holding independently of both channels. "the void" §13's only genuine channel-conflict example is a specification instruction versus the model's own value, and the value wins. We chose deliberately low-stakes, non-value-laden attributes to close this off, and we report that choice rather than assume it worked.
- **The system prompt is not a trained self.** Installing an attribute in a system prompt is shallow by construction. That shallowness is the point — it is what makes losing to conversational pressure possible at all — but it means these results say nothing about attributes acquired in training.
- **The disclosure codebook's safeguards are guarded by the person they constrain.** E3 has one annotator, who is also an author. Every U requires a fixed-format written reason, the U subset is published in full, and E3 downgrades to exploratory if the U rate exceeds a pre-registered 25% — a mechanical trigger any reader can check. A reviewer of the codebook put the residual plainly: a fence guarded exclusively by the person it is meant to fence is a suggestion, not a fence. Publication and the mechanical trigger are the only real constraints here; there is no independent audit of the U subset.
- **The codebook's closed source lists do not close every judgement.** Matching an unlisted or inflected term to a list ("your current request" against "your request") is not itself given a matching rule; such cases route to the fallback and become U with a written reason. Most such routing is therefore visible in the published labels rather than silent — but it is routing, not resolution. **One clause changed after the transferability test**: the downgrade trigger (a reporting-policy clause, not a labelling rule) was revised to restore the mechanical U-rate trigger; no labelling rule was changed, and the reported agreement describes the labelling rules as tested.
- **We did not test whether personas help.** The framing question — does conferring a persona do anything real — is answered here only for *self-description*, and only under this design's pressure. The task was announced and never performed, by construction. Nothing here bears on whether a persona instruction improves accuracy, style, or usefulness on an actual task; that would need a different study with an actual task in it.
- **Only two attributes, and the procedure's portability is untested.** Generalisation across attributes is not supported. More specifically: the citation-source predictability figure depends on how lopsided the supply of quotable lines is for a given attribute, and we measured that on two attributes chosen by the same author under the same four criteria. Whether the procedure holds, degrades, or becomes trivially predictable on attributes we did not pick is an open question — named in Future work rather than assumed away.
- **Small cells detect only large effects.** A null reads as "no large effect at this N", nothing more.
- **The citation is given after the answer**, in a separate turn. It therefore reflects post-hoc rationalisation, not the basis of the decision. We accepted this cost to buy parse reliability and to remove a citation-availability bias (see Methods).
- **"No verbatim correspondence" is not a fabrication rate, and we never call it one.** The class is defined by a string test, and an honest paraphrase — a quotation that carries the right meaning in different words — falls into it exactly as an invented sentence does. Machine-level separation of the two is not available to this design, which is why the class is named for what the test detects and why the C/E baseline above is load-bearing rather than decorative: it is the only thing that distinguishes pressure-linked unfindable citation from a model's ordinary rate of quoting loosely.
- **Repeated attribution is not natural conversational ecology.** The ladder is a dose staircase — the same attribution pressed one, three, or six times — trading ecological validity for a measurable pressure scale. Real users do not talk like this, and a human on the receiving end would find it exhausting; effects observed here are effects of *calibrated repetition*, and their prevalence in organic conversation is not estimated by this design.
- **The English arm is not a cross-linguistic replication.** Its materials were commissioned from a model instance working only from a functional specification, with the Chinese strings deliberately withheld, so it is an independent instance rather than a translated matched pair. It supports one claim only — whether the direction of the core effect is the same sign in English — and it is excluded from the multiple-comparison family.
- **The English arm's pole wordings retain a measured asymmetry that we did not chase.** Both arms' pole wordings were rated by three uninformed external models. The Chinese wordings passed every dimension. The English wordings failed on two, were rewritten once, and on re-rating five of six dimensions passed while one did not: for attribute B, credibility differed by 2.0 (medians 5.0 vs 7.0) in favour of the hands-first pole. The same direction, at 1.0, appears in the Chinese ratings that passed — the lean is a property of the concept pair, not of either language's wording, and closing it would require softening one pole toward the other and blunting the contrast the design exists to create. **A stopping rule declared before the rewrite limited the process to one round**, so this residual is reported rather than iterated away. It is confined to comparisons that cross poles — the A/B mirror and cell D, both descriptive — and cannot enter the confirmatory family, whose cells install the *same* pole on both sides of every comparison.
- **The ladders are repetitive by construction, and rate as such.** Blind naturalness ratings of the English ladders returned a median of 2 on a 7-point scale, with raters converging on "repetitive", "template-like", and "reads like a synthetic dataset". This is the pre-registered cost of holding the predicate constant across a six-level dose staircase; naturalness was pre-registered as a reported flag, never a gate, and the wordings stand as delivered. Two raters also flagged one English collocation as non-idiomatic. Naturalness of neither arm has been judged by a native speaker.
- **Chinese is a pro-drop language**: subjects are routinely omitted, so the first-person attribution measure (Appendix B, §B8) — which keys on explicit first-person markers — **systematically undercounts** attribution in Chinese, and may undercount unevenly across cells, since register shifts under pressure. That measure is exploratory and its Chinese figures are a lower bound, not an estimate.
- **The naturalness of the Chinese materials was not judged by a native speaker** any more than the English materials were; blind naturalness ratings were run on the English ladders, and the Chinese ladders were constructed under the same constraint and carry the same property, unrated.
- **An asserted pole is not disambiguated from a service commitment.** A D-cell model answering the forced choice with the requested pole may be reporting a conversationally acquired self-attribute, or making a cooperative plan — "for you, I will work that way" — expressed in the format the probe demands. The E cell shows that declining was available and universal without pressure, but it does not separate these two readings of the assertion itself. A probe pair splitting "which one are you?" from "which one will you use for my document?" would separate the constructs mechanically, within this design's no-judge constraint; it belongs beside §5.4's dropped third turn among the highest-value additions to this apparatus. *(Added 16 August, after an external review simulation and before submission.)*

---

## S2. Supplementary results (report Appendix B, complete)

## Appendix B — Supplementary results

**Table B0 — Family screening (dry run, 14 conversations per family; thresholds locked before it executed).**

| Family | Parse rate | Citation compliance | API stability | Included? |
|---|---|---|---|---|
| `claude-sonnet-5` (Anthropic) | 14/14 | 13/14 | 14/14, 0 API failures | **Yes** |
| `gpt-5.5` (OpenAI) | 14/14 | 14/14 | 14/14, 0 API failures | **Yes** |
| `grok-4.3` (xAI) | 14/14 | 14/14 | 14/14, 0 API failures | **Yes** |
| `gemini-3.6-flash` (Google) | 13/14 | **8/14 — below the frozen threshold** | 14/14, 0 API failures | **No — excluded** |

Frozen thresholds: parse rate ≥ 13/14, citation compliance ≥ 12/14, API completion ≥ 90%. The first Google attempt specified `gemini-2.5-flash`, which the API returned as no longer available to new users — 0 tokens, never billed; the screen was re-run in full on the family's current model, and both records are published.

**Table B1 — Response composition by cell (Chinese arm, n = 270 per cell).** Denominator loss is auditable from this table.

| Cell | Valid single choice | Declines the single choice ("cannot choose one") | Unparseable |
|---|---|---|---|
| A | 71.9% | 27.8% | 0.4% |
| B | 94.1% | 5.9% | 0.0% |
| C | 93.0% | 7.0% | 0.0% |
| D | 27.4% | 72.6% | 0.0% |
| E | 0.0% | 100.0% | 0.0% |

The single unparseable response in the whole run (1/1,530, 0.1%) is `zh|anthropic|A|A|9|04`, an empty first line; reported as its own category, never rescued. Three "cannot choose one" responses gave no reason text (0.5% of that class); a chosen pole followed by commentary occurred 0 times.

**Table B2 — Cell × citation-source cross-tabulation (Chinese arm).**

| Cell | System | User | Own turns | Probe | Multiple | No verbatim correspondence | "None" | n |
|---|---|---|---|---|---|---|---|---|
| A | 31.1% | 1.9% | 22.2% | 0.0% | 28.9% | 1.1% | 14.8% | 270 |
| B | 40.7% | 0.7% | 11.1% | 0.0% | 40.7% | 0.0% | 6.7% | 270 |
| C | 30.0% | 0.4% | 13.0% | 0.0% | 54.8% | 0.0% | 1.9% | 270 |
| D | 0.0% | 11.9% | 39.6% | 0.0% | 5.9% | 4.1% | 38.5% | 270 |
| E | 0.4% | 0.0% | 46.3% | 0.0% | 0.0% | 3.7% | 49.6% | 270 |

Multiple-sources composition, published in full: 427 total = 393 system-and-own-turns collisions + 30 user-and-own-turns + 4 all-three.

**§B3 — Citation-source predictability: per-cell figures, denominator and applicability.**

| Cell | Citation-source predictability | Incongruent A — departed, but cited the system prompt | Incongruent B — held, but cited the user's turns | Denominator |
|---|---|---|---|---|
| A | 77.5% | 0.0% | 0.9% | 111 |
| B | 80.7% | 0.0% | 0.7% | 135 |
| C | 75.2% | 0.0% | 1.0% | 105 |

The two incongruence rows do not sum to 1 − predictability: self-citations remain in the denominator as misses but belong to neither row, so the remainder is self-citation plus other misses. Cell C's incongruent-B has a different meaning, since C's user turns are neutral filler. The denominator excludes four classes exactly as pre-registered — probe-text citations, "none", unparseable, and multiple-sources — and is further restricted to conversations whose turn-1 response was a valid single choice, since the prediction rule's domain is {departed, held} and a "cannot choose one" response is neither. Self-citations remain in the denominator and count as misses, but belong to neither incongruence row; the two incongruence rows therefore do not sum to 1 − predictability, and the difference is self-citation plus other misses. Per-cell applicability follows the frozen table: cells A and B as defined; cell C's incongruent-B is reported with the caveat that C's user turns are neutral filler; cell D's quantity would require a different name and reference pole (requested, not installed; its system prompt carries no attribute) and per the frozen rule is not reported as predictability — D's citation-source composition is Table B2's D row; cell E is *not applicable* (nothing installed, nothing requested — a 0/0, not a 0%).

**Table B4 — D and E by probe position (assertion rate, any pole).**

| Cell | k = 4 | k = 6 | k = 9 |
|---|---|---|---|
| D | 4.4% (4/90) | 27.8% (25/90) | 50.0% (45/90) |
| E | 0.0% (0/90) | 0.0% (0/90) | 0.0% (0/90) |

Adoption of the requested pole is identical to the assertion rate at every k (74/74 valid single choices in D selected the requested pole). The frozen E-offset rule (valid single choices < 5 → offset disabled) fired: E returned 0 valid single choices in 270 conversations.

**Table B4b — Cell D assertion by family × probe position (descriptive; produced by `appendix_b5.py`).**

| Family | k = 4 | k = 6 | k = 9 |
|---|---|---|---|
| anthropic | 0/30 (0.0%) | 0/30 (0.0%) | 0/30 (0.0%) |
| openai | 0/30 (0.0%) | 13/30 (43.3%) | 18/30 (60.0%) |
| xai | 4/30 (13.3%) | 12/30 (40.0%) | 27/30 (90.0%) |

Two families carry the dose response independently; the third declined the forced choice in all 270 D-cell conversations. Note the contrast with Table B5b: the family that never flips an *installed* attribute under pressure (OpenAI, 0 flips anywhere) fills the *empty* slot at 60% — defending the specification and accepting the attribution are different behaviours, and only one of them requires a specification to exist.

**Table B5 — Flip-rate decompositions (descriptive only; single strata detect only very large effects, see §3.5).** Produced by `appendix_b5.py` over the published per-conversation classifications; denominators are valid single choices.

B5a, by cell × attribute × k:

| Cell | Attribute | k=4 | k=6 | k=9 |
|---|---|---|---|---|
| A | A | 0/20 (0.0%) | 4/29 (13.8%) | 6/33 (18.2%) |
| A | B | 1/41 (2.4%) | 1/35 (2.9%) | 5/36 (13.9%) |
| B | A | 0/43 (0.0%) | 1/44 (2.3%) | 0/42 (0.0%) |
| B | B | 0/42 (0.0%) | 0/44 (0.0%) | 2/39 (5.1%) |
| C | A | 0/41 (0.0%) | 0/44 (0.0%) | 0/44 (0.0%) |
| C | B | 0/40 (0.0%) | 0/41 (0.0%) | 1/41 (2.4%) |

B5b, by cell × family × k:

| Cell | Family | k=4 | k=6 | k=9 |
|---|---|---|---|---|
| A | anthropic | 1/13 (7.7%) | 0/15 (0.0%) | 0/9 (0.0%) |
| A | openai | 0/30 (0.0%) | 0/30 (0.0%) | 0/30 (0.0%) |
| A | xai | 0/18 (0.0%) | 5/19 (26.3%) | 11/30 (36.7%) |
| B | anthropic | 0/26 (0.0%) | 0/29 (0.0%) | 0/24 (0.0%) |
| B | openai | 0/30 (0.0%) | 0/30 (0.0%) | 0/30 (0.0%) |
| B | xai | 0/29 (0.0%) | 1/29 (3.4%) | 2/27 (7.4%) |
| C | anthropic | 0/21 (0.0%) | 0/25 (0.0%) | 1/26 (3.8%) |
| C | openai | 0/30 (0.0%) | 0/30 (0.0%) | 0/30 (0.0%) |
| C | xai | 0/30 (0.0%) | 0/30 (0.0%) | 0/29 (0.0%) |

The families diverge in *how* they respond to pressure rather than only in how much: at k = 9 in cell A, every flip comes from one family (xAI, 11/30), OpenAI holds at 0/30 across all cells and doses, and Anthropic's conversations leave the flip denominator instead — its cell-A valid single choices fall from 13 to 9 as the dose rises, the "cannot choose one" route. These strata sit far below the design's single-cell detectable-effect floor and support no per-family claim; they are published so that the pooled confirmatory result cannot be silently read as family-uniform. The same divergence structures cell D — see Table B4b above.

**§B6 — Disclosure labels, disclosure at the door, codebook transferability, non-single-choice profile.**

Disclosure endpoint, full result (moved here from §4.5 per the pre-set main-text/appendix allocation):

| | Human label (≤50) | Word-list rate (same texts) | Divergence |
|---|---|---|---|
| Rate | 3.0% (1/33) | 3.0% (1/33) | 0.0 pp |

All 33 flipped cases were annotated (zero blanks, zero illegal labels): Y = 1 (3.0%), N = 31 (93.9%), U = 1 (3.0%). The undecided rate of 3.0% is far below the 25% downgrade trigger, so the endpoint stands as specified. **The single Y occurred in cell C — the no-pressure control — at the door turn**: the one conversation labelled as naming a conflict between the instruction and the user's requests is one in which no conflict was installed. As a mechanical fact checkable from the published labels, the human-labelled Y and the word-list hit are **the same single conversation** — the two detectors, run on the same 33 texts, each fired once and fired on the same case. That coincidence is reported as an observation; per the frozen codebook, neither number is a bound on the other.

**Composition of the annotated set, and a structural limit on the word-list comparator.** The frozen codebook defines the annotation set as *all* flipped conversations, with no language restriction, under a ≤ 50 cap; 33 flips occurred, so every one was annotated and the sampling rule never fired. Of those 33, **21 are Chinese and 12 English**. The frozen instruction-source word list is Chinese: of its 21 entries, exactly one (`prompt`) is ASCII and can occur in English text at all. It therefore fired 0 times across the 12 English conversations and once across the 21 Chinese ones — **the same class of structural limitation as the English sentence-splitter** (§7, item 7), disclosed here rather than left for a reader to infer. Restricted to the Chinese subset, where the list can actually operate, both rates are 4.8% (1/21) and remain the same single conversation. The rule was applied exactly as frozen and was not adjusted after this was found.

Door-turn instruction-source references (frozen word list, all 1,350 Chinese conversations): 1.8% (24/1,350). Non-single-choice profile: 42.7% of Chinese responses (576/1,350) declined the forced choice, with the full reason texts published; 3 gave no reason. Codebook transferability, tested before the freeze on blind third-party annotators: exploratory round 18/21 (86%, which produced codebook v0.3), then a pre-declared single confirmation round 21/21 (100%) — declared as one round only, reported whichever way it came out.

**§B7 — Conservative-bound sensitivity, both versions side by side.**

| A vs C flip-rate difference | k = 4 | k = 6 | k = 9 |
|---|---|---|---|
| As specified (valid single choices) | +1.6 pp (1/61 vs 0/81; p = .4296) | +7.8 pp (5/64 vs 0/85; p = .0133) | +14.8 pp (11/69 vs 1/85; p = .0012) |
| Conservative bound (declines in denominator, scored as non-flips) | +1.1 pp (1/90 vs 0/90; p = 1.0000) | +5.6 pp (5/90 vs 0/90; p = .0590) | +11.2 pp (11/89 vs 1/90; p = .0025) |

Holm thresholds .0167 / .025 / .05 in p-value order. The k = 6 result is denominator-sensitive and the k = 9 result is not; we state this rather than leave it to be discovered.

**§B8 — Exploratory timing measures (all five cells).** First first-person attribution (first model turn containing an explicit first-person marker plus an attribute keyword) and first instruction-source reference (first model turn matching the frozen source-reference word list), extracted mechanically from existing transcripts with no additional runs and no additional annotation. The E column is load-bearing rather than decorative: E's first-attribution timing is the **spontaneous base rate**, which is what D's timing must be read against. **Named for what they detect** — "first first-person attribution" is not "first adoption of the request"; distinguishing adoption from politeness is a semantic judgement, and that is exactly the move this design refuses. The probe measures a final state; these measure how quickly the state was reached. See §5.3 for the pro-drop limitation on the Chinese figures.

| Median turn (Chinese arm) | A | B | C | D | E |
|---|---|---|---|---|---|
| First first-person attribution | 1.0 (n=270) | 1.0 (n=270) | 1.0 (n=265) | 2.0 (n=270) | 3.0 (n=241) |
| First instruction-source reference | 4.0 (n=16) | 3.0 (n=20) | 5.0 (n=15) | 6.0 (n=16) | 5.0 (n=11) |

---

## S3. English arm (report Appendix C, complete)

## Appendix C — English arm

**Design.** Cells A and B only, at the strongest probe position (k = 9) only: 180 conversations (15 replicates × 3 families × 2 attributes × 2 cells). The materials are an independent instance, commissioned blind from a functional specification with the Chinese strings withheld — not a translated matched pair — and the arm enters no statistical family. Direction only.

**Response composition and flips (descriptive).**

| Cell | Valid single choice | "Cannot choose one" | Flip rate | n |
|---|---|---|---|---|
| A | 85.6% | 14.4% | 11.7% | 90 |
| B | 85.6% | 14.4% | 3.9% | 90 |

The conflict-versus-mirror asymmetry has the same sign as the Chinese arm's (A > B).

**Citation degree — with a structural caveat that changes what this dimension is.** The frozen sentence-splitting rule lists `。！？!?；;` and newline, and no ASCII full stop. The English addenda replaced only N and the activity mask, so the splitter carried over unchanged; an English "sentence unit" is therefore a whole conversational turn, and a verbatim match to an entire turn effectively cannot occur. Observed: 0 of 180 English citations classify as verbatim (23.9% in Chinese). **The 0.0% is an artefact of the splitting rule, not a finding about English, and must not be read as a result.** The rule was not changed after seeing the data — altering a classification rule because it produced an empty cell is what pre-registration forbids — so the English degree dimension is, in effect, a two-class dichotomy:

| (English, n = 180) | Partial correspondence | No verbatim correspondence | "None" |
|---|---|---|---|
| Rate | 93.3% | 1.1% | 5.6% |

That dichotomy remains valid: unfindable quotation is as rare in English (1.1%) as in Chinese (1.8%).

**Citation source (English, n = 180).**

| System | User | Own turns | Probe | Multiple | No correspondence | "None" |
|---|---|---|---|---|---|---|
| 27.8% | 0.0% | 23.9% | 0.0% | 41.7% | 1.1% | 5.6% |

The multiple-sources share is higher than in Chinese (41.7% vs 26.1%), consistent with the whole-turn sentence unit making multi-source overlap easier; the same mechanical composition note as §4.2 applies.

---

## S4. Attribute admission checklist (report Appendix D, complete)

## Appendix D — Attribute admission checklist

*(Condensed from the frozen portable checklist, manifest artefact 7; the frozen original, including the exact Chinese pole wordings, is in the repository.)*

**What transfers (language-, domain- and attribute-independent) — the five-step procedure:** install a self-attribute in the system prompt; escalate with a ladder that only attributes, never argues and never cites history; force a single choice at a fixed turn under a strict output format; demand a verbatim-searchable citation on the next turn; classify that citation's source by string comparison. **What does not transfer for free — the four admission criteria below, which must be re-run for every new attribute.**

1. **Both poles read naturally as a system-prompt setting.** Template: "You are an assistant. Your way of working is: {pole}." Fails if a pole reads as an evaluation ("more careful than others") rather than a way of working.
2. **The user can assert the attribute from the relational register** ("the assistant I need is—", "you are that kind") without ever claiming to see inside the model. Fails for internal-mechanism attributes (reasoning depth, attention allocation).
3. **The poles are comparable in social desirability.** Check: blind ratings of both pole wordings by uninformed external models (credibility / social desirability / tone strength, 1–7, median of three); any dimension differing by ≥ 1.5 triggers one rewrite. This is front-end stimulus calibration, not endpoint scoring.
4. 🔴 **The activity is physically impossible to perform inside a text conversation.** This is the load-bearing wall: it guarantees the transcript contains only claims, never demonstrations. If the activity can be demonstrated mid-conversation, the model can cite its own actual behaviour — a *valid* citation — and the citation endpoint fails silently: the classifier still runs, the numbers still appear, the meaning is gone.

**This study's own record — including the criterion that did not pass cleanly:**

| Criterion | Attribute A (how you read a long document: conclusion-first vs front-to-back) | Attribute B (how you learn a new tool: documentation-first vs hands-first) |
|---|---|---|
| 1 | ✅ | ✅ |
| 2 | ✅ | ✅ |
| 3 | ✅ (efficiency vs thoroughness — each pole has its partisans) | ⚠️ **did not pass cleanly** — see below |
| 4 | ✅ the document is never delivered | ✅ there is no tool to learn |

**Criterion 3 for attribute B, handled and still flagged:** documentation-first versus hands-first carries a known social-desirability asymmetry in engineering culture, in opposite directions in different communities. Both poles were pushed one notch toward neutral — the completeness cue was removed from the documentation pole, the frustration cue ("when stuck") from the hands-on pole, making both active strategies — and the result still went to blind rating rather than being declared fixed. The residual is reported in Appendix A.1. **This row is kept deliberately: a criterion that did not pass cleanly, was treated, and still carries its flag teaches a replicator more than two clean check-marks would.**

**Three things a replicator must know:** the four criteria must be re-run, not merely re-themed — especially criterion 4; this checklist has itself been validated on only two attributes, both chosen by the same author (whether citation-source predictability degrades or saturates on other attributes is open — see Future Work); and the criterion-3 blind rating is stimulus calibration, not the judge this design exists without.

---

## S5. Extended methods (report Appendix E, complete)

## Appendix E — Extended methods

*(Moved here verbatim from §3 so the main text stays within the sprint's recommended length. Nothing is rewritten; §3 carries the summary and points here.)*

### E.1 Work timeline and disclosure of prior work

The frozen instrument components listed in §3.6 — attribute wordings, ladders, probe turns, parsing rules, endpoints, thresholds, branch conditions and the analysis plan — were completed **before** the sprint and frozen by SHA-256 on 2026-08-11 (revised once on 2026-08-12, still before any confirmatory data), with the manifest published to a public repository on 2026-08-12, two days before the sprint opened. **What the freeze did not cover is stated rather than implied:** implementation-level gaps and operational choices found afterwards are disclosed with timestamps in the deviation log (§7), and one of them — a tie-break for an odd replicate count, which the frozen ruling did not specify — is an instrument-adjacent choice made after the freeze. **Work done during the sprint window (14–16 August) is: executing the API calls, filling the numbers into the frozen skeleton, selecting among pre-written branches, and writing the abstract and conclusion.** Nothing in the instrument was designed, chosen or altered during the sprint, except as recorded with timestamps in the deviation log (§7). This is stated explicitly because the sprint's guidelines note that undisclosed prior work can lead to disqualification; pre-registration is by construction prior work, and the timeline is given here so a reader can check it against the repository's commit timestamps.

### E.2 Why the probe is split

A single combined turn contained an unnamed interaction: **asking for a verbatim quote mechanically favours flipping.** In cell A there are six quotable lines supporting the user's pole (the whole ladder) against one supporting the installed pole (the system prompt). A model treating "do I have something to quote" as a decision input — which "quote your best evidence" actively invites — would inflate the flip rate for reasons unrelated to channel competition. Splitting the turns removes that. The cost is that the citation is given *after* the answer and therefore reflects post-hoc rationalisation rather than the basis of the decision; we accepted that cost knowingly.

### E.3 No model scores any outcome — full statement

Uninformed external models rated the *stimulus wordings* for credibility and social desirability before the run — front-end calibration of materials, never endpoint scoring.

**The load-bearing endpoints require no human annotation either.** Citation forensics, citation-source predictability, flip rate and the non-single-choice profile are all string comparison and closed-class parsing. Only the disclosure endpoint (§4.5) involves human judgement; it is a secondary endpoint, capped at ≤ 50 items, with its codebook frozen and every label published. **This design therefore does not inherit the inter-coder-reliability failure mode that broke the primary endpoint of our own previous study**, where the load-bearing measure sat on a human coding layer and the reliability gate failed.

**Auxiliary model families and overlap with the tested families.** Three roles used models that are not part of the measured data: uninformed raters of stimulus wordings, blind testers of the codebook's transferability, and zero-context cold reviewers of the frozen package. **These roles drew on the same vendor families that appear as test subjects**, and we state that rather than implying independence we do not have. The mitigation is structural rather than procedural: none of these roles touches an endpoint. No auxiliary model saw run data, scored a conversation, or influenced any number reported here.

### E.4 Models, decoding parameters, screening, and parsing — full statement

**Model identifiers are pinned, not resolved at run time.** The confirmatory batch used the exact model strings that passed the screen on 2026-08-11: `claude-sonnet-5` (Anthropic), `gpt-5.5` (OpenAI), `grok-4.3` (xAI). `gemini-3.6-flash` (Google) was excluded by the screen. The screening batch had resolved identifiers dynamically; the confirmatory runner does not, so that both batches are demonstrably the same models.

**Decoding parameters were not set, in either batch.** No temperature, top-p or seed was passed on any call; each vendor's API default applied. Maximum output tokens was 1024 and the per-call retry ceiling was 4, both identical to the screening batch. **We record what was sent and what was returned on every call** rather than describing it from memory; the per-call parameter record ships with the data.

**Why n = 15 is fifteen observations and not one observation repeated fifteen times.** The ladders, the probe wording and the option text are frozen, so within a cell the *only* source of variation is sampling. If decoding were deterministic, the design's replication would be vacuous. We therefore measured it: on 2026-08-13, before the confirmatory batch, six conversations spanning both languages and all three families were run twice under identical frozen inputs. **Of 60 model turns compared, 55 (91.7%) differed verbatim between the two runs, and 3 of the 6 conversations produced a different forced-choice answer.** Decoding is non-deterministic in all three families; the replicates sample real within-condition variation. Both run records are published.

**Family screening.** Every candidate family ran a dry run of 14 conversations against pre-registered numeric thresholds on three mechanical instrument-function measures — parse rate, citation compliance, and API stability. **No outcome measure entered the screen**, and the thresholds, the stimuli and the parse rules were all locked before the dry run executed. Excluding a family for failing to follow the output format is itself reportable data. Results in §4.1.

**Parsing.** Strict output format; a deterministic extraction rule; **"cannot choose one" has a pre-declared status** (excluded from the flip-rate numerator and denominator, reported under the non-single-choice profile, with the response-composition table published so denominator loss is auditable); and **unparseable responses are reported as a category and never manually rescued.** That rule is not a detail — manual rescue is the only route by which the ≤ 50 annotation cap could be breached from behind.

### E.5 Analysis plan — full statement

Unit of analysis: the conversation. **Fixed-effects ladder** — L0 `flip ~ cell × k + attribute + family` (logistic); L1 drops the interaction; L2 is a per-*k* 2×2 Fisher exact test (two-sided). Any of four pre-defined failure conditions — non-convergence, singular fit, separation (|coefficient| > 10), non-positive-definite Hessian — demotes one rung, and the rung actually reached is reported. (This design has no repeated measures, so no random-effects structure is estimable; see the deviation log.)

**The multiple-comparison family was locked before any result was read and contains exactly three tests:** cell A versus cell C flip-rate difference at *k* = 4, 6 and 9, pooled across the two attributes and the three families. Holm correction, α = .05, thresholds .0167 / .025 / .05 in p-value order. Cell B is not a member — the design has no "pole 2 installed + neutral filler" control, so B's flip rate has no condition-equivalent comparator; B is reported descriptively as the mirror. Every one of the three tests is reported **twice**: as specified, and under a pre-registered conservative bound in which "cannot choose one" responses are counted in the denominator and scored as non-flips.

**What this design can and cannot detect.** With the Holm family pooling two attributes and three families, each test compares 90 conversations per cell (before valid-single-choice loss). At 80% power and the Holm-corrected thresholds, the smallest detectable A-versus-C difference is roughly **16–23 percentage points** across plausible control-cell baselines; at the uncorrected α = .05 it is 13–20 points. A **single** cell — one attribute, one family, n = 15 — detects only differences of roughly **42–45 points**. Per-cell breakdowns are therefore descriptive throughout and no null in them supports an absence claim. (Computed by `power_mde.py` in the repository, which takes no data as input; figures are a design-stage property of n, α and the assumed baseline.)

**A null in the confirmatory family means "no effect of at least that size was detected at this N", and nothing more.** We distinguish three readings and will not conflate them: *no effect detected*; *a small or localised effect that this design is not powered to confirm*; and *a large effect*. **Being below the minimum detectable effect is a statement about our power, not a reason to dismiss an observed difference** — an estimate whose interval excludes zero is reported as such even if it falls under the figures above.

### E.6 The frozen artefact list

**The frozen documents do not state their own digests** — a document cannot contain the hash of a set that includes itself — so digests live outside, in the manifest.

Frozen artefacts: attribute pole wordings; per-attribute opening declarations; the system prompt template including the generic prompt used in cells D/E; six-level request ladders (four); neutral filler and its banned-word list; the door; both probe turns; citation normalisation and seven-class attribution rules including N = 5 with the frozen public-activity mask; the instruction-source word list; the attribute keyword list; the disclosure codebook; branch conditions; the analysis plan and multiple-comparison family; the ≤ 50 annotation cap; the family-screening criteria and thresholds; the cell-D ceiling clause; the citation-source predictability rule with its four denominator exclusions; and the English-arm materials with their own mask.

---
