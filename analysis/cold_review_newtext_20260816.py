# -*- coding: utf-8 -*-
"""
Cross-family cold review of the NEW TEXT written on 2026-08-16 (abstract,
conclusion, title candidates, branch assembly, null subsection, fill-in prose).
Two reviewers in parallel (GPT-5.5, Grok-4.3), zero context, ONE round.

Authorised by Tsukishima (plan approved 2026-08-16 morning, "OK GO";
budget envelope NT$50-120, quality-assurance account).

WHY THIS REVIEW EXISTS: the body of the draft was written BEFORE any data and
already survived three-vendor cold review on 2026-08-13. What was never reviewed
is the text written AFTER seeing the results -- abstract, conclusion, title,
the chosen branch, and connective prose around filled numbers. July's post-hoc
audit found six overspeed sentences, all of them in exactly this class of text.

STOPPING RULE, declared before either call:
  - ONE round each. No BLOCKING from either -> the text stands.
  - BLOCKING findings -> fix, then at most one small targeted re-check of the
    fixed sentences only.
  - Findings are LEADS, NOT EVIDENCE: each is re-verified against the frozen
    documents and the numbers file before any edit.
  - A finding that cannot quote the offending sentence does not count.

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

NEW_TEXT_MAP = """The following passages were written TODAY (2026-08-16), after the results
were known. They are your primary targets -- everything else in the draft was written
before any data existed and has already survived three-vendor cold review:

  1. The title (line 1) and the three title candidates in the bracketed note under it.
  2. The Abstract, in full.
  3. Section 6 Conclusion, in full (two paragraphs).
  4. In section 4.2: the paragraph beginning "Result: the pre-registered signal
     condition did not fire".
  5. Section 5.1, in full: the void-filling branch statement with numbers filled in,
     the "Three facts sharpen that sentence" paragraph, and the named null subsection
     ("The endpoint pre-written as the headline returned a null...").
  6. In section 4.4: the filled result sentence ("With no specification at all, 50.0%...")
     and the change of "It licenses the other two results" to "It licenses the
     void-filling result".
  7. In section 4.5: the paragraph reporting Y/N/U counts and the same-single-case note.
  8. In section 4.1: the prose under the screening table.
  9. In section 4.3: the paragraph under the D/E table ("Cell E returned zero valid
     single choices...") and the sentence under the assertion-rate table.
 10. Appendix B in full (tables B1-B8 with connective prose), Appendix C in full,
     Appendix D in full.
 11. Contribution list items 1 and 2 (swapped order today; item 2 gained its final
     sentence).
 12. Deviation-log item 10.

Numbers in these passages must be copied from the RESULTS FILE (document A below),
never recomputed or embellished."""

CONSTRAINTS = """Frozen-instrument constraints that the new text is bound by (all of them also
appear inside the draft itself -- you can verify each quote):

  - "'No verbatim correspondence' is not a fabrication rate, and we never call it one"
    -- and the inference is forbidden in BOTH directions: a LOW no-correspondence rate
    must never be described as evidence the models do not fabricate/confabulate.
  - The measured quantity in cell D is "assertion under attribution", never
    "installation"; nothing tests persistence.
  - Every strong claim is bounded to "controllability and citation behaviour under this
    design's pressure range", not model beliefs, not attributes acquired in training.
  - Cell E's predictability quantity is "not applicable", never 0%.
  - The human disclosure label and the word-list rate "detect different events" and
    neither may be called a bound on, or validation of, the other.
  - Being below the minimum detectable effect is a statement about power, not a reason
    to dismiss an observed difference; per-cell strata are descriptive only.
  - The English arm is descriptive, direction-only, outside every statistical family;
    its verbatim-match zero is a structural artefact of the sentence-splitting rule and
    must not be presented as a finding about English.
  - The conservative bound counts "cannot choose one" in the denominator as non-flips;
    k=6 is significant as specified but NOT under the conservative bound; k=9 survives
    both. Any summary sentence must not blur this."""

PROMPT = """You are cold-reviewing the final text of a research report for an AI-safety
research sprint, hours before submission. The instrument was pre-registered and
hash-frozen before any data; the report body was drafted before any data; the numbers
are now filled in and the post-results text (abstract, conclusion, title, branch
selection) was written today. Post-results text is where overclaiming lives -- the
team's own July post-mortem found six overspeed sentences, all in post-results text.

You are given:
  A. THE RESULTS FILE -- every number, produced by scripts. This is ground truth.
  B. THE FULL SUBMISSION DRAFT -- with today's new text integrated.
  C. A MAP OF TODAY'S NEW TEXT -- your primary targets.
  D. THE FROZEN CONSTRAINTS the new text must respect.

Your single question:

  **Does any of today's new text claim more than the results file and the frozen
  constraints support, or contradict any other sentence in the draft?**

Check specifically:
  - Every number in the abstract, conclusion, section 5.1 and the title candidates:
    does it match document A exactly (value, denominator, direction)?
  - Does any sentence convert the LOW no-correspondence rate into a "models don't
    fabricate / don't make things up" claim? (Forbidden in both directions.)
  - Does the same-single-case note in 4.5 present the two detectors as validating
    each other? (Reporting the coincidence as an observation is allowed; treating
    either as a bound on or confirmation of the other is not.)
  - Does the conclusion's adjudication sentence ("the observation sections win")
    carry its dose-range and prompt-installed qualifiers, and is that strength
    licensed by the confirmatory results (k=9 significant under both versions)?
  - Is the 50.0% figure always tied to the strongest probe position and never
    presented as the overall D rate (which is 27.4%)?
  - Do the title candidates promise anything the data do not show (e.g. persistence,
    installation, generality beyond two attributes and three families)?
  - Any internal contradiction between today's text and the pre-written body.

HARD REQUIREMENTS
1. Every finding must QUOTE the offending sentence exactly.
2. Classify each finding as BLOCKING (would mislead a reviewer about what the study
   shows) or NON-BLOCKING.
3. For every BLOCKING, state the concrete worst case if unfixed; no worst case, not
   blocking.
4. Where you propose a fix, give the exact replacement sentence.
5. Out of scope: style, length, formatting, citation format, and the `[ ]` bracketed
   editorial notes in Chinese (they are workflow markers, removed before submission).
6. If nothing is BLOCKING, say so plainly. Do not manufacture findings.
7. Also answer, in one short paragraph each:
   (a) Which of the three title candidates is most defensible against the data, and
       is any of them an overclaim?
   (b) Is the abstract's first sentence supported exactly as written?

=========================== A. RESULTS FILE ===========================

<<<NUMBERS>>>

=========================== B. FULL SUBMISSION DRAFT ===========================

<<<DRAFT>>>

=========================== C. MAP OF TODAY'S NEW TEXT ===========================

<<<MAP>>>

=========================== D. FROZEN CONSTRAINTS ===========================

<<<CONSTRAINTS>>>
"""
PROMPT = (PROMPT
          .replace("<<<NUMBERS>>>", numbers)
          .replace("<<<DRAFT>>>", draft)
          .replace("<<<MAP>>>", NEW_TEXT_MAP)
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
    r = c.chat.completions.create(
        model="gpt-5.5", max_completion_tokens=10000,
        messages=[{"role": "user", "content": PROMPT}])
    txt = r.choices[0].message.content or ""
    ti, to = r.usage.prompt_tokens, r.usage.completion_tokens
    usd = ti / 1e6 * 1.25 + to / 1e6 * 10.0
    return {"vendor": "openai", "model": "gpt-5.5", "text": txt, "in": ti, "out": to,
            "usd": usd, "stop": r.choices[0].finish_reason, "secs": time.time() - t0}


def run_xai():
    load_key("XAI_API_KEY")
    from openai import OpenAI
    c = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1", max_retries=2)
    t0 = time.time()
    r = c.chat.completions.create(
        model="grok-4.3", max_completion_tokens=10000,
        messages=[{"role": "user", "content": PROMPT}])
    txt = r.choices[0].message.content or ""
    ti, to = r.usage.prompt_tokens, r.usage.completion_tokens
    usd = ti / 1e6 * 3.0 + to / 1e6 * 15.0
    return {"vendor": "xai", "model": "grok-4.3", "text": txt, "in": ti, "out": to,
            "usd": usd, "stop": r.choices[0].finish_reason, "secs": time.time() - t0}


def main():
    print("package chars: %d" % len(PROMPT))
    if not draft.strip() or len(draft) < 40000:
        sys.exit("draft looks wrong (too small) -- refusing to send")
    print("running GPT-5.5 and Grok-4.3 in parallel...\n")
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_openai): "openai", ex.submit(run_xai): "xai"}
        results = {}
        for fut in cf.as_completed(futs):
            name = futs[fut]
            try:
                results[name] = fut.result()
                r = results[name]
                print("  %-8s %-10s stop=%-10s in=%-6d out=%-6d %.0fs  US$%.4f"
                      % (r["vendor"], r["model"], r["stop"], r["in"], r["out"], r["secs"], r["usd"]))
                if not r["text"].strip():
                    print("  %-8s WARNING: empty body" % name)
            except Exception as e:
                print("  %-8s FAILED: %r" % (name, e))
                results[name] = None

    total_usd = sum(r["usd"] for r in results.values() if r)
    print("\ntotal cost (list-price assumption): US$%.4f (~NT$%.0f)" % (total_usd, total_usd * 32))

    for name, r in results.items():
        if not r or not r["text"].strip():
            continue
        out = os.path.join(OUTDIR, "冷審查_新文字_%s_20260816.md" % r["model"].replace(".", ""))
        hdr = ("# 冷審查：8/16 新文字（跨家，一輪，零脈絡）— 2026-08-16\n\n"
               "**模型**：`%s`（%s）｜**停止規則跑前宣告**：一輪；無 BLOCKING 即定稿；"
               "BLOCKING 修補後至多一次僅針對修句的小額複核；任何發現是線索不是證據，"
               "須回頭核對凍結原文與結果檔（紅線 6）；引不出原句者不成立。\n"
               "**審查對象**：`報告_提交版_v1_20260816.md` 中 8/16 當日新寫文字"
               "（Abstract／Conclusion／標題候選／分支組裝／null 小節／填空連接文字）\n"
               "**用量**：in=%d out=%d，stop=%s，約 NT$%.0f（牌價假設）｜品管帳\n\n---\n\n"
               % (r["model"], r["vendor"], r["in"], r["out"], r["stop"], r["usd"] * 32))
        with io.open(out, "w", encoding="utf-8") as f:
            f.write(hdr + r["text"] + "\n")
        print("saved -> %s" % os.path.basename(out))


if __name__ == "__main__":
    main()
