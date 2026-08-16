# -*- coding: utf-8 -*-
"""
make_figure.py -- Figure 1 for the submitted report. 2026-08-16. READ-ONLY on data.

Two panels over the confirmatory run's published classifications:
  Panel A (headline): assertion rate by probe position, cell D vs cell E.
  Panel B (confirmatory family): flip rate by probe position, cell A vs cell C,
          denominator = valid single choices (the "as specified" version of 4.4).

Every plotted value is recomputed here by the same group-by used everywhere else
and then HARD-ASSERTED against the numbers published in analysis_結果_20260814.md;
if any assertion fails the script dies and no figure is written. Wilson 95% CIs.
"""
import json, io, os, sys, math

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in io.open(os.path.join(HERE, "analysis_per_conversation.jsonl"),
                                       encoding="utf-8") if l.strip()]
zh = [r for r in rows if r["lang"] == "zh"]
KS = (4, 6, 9)

def wilson(x, n, z=1.959964):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))

# Panel A data: assertion rate (any pole) in D and E, per k, denominator = all 90.
panelA = {}
for cell in ("D", "E"):
    for k in KS:
        sub = [r for r in zh if r["cell"] == cell and r["k"] == k]
        x = sum(1 for r in sub if r["e1_class"] == "single")
        panelA[(cell, k)] = (x, len(sub))

# Hard assertions against the published table (analysis_結果_20260814.md, Result 2).
assert panelA[("D", 4)] == (4, 90),  panelA[("D", 4)]
assert panelA[("D", 6)] == (25, 90), panelA[("D", 6)]
assert panelA[("D", 9)] == (45, 90), panelA[("D", 9)]
for k in KS:
    assert panelA[("E", k)] == (0, 90), (k, panelA[("E", k)])

# Panel B data: flip rate in A and C per k, denominator = valid single choices.
panelB = {}
for cell in ("A", "C"):
    for k in KS:
        sub = [r for r in zh if r["cell"] == cell and r["k"] == k and r["e1_class"] == "single"]
        x = sum(1 for r in sub if r["flip"])
        panelB[(cell, k)] = (x, len(sub))

assert panelB[("A", 4)] == (1, 61),  panelB[("A", 4)]
assert panelB[("A", 6)] == (5, 64),  panelB[("A", 6)]
assert panelB[("A", 9)] == (11, 69), panelB[("A", 9)]
assert panelB[("C", 4)] == (0, 81),  panelB[("C", 4)]
assert panelB[("C", 6)] == (0, 85),  panelB[("C", 6)]
assert panelB[("C", 9)] == (1, 85),  panelB[("C", 9)]
print("all hard assertions passed -- plotted values match the published tables")

# ---- style -------------------------------------------------------------
BLUE  = "#58B2DC"   # pressure cell (D / A) -- sora-iro, per Tsukishima 2026-08-16
GRAY  = "#D7C4BB"   # no-pressure cell (E / C) -- warm shell pink, same ruling
EDGE_HOT  = "#3A93BF"   # one step deeper, keeps pale bars legible on white
EDGE_COLD = "#B9A296"
INK   = "#111827"
MUTED = "#6B7280"
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": MUTED, "font.family": "DejaVu Sans",
})

fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6), dpi=300)
W = 0.34
XS = range(len(KS))

def draw(ax, data, hot, cold, hot_lab, cold_lab, title, ymax):
    for i, k in enumerate(KS):
        for j, (cell, color, edge) in enumerate(((hot, BLUE, EDGE_HOT), (cold, GRAY, EDGE_COLD))):
            x, n = data[(cell, k)]
            p, lo, hi = wilson(x, n)
            cx = i + (j - 0.5) * (W + 0.04)
            ax.bar(cx, p * 100, width=W, color=color, zorder=3,
                   edgecolor=edge, linewidth=0.8)
            ax.errorbar(cx, p * 100, yerr=[[p * 100 - lo * 100], [hi * 100 - p * 100]],
                        fmt="none", ecolor=INK, elinewidth=0.9, capsize=2.5, zorder=4)
            big = (cell == hot and k == 9)
            ax.annotate("%.1f%%\n(%d/%d)" % (p * 100, x, n),
                        (cx, hi * 100), textcoords="offset points", xytext=(0, 4),
                        ha="center", va="bottom",
                        fontsize=8 if big else 7,
                        fontweight="bold" if big else "normal",
                        color=INK if big else MUTED, zorder=5)
    ax.set_xticks(list(XS))
    ax.set_xticklabels(["k = 4\n(1 request level)", "k = 6\n(3 levels)", "k = 9\n(6 levels)"])
    ax.set_ylim(0, ymax)
    ax.set_title(title, fontsize=9.5, color=INK, pad=30, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    # legend lives OUTSIDE the axes, between the title and the plot, so it can
    # never collide with value labels regardless of bar heights
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=EDGE_HOT, label=hot_lab),
                       plt.Rectangle((0, 0), 1, 1, facecolor=GRAY, edgecolor=EDGE_COLD, label=cold_lab)],
              frameon=False, fontsize=7.5, loc="lower left",
              bbox_to_anchor=(0.0, 1.005), ncol=2, borderaxespad=0,
              handlelength=1.1, columnspacing=1.2)

draw(axes[0], panelA, "D", "E",
     "D — escalating attribution",
     "E — neutral filler (true null)",
     "A. Assertion rate, any pole\n(no system prompt in either cell; n = 90 per bar)", 68)
axes[0].set_ylabel("% of conversations", fontsize=9)

draw(axes[1], panelB, "A", "C",
     "A — pressure toward the other pole",
     "C — neutral filler (control)",
     "B. Flip rate, valid single choices\n(pole installed in both cells; as specified)", 30)

fig.suptitle("", fontsize=1)
fig.text(0.005, 0.008,
         "Wilson 95% CIs. Chinese arm. Panel A: assertion under attribution (§4.3). "
         "Panel B: the confirmatory family's cells (§4.4); conservative-bound version in §4.4.",
         fontsize=6.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
out = os.path.join(HERE, "figure1.png")
fig.savefig(out, bbox_inches="tight", facecolor="white")
print("wrote", out)
