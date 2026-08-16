# -*- coding: utf-8 -*-
"""
prepush_scan.py -- pre-publication safety scan. READ-ONLY. 2026-08-16.

Everything below is about to go into a PUBLIC repository. Before that happens,
scan every candidate file for the two categories the project's red lines forbid
leaving the machine: credentials, and personal data (this workspace also handles
school records, so the scan looks for those patterns even though this dataset
should contain none).

Exits non-zero on any hit. Console ASCII only.
"""
import os, sys, io, re

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FILES = sys.argv[1:]
if not FILES:
    sys.exit("usage: prepush_scan.py <file> [<file> ...]")

PATTERNS = [
    ("Anthropic key",   re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI key",      re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{32,}")),
    ("xAI key",         re.compile(r"\bxai-[A-Za-z0-9]{20,}")),
    ("Google key",      re.compile(r"\bAIza[0-9A-Za-z_\-]{35}")),
    ("GitHub token",    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}")),
    ("Slack token",     re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("JWT",             re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.")),
    ("private key",     re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Supabase URL",    re.compile(r"https://[a-z0-9]{16,}\.supabase\.co")),
    ("ROC ID number",   re.compile(r"\b[A-Z][12]\d{8}\b")),
    ("TW mobile",       re.compile(r"\b09\d{2}[- ]?\d{3}[- ]?\d{3}\b")),
    ("email address",   re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("school id-ish",   re.compile(r"\b(?:學號|座號|班級|身分證)\b")),
]
# Allowed: the sprint's own contact address appears in published materials.
ALLOW = {"sprints@apartresearch.com", "hello@apartresearch.com"}

total_hits = 0
for path in FILES:
    if not os.path.isfile(path):
        print("MISSING: %s" % path)
        total_hits += 1
        continue
    try:
        text = io.open(path, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print("UNREADABLE %s: %r" % (path, e))
        total_hits += 1
        continue
    for name, rx in PATTERNS:
        for m in set(rx.findall(text)):
            hit = m if isinstance(m, str) else str(m)
            if hit in ALLOW:
                continue
            total_hits += 1
            print("HIT  %-14s  %-42s  %s" % (name, os.path.basename(path), hit[:60]))

print("\nscanned %d files, %d hit(s)" % (len(FILES), total_hits))
if total_hits:
    sys.exit("SCAN FAILED -- do not push")
print("CLEAN -- safe to publish")
