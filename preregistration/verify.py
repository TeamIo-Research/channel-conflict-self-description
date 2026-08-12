# -*- coding: utf-8 -*-
"""
VERIFY — read-only integrity check for the frozen pre-registration package.

This script WRITES NOTHING. It reads the frozen artefacts, recomputes their
SHA-256 digests, and compares them line by line against `_freeze_manifest.txt`.

Use THIS to verify a freeze. Do NOT use `freeze.py`: freeze.py regenerates the
English submission body from the (unhashed) bilingual skeleton and overwrites
both the deliverable and the manifest, so running it destroys the very evidence
a verifier is trying to check.

Console output is ASCII only (cp950-safe).

Usage:  python verify.py
Exit:   0 = PASS, 1 = FAIL
"""
import io, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)
MANIFEST_FILE = "_freeze_manifest.txt"


def read_manifest(path):
    """Return (ordered list of (digest, size, name), recorded_manifest_digest)."""
    rows, combined = [], None
    for line in io.open(path, encoding="utf-8").read().split("\n"):
        s = line.strip()
        if s.startswith("MANIFEST "):
            combined = s.split(None, 1)[1].strip()
            continue
        parts = s.split("  ")
        if len(parts) == 3 and len(parts[0]) == 64:
            rows.append((parts[0], int(parts[1]), parts[2]))
    return rows, combined


def main():
    mpath = P(MANIFEST_FILE)
    if not os.path.exists(mpath):
        print("FAIL: %s not found" % MANIFEST_FILE)
        return 1

    rows, recorded_combined = read_manifest(mpath)
    if not rows:
        print("FAIL: no artefact rows parsed from %s" % MANIFEST_FILE)
        return 1

    print("Frozen package verification (read-only)")
    print("artefacts listed in manifest: %d" % len(rows))
    print("")

    ok_all = True
    recomputed = []
    for digest, size, name in rows:
        path = P(name)
        if not os.path.exists(path):
            print("  MISSING  %s" % name)
            ok_all = False
            continue
        b = io.open(path, "rb").read()
        h = hashlib.sha256(b).hexdigest()
        good = (h == digest and len(b) == size)
        ok_all = ok_all and good
        recomputed.append("%s  %d  %s" % (h, len(b), name))
        print("  %-8s %7d bytes  %s...  %s"
              % ("OK" if good else "CHANGED", len(b), h[:16], name))
        if not good:
            print("           expected %d bytes  %s..." % (size, digest[:16]))

    # The manifest digest is the hash of the concatenated per-file lines,
    # in the order recorded. Recompute only if every file was present.
    print("")
    if len(recomputed) == len(rows):
        combined = hashlib.sha256("\n".join(recomputed).encode("utf-8")).hexdigest()
        print("MANIFEST recomputed : %s" % combined)
        print("MANIFEST recorded   : %s" % (recorded_combined or "(not found in file)"))
        if recorded_combined and combined != recorded_combined:
            ok_all = False
    else:
        print("MANIFEST recomputed : (skipped, artefacts missing)")
        ok_all = False

    print("")
    print("RESULT: %s" % ("PASS" if ok_all else "FAIL"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
