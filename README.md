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
- [Prerequisites](#prerequisites)
- [Quick Start (install)](#quick-start-install)
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

## Prerequisites

| To do this | You need |
|---|---|
| **Scenario 1** — look up a package (`lookup.py`) | **Python 3** — nothing else |
| Verify the published numbers (`reproduce_table.py`) | **Python 3** — nothing else |
| Add an article (`add_article.py`, Block A only) | Python 3 + an internet connection (Crossref) — no API key |
| **Scenario 2** — independently re-code a whole volume | Python 3 **and** [Claude Code](https://claude.com/claude-code) with **your own** API access, **and** the **Claude-in-Chrome** extension — because ASR is behind a **SAGE paywall + Cloudflare**, you must open each article in a real browser and **pass the Cloudflare "verify you are human" check once per session** to read its Data Availability Statement |
| **Scenario 3** — code new / historical articles (Block B) | Same as Scenario 2 (Claude Code + Claude-in-Chrome + passing Cloudflare) |

> **The Cloudflare check is manual and unavoidable.** ASR article pages sit behind SAGE's bot
> protection, so an agent cannot fetch them; a human passes the "verify you are human" check in the
> browser once, and the page text is then read out for coding. Everything else is automated.
>
> Coding (Scenarios 2 & 3) runs on **your own** Claude Code account — your API key or Claude
> subscription. Nothing routes through the author, and there is no shared key or server. The `mailto`
> in the fetch scripts is only Crossref's optional politeness identifier, not a credential — set
> `CROSSREF_MAILTO=you@example.com` to use your own, or leave it unset for the anonymous pool.

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
python3 pipeline/check_install.py
```

You should see:

```
Installation succeeded — ASR dataset loaded (vol 91 (2026): 26 articles; vol 90 (2025): 38 articles; 64 total).
```

That's it — nothing else to set up. Open `output/asr_vol90_result.csv` (or the `.xlsx`) to browse
the coding.

---

## Repository structure

```
asr/
├── agent.toml              # the 6-agent ASR pipeline spec (Download→Prep→Locate↺→Execute↺→Write)
├── docs/
│   ├── codebook.md         # the SHARED, journal-neutral codebook (Block B identical to SocSci)
│   └── run_provenance.md   # model / parameters / how the dataset was produced (honest record)
├── skills/                 # 8 sourcing skills the pipeline uses (DAS, OSF, GitHub, Dataverse, …)
├── pipeline/               # user-facing tools (standard library unless noted)
│   ├── check_install.py     #   'Installation succeeded' dataset check
│   ├── lookup.py            #   Scenario 1 — look up a package by DOI / URL
│   ├── reproduce_table.py   #   Scenario 2 — recompute the availability table
│   ├── add_article.py       #   Scenario 3 — add an article (Block A from Crossref; needs internet)
│   └── merge_new.py         #   Scenario 3 — merge coded rows into the dataset, by volume
├── scripts/                # deterministic ingestion; no LLM
│   ├── build_xlsx.py        #   create the empty workbook with headers
│   ├── crossref_fetch.py    #   fill Block A (title/authors/date/url/volume/issue) from Crossref
│   ├── format_xlsx.py       #   derive OnlineFirst + styling
│   └── html_sink.py         #   localhost helper for capturing article HTML from a real browser
├── input/                  # Block A tables, one per volume (asr_vol90.xlsx, asr_vol91.xlsx)
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

### Scenario 1 — find replication packages (by DOI / URL)

Pass a DOI or the SAGE article URL to `lookup.py`. It prints whether data and code were deposited
and the **exact repository link**. **One or many** at once:

```bash
# one article — by DOI
python3 pipeline/lookup.py 10.1177/00031224251320103

# or by URL
python3 pipeline/lookup.py https://journals.sagepub.com/doi/10.1177/00031224251324504

# several at once
python3 pipeline/lookup.py 10.1177/00031224251320103 10.1177/00031224251324504

# a long list — one query per line in a text file (# starts a comment)
python3 pipeline/lookup.py --file my_dois.txt
```

Output is a compact one-line-per-article table:

```
doi                        vol scope data code gate  package / how to obtain
----------------------------------------------------------------------------------------------------
10.1177/00031224251320103  90  Y     Y    Y    N     https://osf.io/jsypa/
10.1177/00031224251324504  90  Y     Y    Y    N     https://osf.io/smjnu/
```

`scope` = in-scope, `data`/`code` = deposited?, `gate` = data access-restricted? Open the package
link to download. For an **access-restricted** paper with no open package the last column shows
`[access-restricted] <how to apply>`. Add **`--detail`** for the full per-field view (title,
authors, and the verification notes). Coverage is the coded volumes; anything else is listed under
"not matched".

### Scenario 2 — reproduce the replication-package-availability table (independent re-coding)

Verify a **whole volume** yourself — re-run the coding method over every article in, say, vol 90 or
vol 91 and compare your table to the shipped one. Because ASR is behind a **SAGE paywall +
Cloudflare**, an agent cannot fetch the pages, so this path needs **Claude Code + the Claude-in-Chrome
extension**, and you must **pass the Cloudflare check once per session** (see
[Prerequisites](#prerequisites)). The output is *comparable, not byte-identical* — the agents make
judgment calls (see [`docs/run_provenance.md`](docs/run_provenance.md)).

**Step 1 — clone the repo and open Claude Code inside it.**

```bash
git clone https://github.com/borun-li/asr-replication-availability.git
cd asr-replication-availability
claude                      # starts Claude Code in this folder
```

**Step 2 — paste this prompt to Claude Code.** It points Claude at the method plus the volume's
worklist (`input/asr_vol90.xlsx` already has Block A filled, coding columns empty):

> Read `agent.toml` (the six-agent spec), `docs/codebook.md` (the coding rubric), and every
> `SKILL.md` under `skills/`. For each article in `input/asr_vol90.xlsx`, drive the Claude-in-Chrome
> browser to open its SAGE page (I will pass the Cloudflare check), read the **Data Availability
> Statement** + abstract + repository links, then run **Scope → Locate → Verify → Execute → Verify**:
> locate the replication package, **verify the repository through its API** (OSF / GitHub / Dataverse
> / OpenICPSR), and fill the coding columns strictly per the codebook. Work in batches and pause for
> me to review. Write the filled rows to `output/my_vol90_recode.csv`.

**Step 3 — compare your coding to the shipped dataset.** Run the same summary over each and check
the numbers line up:

```bash
python3 pipeline/reproduce_table.py output/my_vol90_recode.csv       # your re-coding
python3 pipeline/reproduce_table.py output/asr_vol90_result.csv      # the shipped dataset
```

For a row-by-row comparison, open both in a spreadsheet or `diff` them. Expect close-but-not-identical
agreement, concentrated on borderline judgment calls.

---

**Shortcut — just verify the published numbers** (no re-coding, Python only):

```bash
python3 pipeline/reproduce_table.py
```

It re-derives the per-volume and overall availability rates from the shipped `output/asr_*_result.csv`.

### Scenario 3 — code newly published articles (extend coverage) or check one historical article

New ASR issues keep appearing, and you may want to check whether a **specific historical article**
has a package. Either way: add it, code it, merge it.

**Step 1 — add the article (Block A is auto-filled).** Pass the DOI or URL; the tool fetches the
bibliographic metadata **from Crossref** and appends a row to `input/new_articles.csv` with Block A
filled and the coding columns empty:

```bash
python3 pipeline/add_article.py 10.1177/00031224251320103
python3 pipeline/add_article.py https://journals.sagepub.com/doi/10.1177/00031224251324504
python3 pipeline/add_article.py <doi-or-url> <doi-or-url> …          # several at once
```

This step needs an internet connection but no API key (Python only). No manual data entry.

**Step 2 — code Block B with Claude Code.** In the repo folder run `claude`, then paste:

> Read `agent.toml`, `docs/codebook.md`, and every `SKILL.md` under `skills/`. For each article in
> `input/new_articles.csv` (Block A filled, coding columns empty), drive the Claude-in-Chrome browser
> to open its SAGE page (I will pass the Cloudflare check), read the **Data Availability Statement** +
> abstract + repository links, then run **Scope → Locate → Verify → Execute → Verify**, verify the
> repository through its API, and fill the coding columns strictly per the codebook. Write the filled
> rows back to `input/new_articles.csv`.

**Step 3 — merge into the dataset (one command).** The merge routes each coded row into its volume's
`output/asr_vol<N>_result.csv`, adds **only coded rows**, skips duplicates (by DOI), recomputes the
derived columns, and updates the `.xlsx` if `openpyxl` is installed:

```bash
python3 pipeline/merge_new.py --dry-run    # preview what would be added — writes nothing
python3 pipeline/merge_new.py              # merge input/new_articles.csv into the dataset
```

Then verify with `python3 pipeline/reproduce_table.py`, or look the new articles up with
`python3 pipeline/lookup.py`. New coding uses the pinned parameters in
[`docs/run_provenance.md`](docs/run_provenance.md), so it stays consistent with the existing table.

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
