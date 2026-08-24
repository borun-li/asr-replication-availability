#!/usr/bin/env python3
"""Confirm the ASR availability dataset loads. Standard-library only — no pip install, no API key.

    python3 scripts/check_install.py

Prints 'Installation succeeded' with a per-volume article count if everything is in place.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL_TO_YEAR = 1935  # ASR year = volume + 1935 (vol 91 = 2026)


def discover():
    """Auto-discover every coded volume from output/asr_vol<N>_result.csv, newest first."""
    out = []
    for path in ROOT.glob("output/asr_vol*_result.csv"):
        m = re.search(r"asr_vol(\d+)_result\.csv$", path.name)
        if m:
            vol = int(m.group(1))
            out.append((vol, f"vol {vol} ({vol + VOL_TO_YEAR})", path))
    return [(label, path) for _, label, path in sorted(out, reverse=True)]


def load(path):
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def main():
    if sys.version_info < (3, 7):
        sys.exit(f"Need Python 3.7+, found {sys.version.split()[0]}")

    datasets = discover()
    if not datasets:
        sys.exit("No coded volumes found under output/ (expected asr_vol<N>_result.csv).\n"
                 "(Run this from a full checkout of the repository.)")

    total = 0
    parts = []
    for label, path in datasets:
        rows = load(path)
        n = sum(1 for r in rows if (r.get("title") or "").strip())
        total += n
        parts.append(f"{label}: {n} articles")

    print("Installation succeeded — ASR dataset loaded (" + "; ".join(parts) + f"; {total} total).")
    print("Nothing else to set up. Open output/asr_vol90_result.csv (or the .xlsx) to browse the coding.")


if __name__ == "__main__":
    main()
