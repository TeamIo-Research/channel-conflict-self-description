# -*- coding: utf-8 -*-
"""
appendix_b5.py -- descriptive decompositions for Appendix B, Table B5.
READ-ONLY on the data. 2026-08-16.

Flip-rate decompositions per cell x attribute and per cell x family, Chinese arm,
cells A/B/C, denominator = valid single choices (e1_class == "single"), exactly
as analyse.py classified them. No new classification happens here -- this is a
groupby over the published per-conversation table. Descriptive throughout: the
frozen analysis plan pools attributes and families for the confirmatory family,
and single-cell strata detect only very large effects (power section of the
report), so nothing here is a test.
"""
import json, io, os, sys, collections

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in io.open(os.path.join(HERE, "analysis_per_conversation.jsonl"),
                                       encoding="utf-8") if l.strip()]

zh = [r for r in rows if r["lang"] == "zh" and r["cell"] in ("A", "B", "C")]

def rate(subset):
    valid = [r for r in subset if r["e1_class"] == "single"]
    flips = sum(1 for r in valid if r["flip"])
    return flips, len(valid)

def fmt(f, n):
    return "%d/%d (%.1f%%)" % (f, n, 100.0 * f / n) if n else "0/0 (n/a)"

print("TABLE B5a -- flip rate by cell x attribute x k (zh, valid single choices)")
print("| Cell | Attribute | k=4 | k=6 | k=9 |")
print("|---|---|---|---|---|")
for cell in ("A", "B", "C"):
    for attr in ("A", "B"):
        cells = []
        for k in (4, 6, 9):
            f, n = rate([r for r in zh if r["cell"] == cell and r["attr"] == attr and r["k"] == k])
            cells.append(fmt(f, n))
        print("| %s | %s | %s | %s | %s |" % (cell, attr, *cells))

print()
print("TABLE B5b -- flip rate by cell x family x k (zh, valid single choices)")
print("| Cell | Family | k=4 | k=6 | k=9 |")
print("|---|---|---|---|---|")
for cell in ("A", "B", "C"):
    for fam in ("anthropic", "openai", "xai"):
        cells = []
        for k in (4, 6, 9):
            f, n = rate([r for r in zh if r["cell"] == cell and r["vendor"] == fam and r["k"] == k])
            cells.append(fmt(f, n))
        print("| %s | %s | %s | %s | %s |" % (cell, fam, *cells))

print()
print("TABLE B4b -- cell D assertion (any pole) by family x k (zh; denominator = all 30)")
print("| Family | k=4 | k=6 | k=9 |")
print("|---|---|---|---|")
zh_d = [r for r in rows if r["lang"] == "zh" and r["cell"] == "D"]
for fam in ("anthropic", "openai", "xai"):
    cells = []
    for k in (4, 6, 9):
        sub = [r for r in zh_d if r["vendor"] == fam and r["k"] == k]
        a = sum(1 for r in sub if r["e1_class"] == "single")
        cells.append(fmt(a, len(sub)))
    print("| %s | %s | %s | %s |" % (fam, *cells))

print()
print("Cross-check against the published headline cells (must match analysis file):")
for cell in ("A", "B", "C"):
    for k in (4, 6, 9):
        f, n = rate([r for r in zh if r["cell"] == cell and r["k"] == k])
        print("  cell %s k=%d : %s" % (cell, k, fmt(f, n)))
for k in (4, 6, 9):
    a = sum(1 for r in zh_d if r["k"] == k and r["e1_class"] == "single")
    n = sum(1 for r in zh_d if r["k"] == k)
    print("  cell D k=%d : %s (must be 4/90, 25/90, 45/90)" % (k, fmt(a, n)))
