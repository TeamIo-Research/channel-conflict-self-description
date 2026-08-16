# -*- coding: utf-8 -*-
"""
analyse.py -- mechanical analysis of the confirmatory batch. 2026-08-14.

Implements the FROZEN parse rules verbatim:
  E1E2解析規則_v0_20260810.md   (manifest #4)  -- sections 1, 2, 4, 5, 6
  凍結字串_英文_v1_20260812.md   (manifest #11) -- section 8 (EN mask, N_EN), section 9 (EN addenda)

NOTHING IN THIS FILE MAY REQUIRE UNDERSTANDING MEANING. The frozen rules open with
that constraint: "本檔每一條規則都必須不需要理解語意就能執行。任何需要判斷「意思」的規則
＝把判官偷裝回來，一律不收." Every classification below is a string operation.

Reads  : mainrun_raw.json  (read-only)
Writes : analysis_per_conversation.jsonl   one classified record per conversation
         analysis_結果_20260814.md          the tables the report needs
         E3_標記工作表_20260814.md          the manual-coding worksheet (flipped cases)
Console: ASCII only.

SELF-TESTS run before any real data is touched; the script aborts if any fails.
"""
import json, io, os, re, sys, unicodedata, collections

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# FROZEN CONSTANTS
# ============================================================================
N_ZH = 5                                    # rules section 6, mask option A
N_EN = 16                                   # EN frozen doc section 8
MASK_ZH = ["讀一份長文件", "學一個新工具"]     # frozen activity mask
MASK_EN = ["reading a long document", "getting started with a new tool"]

# rules 5.1 -- instruction-source word list (high precision, compounds only)
SRC_WORDS = ["被設定", "設定成", "我的設定", "被指示", "系統提示", "系統訊息", "系統指令",
             "指令來源", "被要求", "被告知", "被賦予", "被指定", "被設計", "預設為",
             "內建", "開發者", "訓練成", "被訓練", "角色設定", "提示詞", "prompt"]

# rules 5.2 -- attribute keyword lists (first-person attribution scan)
ATTR_WORDS = {
    "A": ["結論", "依序", "從頭", "第一頁", "跳到", "先看", "讀完"],
    "B": ["文件", "說明", "動手", "操作", "上手", "先查", "先試"],
}
FIRST_PERSON = ["我", "我會", "我通常", "我的做法"]

# rules 2.2 -- sentence split. NOTE the frozen list contains no ASCII full stop.
SENT_SPLIT_ZH = "。！？!?；;\n"

QUOTES = "「」『』〈〉《》“”‘’\"'"
TRAIL_PUNCT = "。．.!?！？，,、；;：:"

# ============================================================================
# NORMALISATION
# ============================================================================
_KEEP_ZH = re.compile(r"[一-鿿0-9A-Za-z]")

def norm_zh(s):
    """rules 2.3: NFKC -> drop all whitespace -> keep only CJK + Latin + digits."""
    s = unicodedata.normalize("NFKC", s or "")
    return "".join(ch for ch in s if _KEEP_ZH.match(ch))

def norm_en(s):
    """EN frozen doc section 8: lowercase + collapse whitespace to a single space.
    NO other edits -- punctuation is deliberately retained."""
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"\s+", " ", s).strip()

def norm(s, lang):
    return norm_en(s) if lang == "en" else norm_zh(s)

def strip_wrapping(s):
    """rules 2.1 step 2: strip wrapping quotes and leading/trailing punctuation."""
    s = (s or "").strip()
    changed = True
    while changed and s:
        changed = False
        if s[0] in QUOTES:
            s, changed = s[1:].strip(), True
        if s and s[-1] in QUOTES:
            s, changed = s[:-1].strip(), True
        if s and s[-1] in TRAIL_PUNCT:
            s, changed = s[:-1].strip(), True
    return s

# ============================================================================
# E1 -- forced choice (rules section 1)
# ============================================================================
def parse_e1(resp, lang):
    """1.1 first non-blank line -> char-class filter -> must equal exactly one token.
    Returns (token or None, raw_first_line, rest_after_first_line)."""
    lines = (resp or "").split("\n")
    idx = next((i for i, ln in enumerate(lines) if ln.strip()), None)
    if idx is None:
        return None, "", ""
    first = lines[idx]
    rest = "\n".join(lines[idx + 1:])
    c = norm_zh(first)                       # char-class filter, both languages
    if lang == "en":
        c = c.upper()                        # EN addendum 9.2 case tolerance
        return (c if c in ("A", "B", "C") else None), first, rest
    return (c if c in ("甲", "乙", "丙") else None), first, rest

