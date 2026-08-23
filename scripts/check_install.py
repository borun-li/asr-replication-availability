#!/usr/bin/env python3
"""Confirm the ASR availability dataset loads. Standard-library only — no pip install, no API key.

    python3 scripts/check_install.py

Prints 'Installation succeeded' with a per-volume article count if everything is in place.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS = [
    ("vol 91 (2026)", ROOT / "output" / "asr_vol91_result.csv"),
    ("vol 90 (2025)", ROOT / "output" / "asr_vol90_result.csv"),
]


def load(path):
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def main():
    if sys.version_info < (3, 7):
        sys.exit(f"Need Python 3.7+, found {sys.version.split()[0]}")

    total = 0
    parts = []
    for label, path in DATASETS:
        if not path.exists():
            sys.exit(f"Dataset not found: {path}\n(Run this from a full checkout of the repository.)")
        rows = load(path)
        n = sum(1 for r in rows if (r.get("title") or "").strip())
        total += n
        parts.append(f"{label}: {n} articles")

    print("Installation succeeded — ASR dataset loaded (" + "; ".join(parts) + f"; {total} total).")
    print("Nothing else to set up. Open output/asr_vol90_result.csv (or the .xlsx) to browse the coding.")


if __name__ == "__main__":
    main()
