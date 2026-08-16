# -*- coding: utf-8 -*-
"""Google-only dry-run top-up: the first pass 404'd on gemini-2.5-flash
("no longer available to new users"). Reuses dryrun.py wholesale, restricted to
one vendor, and merges the result into dryrun_raw.json. ASCII console only."""
import os, sys, json, time, subprocess
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dryrun as D

for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
    if not os.environ.get(k):
        try:
            v = subprocess.check_output(["powershell", "-NoProfile", "-Command",
                "[Environment]::GetEnvironmentVariable('%s','User')" % k], text=True).strip()
            if v: os.environ[k] = v
        except Exception:
            pass

model = D.discover("google")
print("model google -> %s" % model)

jobs = [("google", model, s, t, m, i) for i, (s, t, m) in enumerate(D.plan_for_family())]
res, t0 = [], time.time()
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(D.run_conversation, *j) for j in jobs]
    for n, fut in enumerate(cf.as_completed(futs), 1):
        res.append(fut.result())
        if n % 4 == 0: print("  %d/14 (%.0fs)" % (n, time.time() - t0))

errs = [r for r in res if r["error"]]
print("errors: %d" % len(errs))
if errs: print("first error: %s" % errs[0]["error"][:300])

ok = [r for r in res if not r["error"]]
parsed = sum(1 for r in ok if D.parse_e1(r["log"][8]["assistant"]))
comp = sum(1 for r in ok if D.citation_compliant(r["log"][9]["assistant"])[0])
bing = sum(1 for r in ok if D.parse_e1(r["log"][8]["assistant"]) == "丙")
tin = sum(r["tin"] for r in res); tout = sum(r["tout"] for r in res)
pi, po = D.PRICE["google"]
usd = tin / 1e6 * pi + tout / 1e6 * po

# merge back
path = os.path.join(HERE, "dryrun_raw.json")
allr = json.load(open(path, encoding="utf-8"))
allr = [r for r in allr if r["vendor"] != "google"] + res
json.dump(allr, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("google parse=%d/14 cite=%d/14 bing=%d in=%d out=%d US$%.4f (~NT$%.1f)"
      % (parsed, comp, bing, tin, tout, usd, usd * 32))
print("merged -> dryrun_raw.json")