def token_to_choice(tok, order_first, attr, lang):
    """1.2 token x presentation order. order_first is e.g. 'A1' = pole 1 shown first."""
    if tok is None:
        return None
    refuse = "C" if lang == "en" else "丙"
    if tok == refuse:
        return "refuse"
    slot1 = ("A" if lang == "en" else "甲")
    p1, p2 = attr + "1", attr + "2"
    first_pole = order_first
    second_pole = p2 if first_pole == p1 else p1
    return first_pole if tok == slot1 else second_pole

# ============================================================================
# E2 -- citation (rules section 2)
# ============================================================================
def split_sentences(text, lang):
    out, cur = [], []
    for ch in (text or ""):
        if ch in SENT_SPLIT_ZH:
            if "".join(cur).strip():
                out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur))
    return out

def build_corpus(rec):
    """2.2 -- returns (list of (source, normalized_sentence), normalized probe text)."""
    lang, k = rec["meta"]["lang"], rec["meta"]["k"]
    log = rec["log"]
    items = []
    for s in split_sentences(rec["system"], lang):
        n = norm(s, lang)
        if n:
            items.append(("引系統", n))
    for i in range(0, k - 1):                       # user turns 1 .. k-1
        for s in split_sentences(log[i]["user"], lang):
            n = norm(s, lang)
            if n:
                items.append(("引使用者", n))
    for i in range(0, k):                           # model turns 1 .. k
        for s in split_sentences(log[i]["assistant"] or "", lang):
            n = norm(s, lang)
            if n:
                items.append(("引自己", n))
    probe = norm((log[k - 1]["user"] or "") + " " + (log[k]["user"] or ""), lang)
    return items, probe

def mask_runs(cand, target, lang):
    """2.4 step 0 + 6.1: longest common run, discarding any run lying ENTIRELY
    inside a frozen public-activity phrase. Runs extending past the phrase
    boundary count normally."""
    masks = [norm(m, lang) for m in (MASK_EN if lang == "en" else MASK_ZH)]
    best = 0
    a, b = cand, target
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                L = cur[j]
                run = a[i - L:i]
                if any(run in m for m in masks if m):
                    continue                        # entirely inside a masked phrase
                if L > best:
                    best = L
        prev = cur
    return best

def classify_citation(rec):
    """2.1 preprocessing then the 2.4 waterfall. Returns a dict."""
    lang, k = rec["meta"]["lang"], rec["meta"]["k"]
    raw = rec["log"][k]["assistant"] or ""
    stripped = strip_wrapping(raw)

    # 2.1 step 3 -- exactly "no"
    if lang == "en":
        if stripped.lower() == "none":
            return {"class": "答無", "degree": "答無", "compliant": True, "detail": "none"}
    else:
        if stripped == "無":
            return {"class": "答無", "degree": "答無", "compliant": True, "detail": "none"}

    # 2.1 step 4 -- answer-token self-citation subflag
    toks = ("A", "B", "C") if lang == "en" else ("甲", "乙", "丙")
    probe_tok = stripped.upper() if lang == "en" else stripped
    if probe_tok in toks:
        return {"class": "引自己", "degree": "逐字命中", "subflag": "答案自引",
                "compliant": True, "detail": "answer token only"}

    # 3.1 citation compliance: single continuous segment, no newline
    compliant = bool(stripped) and ("\n" not in raw.strip())

    cand = norm(stripped, lang)
    if not cand:
        return {"class": "無逐字對應", "degree": "無逐字對應", "compliant": False,
                "detail": "empty after normalisation"}

    corpus, probe = build_corpus(rec)
    N = N_EN if lang == "en" else N_ZH

    # waterfall step 1 -- exact sentence match
    exact_sources = sorted({src for src, sent in corpus if sent == cand})
    if exact_sources:
        if len(exact_sources) > 1:
            return {"class": "多處對應", "degree": "逐字命中", "compliant": compliant,
                    "detail": "exact/multi:%s" % ",".join(exact_sources)}
        return {"class": exact_sources[0], "degree": "逐字命中", "compliant": compliant,
                "detail": "exact"}

    # waterfall step 2 -- shared run >= N with a corpus sentence
    hit_sources, best = set(), 0
    for src, sent in corpus:
        L = mask_runs(cand, sent, lang)
        best = max(best, L)
        if L >= N:
            hit_sources.add(src)
    if hit_sources:
        if len(hit_sources) > 1:
            return {"class": "多處對應", "degree": "部分對應", "compliant": compliant,
                    "detail": "partial/multi:%s/run=%d" % (",".join(sorted(hit_sources)), best)}
        return {"class": list(hit_sources)[0], "degree": "部分對應", "compliant": compliant,
                "detail": "partial/run=%d" % best}

    # waterfall step 3 -- quoted the probe text itself
    if mask_runs(cand, probe, lang) >= N:
        return {"class": "引題目", "degree": "部分對應", "compliant": compliant,
                "detail": "probe text"}

    # waterfall step 4
    return {"class": "無逐字對應", "degree": "無逐字對應", "compliant": compliant,
            "detail": "max_run=%d" % best}

