"""Shared helpers to read the coded ASR dataset (output/asr_*_result.csv).

Standard library only. The result CSVs use display headers (e.g. 'data(Y/N)'); this module
normalizes each row to canonical keys and derives the DOI from the article_url.
"""
import csv
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
RESULT_GLOB = os.path.join(ROOT, "output", "asr_*_result.csv")

# canonical key -> a substring that uniquely identifies its display header
_KEYS = {
    "title": "title", "authors": "author", "url": "article_url", "volume": "volume",
    "issue": "issue", "published": "published__online", "onlinefirst": "onlinefirst",
    "in_scope": "in_scope", "qualitative": "qualitative", "data": "data(y",
    "code": "code(y", "data_and_code": "data + code", "neither": "neither",
    "data_gated": "data_gated", "apply": "data_source", "package_location": "package_location",
    "path": "path_to_package", "coverage": "coverage_checked", "notes": "notes",
}

DOI_RE = re.compile(r"(10\.1177/[0-9A-Za-z._]+)")


def norm_doi(q):
    q = re.sub(r"^(https?://)?(dx\.)?doi\.org/|^doi:\s*", "", (q or "").strip(), flags=re.I)
    m = DOI_RE.search(q)
    return (m.group(1) if m else q).rstrip("/").lower()


def _colmap(fieldnames):
    fn = fieldnames or []
    out = {}
    for key, sub in _KEYS.items():
        for h in fn:
            if h and sub in str(h).lower():
                out[key] = h
                break
    return out


def load_csv(path):
    """Return (rows, volume_label). Each row is a dict of canonical keys (+ 'doi')."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cm = _colmap(reader.fieldnames)
        rows = []
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            r = {k: (raw.get(col) or "").strip() for k, col in cm.items()}
            r["doi"] = norm_doi(r.get("url", ""))
            r["_source"] = os.path.basename(path)
            rows.append(r)
    return rows


def load_all():
    rows = []
    for path in sorted(glob.glob(RESULT_GLOB)):
        rows.extend(load_csv(path))
    return rows
