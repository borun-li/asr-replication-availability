# American Sociological Review — Replication-Package Availability

An open coding of whether *American Sociological Review* (ASR) articles ship a **replication
package** — i.e. whether the authors deposited the **data** and/or the **code** needed to reproduce
their results — built with a small multi-agent pipeline (Claude Code) on a shared, journal-neutral
codebook.

This is the ASR companion to the [Sociological Science availability
project](https://github.com/borun-li/socsci-replication-availability): **Block B (the availability
coding) is identical across the two journals**, so take-up rates are directly comparable. Only the
*sourcing* layer differs (ASR is published by SAGE, behind a paywall + Cloudflare), captured in this
repo's `agent.toml` and `skills/`.

## Description

Each in-scope empirical article is coded for whether the authors deposited an analysis **dataset**
and/or **code**, where the package lives (the exact repository link), and — when the underlying data
is access-restricted — how to apply for it. Because Block B is identical to the SocSci project, the
two datasets are directly comparable. Coverage so far, by volume:

| volume | year | in-scope articles | data=Y | code=Y | Availability (data and/or code deposited) |
|---|---|---|---|---|---|
| vol 91 | 2026 (pilot) | 24 | 10 | 12 | **13 / 24 = 54.2%** |
| vol 90 | 2025 | 32 | 7 | 12 | **12 / 32 = 37.5%** |

The denominator is in-scope empirical articles and is **access-agnostic** — a paywalled article is
coded and counted exactly like an open one (the Data Availability Statement is public regardless).

---

## Table of Contents

