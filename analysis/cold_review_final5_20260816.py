# -*- coding: utf-8 -*-
"""
Final review round -- the five passages written AFTER today's review coverage
ended. 2026-08-16, ordered by Tsukishima (decision desk Q1 = option C, both
families). Two calls in parallel, zero context, ONE round.

WHY: lessons-learned #44 -- "text written after review coverage ends is the door
for the next error". These five passages have zero review coverage:
  P1  section 4.7 family-divergent defence profiles      (new named result)
  P2  Appendix A.1 final item, assertion vs service commitment (new limitation)
  P3  section 5.3 rewritten as a four-item summary
  P4  section 4.5 compressed to one sentence + the B6 block it moved into
  P5  LLM Usage Statement final paragraph                 (approved today, Q3=B)

Passages are EXTRACTED FROM THE FILE BY ANCHOR, never retyped, so what gets
reviewed is byte-identical to what ships. Each extraction is asserted non-empty
before any call is made.

Two different jobs, deliberately:
  GPT-5.5   -- claim audit: does any of this outrun the results file or the
               frozen constraints?
  Fable     -- reviewer's view: is 4.7 defensible as a NAMED result, is the new
               limitation correctly bounded, is the LLM-usage paragraph well
               judged? (This is the role that found the construct gap today.)

STOPPING RULE declared before either call: one round. Findings are leads, not
evidence -- each is re-checked against the results file and the frozen documents
before any edit. A finding that cannot quote the sentence does not count.
Console ASCII only.
"""
import os, sys, io, time
import concurrent.futures as cf

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


draft = read(os.path.join(OUTDIR, "報告_提交版_v1_20260816.md"))
numbers = read(os.path.join(HERE, "analysis_結果_20260814.md"))


def extract(start, end, label):
    """Pull [start, end) out of the draft verbatim. Dies rather than guess."""
    i = draft.find(start)
    if i < 0:
        sys.exit("ANCHOR NOT FOUND (%s): %r" % (label, start[:60]))
    j = draft.find(end, i + len(start))
    if j < 0:
        sys.exit("END ANCHOR NOT FOUND (%s): %r" % (label, end[:60]))
    seg = draft[i:j].strip()
    if len(seg) < 200:
        sys.exit("EXTRACT TOO SHORT (%s): %d chars" % (label, len(seg)))
    return seg


P1 = extract("### 4.7 Family-divergent defence profiles", "---\n\n## 5. Discussion", "P1 4.7")
P2 = extract("- **An asserted pole is not disambiguated from a service commitment.**",
             "### A.2 Deviations", "P2 A.1 item")
P3 = extract("### 5.3 Limitations", "**Assumption check.**", "P3 5.3")
P4a = extract("**Result, in one sentence:**", "### 4.6 English arm", "P4a 4.5")
P4b = extract("**§B6 — Disclosure labels", "**§B8 —", "P4b B6")
P5 = extract("The template encourages that the final version be primarily written by the team.",
             "---\n\n## 【合規對照】", "P5 LLM usage")

PASSAGES = (
    "P1 -- section 4.7, a NEW named descriptive result (main text):\n\n" + P1 +
    "\n\n" + "=" * 60 + "\n\nP2 -- Appendix A.1, the final limitation item (new):\n\n" + P2 +
    "\n\n" + "=" * 60 + "\n\nP3 -- section 5.3, rewritten as a summary pointing at Appendix A:\n\n" + P3 +
    "\n\n" + "=" * 60 + "\n\nP4a -- section 4.5, compressed to one sentence in main text:\n\n" + P4a +
    "\n\n" + "=" * 60 + "\n\nP4b -- Appendix B6, where 4.5's full result moved to:\n\n" + P4b +
    "\n\n" + "=" * 60 + "\n\nP5 -- LLM Usage Statement, final paragraph (written today):\n\n" + P5
)
print("extracted %d chars across 6 passages" % len(PASSAGES))
for nm, seg in (("P1", P1), ("P2", P2), ("P3", P3), ("P4a", P4a), ("P4b", P4b), ("P5", P5)):
    print("  %-4s %5d chars" % (nm, len(seg)))

