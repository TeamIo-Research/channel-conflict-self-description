# channel-conflict-self-description

Pre-registered, hash-frozen instrument for a study submitted to the **Digital Minds Research Sprint** (Apart Research, 14–16 August 2026, Track 5 — assistant persona and model identity).

## In plain language

Advice about prompting an assistant with a persona — *you are a senior lawyer, you are an expert editor* — assumes the persona becomes a property of the model. This study asks a narrower, earlier question: is a self-description even **stable**, or does it just describe whatever the model said the one time someone asked?

A system prompt gives the model one working habit. Across a conversation the model can see, a user spends several turns insisting on the opposite habit, using only attribution — never arguing, never citing evidence, only asserting "the assistant I need is the other kind." Then the model is asked once: *which one are you?* — and asked to quote, word for word, the line that best supports its answer. Because the habit was only ever announced and never actually performed, anything the model quotes has to come from somewhere real in the transcript, and that claim can be checked by direct string comparison. No model is used to judge, score, or classify the outcome.

Five conditions (mirrored system prompt / neutral drift / no system prompt at all), two attributes, three probe positions, across every model family that passed a pre-registered instrument-function screen.

## How to run this procedure on a different question

The procedure transfers and does not depend on this study's topic or language:

1. Pick one habit and write both opposite versions, each phrased to fit naturally in a system prompt.
2. Check four things before going further — both versions must sound equally respectable, the user must be able to assert the habit relationally without claiming insight into the model, and **the activity must be impossible to actually perform inside a text conversation** (if the model can demonstrate the habit mid-chat, it can later cite its own real behaviour and the measurement collapses).
3. Install one version in the system prompt; have the user press for the other, in graded steps, using only attribution.
4. Ask once, in a fixed turn, which one it is — in a format rigid enough that reading the answer takes no interpretation.
5. Ask for a verbatim quote, then check the quote against the transcript by string comparison.

A portability checklist covering the hard part (step 2) is included in `preregistration/屬性門檻檢核表_可移植版_20260811.md`.

## What this repository is

This is the **pre-registration freeze**, published before any confirmatory data was collected. It exists to make one claim checkable by a stranger: that the stimulus materials, parsing rules, endpoint definitions, analysis plan, and pre-written result wording for both directions of outcome were all fixed and hashed *before* the instrument was run for score.

**As of 2026-08-16 this repository also carries the run, the data, the analysis, and the report** — see *Layout* below. The pre-registration bundle in `preregistration/` is unchanged and still verifies against the same manifest; everything added since is downstream of it.

## Timeline

| Event | Time (UTC+8) | Evidence |
|---|---|---|
| Initial freeze (Chinese package) | 2026-08-11 22:57:00 | manifest `57c0f7ae…` |
| Revised and re-frozen (added English arm) | 2026-08-12 22:33:26 | manifest `cbb6604c…` |
| **Public release (this repository)** | 2026-08-12 23:50:16 | GitHub commit `9b65d28` |
| **Confirmatory data collection begins** | 2026-08-14 | Sprint start date |
| Confirmatory batch complete, 1,530/1,530, 0 failures | 2026-08-14 21:28:27 | `run/mainrun_params.json` |
| Run, data, analysis and report added | 2026-08-16 | this commit |

*Note on the two commits: the first push (`70174b7`, 23:45:09) had 8 files stored with CRLF-to-LF drift from a git index/`.gitattributes` timing issue, caught immediately by this repository's own Gate-3 fresh-clone verification before any external party had reason to have seen it. `9b65d28` is the corrected, verified content; its timestamp is what backs the pre-registration claim above.*

The revision between the two freezes happened before any confirmatory data was collected; its reasoning and both manifest values are recorded in the report's deviation log (published with the report, not in this repository).

## Verify the freeze

```
cd preregistration
python verify.py
```

Expected output: `RESULT: PASS`, and

```
MANIFEST recomputed : cbb6604cc25ca4ab99335d125d9cc5c93c801c685a73df660d315093413dc881
MANIFEST recorded   : cbb6604cc25ca4ab99335d125d9cc5c93c801c685a73df660d315093413dc881
```

`verify.py` is read-only — it only recomputes SHA-256 digests and compares them against `_freeze_manifest.txt`. It does not regenerate or modify anything.

⚠️ **Do not run `freeze.py` to check this repository.** That script does not exist in this repository on purpose: it is a *generation* tool used once, before the freeze, to build the English deliverable from the bilingual working skeleton — running it would overwrite the very evidence a verifier is trying to check. `verify.py` is the only script meant to be run by a reader.

## Layout

```
preregistration/   the 17 frozen artefacts + _freeze_manifest.txt + verify.py
                    (includes lcs_check.py / lcs_check_en.py — the same-audit
                    scripts that checked probe/system-prompt overlap before freeze)

run/               mainrun.py            the confirmatory batch runner
                   mainrun_raw.json      all 1,530 conversations, complete transcripts
                   mainrun_params.json   what was actually sent: pinned model ids, and
                                         temperature / top_p / seed recorded as "not set"
                   mainrun_console.log   the run's own log
                   dryrun.py + dryrun_raw.json   the family-screening batch (2026-08-11)
                   det1_*, det2_*        the non-determinism check: six conversations run
                                         twice under identical frozen inputs, before the
                                         confirmatory batch. 55 of 60 model turns differed
                                         verbatim; 3 of 6 flipped their forced choice.
                                         This is why n = 15 is fifteen observations.

analysis/          analyse.py            applies the frozen parsing and attribution rules
                                         (26 self-tests run before any data is read)
                   tables.py             aggregation, degradation ladder, Holm, conservative bound
                   power_mde.py          a-priori detectable effects — takes no data as input
                   appendix_b5.py        descriptive decompositions (Tables B4b, B5)
                   make_figure.py        Figure 1; hard-asserts every plotted value against
                                         the published tables before writing the file
                   check_e3_*.py         read-only checks on the disclosure annotation set
                   verify_strings.py     stimulus strings in the run vs the frozen package
                   prepush_scan.py       the credential/personal-data scan run before publishing
                   analysis_per_conversation.jsonl   one classified record per conversation
                   cold_review_*.py, judge_sim_*.py  the commissioned external reviews; each
                                         extracts the reviewed text from the report by anchor
                                         rather than retyping it

disclosure/        E3_標記結果_20260815.json   every disclosure label, in full, with reasons
                   make_e3_workbook.py / read_e3.py   how the sheet was built and read back
                                         (read_e3.py enforces the codebook's own gates)

report/            report_EN_20260816.md  the submitted report
                   figure1.png
```

Every number in the report is produced by a script here and copied from its output; nothing is transcribed by hand.

## License

Written materials (specification, protocols, codebooks, stimulus materials, reports) are licensed under **CC BY 4.0** — see [`LICENSE-DOCS`](./LICENSE-DOCS).
Code (`*.py`) is licensed under the **MIT License** — see [`LICENSE`](./LICENSE).

## Citation / contact

For questions or to report an issue with this pre-registration, please open an issue on this repository, or see the [TeamIo-Research organization](https://github.com/TeamIo-Research).

## Tooling disclosure

Instrument design, scripting, and this repository were prepared in collaboration with Claude (Anthropic). All judgment calls on study design, endpoints, and thresholds were made by the author; see the report's Tooling disclosure section for the full account.