- [Description](#description)
- [Quick Start (install)](#quick-start-install)
  - [Prerequisites](#prerequisites)
- [Repository structure](#repository-structure)
- [The dataset](#the-dataset)
- [Using it](#using-it)
- [Methodology & quality control](#methodology--quality-control)
- [Reproducibility](#reproducibility)
- [Citation](#citation)
- [License](#license)
- [Contributions](#contributions)
- [Contact](#contact)

---

## Quick Start (install)

The shipped dataset is plain **CSV** (plus an `.xlsx` copy). Confirming the install and browsing the
data need **only Python 3** — no `pip install`, no API key — and run the same on **macOS, Linux, and
Windows**. (Independently *coding new articles* is a separate, heavier path that needs Claude Code —
see [Using it](#using-it).)

**Step 1 — make sure Python 3 is installed.** In a terminal:

```bash
python3 --version
```

You should see `Python 3.x.x`. If it says "command not found":
- **macOS** — `brew install python` (or install from <https://www.python.org/downloads/>)
- **Ubuntu/Debian Linux** — `sudo apt update && sudo apt install -y python3`
- **Windows** — install from <https://www.python.org/downloads/> and tick **"Add python.exe to
  PATH"**; then use `python` instead of `python3` in PowerShell.

**Step 2 — download this repository.**

```bash
git clone https://github.com/borun-li/asr-replication-availability.git
cd asr-replication-availability
```

(No `git`? Use the green **Code → Download ZIP** button on GitHub, unzip it, and `cd` into the
folder.)

**Step 3 — confirm it works.**

```bash
python3 scripts/check_install.py
```

You should see:

```
Installation succeeded — ASR dataset loaded (vol 91 (2026): 26 articles; vol 90 (2025): 38 articles; 64 total).
```

That's it — nothing else to set up. Open `output/asr_vol90_result.csv` (or the `.xlsx`) to browse
the coding.

### Prerequisites

| To do this | You need |
|---|---|
| **Browse the dataset** / run `check_install.py` | **Python 3** — nothing else (standard library only) |
| Re-run the **ingestion** (`scripts/`) for a new volume | Python 3 + `pip install requests openpyxl` + internet |
| **Code new articles** (extend coverage) | [Claude Code](https://claude.com/claude-code) with **your own** API access + the Claude-in-Chrome extension (to read paywalled SAGE pages) |

> Coding runs on **your own** Claude Code account — your API key or Claude subscription. Nothing
> routes through the author, and there is no shared key or server. The `mailto` in the fetch scripts
> is only Crossref's optional politeness identifier, not a credential — set
> `CROSSREF_MAILTO=you@example.com` to use your own, or leave it unset for the anonymous pool.

---

## Repository structure

```
asr/
├── agent.toml              # the 6-agent ASR pipeline spec (Download→Prep→Locate↺→Execute↺→Write)
├── docs/
│   ├── codebook.md         # the SHARED, journal-neutral codebook (Block B identical to SocSci)
│   └── run_provenance.md   # model / parameters / how the dataset was produced (honest record)
├── skills/                 # 8 sourcing skills the pipeline uses (DAS, OSF, GitHub, Dataverse, …)
├── scripts/                # deterministic ingestion + install check; no LLM
│   ├── build_xlsx.py        #   create the empty workbook with headers
│   ├── crossref_fetch.py    #   fill Block A (title/authors/date/url/volume/issue) from Crossref
│   ├── format_xlsx.py       #   derive OnlineFirst + styling
│   ├── html_sink.py         #   localhost helper for capturing article HTML from a real browser
│   └── check_install.py     #   'Installation succeeded' dataset check (standard library only)
├── input/                  # Block A tables, one per volume (asr_vol90.xlsx, asr_2026.xlsx = vol 91)
├── output/                 # the coded dataset — CSV + xlsx (asr_vol90_result.*, asr_vol91_result.*)
├── instructions.md         # ingestion runbook
└── LICENSE
```

`cache/` (raw SAGE article HTML) is **not** published — it is copyrighted full-text and only a
working cache.

## The dataset

One row per article, keyed by DOI. **Block A** is bibliographic (DOI, title, authors,
published-online date, URL, volume, issue). **Block B** is the availability coding, identical to the
SocSci project:

| column | meaning |
|---|---|
| `in_scope` | `Y` = original empirical analysis; `NA` = nothing to reproduce (essay/comment/index) |
| `qualitative` | `Y` = primary evidence non-numeric (interviews/ethnography), interpreted directly |
| `data` | `Y` = authors **physically deposited** the analysis data files (a pointer/link is not a deposit) |
| `code` | `Y` = authors deposited code that reproduces this paper |
| `data + code` / `neither` | derived |
| `data_gated` | `Y` = the underlying data is **access-restricted** (not freely downloadable). Quantitative papers only |
| `data_source / apply_at` | the concrete access route when `data_gated = Y` |
| `package_location` / `path_to_package` / `coverage_checked` / `notes` | provenance of the judgement |

Two guiding rules worth flagging: **`data = Y` is a deposit test, not a public/private test** (files
physically settled into the package count, even public-sourced ones; a mere link to an external
archive does not); and **a free hosting-platform login is not a gate** (needing an OSF/Dataverse
account to download an open deposit does not make the data access-restricted).

## Using it

- **Browse the coding.** Open `output/asr_vol90_result.csv` / `output/asr_vol91_result.csv` (or the
  `.xlsx`) in any spreadsheet or with Python. Every row carries the repository link
  (`package_location`) and a `notes` field explaining the judgement.
- **Reproduce the ingestion** for a volume: run `scripts/build_xlsx.py` → `crossref_fetch.py` →
  `format_xlsx.py` (see `instructions.md`) to rebuild Block A from Crossref.
- **Extend coverage** (code a new volume): this is the agent pipeline described under
  [Methodology](#methodology--quality-control); it needs Claude Code + the browser-capture step.
- User-facing **lookup / reproduce-table** tools (as in the SocSci repo) are planned.

## Methodology & quality control

1. **Ingest (deterministic, no LLM).** `scripts/` query Crossref by ISSN + year and fill Block A;
   articles are grouped by **volume**.
2. **Capture the article evidence.** ASR sits behind a SAGE paywall + Cloudflare bot-check, so each
   article's **Data Availability Statement**, abstract, and repository links are read from a **real
   browser** (a human passes the Cloudflare check once per session). This is the one step that
   cannot be fully automated.
3. **Code (agent pipeline).** For each article an agent reads the codebook + skills, decides scope,
   locates the package from the DAS, and **verifies the repository through its API** (OSF, GitHub,
   Dataverse, OpenICPSR) — opening the actual file listing to decide `data` / `code` — then writes
   Block B.
4. **Quality control.** The pilot volume was validated by an independent **blind re-coding**
   (fresh agents, no access to the answer key): **96.5% agreement**, with the disagreements resolved
   by human review. The coded rows are then human-spot-checked before a volume is finalized.

## Reproducibility

See `docs/run_provenance.md` for the full record. In short: model `claude-opus-4-8`; **temperature =
platform default** (the workflow harness exposes no temperature parameter — this is recorded
honestly, not back-filled to `0`); `agent.toml` v1.1.0; shared codebook. The coded dataset is a
**hybrid** — an agent-pipeline base that was then human-reviewed — so it should be cited as a
human-verified coding, not raw model output.

## Citation

> Li, Borun. *American Sociological Review — Replication-Package Availability.* 2026.
> https://github.com/borun-li/asr-replication-availability

## License

MIT — see [LICENSE](LICENSE). Note that `cache/` (SAGE full-text) is intentionally excluded; this
repo redistributes only bibliographic metadata and our own coding.

## Contributions

Issues and corrections are welcome — please open a GitHub issue with the DOI and the specific field
in question.

## Contact

Open a [GitHub issue](https://github.com/borun-li/asr-replication-availability/issues) for anything
about the data or the method — that keeps the discussion attached to the DOI in question.
