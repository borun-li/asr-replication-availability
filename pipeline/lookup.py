#!/usr/bin/env python3
"""Look up ASR articles' replication packages by DOI or article URL.

Usage:
    python3 pipeline/lookup.py <query> [<query> ...]     # one or more DOIs / SAGE URLs
    python3 pipeline/lookup.py --file queries.txt        # one query per line (# = comment)
    python3 pipeline/lookup.py --detail <query> ...      # full per-field view (with notes)

Examples:
    python3 pipeline/lookup.py 10.1177/00031224251320103
    python3 pipeline/lookup.py https://journals.sagepub.com/doi/10.1177/00031224251324504
    python3 pipeline/lookup.py --file my_dois.txt

DOI matches exactly (a pasted doi.org/ or journals.sagepub.com/doi/ prefix is stripped);
article_url and package_location also match by substring. Default output is a compact
one-line-per-article table; --detail prints every field including the coding notes. Reads
output/asr_*_result.csv — standard library only, no pip install.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _dataset import load_all, norm_doi  # noqa: E402

DETAIL_FIELDS = [
    ("doi", "DOI"), ("title", "Title"), ("authors", "Authors"), ("volume", "Volume"),
    ("url", "Article URL"), ("in_scope", "In scope"), ("qualitative", "Qualitative"),
    ("data", "Data deposited"), ("code", "Code deposited"), ("data_gated", "Data access-restricted"),
    ("apply", "How to obtain the data"), ("package_location", "Replication package"),
    ("notes", "Notes"),
]


def find(rows, query):
    raw = (query or "").strip().lower()
    if not raw:
        return []
    doi_q = norm_doi(raw)
    out = []
    for r in rows:
        if r.get("doi") == doi_q:
            out.append(r)
        elif any(raw in (r.get(c) or "").lower() for c in ("url", "package_location")):
            out.append(r)
    return out


def route(r):
    pkg = (r.get("package_location") or "").strip()
    if pkg:
        return pkg
    if r.get("data_gated") == "Y":
        return "[access-restricted] " + ((r.get("apply") or "").strip() or "see --detail notes")
    return "—"


def print_compact(hits):
    print(f'{"doi":<26} {"vol":<3} {"scope":<5} {"data":<4} {"code":<4} {"gate":<4}  package / how to obtain')
    print("-" * 100)
    for r in hits:
        rt = route(r)
        rt = rt[:52] + "..." if len(rt) > 55 else rt
        print(f'{r.get("doi", ""):<26} {r.get("volume") or "":<3} {r.get("in_scope") or "":<5} '
              f'{r.get("data") or "":<4} {r.get("code") or "":<4} {r.get("data_gated") or "":<4}  {rt}')


def print_detail(hits):
    for r in hits:
        print("=" * 76)
        for key, label in DETAIL_FIELDS:
            val = (r.get(key) or "").strip()
            if val:
                print(f"{label:>24} : {val}")
    print("=" * 76)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    detail, queries, i = False, [], 0
    while i < len(args):
        a = args[i]
        if a in ("--detail", "-v"):
            detail = True
        elif a in ("--file", "-f"):
            i += 1
            if i >= len(args):
                print("ERROR: --file needs a path", file=sys.stderr)
                return 2
            if not os.path.exists(args[i]):
                print(f"ERROR: file not found: {args[i]}", file=sys.stderr)
                return 2
            with open(args[i], encoding="utf-8") as fh:
                queries += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
        else:
            queries.append(a)
        i += 1

    if not queries:
        print("No queries. Try: lookup.py 10.1177/00031224251320103")
        return 1

    rows = load_all()
    if not rows:
        print("ERROR: no dataset found under output/asr_*_result.csv", file=sys.stderr)
        return 2

    seen, hits, unmatched = set(), [], []
    for q in queries:
        found = find(rows, q)
        if not found:
            unmatched.append(q)
            continue
        for r in found:
            if r["doi"] not in seen:
                seen.add(r["doi"])
                hits.append(r)

    if hits:
        (print_detail if detail else print_compact)(hits)
    print(f"\n{len(hits)} article(s) found from {len(queries)} query(ies).")
    if unmatched:
        print(f"{len(unmatched)} not matched: " + ", ".join(unmatched))
        print("  (coverage is the coded volumes only — check the DOI / URL, or add it with add_article.py.)")
    return 0 if hits else 1


if __name__ == "__main__":
    raise SystemExit(main())
