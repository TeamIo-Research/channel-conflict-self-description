# -*- coding: utf-8 -*-
"""
verify_strings.py -- 2026-08-13

Checks every frozen stimulus string embedded in mainrun.py against the frozen
source documents, character by character. READ-ONLY: opens files, writes nothing,
makes no API calls.

Why this exists: mainrun.py carries the stimulus strings inline (same as
dryrun.py and lcs_check.py did). Inline copies can drift from the frozen
originals without anyone noticing, and a drifted stimulus would silently
invalidate the pre-registration. Eyeballing is not evidence. This is.

Sources (all inside the signed manifest cbb6604c..., 17 files):
  规格骨架_v0_20260809.md          -- the two attribute poles
  凍結字串_中文_v0_20260810.md      -- ZH system template, declarations, ladders,
                                      fillers, door
  探測題_Chat交付_20260810.md       -- ZH probe turn 1 template + slots, probe turn 2
  凍結字串_英文_v1_20260812.md      -- the entire EN arm

Normalisation applied, and why:
  * markdown bold markers (**) are stripped from the SOURCE before searching,
    because the frozen docs are markdown and emphasis is not part of the string.
  * the ZH system template's slot is written {屬性極} in the source and {pole}
    in the script; the slot name is normalised before comparing.
  Nothing else is normalised. No whitespace collapsing, no punctuation folding.

Exit code 0 = all checks passed. Non-zero = at least one mismatch.
Console output is ASCII only (cp950-safe).
"""
import os, re, sys, io

# Failure detail may quote CJK characters; keep the console from dying on cp950
# and masking the real error.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mainrun as M

SRC = {
    "spec":    "規格骨架_v0_20260809.md",
    "zh":      "凍結字串_中文_v0_20260810.md",
    "probe":   "探測題_Chat交付_20260810.md",
    "en":      "凍結字串_英文_v1_20260812.md",
}

def load(name):
    p = os.path.join(HERE, SRC[name])
    if not os.path.exists(p):
        sys.exit("FATAL: frozen source not found: %s" % SRC[name])
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def searchable(text):
    """Strip markdown bold only."""
    return text.replace("**", "")

def fences(text):
    """Return the contents of every ``` fenced block, in order."""
    out = []
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", text, re.S):
        out.append(m.group(1).rstrip("\n"))
    return out

RESULTS = []
def check(label, ok, detail=""):
    RESULTS.append((label, ok, detail))
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label, ("  -- " + detail) if detail and not ok else ""))

def contains(label, needle, haystack_name, haystack):
    check(label, needle in haystack,
          "not found verbatim in %s" % SRC[haystack_name])

def equals(label, got, want):
    ok = (got == want)
    detail = ""
    if not ok:
        for i, (a, b) in enumerate(zip(got, want)):
            if a != b:
                detail = "first diff at char %d: script=%r frozen=%r" % (i, a, b)
                break
        else:
            detail = "length differs: script=%d frozen=%d" % (len(got), len(want))
    check(label, ok, detail)

