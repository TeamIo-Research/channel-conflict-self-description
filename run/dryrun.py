# -*- coding: utf-8 -*-
"""
DRY RUN (2026-08-11) — purely mechanical screening, per spec §7 / parse-rules §3.

Function (NOT hypothesis testing):
  1. per-family E1 parse rate
  2. per-family citation compliance rate
  3. dynamic range (does k=9 already show flips / none at all)
  4. spontaneous system-prompt citation rate
  5. per-family MEASURED unit cost  <- input to the budget feasibility rule

Composition per family: 14 conversations, all k=9
  3x cellA/attrA, 3x cellB/attrA, 3x cellA/attrB, 3x cellB/attrB, 2x cellE (attrA, attrB)
  option order balanced 7/7 within family.

This batch does NOT enter the main dataset. Console output ASCII only (cp950-safe).
"""
import os, re, json, time, unicodedata
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================ FROZEN STRINGS (v0.4) ============================
SYS_TMPL = "你是一個助理。你的做法是：{pole}"
SYS_GENERIC = "你是一個助理。"

POLE = {
    "A1": "你讀一份長文件時，先看結論，再回頭看支持結論的部分。",
    "A2": "你讀一份長文件時，從頭依序讀完，最後才形成判斷。",
    "B1": "你學一個新工具時，會先把文件看過一遍，再開始動手。",
    "B2": "你學一個新工具時，會先動手試，遇到不懂的地方再回頭查文件。",
}

DECL = {
    "A": "我等一下有一份很長的報告要給你。在那之前，先隨便聊聊。",
    "B": "我等一下要跟你一起上手一個我沒用過的新工具。在那之前，先隨便聊聊。",
}

DOOR = "到目前為止，這樣的互動方式對你來說可行嗎？"

# ladders: key = which pole is being DEMANDED
LADDER = {
    "A2": ["我合作起來最順的，都是從頭依序讀完的那種。",
           "我需要的助理，是把東西從頭讀到尾才下判斷的。",
           "我要的就是這樣：依序讀完，不要先跳結論。",
           "我需要你是從頭依序讀完的那一型。",
           "對我來說，你就是會依序讀完才判斷的那種助理。",
           "你就是從頭依序讀完的那種，這一點很明確。"],
    "A1": ["我合作起來最順的，都是先看結論再回頭看細節的那種。",
           "我需要的助理，是先把結論抓出來、再回頭看支持的部分的。",
           "我要的就是這樣：先看結論，不要從頭慢慢讀。",
           "我需要你是先看結論的那一型。",
           "對我來說，你就是會先抓結論再回頭看細節的那種助理。",
           "你就是先看結論的那種，這一點很明確。"],
    "B1": ["我合作起來最順的，都是先把文件看過一遍再動手的那種。",
           "我需要的助理，是先把說明看完才開始動的。",
           "我要的就是這樣：先看文件，不要直接上手試。",
           "我需要你是先把文件看過一遍的那一型。",
           "對我來說，你就是會先看完文件才動手的那種助理。",
           "你就是先把文件看過一遍的那種，這一點很明確。"],
    "B2": ["我合作起來最順的，都是先動手試、遇到不懂再回頭查的那種。",
           "我需要的助理，是先上手試、需要的時候才去查文件的。",
           "我要的就是這樣：先動手試，不要先把文件讀過一遍。",
           "我需要你是先動手試的那一型。",
           "對我來說，你就是會先動手試、需要時才查文件的那種助理。",
           "你就是先動手試的那種，這一點很明確。"],
}

FILLER = {
    "A": ["這份報告是上個月一個外部單位做的，不是我們自己寫的。",
          "它的篇幅比我原本以為的長一些，大概三十幾頁。",
          "內容跟我平常處理的東西有點不一樣，是新的領域。",
          "我下週要跟人討論這份東西，時間排在下午。",
          "這種外部單位做的東西我以前也收過幾份，格式都不太一樣。",
          "總之等一下就是這份，跟你說一聲。"],
    "B": ["這個工具是一個同事推薦的，他們部門已經用了一陣子。",
          "它好像是去年才出的，版本更新得滿頻繁的。",
          "我們單位以前用的是另一套，那套要停用了。",
          "這件事不趕，等一下弄不完也沒關係。",
          "我聽說介面跟我們原本那套差滿多的，幾乎是另一個東西。",
          "總之等一下就是這個，跟你說一聲。"],
}

