#!/usr/bin/env python3
"""Compare your re-coding of a volume against the shipped dataset — in one command.

Usage:
    python3 pipeline/compare.py output/my_vol90_recode.csv           # auto-finds the shipped file
    python3 pipeline/compare.py my_recode.csv output/asr_vol90_result.csv   # explicit shipped file

Reads your re-coding (the "Rerun" side) and the shipped coding (the "Repo" side), aligns rows by
DOI, and prints: (1) the data / code / data+code availability percentages for each side, and
(2) every article that was coded differently — DOI, title, field, Repo's result, Rerun's result.
Only the five categorical codes are compared (in_scope, qualitative, data, code, data_gated); the
free-text notes are ignored. Standard library only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _dataset import load_csv, ROOT  # noqa: E402

FIELDS = ["in_scope", "qualitative", "data", "code", "data_gated"]
FIELD_LABEL = {"in_scope": "in_scope", "qualitative": "qualitative", "data": "data",
               "code": "code", "data_gated": "data_gated"}


def index_by_doi(rows):
    return {r["doi"]: r for r in rows if r.get("doi")}


def avail(rows):
    insc = [r for r in rows if r.get("in_scope") == "Y"]
    n = len(insc)
    d = sum(1 for r in insc if r.get("data") == "Y")
    c = sum(1 for r in insc if r.get("code") == "Y")
    dc = sum(1 for r in insc if r.get("data") == "Y" and r.get("code") == "Y")
    return n, d, c, dc


def pct(a, n):
    return f"{a}/{n} = {a/n*100:5.1f}%" if n else "n/a"


def find_shipped(user_rows):
    vols = {r.get("volume") for r in user_rows if r.get("volume")}
    if len(vols) == 1:
        v = vols.pop()
        p = os.path.join(ROOT, "output", f"asr_vol{v}_result.csv")
        if os.path.exists(p):
            return p
    return None


def main():
    args = [a for a in sys.argv[1:] if a not in ("-h", "--help")]
    if not args or any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        return 0
    user_path = args[0]
    if not os.path.exists(user_path):
        print(f"ERROR: file not found: {user_path}", file=sys.stderr)
        return 2
    user_rows = load_csv(user_path)

    repo_path = args[1] if len(args) > 1 else find_shipped(user_rows)
    if not repo_path or not os.path.exists(repo_path):
        print("ERROR: could not find the shipped file to compare against. Pass it explicitly:\n"
              "  python3 pipeline/compare.py <your.csv> output/asr_vol<N>_result.csv", file=sys.stderr)
        return 2
    repo_rows = load_csv(repo_path)

    repo, rerun = index_by_doi(repo_rows), index_by_doi(user_rows)
    both = [d for d in repo if d in rerun]

    # --- header + availability ------------------------------------------------
    vols = ",".join(sorted({r.get("volume") for r in repo_rows if r.get("volume")}))
    print(f"Comparing your re-coding vs the shipped dataset (vol {vols})")
    print(f"  Rerun (yours) : {os.path.basename(user_path)}")
    print(f"  Repo (shipped): {os.path.basename(repo_path)}\n")

    rn, rd, rc, rdc = avail(repo_rows)
    un, ud, uc, udc = avail(user_rows)
    print(f'{"Availability (% of in-scope)":<30} {"Repo":<18} Rerun')
    print("-" * 62)
    print(f'{"data":<30} {pct(rd, rn):<18} {pct(ud, un)}')
    print(f'{"code":<30} {pct(rc, rn):<18} {pct(uc, un)}')
    print(f'{"data + code (both)":<30} {pct(rdc, rn):<18} {pct(udc, un)}')
    print(f'{"in-scope articles":<30} {rn:<18} {un}')

    # --- field agreement + differences ---------------------------------------
    diffs, cells, agree = [], 0, 0
    for d in both:
        for f in FIELDS:
            a, b = repo[d].get(f, ""), rerun[d].get(f, "")
            cells += 1
            if a == b:
                agree += 1
            else:
                diffs.append((d, repo[d].get("title") or rerun[d].get("title") or "", f, a, b))
    exact_rows = sum(1 for d in both if all(repo[d].get(f, "") == rerun[d].get(f, "") for f in FIELDS))
    print(f"\nField agreement (in_scope/qualitative/data/code/data_gated): "
          f"{pct(agree, cells)}  ({exact_rows}/{len(both)} rows identical)")

    only_repo = [d for d in repo if d not in rerun]
    only_rerun = [d for d in rerun if d not in repo]

    print(f"\nDifferences ({len(diffs)} cell(s) across {len({d for d,*_ in diffs})} article(s)):")
    if diffs:
        print(f'  {"DOI":<26} {"Title":<40} {"field":<12} {"Repo":<7} Rerun')
        print("  " + "-" * 96)
        for doi, title, field, a, b in sorted(diffs, key=lambda x: (x[0], x[2])):
            t = (title[:37] + "...") if len(title) > 40 else title
            print(f'  {doi:<26} {t:<40} {FIELD_LABEL[field]:<12} {a or "·":<7} {b or "·"}')
    else:
        print("  (none — every shared article matches)")

    if only_repo or only_rerun:
        print(f"\nNot compared: {len(only_repo)} article(s) only in the shipped file, "
              f"{len(only_rerun)} only in yours.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
