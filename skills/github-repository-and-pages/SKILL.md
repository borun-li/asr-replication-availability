---
name: github-repository-and-pages
description: The replication package is a GitHub repository (often owned by a lab/project ORG, not a personal author handle, in ASR). Step-by-step to read the repo tree + README via the API, judge data/code, and verify provenance by repo NAME / README / DOI back-reference rather than owner==author.
---

# Source: GitHub (github.com)

## When you get routed here
A `github.com/<owner>/<repo>` link from `asr-data-availability-statement`, the PDF, or an author
page. In ASR the owner is frequently a **lab / project organization** (e.g.
`OSU-UW-CCP`, `OSU-UW`), and repos are often named for the article
(`State-Safety-Net-ASR26`, `Replication-…-ASR`, `..._ASR_26_RTW`).

## Step-by-step: READ (API, no auth)
1. Normalize to `owner/repo`. Read the default branch tree:
   `https://api.github.com/repos/<owner>/<repo>/git/trees/<branch>?recursive=1`
   (or the repo landing HTML if the API is rate-limited).
2. Read the **README** and any `Read.Me`/`replication`/`docs` file — it states what is included and
   where the data come from.
3. Note scripts (`.do`/`.R`/`.py`/`.ipynb`) vs datasets (`.dta`/`.csv`/`.rda`) in the tree.

## Coding from GitHub — [v3.3 physical-deposit rule]
- `code = Y` if the authors' analysis scripts for THIS paper are present.
- `data = Y` when the authors **physically deposited analysis data files** in the repo tree — even
  when those files come from **public sources** (BEA/ACS/policy `.dta` committed into the repo are
  a deposit, not a pointer). The authors settled the data into a package → `data = Y`.
- **Partial/mixed deposit (common in ASR):** the repo commits some public-sourced analysis data
  BUT a **core portion is proprietary/restricted and ABSENT** (e.g. individual-level microdata the
  authors cannot share). This is still `data = Y` **and** `data_gated = Y` — the restricted portion
  sets the gate, it does **not** erase the deposit. State the basis in `notes`.
- `data = N` only when **no analysis data files are committed** — the tree holds scripts only, or
  the README merely **points** to an external source the replicator must download themselves.
- `package_location` = the repo URL (a specific release/tag if the README pins one).

## Provenance — [ASR] match by repo, not by personal owner
Do NOT require `owner == a personal author handle`. Confirm the repo belongs to THIS paper by:
- **repo name** referencing the article / "ASR" / the topic, AND/OR
- the **README** naming the paper, the authors, or the article DOI (a DOI back-reference is
  strongest), AND/OR
- the DAS/article explicitly linking this repo.
A lab/project **org** owner (a co-author's lab) is valid provenance — do not false-reject it.

## Gotchas
- A repo of a **general method/software** the authors wrote is a **tool**, not a package
  (RULE 2) — unless it bundles this paper's own analysis scripts.
- A fork/mirror of someone else's tool (e.g. `lme4/lme4`, `OxCGRT/...`) is a **dependency**, not
  the authors' deposit → do not record it as the package.
- A repo with only a manuscript/PDF is not a package.

## Worked example (ASR-2026 pilot)
- **"Unsecured Credit and the Social Safety Net":** `github.com/OSU-UW-CCP/State-Safety-Net-ASR26`
  — owner is the project **org** (not a personal handle), repo name references the article and ASR;
  README + `.do` file confirm it reproduces this paper → valid provenance, `code = Y`. The repo
  **physically commits** public-sourced `.dta` (BEA price parities / ACS extracts / state-policy
  tables) → **`data = Y`** (v3.3 — a deposit, not a pointer). The individual-level credit-bureau
  panel is proprietary and absent → **`data_gated = Y`**, noted as the basis for the gate.

## After reading → `agent.toml` Exec-Verify (repo-name/README/DOI provenance; org-owned is OK).
