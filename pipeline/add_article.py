#!/usr/bin/env python3
"""Add an ASR article to a coding worklist by DOI or URL — Block A filled automatically.

Give it a DOI or a SAGE article URL; it fetches the bibliographic metadata **from Crossref**
(the SAGE page is paywalled, so we never scrape it) and appends a row with Block A filled
(title, authors, published-online date, url, volume, issue, OnlineFirst) and Block B (the coding
columns) left empty — ready for the Scenario 3 coding step. Works for a newly published article
OR any historical ASR article you want to check.

Usage:
    python3 pipeline/add_article.py <doi-or-url> [<doi-or-url> ...]
    python3 pipeline/add_article.py --out input/new_articles.csv <doi-or-url> ...

Examples:
    python3 pipeline/add_article.py 10.1177/00031224251320103
    python3 pipeline/add_article.py https://journals.sagepub.com/doi/10.1177/00031224251324504

Needs an internet connection; standard library only, no pip install, no API key. Set
CROSSREF_MAILTO to your email to use Crossref's faster polite pool (optional).
"""
import csv
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
_MAILTO = os.environ.get("CROSSREF_MAILTO", "").strip()
UA = {"User-Agent": "asr-availability/1.0" + (f" (mailto:{_MAILTO})" if _MAILTO else "")}

# the shipped 19-column ASR layout (Block A then Block B)
COLS = [
    "title", "author(s)", "published__online_date", "article_url", "OnlineFirst (Y/N)",
    "volume", "issue", "in_scope(Y/NA)", "qualitative(Y/N)", "data(Y/N)", "code(Y/N)",
    "data + code", "neither", "data_gated(Y/N)", "data_source / apply_at",
    "package_location", "path_to_package", "coverage_checked", "notes",
]
DOI_RE = re.compile(r"(10\.1177/[0-9A-Za-z._]+)")


def norm_doi(q):
    q = re.sub(r"^(https?://)?(dx\.)?doi\.org/|^doi:\s*|^https?://journals\.sagepub\.com/doi/(abs/|full/|epdf/)?",
               "", (q or "").strip(), flags=re.I)
    m = DOI_RE.search(q)
    return (m.group(1) if m else q).rstrip("/")


def crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    if _MAILTO:
        url += f"?mailto={_MAILTO}"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    return json.loads(raw)["message"]


def block_a(doi):
    m = crossref(doi)
    title = (m.get("title") or [""])[0].strip()
    authors = "; ".join(
        " ".join(x for x in ((a.get("given") or "").strip(), (a.get("family") or "").strip()) if x)
        or (a.get("name") or "").strip()
        for a in (m.get("author") or [])
    ).strip("; ")
    parts = ((m.get("published-online") or {}).get("date-parts") or [[]])[0]
    date = "-".join(f"{int(p):02d}" if i else f"{int(p):04d}" for i, p in enumerate(parts)) if parts else ""
    url = ((m.get("resource") or {}).get("primary") or {}).get("URL", "")
    vol = str(m.get("volume") or "").strip()
    iss = str(m.get("issue") or "").strip()
    row = {c: "" for c in COLS}
    row.update({
        "title": title, "author(s)": authors, "published__online_date": date,
        "article_url": url or f"https://journals.sagepub.com/doi/{doi}",
        "volume": vol, "issue": iss, "OnlineFirst (Y/N)": "N" if (vol and iss) else "Y",
    })
    return row, title, vol, iss


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    out = os.path.join(ROOT, "input", "new_articles.csv")
    inputs, i = [], 0
    while i < len(args):
        if args[i] in ("--out", "-o"):
            i += 1
            if i >= len(args):
                print("ERROR: --out needs a path", file=sys.stderr)
                return 2
            out = args[i]
        else:
            inputs.append(args[i])
        i += 1

    new_rows = []
    for q in inputs:
        doi = norm_doi(q)
        if not DOI_RE.match(doi):
            print(f"  SKIP {q}: not an ASR DOI (10.1177/…)")
            continue
        try:
            row, title, vol, iss = block_a(doi)
            new_rows.append(row)
            print(f"  {doi}  vol {vol or '?'}.{iss or '?'}  {title[:55]}")
        except Exception as e:
            print(f"  SKIP {q}: {type(e).__name__}: {e}")

    if not new_rows:
        print("Nothing added.")
        return 1

    write_header = not os.path.exists(out) or os.path.getsize(out) == 0
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if write_header:
            w.writeheader()
        for r in new_rows:
            w.writerow(r)
    print(f"\nAdded {len(new_rows)} article(s) to {out} — Block A filled, coding columns empty.")
    print("Next: code Block B with Claude Code + Claude-in-Chrome (README Scenario 3, Step 2).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
