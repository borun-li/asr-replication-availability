#!/usr/bin/env python3
"""Reproduce the ASR replication-package-availability table from the shipped dataset.

Usage:
    python3 pipeline/reproduce_table.py                       # all shipped volumes
    python3 pipeline/reproduce_table.py output/asr_vol90_result.csv   # one file (e.g. your re-coding)

Recomputes, per volume and overall, the numbers reported in the README: in-scope empirical
articles, data / code deposited, data access-restricted, and the availability rate (data and/or
code deposited). Standard library only — no pip install.

This verifies the *published numbers* from the coded dataset. Independently *re-coding* the
articles from scratch is the separate, browser-driven Scenario 2 in the README.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _dataset import load_csv, load_all  # noqa: E402


def available(r):
    return r.get("data") == "Y" or r.get("code") == "Y"


def pct(a, n):
    return f"{a}/{n} = {a / n * 100:5.1f}%" if n else "n/a"


def summarize(rows, label):
    insc = [r for r in rows if r.get("in_scope") == "Y"]
    na = sum(1 for r in rows if r.get("in_scope") == "NA")
    d = sum(1 for r in insc if r.get("data") == "Y")
    c = sum(1 for r in insc if r.get("code") == "Y")
    g = sum(1 for r in insc if r.get("data_gated") == "Y")
    av = sum(1 for r in insc if available(r))
    print(f"{label:<22} in-scope {len(insc):>3} | NA {na:>2} | "
          f"data=Y {d:>2} code=Y {c:>2} gated=Y {g:>2} | availability {pct(av, len(insc))}")
    return len(insc), av


def main():
    args = [a for a in sys.argv[1:] if a not in ("-h", "--help")]
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        return 0

    print("American Sociological Review — replication-package availability\n")
    if args:
        path = args[0]
        if not os.path.exists(path):
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2
        summarize(load_csv(path), os.path.basename(path))
        return 0

    # default: every shipped volume, then the overall total
    import glob
    from _dataset import RESULT_GLOB
    files = sorted(glob.glob(RESULT_GLOB))
    if not files:
        print("ERROR: no dataset found under output/asr_*_result.csv", file=sys.stderr)
        return 2
    tot_insc = tot_av = 0
    for path in files:
        vol = os.path.basename(path).replace("asr_", "").replace("_result.csv", "")
        n, av = summarize(load_csv(path), vol)
        tot_insc += n
        tot_av += av
    print("-" * 96)
    print(f'{"OVERALL":<22} in-scope {tot_insc:>3} | '
          f'availability {pct(tot_av, tot_insc)}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