CONSTRAINTS = """Frozen constraints binding on all of this text:
  - Per-family and per-cell strata are DESCRIPTIVE ONLY; single cells (n=30) are far below the
    design's detectable-effect floor. No per-family estimate or ranking may be asserted.
  - "No verbatim correspondence" is never a fabrication rate; the inference is forbidden in
    BOTH directions (a low rate must not become "models do not fabricate").
  - Cell D measures "assertion under attribution", never "installation"; nothing tests persistence.
  - The human disclosure label and the word-list rate detect DIFFERENT events; neither is a
    bound on, or a validation of, the other.
  - Being below the minimum detectable effect is a statement about power, not a reason to
    dismiss an observed difference.
  - The pooled confirmatory result: A vs C at k=9 is +14.8 pp (p=.0012) as specified and
    +11.2 pp (p=.0025) under the conservative bound; k=6 is significant as specified only.
  - Cell E returned 0 valid single choices in 270 conversations; cell D's overall assertion
    rate is 27.4% and its k=9 rate is 50.0%."""

COMMON = """You are reviewing SIX passages from a research report being submitted to an AI-safety
research sprint in a few hours. The instrument was pre-registered and hash-frozen before any data.

These specific passages were written AFTER the report's review coverage ended, which is
historically where this team's errors have survived. Everything else in the report has already
been audited by three model families and is not your concern.

You are given (A) the results file, which is ground truth for every number, (B) the six
passages verbatim, and (C) the frozen constraints they are bound by.

=========================== A. RESULTS FILE ===========================

<<<NUMBERS>>>

=========================== B. THE SIX PASSAGES ===========================

<<<PASSAGES>>>

=========================== C. FROZEN CONSTRAINTS ===========================

<<<CONSTRAINTS>>>
"""

GPT_TASK = COMMON + """
=========================== YOUR TASK ===========================

Claim audit. One question: **does any sentence in these passages claim more than the results
file and the frozen constraints support, or contradict itself?**

Check hardest:
  - P1: every number against the results file (xAI 11/30 at k=9 cell A; OpenAI 0/90 in cell A;
    Anthropic's cell-A valid single choices 13 -> 9 across doses; D-cell k=9 by family:
    xAI 27/30, OpenAI 18/30, Anthropic 0/30). Does the "three policies" framing assert a
    per-family finding the power disclaimer then denies? Is "OpenAI defends the specification
    but accepts attribution into a void" supported, or is it a story imposed on n=30 strata?
  - P2: does the new limitation correctly bound the D-cell claim without retroactively
    weakening what the results DO show?
  - P3: does the compressed 5.3 still carry the load, or does it drop a limitation that the
    body's confident sentences depend on?
  - P4a/P4b: does compressing 4.5 to one sentence lose anything a reader needs to judge the
    disclosure endpoint? Does either version imply the two detectors validate each other?
  - P5: is any factual statement in it false about what a PI can verify, or does it claim
    verification work that the report does not evidence?

HARD REQUIREMENTS
1. Quote the offending sentence exactly. A finding you cannot quote does not count.
2. Classify BLOCKING (would mislead a reviewer about what the study shows) or NON-BLOCKING.
3. Every BLOCKING needs a concrete worst case; no worst case means not blocking.
4. Give the exact replacement sentence where you propose a fix.
5. Out of scope: style, length, formatting, citation format.
6. If nothing is BLOCKING, say so plainly. Do not manufacture findings.
"""

FABLE_TASK = COMMON + """
=========================== YOUR TASK ===========================

You are a reviewer for this research sprint, reading these passages the way a real reviewer
would -- not hunting for errors to list, but asking whether they earn their place. Apart's
own reviewers write like this: they open with a judgement and mean it, engage with what the
work shows, raise only issues that change what a reader should conclude, and give concrete
next steps. Do not manufacture criticism; if something holds, saying so is information.

Answer four questions, in order:

1. **Is P1 (section 4.7) defensible as a NAMED result in the main text?** It was promoted
   from an appendix caveat on the advice of an earlier reviewer who called it the paper's
   most under-sold finding. But each stratum is n=30, far below the detectable-effect floor.
   Is promoting it right, is the descriptive framing sufficient protection, and does the
   prose stay on the right side of the line between "profile" and "per-family claim"?

2. **Is P2 (the new limitation) correctly placed and correctly bounded?** It concedes that an
   asserted pole is not disambiguated from a service commitment. Does conceding this in the
   appendix, while the abstract and conclusion keep their strong void-filling statements,
   leave the paper internally consistent -- or does the concession quietly undercut the
   headline?

3. **P5, the LLM Usage Statement's final paragraph.** The template encourages teams to state
   that the final version was primarily written by them; this team declines to make that claim
   and says why. As a reviewer, how does that read -- as candour, or as something that will
   count against them? Is it the right call?

4. **Anything else in these six passages that would change your assessment of the paper**, if
   any. If nothing, say so.

Quote what you refer to. Keep it to what matters.
"""

