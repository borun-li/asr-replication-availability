---
name: openicpsr-repository
description: The replication package is on OpenICPSR (openicpsr.org) — the AEA/ASA-style self-deposit archive that ASR authors commonly use. Step-by-step to read the project's file manifest and README, handle the login/agreement gate WITHOUT signing in, and code data/code + data_gated.
---

# Source: OpenICPSR (openicpsr.org)

## When you get routed here
An `openicpsr.org/openicpsr/project/<id>/...` link (or a `doi.org/10.3886/E<id>...` dataset DOI
that resolves to OpenICPSR), handed over by `asr-data-availability-statement` or found via repo
search. OpenICPSR is a **self-deposit** archive (authors upload their own package); it is very
common for ASR quantitative articles.

## Step-by-step: LOCATE + READ (without logging in)
1. Open the project page. Note the **project id** and version (e.g. `project/157201/version/V2`).
2. Read the public **project description**, the **file manifest / "Data and Program Files"** list,
   and any **README** — these are usually visible without login and tell you what is deposited
   (scripts, datasets, documentation) and where the data come from.
3. The manifest distinguishes **program files** (`.do`, `.R`, `.py`) from **data files**
   (`.dta`, `.csv`) — use it to judge `code` and `data` even if the actual download is gated.

## The download/agreement gate — record it, NEVER sign in
Many OpenICPSR projects require **agreeing to Terms of Use / logging in / requesting access** to
download the files. That is a human decision — the agent **must not** log in, register, or accept
any agreement. Instead:
- treat the login/agreement wall as **normal, not "dead"** (the package exists);
- code from the **public manifest + README** (what is deposited);
- if the DATA files are behind an access application (restricted-use deposit), that is
  `data_gated = Y` with the OpenICPSR project URL as the apply-at.

## Coding from OpenICPSR — [v3.3 physical-deposit rule]
- `code = Y` if the manifest lists the authors' analysis program files for THIS paper.
- `data = Y` when the authors **physically deposited the analysis data files** in the project —
  even if those data came from a **public source** (the deposit test is *in the package vs.
  pointer*, not public vs. private). A **restricted download/agreement gate** on a deposited file
  does not flip it to `N`: the file is deposited → `data = Y` **and** `data_gated = Y`.
- `data = N` only when **no analysis data files are deposited** — the manifest holds program files
  only, or the README merely **points** the replicator to an external source they must fetch
  themselves.
- **Partial/mixed deposit:** if the project deposits some analysis data but a **core portion is
  proprietary/absent** (e.g. a vendor panel the authors cannot share) → `data = Y` **and**
  `data_gated = Y`; state the basis in `notes`.
- `package_location` = the OpenICPSR project URL (canonical, with version if shown).

## Gotchas
- A **restricted-use** OpenICPSR deposit ("access requires application/DUA") = package found, data
  gated → record apply-at = the project URL; do not conclude "no package".
- Version matters: prefer the version the DAS/article cites; note it in `path_to_package`.
- OpenICPSR mints DOIs (`10.3886/E<id>Vn`) — a dataset DOI in the DAS or Crossref relation
  metadata resolves here.

## Worked example — a THIRD-PARTY OpenICPSR project is NOT the authors' deposit
- **"Unsecured Credit and the Social Safety Net" (10.1177/00031224251411563):** OpenICPSR project
  `157201` appears near the DAS, but it is a **third-party eviction-moratorium dataset the authors
  cite**, NOT their own package (RULE 2 — a cited source is not a deposit). The authors' real
  package is the **GitHub** repo `OSU-UW-CCP/State-Safety-Net-ASR26`, which **physically deposits**
  public-sourced `.dta` (BEA/ACS/policy tables) → `data = Y`; the proprietary credit-bureau panel
  is not deposited → `data_gated = Y`; analysis scripts → `code = Y`. **Lesson:** verify an
  OpenICPSR project's *owner and title* before crediting it — an author-cited public deposit is
  not the authors' replication package.

## After reading → `agent.toml` Exec-Verify (confirm the project belongs to THESE authors / THIS paper).