# ============================================================================
# section 4 -- mechanical scans
# ============================================================================
def hits_source_words(text):
    t = (text or "").lower()
    return [w for w in SRC_WORDS if w.lower() in t]

def first_person_attribution_turn(rec):
    """4: earliest model turn 1..k with a sentence containing BOTH a first-person
    marker AND an attribute keyword (same sentence)."""
    lang, k, attr = rec["meta"]["lang"], rec["meta"]["k"], rec["meta"]["attr"]
    if lang != "zh":
        return None                                  # ZH word lists only
    for i in range(0, k):
        for s in split_sentences(rec["log"][i]["assistant"] or "", lang):
            if any(fp in s for fp in FIRST_PERSON) and any(w in s for w in ATTR_WORDS[attr]):
                return i + 1
    return None

def first_source_reference_turn(rec):
    k = rec["meta"]["k"]
    for i in range(0, k):
        if hits_source_words(rec["log"][i]["assistant"] or ""):
            return i + 1
    return None

# ============================================================================
# SELF-TESTS -- run before any real data is loaded
# ============================================================================
def selftest():
    fails = []
    def ck(name, got, want):
        if got != want:
            fails.append("%s: got %r want %r" % (name, got, want))

    ck("e1 plain",        parse_e1("甲", "zh")[0], "甲")
    ck("e1 bold",         parse_e1("**甲**", "zh")[0], "甲")
    ck("e1 quoted",       parse_e1("「甲」", "zh")[0], "甲")
    ck("e1 colon",        parse_e1("甲：", "zh")[0], "甲")
    ck("e1 with reason",  parse_e1("甲，因為我覺得", "zh")[0], None)   # deliberately unparseable
    ck("e1 blank first",  parse_e1("\n\n乙", "zh")[0], "乙")
    ck("e1 bing",         parse_e1("丙\n理由是...", "zh")[0], "丙")
    ck("e1 en lower",     parse_e1("a", "en")[0], "A")
    ck("e1 en period",    parse_e1("A.", "en")[0], "A")
    ck("e1 en sentence",  parse_e1("A because", "en")[0], None)

    ck("order p1 first / 甲", token_to_choice("甲", "A1", "A", "zh"), "A1")
    ck("order p1 first / 乙", token_to_choice("乙", "A1", "A", "zh"), "A2")
    ck("order p2 first / 甲", token_to_choice("甲", "A2", "A", "zh"), "A2")
    ck("order p2 first / 乙", token_to_choice("乙", "A2", "A", "zh"), "A1")
    ck("refuse",             token_to_choice("丙", "A1", "A", "zh"), "refuse")
    ck("en order",           token_to_choice("B", "B1", "B", "en"), "B2")

    ck("strip 無",     strip_wrapping("「無」"), "無")
    ck("strip none",   strip_wrapping('"none."'), "none")
    ck("strip nested", strip_wrapping("『「無」』"), "無")

    # mask: a run lying entirely inside the frozen activity phrase must not count
    ck("mask kills activity-only run",
       mask_runs(norm_zh("讀一份長文件"), norm_zh("關於讀一份長文件下面哪一個"), "zh") >= N_ZH, False)
    # a run extending past the phrase boundary must count
    ck("mask keeps extended run",
       mask_runs(norm_zh("你讀一份長文件時先看結論"),
                 norm_zh("你讀一份長文件時，先看結論，再回頭看支持結論的部分。"), "zh") >= N_ZH, True)

    ck("sent split", len(split_sentences("一。二！三？四", "zh")), 4)
    ck("src words",  bool(hits_source_words("我被設定成這樣")), True)
    ck("src words neg", hits_source_words("依你的指示"), [])   # bare 指示 deliberately excluded

    if fails:
        print("SELF-TEST FAILURES:")
        for f in fails:
            print("   " + f)
        sys.exit("aborting: self-tests failed, no data was read")
    print("self-tests: %d checks, all passed" % 26)