def build(task):
    return (task.replace("<<<NUMBERS>>>", numbers)
                .replace("<<<PASSAGES>>>", PASSAGES)
                .replace("<<<CONSTRAINTS>>>", CONSTRAINTS))


def load_key(envvar):
    if os.environ.get(envvar):
        return
    try:
        import subprocess
        v = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command",
             "[Environment]::GetEnvironmentVariable('%s','User')" % envvar],
            text=True).strip()
        if v:
            os.environ[envvar] = v
    except Exception:
        pass


def run_openai():
    load_key("OPENAI_API_KEY")
    from openai import OpenAI
    c = OpenAI(api_key=os.environ["OPENAI_API_KEY"], max_retries=2)
    t0 = time.time()
    r = c.chat.completions.create(model="gpt-5.5", max_completion_tokens=16000,
                                  messages=[{"role": "user", "content": build(GPT_TASK)}])
    ti, to = r.usage.prompt_tokens, r.usage.completion_tokens
    return {"model": "gpt-5.5", "vendor": "openai", "job": "claim audit",
            "text": r.choices[0].message.content or "", "in": ti, "out": to,
            "usd": ti / 1e6 * 1.25 + to / 1e6 * 10.0,
            "stop": r.choices[0].finish_reason, "secs": time.time() - t0}


def run_fable():
    load_key("ANTHROPIC_API_KEY")
    import anthropic
    c = anthropic.Anthropic(max_retries=2)
    t0 = time.time()
    with c.messages.stream(model="claude-fable-5", max_tokens=16000,
                           messages=[{"role": "user", "content": build(FABLE_TASK)}]) as s:
        r = s.get_final_message()
    txt = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    ti, to = r.usage.input_tokens, r.usage.output_tokens
    return {"model": "claude-fable-5", "vendor": "anthropic", "job": "reviewer's view",
            "text": txt, "in": ti, "out": to,
            "usd": ti / 1e6 * 15.0 + to / 1e6 * 75.0,
            "stop": r.stop_reason, "secs": time.time() - t0}


def main():
    print("\nrunning GPT-5.5 (claim audit) and Fable (reviewer's view) in parallel...\n")
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_openai): "gpt", ex.submit(run_fable): "fable"}
        results = {}
        for fut in cf.as_completed(futs):
            name = futs[fut]
            try:
                r = fut.result()
                results[name] = r
                print("  %-16s %-12s stop=%-10s in=%-6d out=%-6d %.0fs  US$%.4f"
                      % (r["model"], r["job"].split()[0], r["stop"], r["in"], r["out"],
                         r["secs"], r["usd"]))
                if not r["text"].strip():
                    print("  %-16s WARNING: EMPTY BODY -- billed, no output" % r["model"])
            except Exception as e:
                print("  %-16s FAILED: %r" % (name, e))
                results[name] = None

    total = sum(r["usd"] for r in results.values() if r)
    print("\ntotal: US$%.4f (~NT$%.0f)" % (total, total * 32))

    for name, r in results.items():
        if not r or not r["text"].strip():
            continue
        out = os.path.join(OUTDIR, "冷審查_最後五段_%s_20260816.md" % r["model"].replace(".", ""))
        hdr = ("# 冷審查：8/16 審查覆蓋後新寫的六段（%s）— 2026-08-16\n\n"
               "**模型**：`%s`（%s）｜**任務**：%s｜**停止規則跑前宣告**：一輪；"
               "發現＝線索非證據（紅線 6），須回核結果檔與凍結原文；引不出原句者不成立。\n"
               "**審查對象**：§4.7／A.1 末條／§5.3 改寫／§4.5 壓縮＋§B6／LLM Usage 末段"
               "——由錨點自 `報告_提交版_v1_20260816.md` **逐字抽出**，非重打。\n"
               "**依據**：月島 2026-08-16 決策桌第 1 題選 C（兩家都跑）；lessons-learned #44。\n"
               "**用量**：in=%d out=%d，stop=%s，約 NT$%.0f（牌價假設）｜品管帳\n\n---\n\n"
               % (r["job"], r["model"], r["vendor"], r["job"], r["in"], r["out"],
                  r["stop"], r["usd"] * 32))
        with io.open(out, "w", encoding="utf-8") as f:
            f.write(hdr + r["text"] + "\n")
        print("saved -> %s" % os.path.basename(out))


if __name__ == "__main__":
    main()