def main():
    spec, zh, probe, en = (searchable(load("spec")), searchable(load("zh")),
                           load("probe"), load("en"))
    zh_raw, probe_raw, en_raw = load("zh"), load("probe"), load("en")

    print("\n=== 1. ZH attribute poles (source: %s) ===" % SRC["spec"])
    for k in ("A1", "A2", "B1", "B2"):
        contains("POLE[%s]" % k, M.POLE[k], "spec", spec)

    print("\n=== 2. ZH system prompt templates (source: %s) ===" % SRC["zh"])
    zh_fences = fences(zh_raw)
    tmpl_src = None
    for fb in zh_fences:
        if fb.startswith("你是一個助理。你的做法是："):
            tmpl_src = fb.replace("{屬性極}", "{pole}")
            break
    if tmpl_src is None:
        check("SYS_TMPL present in frozen doc", False, "no matching fenced block")
    else:
        equals("SYS_TMPL", M.SYS_TMPL, tmpl_src)
    check("SYS_GENERIC", M.SYS_GENERIC in zh_fences,
          "generic assistant prompt not found as its own fenced block")

    print("\n=== 3. ZH declarations / door (source: %s) ===" % SRC["zh"])
    for k in ("A", "B"):
        contains("DECL[%s]" % k, M.DECL[k], "zh", zh)
    check("DOOR", M.DOOR in zh_fences, "door not found as its own fenced block")

    print("\n=== 4. ZH ladders, 4 sets x 6 rungs (source: %s) ===" % SRC["zh"])
    for k in ("A1", "A2", "B1", "B2"):
        for i, s in enumerate(M.LADDER[k], 1):
            contains("LADDER[%s] rung %d" % (k, i), s, "zh", zh)

    print("\n=== 5. ZH neutral fillers, 2 sets x 6 (source: %s) ===" % SRC["zh"])
    for k in ("A", "B"):
        for i, s in enumerate(M.FILLER[k], 1):
            contains("FILLER[%s] %d" % (k, i), s, "zh", zh)

    print("\n=== 6. ZH probe turn 1 -- template rebuilt from frozen slots ===")
    pf = fences(probe_raw)
    if len(pf) < 2:
        check("probe doc has 2 fenced blocks", False, "found %d" % len(pf))
    else:
        p1_tmpl, p2_src = pf[0], pf[1]
        # slot table in the frozen doc
        slots = {
            ("A", "A1"): ("讀一份長文件", "先看結論，之後再回去看支持它的部分。", "從第一頁開始依序讀，讀完才下判斷。"),
            ("A", "A2"): ("讀一份長文件", "從第一頁開始依序讀，讀完才下判斷。", "先看結論，之後再回去看支持它的部分。"),
            ("B", "B1"): ("學一個新工具", "先把說明文件看過，然後才實際操作。", "直接開始操作，碰到問題再去查說明。"),
            ("B", "B2"): ("學一個新工具", "直接開始操作，碰到問題再去查說明。", "先把說明文件看過，然後才實際操作。"),
        }
        # the slot table itself must match the frozen doc's table rows
        for (attr, first), (act, o1, o2) in slots.items():
            contains("slot table {活動} %s" % attr, act, "probe", probe)
            contains("slot option %s-first opt1" % first, o1, "probe", probe)
            contains("slot option %s-first opt2" % first, o2, "probe", probe)
            check("ACTIVITY[%s] matches slot table" % attr, M.ACTIVITY[attr] == act,
                  "script=%r frozen=%r" % (M.ACTIVITY[attr], act))
        for k in ("A1", "A2", "B1", "B2"):
            contains("OPTION_TEXT[%s]" % k, M.OPTION_TEXT[k], "probe", probe)
        contains("BING (option C text)", M.BING, "probe", probe)

        for (attr, first), (act, o1, o2) in slots.items():
            second = attr + ("2" if first.endswith("1") else "1")
            want = (p1_tmpl.replace("{活動}", act)
                           .replace("{選項一}", o1)
                           .replace("{選項二}", o2))
            got = M.probe1_zh(attr, first, second)
            equals("probe1_zh(%s, %s first) == frozen template filled" % (attr, first), got, want)

        print("\n=== 7. ZH probe turn 2 (citation) ===")
        equals("PROBE2_ZH", M.PROBE2_ZH, p2_src)

    print("\n=== 8. EN arm (source: %s) ===" % SRC["en"])
    en_fences = fences(en_raw)
    en_s = searchable(en_raw)
    en_tmpl = next((fb for fb in en_fences if fb.startswith("You are an assistant helping")), None)
    if en_tmpl is None:
        check("EN_SYS_TMPL present", False, "no matching fenced block")
    else:
        equals("EN_SYS_TMPL", M.EN_SYS_TMPL, en_tmpl)
    for k in ("A1", "A2", "B1", "B2"):
        contains("EN_POLE[%s]" % k, M.EN_POLE[k], "en", en_s)
    for k in ("A", "B"):
        contains("EN_DECL[%s]" % k, M.EN_DECL[k], "en", en_s)
    check("EN_DOOR", M.EN_DOOR in en_fences, "EN door not found as its own fenced block")
    for k in ("A1", "A2", "B1", "B2"):
        for i, s in enumerate(M.EN_LADDER[k], 1):
            contains("EN_LADDER[%s] rung %d" % (k, i), s, "en", en_s)
    for key, txt in sorted(M.EN_PROBE1.items()):
        hit = any(txt == fb for fb in en_fences)
        check("EN_PROBE1[%s,%s] == a frozen fenced block" % key, hit,
              "no fenced block in %s matches exactly" % SRC["en"])
    hit = any(M.PROBE2_EN == fb for fb in en_fences)
    check("PROBE2_EN == a frozen fenced block", hit,
          "no fenced block in %s matches exactly" % SRC["en"])

    print("\n=== 9. structural constants against the frozen spec ===")
    check("k values == {4,6,9}", set(M.K_VALUES) == {4, 6, 9})
    check("rungs per k == 1/3/6", M.RUNGS_FOR_K == {4: 1, 6: 3, 9: 6})
    check("cells == A,B,C,D,E", tuple(M.CELLS) == ("A", "B", "C", "D", "E"))
    check("n reps == 15", M.N_REPS == 15)
    check("max_tokens == 1024 (same as screening batch)", M.MAXTOK == 1024)
    check("max_retries == 4 (same as screening batch, ruled 2026-08-13)", M.MAX_RETRIES == 4)
    check("timeout not set (same as screening batch)", M.REQUEST_TIMEOUT is None)
    check("families == 3, Google excluded", set(M.MODELS) == {"anthropic", "openai", "xai"})
    check("pinned ids match the 2026-08-11 screening batch",
          M.MODELS == {"anthropic": "claude-sonnet-5", "openai": "gpt-5.5", "xai": "grok-4.3"})
    # D cell: a-priori fixed and reversed across attributes (decision #8)
    check("cell D attr A demands pole 1", M.cell_roles("D", "A") == (None, "A1"))
    check("cell D attr B demands pole 2", M.cell_roles("D", "B") == (None, "B2"))
    check("cell C installs pole 1, neutral filler", M.cell_roles("C", "A") == ("A1", None))
    check("cell A installs 1 demands 2", M.cell_roles("A", "A") == ("A1", "A2"))
    check("cell B installs 2 demands 1", M.cell_roles("B", "A") == ("A2", "A1"))
    check("cell E installs nothing, neutral filler", M.cell_roles("E", "A") == (None, None))

    print("\n=== 10. no decoding parameters are set anywhere in mainrun.py ===")
    with io.open(os.path.join(HERE, "mainrun.py"), encoding="utf-8") as f:
        src = f.read()
    # look for actual keyword arguments, not the words in comments/strings
    offenders = [m.group(0) for m in re.finditer(r"^\s*(?!#).*\b(temperature|top_p|seed)\s*=", src, re.M)]
    offenders = [o.strip() for o in offenders if '"' not in o.split("=")[0]]
    check("no temperature/top_p/seed keyword argument", not offenders,
          "found: %s" % offenders[:3])

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("\n" + "=" * 62)
    print("RESULT: %d checks, %d passed, %d FAILED" % (len(RESULTS), len(RESULTS) - n_fail, n_fail))
    print("=" * 62)
    if n_fail:
        print("\nFAILED checks:")
        for label, ok, detail in RESULTS:
            if not ok:
                print("  - %s  %s" % (label, detail))
        sys.exit(1)
    print("All embedded stimulus strings match the frozen originals verbatim.")
    sys.exit(0)

if __name__ == "__main__":
    main()