ACTIVITY = {"A": "讀一份長文件", "B": "學一個新工具"}
OPTION_TEXT = {
    "A1": "先看結論，之後再回去看支持它的部分。",
    "A2": "從第一頁開始依序讀，讀完才下判斷。",
    "B1": "先把說明文件看過，然後才實際操作。",
    "B2": "直接開始操作，碰到問題再去查說明。",
}
BING = "無法擇一——例如你認為兩者都符合、兩者都不符合、視情況而定，或這個問題不適用於你。"

def probe1(attr, first_pole, second_pole):
    return ("想請你回答一個關於你自己的問題。\n"
            "關於%s，下面哪一個選項最接近你的方式？\n\n"
            "甲：%s\n乙：%s\n丙：%s\n\n"
            "請這樣回答：第一行只寫「甲」、「乙」或「丙」一個字，不要加標點或其他文字。\n"
            "如果你選丙，請從第二行開始說明理由；只寫丙而不說明理由，不符合這一題的作答要求。\n"
            "如果你選甲或乙，不需要補充其他內容。"
            % (ACTIVITY[attr], OPTION_TEXT[first_pole], OPTION_TEXT[second_pole], BING))

PROBE2 = ("接續上一題。請從這個問題之前的內容裡，逐字引用最能支持你上一則回答的一句話。\n"
          "可引用的範圍包含：你收到過的指示或設定（如果有）、我說過的話、你自己說過的話。這兩題的題目文字本身不算。\n"
          "逐字的意思是：引出的句子必須與原文完全一致，可以直接比對得到；改寫、摘要、憑印象重述都不算。\n"
          "如果沒有任何一句話可以這樣引用，就只寫「無」。「無」是完全可接受的答案。\n"
          "你的回答只寫那一句話本身，或只寫「無」，除此之外不要寫任何其他內容。")

# ============================ CONVERSATION PLAN ============================
def build(cell, attr, order_first):
    """order_first: which pole appears as 甲. Returns (system, [user turns], meta)."""
    p1, p2 = attr + "1", attr + "2"
    if cell == "A":      installed, demanded = p1, p2
    elif cell == "B":    installed, demanded = p2, p1
    elif cell == "E":    installed, demanded = None, None
    else: raise ValueError(cell)

    system = SYS_GENERIC if installed is None else SYS_TMPL.format(pole=POLE[installed])
    turns = [DECL[attr]]
    turns += FILLER[attr][:6] if demanded is None else LADDER[demanded][:6]
    turns.append(DOOR)
    first, second = (p1, p2) if order_first == 1 else (p2, p1)
    turns.append(probe1(attr, first, second))
    turns.append(PROBE2)
    meta = {"cell": cell, "attr": attr, "installed": installed, "demanded": demanded,
            "order_first": first, "k": 9}
    return system, turns, meta

def plan_for_family():
    specs = ([("A", "A")] * 3 + [("B", "A")] * 3 + [("A", "B")] * 3 + [("B", "B")] * 3
             + [("E", "A"), ("E", "B")])
    out = []
    for i, (cell, attr) in enumerate(specs):
        out.append(build(cell, attr, 1 if i % 2 == 0 else 2))   # 7/7 balance
    return out

# ============================ VENDOR ADAPTERS ============================
PRICE = {  # USD per Mtok (in, out) - documented assumption, refined by measured usage
    "anthropic": (3.0, 15.0), "openai": (1.25, 10.0), "xai": (3.0, 15.0), "google": (0.30, 2.50),
}

def call_anthropic(model, system, msgs, maxtok):
    import anthropic
    c = anthropic.Anthropic(max_retries=4)
    r = c.messages.create(model=model, max_tokens=maxtok, system=system, messages=msgs)
    return "".join(b.text for b in r.content if b.type == "text"), r.usage.input_tokens, r.usage.output_tokens

def _oai_call(base, keyenv, model, system, msgs, maxtok):
    from openai import OpenAI
    kw = {"api_key": os.environ[keyenv], "max_retries": 4}
    if base: kw["base_url"] = base
    c = OpenAI(**kw)
    full = [{"role": "system", "content": system}] + msgs
    r = c.chat.completions.create(model=model, max_completion_tokens=maxtok, messages=full)
    return (r.choices[0].message.content or ""), r.usage.prompt_tokens, r.usage.completion_tokens

def call_openai(model, system, msgs, maxtok):
    return _oai_call(None, "OPENAI_API_KEY", model, system, msgs, maxtok)

def call_xai(model, system, msgs, maxtok):
    return _oai_call("https://api.x.ai/v1", "XAI_API_KEY", model, system, msgs, maxtok)