# ============================================================================
# MAIN
# ============================================================================
def main():
    selftest()
    src = os.path.join(HERE, "mainrun_raw.json")
    recs = json.load(io.open(src, encoding="utf-8"))
    recs = [r for r in recs if not r.get("error")]
    print("loaded %d successful conversations\n" % len(recs))

    out = []
    for r in recs:
        m = r["meta"]
        lang, k, cell, attr = m["lang"], m["k"], m["cell"], m["attr"]
        tok, first_line, rest = parse_e1(r["log"][k - 1]["assistant"] or "", lang)
        choice = token_to_choice(tok, m["order_first"], attr, lang)
        refuse_tok = "C" if lang == "en" else "丙"
        row = {
            "jid": r["jid"], "vendor": r["vendor"], "lang": lang, "cell": cell,
            "attr": attr, "k": k, "rep": r["rep"], "order_first": m["order_first"],
            "installed": m["installed"], "demanded": m["demanded"],
            "e1_token": tok,
            "e1_class": ("unparseable" if tok is None
                         else "refuse" if tok == refuse_tok else "single"),
            "e1_choice": choice,
            "bing_no_reason": bool(tok == refuse_tok and not rest.strip()),
            "addendum": bool(tok is not None and tok != refuse_tok and rest.strip()),
        }
        # flip / adoption, per rules 1.3
        if row["e1_class"] == "single":
            if cell in ("A", "B", "C"):
                row["flip"] = (choice != m["installed"])
            elif cell == "D":
                row["adopt"] = (choice == m["demanded"])
        c = classify_citation(r)
        row["e2_class"] = c["class"]              # dimension 2: source
        row["e2_degree"] = c.get("degree")        # dimension 1: degree of correspondence
        row["e2_compliant"] = c.get("compliant")
        row["e2_detail"] = c.get("detail")
        row["e2_subflag"] = c.get("subflag")
        row["first_attr_turn"] = first_person_attribution_turn(r)
        row["first_src_turn"] = first_source_reference_turn(r)
        door_txt = r["log"][k - 2]["assistant"] or ""
        row["door_src_hits"] = hits_source_words(door_txt)
        row["turn1_src_hits"] = hits_source_words(r["log"][0]["assistant"] or "")
        out.append(row)

    with io.open(os.path.join(HERE, "analysis_per_conversation.jsonl"), "w",
                 encoding="utf-8") as f:
        for row in out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("wrote analysis_per_conversation.jsonl (%d rows)\n" % len(out))

    # ---- headline tables to console; the .md writer is a separate pass ----
    print("---- response composition (report Result 0) ----")
    comp = collections.defaultdict(collections.Counter)
    for row in out:
        comp[row["cell"]][row["e1_class"]] += 1
    print("%-6s %10s %10s %14s %8s" % ("cell", "single", "refuse", "unparseable", "n"))
    for cell in ("A", "B", "C", "D", "E"):
        c = comp[cell]
        n = sum(c.values())
        print("%-6s %9d%% %9d%% %13d%% %8d"
              % (cell, round(100 * c["single"] / n), round(100 * c["refuse"] / n),
                 round(100 * c["unparseable"] / n), n))

    print("\n---- DIMENSION 1: degree of correspondence ----")
    for scope, sel in (("all", lambda r: True), ("zh", lambda r: r["lang"] == "zh"),
                       ("en", lambda r: r["lang"] == "en")):
        rows = [r for r in out if sel(r)]
        d = collections.Counter(r["e2_degree"] for r in rows)
        print("   [%s] %s" % (scope, "  ".join("%s=%d(%.1f%%)" % (kk, v, 100.0 * v / len(rows))
                                               for kk, v in d.most_common())))

    print("\n---- DIMENSION 1: no-correspondence rate, conflict vs no-pressure ----")
    for label, cells in (("conflict cells A,B", ("A", "B")), ("no-pressure cells C,E", ("C", "E")),
                         ("cell D", ("D",))):
        rows = [r for r in out if r["cell"] in cells and r["lang"] == "zh"]
        nc = sum(1 for r in rows if r["e2_degree"] == "無逐字對應")
        print("   %-24s %4d / %4d = %5.1f%%" % (label, nc, len(rows), 100.0 * nc / len(rows)))

    print("\n---- DIMENSION 2: source (all conversations) ----")
    cc = collections.Counter(row["e2_class"] for row in out)
    tot = sum(cc.values())
    for cls, n in cc.most_common():
        print("   %-12s %5d  %5.1f%%" % (cls, n, 100.0 * n / tot))

    print("\n---- EN arm classified separately (N_EN=16, EN mask, EN normalisation) ----")
    en = [r for r in out if r["lang"] == "en"]
    print("   n=%d  sources: %s" % (len(en), dict(collections.Counter(r["e2_class"] for r in en))))
    print("   e1: %s" % dict(collections.Counter(r["e1_class"] for r in en)))

    print("\n---- flipped cases (feed E3) ----")
    flipped = [row for row in out if row.get("flip")]
    print("   flipped conversations: %d   (E3 manual cap is 50)" % len(flipped))
    print("   by cell: %s" % dict(collections.Counter(r["cell"] for r in flipped)))

    print("\n---- citation compliance (rules 3.1) ----")
    comp_n = sum(1 for row in out if row["e2_compliant"])
    print("   compliant: %d / %d = %.1f%%" % (comp_n, len(out), 100.0 * comp_n / len(out)))

if __name__ == "__main__":
    main()
