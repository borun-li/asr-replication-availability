---
name: dataverse-any-host
description: The replication package is in a Dataverse repository — Harvard Dataverse OR any other institutional/national Dataverse installation (ASR authors use many). Step-by-step to read any Dataverse dataset via its API (landing pages are JS-rendered), list files, and code data/code + data_gated.
---

# Source: Dataverse (Harvard **and any other** installation)

## When you get routed here
A Dataverse URL or dataset DOI from `asr-data-availability-statement`. Unlike SocSci (Harvard
Dataverse only), ASR authors deposit on **many Dataverse installs** — Harvard
(`dataverse.harvard.edu`), but also university/national ones (e.g. `edatos.consorciomadrono.es`,
`dataverse.nl`, `data.sciencespo.fr`). Treat the **host as a variable**, not a constant.

## Identify the dataset
- Landing URL: `https://<host>/dataset.xhtml?persistentId=doi:10.7910/DVN/XXXXXX` (or `/DVN/...`).
- Dataset DOI: `10.7910/DVN/...` (Harvard) or another prefix for other installs; a DAS/Crossref
  dataset DOI resolves to its host.

## Step-by-step: READ VIA THE API (landing pages are JS-rendered — HTML fetch returns little)
1. Take the **host** and the **persistentId** (the `doi:...`).
2. Query the native API on that host:
   `https://<host>/api/datasets/:persistentId/?persistentId=doi:<DVN-id>`
   → JSON with `latestVersion.files[]` (each has `label`, `directoryLabel`, `restricted`) and the
   dataset metadata (title, authors).
3. List the files from the API response — do NOT scrape the JS landing page.
4. If a file's `restricted: true`, its content is access-gated (request/approval) — the file is
   **catalogued and physically in the dataset**, just not openly downloadable.
5. **Retry once on a failed/empty API response before concluding empty** — transient errors happen.

## Coding from Dataverse — [v3.3 physical-deposit rule]
- `code = Y` if the authors' analysis scripts for THIS paper are present.
- `data = Y` when the authors' **analysis data files are physically in the dataset** — public-
  sourced files count, and a `restricted: true` file is **still a deposit**: the authors uploaded
  it, access is merely gated → `data = Y` **and** `data_gated = Y` (apply-at = the Dataverse
  "request access" route).
- `data = N` only when **no analysis data files are in the dataset** — the deposit is scripts-only,
  or the data lives in an **external** source the dataset merely points to (then `data_gated = Y`
  with apply-at = the underlying provider).
- `package_location` = the dataset landing URL (with persistentId).

## Gotchas
- **Non-Harvard host** is normal for ASR — always read the host from the URL; never assume Harvard.
- A file marked `restricted` in the API = gated data, package still found.
- Some installs require an API token for restricted files — do NOT authenticate; code from the
  public file list + metadata.
- **Bot-walled installs.** Some non-Harvard Dataverse installs (e.g. `edatos.consorciomadrono.es`)
  sit behind an anti-bot challenge (Anubis "Access Denied") that blocks even the native API. Retry
  once; if it stays blocked, do **not** conclude "no package" — code from the **DAS text** (which
  names the deposit and what is in it) and record "Dataverse API bot-walled; coded from DAS" in
  `notes`. Never attempt to defeat the challenge.
- **A COLLECTION holds several datasets — enumerate and OPEN the files; never judge by title.**
  When the DAS points to a Dataverse **collection** (`/dataverse/<name>`, not a single dataset),
  list every dataset in it (`/api/dataverses/<name>/contents`) and then **every file in each
  dataset** (`/api/datasets/:persistentId/?persistentId=doi:<id>`). **Do NOT decide whether code or
  data exists from a dataset's TITLE, a file's name, or the DAS's tense** — always inspect the
  actual file list, and if a file is a `.zip`, download and list its contents. Replication **code**
  is frequently filed inside a dataset whose title says "data," and DAS wording is often future
  tense even when the file is already present. *(Effort case: the paper's R code
  `Radl_et_al_2026.zip` — 12 `.R`/`.Rmd` files — sat inside the dataset titled "Parent experimental
  **data**", and the DAS said code "will be available"; a title/tense-based read wrongly concluded
  code=N. Listing the collection's files and unzipping the archive gives the correct code=Y.)*
- Distinguish a **data-only** deposit from a full package: a Dataverse holding only `.tab`/`.dta`
  and no scripts is `data`-relevant but may leave `code = N` (check the DAS for a separate code host).

## After reading → `agent.toml` Exec-Verify (confirm dataset authors match THIS paper).