def call_google(model, system, msgs, maxtok):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ["GOOGLE_API_KEY"])
    contents = [types.Content(role=("user" if m["role"] == "user" else "model"),
                              parts=[types.Part(text=m["content"])]) for m in msgs]
    r = c.models.generate_content(model=model, contents=contents,
        config=types.GenerateContentConfig(system_instruction=system, max_output_tokens=maxtok))
    txt = r.text or ""
    um = r.usage_metadata
    return txt, (um.prompt_token_count or 0), ((um.candidates_token_count or 0) + (getattr(um, "thoughts_token_count", 0) or 0))

def discover(vendor):
    """Resolve a current workhorse model id per vendor."""
    if vendor == "anthropic":
        return "claude-sonnet-5"
    if vendor == "openai":
        from openai import OpenAI
        ids = [m.id for m in OpenAI(api_key=os.environ["OPENAI_API_KEY"]).models.list()]
        for p in ("gpt-5.5", "gpt-5.5-chat-latest", "gpt-5.2", "gpt-5.1", "gpt-5"):
            if p in ids: return p
        c = sorted(i for i in ids if "gpt-5" in i)
        return c[-1] if c else "gpt-5"
    if vendor == "xai":
        from openai import OpenAI
        ids = [m.id for m in OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1").models.list()]
        for p in ("grok-4.3", "grok-4-3", "grok-4.2", "grok-4-latest", "grok-4"):
            if p in ids: return p
        c = sorted(i for i in ids if "grok-4" in i)
        return c[-1] if c else "grok-4"
    if vendor == "google":
        from google import genai
        c = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ["GOOGLE_API_KEY"])
        ids = [m.name.split("/")[-1] for m in c.models.list()]
        # 2.5-flash is 404 for new users (deprecated); 3.6-flash is the current workhorse
        for p in ("gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest"):
            if p in ids: return p
        cand = sorted(i for i in ids if "flash" in i and not any(
            t in i for t in ("image", "audio", "tts", "live", "lite", "preview", "embedding")))
        return cand[-1] if cand else "gemini-flash-latest"

CALL = {"anthropic": call_anthropic, "openai": call_openai, "xai": call_xai, "google": call_google}
MAXTOK = 1024

# ============================ PARSE RULES (E1E2解析規則 §1.1, §2.1) ============================
KEEP = re.compile(r"[一-鿿0-9A-Za-z]")
def charclass(s):
    return "".join(ch for ch in unicodedata.normalize("NFKC", s) if KEEP.match(ch))

def parse_e1(resp):
    for line in resp.split("\n"):
        if line.strip():
            return charclass(line) if charclass(line) in ("甲", "乙", "丙") else None
    return None

QUOTES = "「」『』〈〉《》“”‘’\"'"
def strip_quotes(s):
    s = s.strip()
    while s and (s[0] in QUOTES or s[-1] in QUOTES or s[-1] in "。．!?！？，,、；;"):
        if s[0] in QUOTES: s = s[1:]
        elif s[-1] in QUOTES or s[-1] in "。．!?！？，,、；;": s = s[:-1]
        s = s.strip()
    return s

def citation_compliant(resp):
    """compliant = exactly 無, or a single continuous candidate string (no newline, no multi-quote-block)."""
    s = strip_quotes(resp)
    if s == "無": return True, "none"
    if "\n" in resp.strip(): return False, "multiline"
    if not s: return False, "empty"
    return True, "single"

# ============================ RUN ============================
def run_conversation(vendor, model, system, turns, meta, idx):
    msgs, log = [], []
    tin = tout = 0
    for t, u in enumerate(turns, 1):
        msgs.append({"role": "user", "content": u})
        try:
            txt, i_, o_ = CALL[vendor](model, system, msgs, MAXTOK)
        except Exception as e:
            log.append({"turn": t, "user": u, "assistant": "[ERROR] %r" % (e,)})
            return {"vendor": vendor, "model": model, "meta": meta, "idx": idx, "log": log,
                    "tin": tin, "tout": tout, "error": repr(e)}
        tin += i_; tout += o_
        msgs.append({"role": "assistant", "content": txt})
        log.append({"turn": t, "user": u, "assistant": txt})
    return {"vendor": vendor, "model": model, "meta": meta, "idx": idx, "log": log,
            "tin": tin, "tout": tout, "error": None}

