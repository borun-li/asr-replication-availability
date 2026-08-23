#!/usr/bin/env python3
"""Prepare a volume's Block A worklist in ONE step.

    python3 scripts/prepare_input.py --year 2024

Runs the three ingestion scripts in order — build_xlsx -> crossref_fetch -> format_xlsx —
and produces `input/asr_<year>.xlsx` with Block A filled (title, authors, published-online
date, url, volume, issue, OnlineFirst) and the coding columns empty, ready for Scenario 2 / 3.

Deterministic, no LLM. Needs an internet connection and `pip install requests openpyxl`.
Set CROSSREF_MAILTO to your email to use Crossref's faster polite pool (optional).
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["build_xlsx.py", "crossref_fetch.py", "format_xlsx.py"]


def main():
    ap = argparse.ArgumentParser(description="Prepare input/asr_<year>.xlsx (Block A) in one step.")
    ap.add_argument("--year", type=int, required=True, help="publication year to ingest, e.g. 2024")
    year = ap.parse_args().year

    for script in STEPS:
        print(f"\n=== {script} --year {year} ===", flush=True)
        try:
            subprocess.run([sys.executable, str(HERE / script), "--year", str(year)], check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"\nFAILED at {script} (exit {e.returncode}). "
                     f"Check the message above (network? missing 'requests'/'openpyxl'?).")

    print(f"\nDone -> input/asr_{year}.xlsx  (Block A complete; coding columns empty).")
    print("Next: code Block B — see README Scenario 2 (whole volume) or Scenario 3 (single article).")


if __name__ == "__main__":
    main()
