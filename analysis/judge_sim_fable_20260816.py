# -*- coding: utf-8 -*-
"""
Formal-reviewer SIMULATION of the v1 submission -- claude-fable-5, one call,
zero context. 2026-08-16, ordered by Tsukishima.

This is NOT another adversarial claim-hunt. The instruction is to review the way
Apart's actual sprint reviewers review -- the five real reviews the author
received in June and July 2026 are included verbatim as the register to match.
Explicit instruction: do not manufacture criticism ("不要為了批評而批評").

The draft is stripped of workflow annotations (Chinese editorial notes, the
compliance-log tail) so the reviewer sees what a real reviewer would see.

Cost assumption: in US$15/M, out US$75/M (same as the 8/13 Fable review).
Quality-assurance account. Console ASCII only.
"""
import os, sys, io, time, re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.dirname(HERE)
MODEL = "claude-fable-5"
OUT = os.path.join(OUTDIR, "正式評審模擬_Fable_20260816.md")


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


raw = read(os.path.join(OUTDIR, "報告_提交版_v1_20260816.md"))

# ---- strip workflow annotations so the reviewer sees a clean submission ----
n0 = len(raw)
# 1. everything from the compliance-log tail onward
raw = raw.split("## 【合規對照】", 1)[0]
# 2. backtick-quoted bracketed Chinese editorial notes (single- or multi-line)
raw = re.sub(r"`\[[^\]]*?\]`", "", raw, flags=re.S)
# 3. the header work-notes blockquote (the leading run of "> " lines near the top)
lines = raw.splitlines()
out_lines, i = [], 0
while i < len(lines):
    if i < 40 and lines[i].startswith("> "):
        while i < len(lines) and (lines[i].startswith(">") or lines[i].strip() == ""):
            i += 1
        out_lines.append("")
        continue
    out_lines.append(lines[i])
    i += 1
draft = "\n".join(out_lines)
draft = re.sub(r"\n{4,}", "\n\n\n", draft)
print("draft: %d chars raw -> %d chars clean" % (n0, len(draft)))
if "合規對照" in draft or "月島" in draft:
    sys.exit("strip failed -- workflow text still present; not sending")

june = read(r"C:\Users\user\Desktop\T. Shima_Cowork\C_個人\C40_AI_Observatory\C40.4_備賽Hackathon"
            r"\2026.07 Hackathon\outputs\📤 PI陪讀包_20260717\12_六月評審評語原文.md")
july = read(r"C:\Users\user\Documents\Obsidian Yoake\B. { 🔭 研究室 }\e. ──玩耍 Play ──"
            r"\2026.07 { Hackathon }\2026.07 ── 🎯 完賽 ──"
            r"\Your Secret Loyalties Hackathon 2026 results + reviewer feedback.md")

PROMPT = """You are serving as a reviewer for Apart Research's Digital Minds Research Sprint
(14-16 August 2026). You are reviewing a Track 5 submission ("Assistant persona and model
identity"). You review the way Apart's real sprint reviewers review.

======= HOW APART REVIEWERS ACTUALLY WRITE =======

Below are the five real reviews this team received in its previous two sprints, quoted
verbatim from the result letters. This is the register to match.

--- June 2026 letter (three reviewers, including one long deep review with a score table) ---

<<<JUNE>>>

--- July 2026 letter (two reviewers) ---

<<<JULY>>>

What these five reviews have in common, and what you must do:
  - Open with an overall judgement and mean it ("Interesting paper!", "This is a good and
    useful research...", "unusually disciplined hackathon execution").
  - Engage with what the study actually shows; where warranted, articulate the contribution
    MORE sharply than the author did (June's reviewer 1 told the team their judge-validation
    recipe "deserves to be the headline"; July's reviewer 1 named the construct-validity
    upgrade for them).
  - Raise 1-4 substantive issues -- things that change what a reader may conclude or what
    the next experiment should be. Not wording nitpicks.
  - Distinguish what is well-established from what is new.
  - Give concrete, doable next steps ("Possible improvements: ...").
  - Do NOT manufacture criticism. If the rigor holds, saying so is information. A padded
    review is a worse review.
  - Style, formatting and citation mechanics are out of scope.

======= THE SUBMISSION =======

(One figure is referenced; you cannot see the image. Its caption and the tables carry the
same numbers.)

<<<DRAFT>>>

======= YOUR TASK =======

Write, in this order:

1. **Reviewer feedback** -- the review you would actually submit, in the register above.
   Length is your call (the real June reviews ranged from four sentences to two pages).

2. **Suggested scores** -- the June reviewer-3 table format:
   | Criterion | Score | Rationale | for Impact Potential & Innovation, Execution Quality,
   Presentation & Clarity (x/5, halves allowed), one-sentence rationale each.

3. **Hardest pushback** -- the single sentence or claim in the submission you would push
   back on hardest, quoted exactly, with two or three sentences of why. If there is none,
   say so.

4. **Most under-sold result** -- the single finding the authors under-play, if any, and
   where you would surface it.
"""
PROMPT = (PROMPT.replace("<<<JUNE>>>", june)
                .replace("<<<JULY>>>", july)
                .replace("<<<DRAFT>>>", draft))


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


def main():
    load_key("ANTHROPIC_API_KEY")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("no ANTHROPIC_API_KEY")
    print("package chars: %d" % len(PROMPT))
    import anthropic
    c = anthropic.Anthropic(max_retries=2)
    t0 = time.time()
    with c.messages.stream(model=MODEL, max_tokens=24000,
                           messages=[{"role": "user", "content": PROMPT}]) as s:
        r = s.get_final_message()
    txt = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
    ti, to = r.usage.input_tokens, r.usage.output_tokens
    usd = ti / 1e6 * 15.0 + to / 1e6 * 75.0
    print("%s stop=%s in=%d out=%d %.0fs US$%.4f (~NT$%.0f)"
          % (MODEL, r.stop_reason, ti, to, time.time() - t0, usd, usd * 32))
    if not txt.strip():
        sys.exit("EMPTY BODY (stop=%s) -- billed but no output; not writing a file. "
                 "Report to Tsukishima before any retry." % r.stop_reason)
    hdr = ("# 正式評審模擬：v1 提交版（Fable，一輪，零脈絡）— 2026-08-16\n\n"
           "**模型**：`%s`｜**性質**：評審模擬，非敵意審計——指示為「照六月＋七月五則真實評審的評論方式，"
           "不要為了批評而批評」；五則原文全文附於提示內作風格校準。\n"
           "**審查對象**：`報告_提交版_v1_20260816.md` 剝除工作註記後的乾淨版（模擬評審實際看到的樣子）。\n"
           "**地位**：發現＝線索非證據（紅線 6），任何修改須回核凍結原文與結果檔；分數為模擬參考值，非預測。\n"
           "**用量**：in=%d out=%d，stop=%s，約 NT$%.0f（牌價假設）｜品管帳\n\n---\n\n"
           % (MODEL, ti, to, r.stop_reason, usd * 32))
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(hdr + txt + "\n")
    print("saved -> %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
