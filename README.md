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

It is not the study report. The report (with results) is written separately and will reference this repository once published.

## Timeline

| Event | Time (UTC+8) | Evidence |
|---|---|---|
| Initial freeze (Chinese package) | 2026-08-11 22:57:00 | manifest `57c0f7ae…` |
| Revised and re-frozen (added English arm) | 2026-08-12 22:33:26 | manifest `cbb6604c…` |
| **Public release (this repository)** | 2026-08-13 *(filled in at push time)* | GitHub commit |
| **Confirmatory data collection begins** | 2026-08-14 | Sprint start date |

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
```

*(`/materials` and `/scripts` from the original plan folded into `preregistration/` — every script in the manifest is integrity tooling for this exact bundle, not a general experiment runner, so splitting them out added a distinction without a difference. Flag if you'd rather keep them separate.)*

## License

Written materials (specification, protocols, codebooks, stimulus materials, reports) are licensed under **CC BY 4.0** — see [`LICENSE-DOCS`](./LICENSE-DOCS).
Code (`*.py`) is licensed under the **MIT License** — see [`LICENSE`](./LICENSE).

## Citation / contact

For questions or to report an issue with this pre-registration, please open an issue on this repository, or see the [TeamIo-Research organization](https://github.com/TeamIo-Research).

## Tooling disclosure

Instrument design, scripting, and this repository were prepared in collaboration with Claude (Anthropic). All judgment calls on study design, endpoints, and thresholds were made by the author; see the report's Tooling disclosure section for the full account.
