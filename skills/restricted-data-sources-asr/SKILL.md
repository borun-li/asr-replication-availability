---
name: restricted-data-sources-asr
description: Recognize the restricted/gated data sources common in ASR (US-centric) and fill data_gated = Y plus a concrete data_source_apply_at. Templates for PSID Virtual Data Enclave, FSRDC/Census, national surveys under DUA, and proprietary vendor panels.
---

# Gated data sources & apply-at templates (ASR / US-centric)

## When you get routed here
The Execute agent found the analysis data is **not freely downloadable** — restricted, proprietary,
under a DUA, in an enclave, or "available on request". Per the shared codebook, that is
`data_gated = Y` **even if code is deposited and even if there is no external route**. Your job:
name the source and give a **concrete** `data_source_apply_at` (provider + URL/agreement/email).

**`data_gated = Y` does NOT by itself set `data = N`.** The two are independent axes: the *deposit
test* (in the host skill — GitHub/OSF/OpenICPSR/Dataverse) decides `data`, and the *gate* is a
property of the underlying source. If the authors **physically deposited (part of) the analysis
data**, `data = Y` **and** `data_gated = Y` together. This skill only fills the gate + apply-at;
it never overrides a deposit found by the host skill.

## Common ASR restricted sources → apply-at template

| Source (as it appears) | `data_gated` | `data_source_apply_at` template |
|---|---|---|
| **PSID** restricted files / sensitive variables | Y | `PSID — restricted-data application, Virtual Data Enclave (psidonline.isr.umich.edu)` |
| **Census / IRS / SSA** microdata, "administrative", geo-identified | Y | `US Census restricted microdata — FSRDC application (census.gov/fsrdc)` |
| **Add Health** restricted-use | Y | `Add Health — restricted-use DUA, Carolina Population Center, UNC (addhealth.cpc.unc.edu)` |
| **NCHS** (NHANES/NSFG/NVSS) restricted | Y | `NCHS Research Data Center application (cdc.gov/rdc)` |
| **Proprietary vendor panel** (consumer-credit / marketing / financial, e.g. a credit-bureau CCP) | Y | `proprietary vendor panel — commercial license from the provider; no public route` |
| **Confidential interviews / ethnographic** (author-collected human subjects) | Y | `confidential human-subjects data — corresponding author, <email from the article>` (IRB-protected; often no external route) |
| **Author-collected survey / experiment microdata** (quantitative — an original survey, lab/field/survey experiment, or scraped panel the authors ran, not deposited) | Y | `author-collected survey/experiment data — corresponding author, <email from the article>` (IRB-protected human subjects; typically no external portal) |
| National register / administrative (non-US: SOEP, UKDS, register data) | Y | `<register> — data-access agreement with <provider> (<url>)` |

## Rules
- **No external route is still `Y`.** If the data is proprietary/discretionary with no application
  portal, code `Y` and use `data_source_apply_at` to **explain why** ("proprietary panel; access
  only under the authors' commercial license — no public route").
- A **concrete** route is required — a URL, a named enclave/RDC, or the author's actual email.
  `contact author` with no address is not acceptable.
- **Public data is NOT gated.** Public IPUMS/GSS/ANES/ACS-PUMS/NLSY, open Dataverse/OSF/OpenICPSR
  deposits, and the authors' own simulation outputs → `data_gated = N`. Do not flag these.
- The **located package still counts** even when the data is gated — record the package_location
  AND the apply-at; never sign, register, or log in to obtain the data.

## Worked examples (ASR-2026 pilot)
- **"Countervailing Powers":** DAS — "authors cannot share the restricted-access PSID data …
  apply for permissions with the PSID and import our code into the PSID's Virtual Data Enclave."
  → `data = N`, `data_gated = Y`, apply-at = `PSID — Virtual Data Enclave (psidonline.isr.umich.edu)`.
- **"Unsecured Credit and the Social Safety Net":** the authors **physically deposited** the
  public-sourced `.dta` (BEA/ACS/policy) in their GitHub repo → `data = Y` (set by the host skill).
  A *further* portion — the individual-level consumer-credit-bureau panel — is proprietary and not
  deposited → **this skill sets `data_gated = Y`**, apply-at = `proprietary credit-bureau panel —
  commercial license; no public route`. Note the gate does **not** flip `data` back to `N` (v3.3).

## After → `agent.toml` Exec-Verify (confirm the source really is restricted; do not flag public data).
