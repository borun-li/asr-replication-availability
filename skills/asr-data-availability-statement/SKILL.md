---
name: asr-data-availability-statement
description: For ASR (SAGE), the replication-package link lives in the article landing page's "Data Availability Statement" section — rendered in the PUBLIC HTML even for Restricted-Access articles. Start here for every ASR article. Includes the fallback chain when the DAS is missing, and how to ignore SAGE's decoy signals.
---

# Source: ASR / SAGE landing page → "Data Availability Statement"

## When you get routed here
This is the **first place to look for every ASR article** — but it is **NOT guaranteed present**:
several ASR articles (including Open-Access ones) carry **no DAS at all**. When a DAS exists, SAGE
renders it in the **public landing-page HTML even when the article itself is Restricted Access** —
so you never need the paywalled PDF to find the package. ASR **never** uses the phrase
"Reproducibility Package".

## Where the real DAS actually is — [ASR], read carefully
Two traps in locating the DAS text:
- **The real DAS paragraph is rendered INLINE in the article body**, usually **just before the
  References** (a "Data availability" paragraph in the back-matter). The section merely *labelled*
  "Data availability statement" in SAGE's section list often shows only a **decoy stub** ("Data is
  available for this article. View more…") — that stub is NOT the statement.
- **Read the DAS paragraph to its END.** Authors frequently list several cited public sources
  first and name **their own repository in the LAST clause** — a first-pass grep that stops early
  misses it.

## Step-by-step: LOCATE
1. Open the cached landing page (`cache/<doi_slug>.html`) or `article_url`
   (`journals.sagepub.com/doi/10.1177/...`).
2. Find the **inline DAS paragraph in the back-matter** (before the References), not just the
   labelled section stub. Read the **whole** paragraph to the end — it names the host AND states
   what is and is not shared (e.g. "code on OSF; the PSID data are restricted; our repository is
   at …"). If there is genuinely no DAS paragraph anywhere, go to the fallback chain.
3. Extract the repository URL(s) and the surrounding sentence (provenance + what's included).
4. **Route by host:**
   - `openicpsr.org/...`        → `openicpsr-repository`
   - `osf.io/...`               → `osf-repository`  (use the API — see that skill)
   - `github.com/...`           → `github-repository-and-pages`
   - any `*/dataverse/...` host  → `dataverse-any-host`
   - a bare dataset DOI (`doi.org/10.3886/...` = OpenICPSR; `.../DVN/...` = Dataverse) → resolve, then route.

## Ignore SAGE decoys (do NOT record these as the package)
- The boilerplate **"Supplementary Material"** license paragraph appears on **every** ASR article
  and usually links only the online **appendix PDF** (`sj-pdf-1-asr-…`). A Supplemental section is
  NOT evidence of a replication package — the package is in the DAS, a different section.
- A generic **"Data is available for this article. View more information"** rights stub is not the
  package either.

## Multi-source DAS — separate cited sources from the authors' own deposit
A DAS often lists SEVERAL entries: public sources the authors point to (a public GitHub dataset,
`data.cdc.gov`, a census portal), a restricted main source (apply-at), AND the authors' own
repository. Do NOT route a cited public source as "the package":
- **Cited public source** (`OxCGRT/covid-policy-dataset`, `data.cdc.gov`, MIT Election Lab, Google
  Trends, a census portal) → a pointer, not the deposit. Alone it is `data = N` and is **not**
  gated (it is public). A public third-party GitHub/Dataverse/OpenICPSR project the authors merely
  cite is NEVER the package (this is the OpenICPSR-157201 trap generalized).
- **Restricted main source** ("cannot be shared … request at `<portal>`") → sets `data_gated = Y`;
  hand it to `restricted-data-sources-asr` for the apply-at.
- **The authors' own repo** — usually the **LAST clause** ("all code and non-sensitive data can be
  found at `github.com/<authors>/…`") → this is THE package. Decide `data`/`code` from what IT
  deposits (physical-deposit rule), via the matching Execute host skill.

Verdict = the authors' own deposit (physical-deposit rule) **+** the restricted source's gate. So a
DAS that points to several public sources, names a restricted panel, and ends with the authors'
repo of "code + non-sensitive data" → `code = Y`, `data = Y` (non-sensitive data physically in the
repo), `data_gated = Y` (the restricted panel). *(ASR-2026 "Political Pivots" is exactly this shape.)*

## Fallback chain — when the DAS is absent or has no link
Try in order (all are paywall-independent; Restricted access does not block them):
1. **Article PDF / preprint statement** → `article-pdf-availability-statement` (only if Open
   Access, or a preprint on SocArXiv/SSRN/OSF carries the same statement).
2. **Author / lab homepage** → `author-homepage`.
3. **Direct repository search** — OpenICPSR ASA collection, GitHub, OSF, Dataverse by
   `DOI + author + title` (ASR repos are often named `…-ASR26`, `Replication-…-ASR`).
4. **Crossref / DataCite relation metadata** — `api.crossref.org/works/<doi>` → `relation`
   (isSupplementedBy / references) may carry a **dataset DOI** (OpenICPSR/Dataverse mint DOIs).
   Deterministic and paywall-proof.
A package found via the fallback chain is valid but must clear the **higher provenance bar** at
Exec-Verify (belongs to these authors / reproduces this paper). When the DAS is absent AND the PDF
is paywalled AND **every fallback is dry**, that is a **confident "no package"**, not a deferral:
code `data = N` / `code = N` and record in `coverage_checked` exactly what was searched (DAS +
PDF/preprint + homepage + which repository APIs). Do not leave the row unresolved and do not
default to "unavailable" without recording the search.

## Worked examples (from the ASR-2026 pilot)
- **"Unsecured Credit and the Social Safety Net" (10.1177/00031224251411563, Restricted):** the
  public inline DAS names the authors' **GitHub** repo (`github.com/OSU-UW-CCP/State-Safety-Net-ASR26`)
  — recovered without the paywalled PDF. The repo **physically deposits** public-sourced `.dta`
  (BEA price parities, ACS extracts, state-policy tables) → **`data = Y`**; the individual-level
  credit-bureau panel is proprietary and NOT deposited → **`data_gated = Y`** (see
  `restricted-data-sources-asr`); analysis scripts present → `code = Y`. **Caution:** the
  OpenICPSR project `157201` that also appears near the DAS is a **third-party dataset** (an
  external eviction-moratorium source the authors *cite*), **not the authors' own deposit** — do
  not treat it as the package (RULE 2: a cited source is not a deposit).
- **"Countervailing Powers" (10.1177/00031224261437057, Open):** DAS → **OSF** `osf.io/3mcv5`
  (code only); "authors cannot share the restricted-access PSID data" → PSID Virtual Data Enclave.

## After locating → hand the host URL to the matching Execute skill, then `agent.toml` Exec-Verify.
