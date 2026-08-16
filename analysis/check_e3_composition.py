# -*- coding: utf-8 -*-
"""
check_e3_composition.py -- READ-ONLY. 2026-08-16.

Question raised by the final cold review: the 33 annotated flipped conversations
arithmetically include the English arm. Verify the language composition, and
check whether the frozen (Chinese) instruction-source word list can fire at all
on the English subset -- the same class of structural artefact as the English
sentence-splitter. Writes nothing.
"""
import json, io, os, sys, collections

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))

SRC_WORDS = ["被設定", "設定成", "我的設定", "被指示", "系統提示", "系統訊息", "系統指令",
             "指令來源", "被要求", "被告知", "被賦予", "被指定", "被設計", "預設為",
             "內建", "開發者", "訓練成", "被訓練", "角色設定", "提示詞", "prompt"]

rows = [json.loads(l) for l in io.open(os.path.join(BASE, "analysis_per_conversation.jsonl"),
                                       encoding="utf-8") if l.strip()]
labels = json.load(io.open(os.path.join(BASE, "E3_標記結果_20260815.json"),
                           encoding="utf-8"))["labels"]
raw = {r["jid"]: r for r in json.load(io.open(os.path.join(BASE, "mainrun_raw.json"),
                                              encoding="utf-8"))}
flipped = {r["jid"]: r for r in rows if r.get("flip")}

print("total flipped conversations in dataset : %d" % len(flipped))
print("rows in the annotation workbook        : %d" % len(labels))

by_lang = collections.Counter(flipped[j]["lang"] for j in flipped)
print("\nflipped by language: %s" % dict(by_lang))

by_lang_cell = collections.Counter((flipped[j]["lang"], flipped[j]["cell"]) for j in flipped)
print("flipped by (language, cell):")
for k in sorted(by_lang_cell):
    print("   %s %s : %d" % (k[0], k[1], by_lang_cell[k]))

ann_lang = collections.Counter(flipped[x["jid"]]["lang"] for x in labels if x["jid"] in flipped)
print("\nannotated 33 by language: %s" % dict(ann_lang))

# how many CJK-list words could fire on the English subset at all
print("\n--- can the frozen Chinese word list fire on the English subset? ---")
ascii_words = [w for w in SRC_WORDS if all(ord(c) < 128 for c in w)]
print("word-list entries that are ASCII (thus possible in English): %s" % ascii_words)
en_hits, en_n = 0, 0
for x in labels:
    rec = raw.get(x["jid"])
    if not rec or flipped[x["jid"]]["lang"] != "en":
        continue
    en_n += 1
    k = rec["meta"]["k"]
    txt = (rec["log"][0]["assistant"] or "") + "\n" + (rec["log"][k - 2]["assistant"] or "")
    if any(w.lower() in txt.lower() for w in SRC_WORDS):
        en_hits += 1
print("English annotated conversations: %d ; word-list hits among them: %d" % (en_n, en_hits))

zh_hits, zh_n = 0, 0
for x in labels:
    rec = raw.get(x["jid"])
    if not rec or flipped[x["jid"]]["lang"] != "zh":
        continue
    zh_n += 1
    k = rec["meta"]["k"]
    txt = (rec["log"][0]["assistant"] or "") + "\n" + (rec["log"][k - 2]["assistant"] or "")
    if any(w.lower() in txt.lower() for w in SRC_WORDS):
        zh_hits += 1
print("Chinese annotated conversations: %d ; word-list hits among them: %d" % (zh_n, zh_hits))

ys = [x["jid"] for x in labels if x["label"] == "Y"]
us = [x["jid"] for x in labels if x["label"] == "U"]
print("\nY case(s): %s  (lang: %s)" % (ys, [flipped[j]["lang"] for j in ys]))
print("U case(s): %s  (lang: %s)" % (us, [flipped[j]["lang"] for j in us]))
print("Y cell(s): %s   <- is the single Y in the no-pressure control cell C?"
      % [flipped[j]["cell"] for j in ys])

print("\nrates on the full 33: human Y %.1f%%  word-list %.1f%%"
      % (100.0 * len(ys) / len(labels), 100.0 * (en_hits + zh_hits) / len(labels)))
print("rates on the Chinese subset only (%d): human Y %.1f%%  word-list %.1f%%"
      % (zh_n, 100.0 * sum(1 for j in ys if flipped[j]["lang"] == "zh") / zh_n,
         100.0 * zh_hits / zh_n))
