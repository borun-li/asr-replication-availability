# American Sociological Review — Replication-Package Availability

An open coding of whether *American Sociological Review* (ASR) articles ship a **replication
package** — i.e. whether the authors deposited the **data** and/or the **code** needed to reproduce
their results — built with a small multi-agent pipeline (Claude Code) on a shared, journal-neutral
codebook.

This is the ASR companion to the [Sociological Science availability
project](https://github.com/borun-li/socsci-replication-availability): **Block B (the availability
coding) is identical across the two journals**, so take-up rates are directly comparable. What
differs is only the *sourcing* layer (ASR is published by SAGE, behind a paywall + Cloudflare),
captured in this repo's `agent.toml` and `skills/`.

## Description

For every in-scope ASR article we record, under a fixed codebook, whether the authors deposited
their **analysis data** (`data`), the **code** that reproduces the paper (`code`), and whether the
underlying data is **gated** (restricted / proprietary / IRB / register / available-on-request).
Bibliographic fields (Block A) come deterministically from Crossref; the availability judgement
(Block B) is produced by an agent pipeline that reads each article's **Data Availability Statement**
and then verifies the named repository (OSF / GitHub / Dataverse / OpenICPSR) through its API.

## Table of Contents

- [Repository structure](#repository-structure)
- [The dataset](#the-dataset)
- [The codebook](#the-codebook)
- [How it works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Reproducibility & provenance](#reproducibility--provenance)
- [Roadmap](#roadmap)
- [Citation](#citation)
- [License](#license)
- [Contributions](#contributions)

## Repository structure

```
asr/
├── agent.toml              # the 6-agent ASR pipeline spec (Download→Prep→Locate↺→Execute↺→Write)
├── docs/
│   ├── codebook.md         # the SHARED, journal-neutral codebook (Block B identical to SocSci)
│   └── run_provenance.md   # model / parameters / how the dataset was produced (honest record)
├── skills/                 # 8 sourcing skills the pipeline uses (DAS, OSF, GitHub, Dataverse, …)
├── scripts/                # deterministic ingestion (Crossref → input table); no LLM
│   ├── build_xlsx.py        #   create the empty workbook with headers
│   ├── crossref_fetch.py    #   fill Block A (title/authors/date/url/volume/issue) from Crossref
│   ├── format_xlsx.py       #   derive OnlineFirst + styling
│   └── html_sink.py         #   localhost helper for capturing article HTML from a real browser
├── input/                  # Block A tables, one per volume (asr_vol90.xlsx, asr_2026.xlsx = vol 91)
├── output/                 # the coded dataset (asr_vol90_result.xlsx, asr_2026_result.xlsx)
├── instructions.md         # ingestion runbook
├── PROJECT_LOG.md          # phase-by-phase build log
└── LICENSE
```

`cache/` (raw SAGE article HTML) is **not** published — it is copyrighted full-text and only a
working cache.

## The dataset

One row per article, keyed by DOI. **Block A** is bibliographic (DOI, title, authors,
published-online date, URL, volume, issue). **Block B** is the availability coding, identical to
the SocSci project:

| column | meaning |
|---|---|
| `in_scope` | `Y` = original empirical analysis; `NA` = nothing to reproduce (essay/comment/index) |
| `qualitative` | `Y` = primary evidence non-numeric (interviews/ethnography), interpreted directly |
| `data` | `Y` = authors **physically deposited** the analysis data files (a pointer/link is not a deposit) |
| `code` | `Y` = authors deposited code that reproduces this paper |
| `data + code` / `neither` | derived |
| `data_gated` | `Y` = underlying data not freely public (restricted/IRB/register/on-request). **Quantitative papers only** |
| `data_source / apply_at` | the concrete access route when `data_gated = Y` |
| `package_location` / `path_to_package` / `coverage_checked` / `notes` | provenance of the judgement |

**Coverage so far** (by volume):

| volume | year | articles | in-scope | data=Y | code=Y | availability (data or code) |
|---|---|---|---|---|---|---|
| vol 91 | 2026 (pilot) | 26 | 24 | 10 | 12 | **13/24 = 54.2%** |
| vol 90 | 2025 | 38 | 32 | 7 | 12 | **12/32 = 37.5%** |

The denominator is in-scope empirical articles and is **access-agnostic** — a paywalled article is
coded and counted exactly like an open one (the Data Availability Statement is public regardless).

## The codebook

`docs/codebook.md` is **shared and journal-neutral**. Block B (the coding definitions) is byte-for-byte
the same as in the SocSci project, which is what makes the two datasets comparable. Only Block A and
the *sourcing* (where materials live on SAGE) are ASR-specific. Key rules:

- **`data = Y` is a deposit test, not a public/private test.** Data files physically settled into
  the package count (even public-sourced ones); a mere link to an external archive does not.
- **`data_gated` applies to quantitative papers only** — it is left blank for `qualitative = Y`
  (a qualitative study is not reproduced from its data, so data-gating is not the operative frame).
- **A free hosting-platform login is not a gate** (needing an OSF/Dataverse account to download an
  open deposit ≠ `data_gated = Y`).

## How it works

1. **Ingest (deterministic, no LLM).** `scripts/` query Crossref by ISSN + year and fill Block A;
   articles are grouped by **volume**.
2. **Capture the article evidence.** ASR sits behind a SAGE paywall + Cloudflare bot-check, so the
   article's **Data Availability Statement**, abstract, and repository links are captured from a
   **real browser** (a human passes the Cloudflare check once per session; the page text is then
   read out). This is the one step that cannot be fully automated.
3. **Code (agent pipeline).** For each article an agent reads the codebook + skills, decides scope,
   locates the package from the DAS, and **verifies the repository through its API** (OSF, GitHub,
   Dataverse, OpenICPSR) — opening the actual file listing to decide `data` / `code` — then writes
   Block B.
4. **Merge** the coded rows into the volume's `output/` workbook.

## Prerequisites

- Python 3.9+ with `requests` and `openpyxl` (for the ingestion scripts).
- [Claude Code](https://claude.com/claude-code) to run the agent pipeline, plus the Claude-in-Chrome
  extension for the browser-capture step.
- `CROSSREF_MAILTO` (optional) — set it to your email for Crossref's faster "polite pool"; unset,
  the scripts query the anonymous pool. **No personal contact is hard-coded.**

## Reproducibility & provenance

See `docs/run_provenance.md` for the full record. In short: model `claude-opus-4-8`; **temperature =
platform default** (the workflow harness exposes no temperature parameter — this is recorded
honestly, not back-filled to 0); `agent.toml` v1.1.0; shared codebook. The coded dataset is a
**hybrid** — an agent-pipeline base that was then human-reviewed — so it should be cited as a
human-verified coding, not raw model output.

## Roadmap

- User-facing lookup / reproduce / add-article tools (as in the SocSci repo) are planned.
- Extending coverage backward, one volume per year, toward 2014.

## Citation

> Li, Borun. *American Sociological Review — Replication-Package Availability.* 2026.
> https://github.com/borun-li/asr-replication-availability

## License

MIT — see [LICENSE](LICENSE). Note that `cache/` (SAGE full-text) is intentionally excluded; this
repo redistributes only bibliographic metadata and our own coding.

## Contributions

Issues and corrections are welcome — please open a GitHub issue with the DOI and the specific
field in question.