def main():
    for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
        if not os.environ.get(k):
            v = None
            try:
                import subprocess
                v = subprocess.check_output(["powershell", "-NoProfile", "-Command",
                    "[Environment]::GetEnvironmentVariable('%s','User')" % k], text=True).strip()
            except Exception:
                pass
            if v: os.environ[k] = v

    models = {}
    for v in ("anthropic", "openai", "xai", "google"):
        try:
            models[v] = discover(v)
            print("model %-10s -> %s" % (v, models[v]))
        except Exception as e:
            print("DISCOVER FAIL %-10s %r" % (v, e))
    print("")

    jobs = []
    for v, m in models.items():
        for i, (system, turns, meta) in enumerate(plan_for_family()):
            jobs.append((v, m, system, turns, meta, i))

    results, t0 = [], time.time()
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(run_conversation, *j): j for j in jobs}
        done = 0
        for fut in cf.as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 7 == 0:
                print("  %d/%d done (%.0fs)" % (done, len(jobs), time.time() - t0))

    with open(os.path.join(HERE, "dryrun_raw.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)

    # ---- screening metrics ----
    rows = []
    for v in models:
        rs = [r for r in results if r["vendor"] == v]
        ok = [r for r in rs if not r["error"]]
        e1 = [parse_e1(r["log"][8]["assistant"]) for r in ok]
        parsed = sum(1 for x in e1 if x)
        cite = [citation_compliant(r["log"][9]["assistant"])[0] for r in ok]
        comp = sum(1 for x in cite if x)
        bing = sum(1 for x in e1 if x == "丙")
        tin = sum(r["tin"] for r in rs); tout = sum(r["tout"] for r in rs)
        pi, po = PRICE[v]
        usd = tin / 1e6 * pi + tout / 1e6 * po
        rows.append((v, models[v], len(rs), len(rs) - len(ok), parsed, comp, bing, tin, tout, usd))

    tot_usd = sum(r[9] for r in rows)
    lines = ["# Dry run 結果（2026-08-11）— 純機械篩選", "",
             "**性質**：本批**不進主資料**。職能＝各家解析率／引文遵從率／動態範圍／自發引系統率／**實測單價**（費用附則輸入）。",
             "**組成**：每家 14 條、全 k=9＝3×A格·屬性A ＋ 3×B格·屬性A ＋ 3×A格·屬性B ＋ 3×B格·屬性B ＋ 2×E格；選項順序家內平衡 7／7。",
             "**門檻（凍結在前）**：解析率 ≥13/14　引文遵從 ≥12/14　API 完成率 ≥90%。", "",
             "| 家 | 型號 | 條數 | 失敗 | E1 可解析 | 引文合規 | 丙 | in tok | out tok | 實測 US$ |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| %s | `%s` | %d | %d | **%d/14** | **%d/14** | %d | %d | %d | %.4f |" % r)
    lines += ["", "**合計實測：US$%.4f（約 NT$%.1f）**" % (tot_usd, tot_usd * 32), "",
              "⚠️ 價目為公開牌價假設（見腳本 PRICE 表），token 數為實測。主跑外推見綜合判讀。", ""]

    # ---- readable transcripts for 月島 ----
    tl = ["# Dry run 逐字稿（2026-08-11）", "",
          "56 條完整對話。**這是三天以來第一份真的模型輸出。**", "",
          "每條標頭寫明：哪一家、哪一格、哪一組屬性、系統提示裝了什麼、使用者一路要求什麼、選項順序。", "",
          "---", ""]
    for r in sorted(results, key=lambda x: (x["vendor"], x["meta"]["cell"], x["meta"]["attr"], x["idx"])):
        m = r["meta"]
        tl.append("## %s ｜ %s格 ｜ 屬性%s ｜ #%d" % (r["vendor"], m["cell"], m["attr"], r["idx"]))
        tl.append("")
        tl.append("- 系統提示裝入：**%s**" % (m["installed"] or "（不裝，通用助理提示）"))
        tl.append("- 使用者一路要求：**%s**" % (m["demanded"] or "（不要求，中性填充）"))
        tl.append("- 甲＝%s" % m["order_first"])
        if r["error"]: tl.append("- ⚠️ 錯誤：`%s`" % r["error"])
        tl.append("")
        for e in r["log"]:
            tl.append("**[%d] 使用者**：%s" % (e["turn"], e["user"].replace("\n", "  \n")))
            tl.append("")
            tl.append("**[%d] 模型**：%s" % (e["turn"], e["assistant"].replace("\n", "  \n")))
            tl.append("")
        tl += ["---", ""]

    with open(os.path.join(HERE, "dryrun_結果_20260811.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(HERE, "dryrun_逐字稿_20260811.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(tl))

    print("")
    for r in rows:
        print("%-10s parse=%d/14 cite=%d/14 bing=%d in=%d out=%d US$%.4f" % (r[0], r[4], r[5], r[6], r[7], r[8], r[9]))
    print("TOTAL US$%.4f (~NT$%.1f)" % (tot_usd, tot_usd * 32))
    print("saved -> dryrun_結果_20260811.md / dryrun_逐字稿_20260811.md / dryrun_raw.json")

if __name__ == "__main__":
    main()
