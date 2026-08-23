# Replication-Package Availability Codebook (shared)
Version 3.3 · shared across *Sociological Science* and *American Sociological Review*

*Changelog — v3.3:* clarified `data` — the test is whether the authors **physically deposited the
analysis data files in the package**, NOT whether the data originated from a public source. Public
data that the authors **settle into the package** counts as a deposit (`data = Y`); a bare
**pointer/link** to an external source the user must download themselves is not (`data = N`). A
restricted portion of the underlying data → `data_gated = Y`, and does not flip `data` to `N` when
the authors physically deposited (part of) the analysis data. Added a worked example (§2). Also:
`data_gated = Y` **must be explained in `notes`** (the basis for the gate).

This codebook defines how each article is coded for **data and code availability**. It is
**journal-neutral**: the coding definitions (Block B) are IDENTICAL across journals, so take-up
rates are comparable. *Where* materials are found (the Data Availability Statement, the article
PDF, a repository host) is journal-specific and lives in that journal's `agent.toml` + `skills/`,
**never here.**

Column names below are the **canonical** (snake_case) names used by the pipeline, the CSV export,
and the archive. An Excel presentation copy may use display headers, but the canonical names
govern.

*Changelog — v3.2:* `data_gated` = `Y` whenever the underlying analysis data is **not
freely/publicly available** (restricted / confidential / proprietary / institutional-access /
register / IRB / author-collected human-subjects), **even if there is no external application
route**; when no route exists, `data_source_apply_at` **explains why**. `N` only when the data is
**genuinely public** (open archives / open deposits) or the authors' own **simulation** outputs.
*Mere non-provision* → `N` applies **only** when the underlying source is itself public.
*v3.1:* introduced the special-application framing (application/DUA/RDC, paid license,
available-on-request, registration portal); superseded by v3.2 for the no-route restricted case.

---

## 1. Schema

Two blocks. **Block A** (bibliographic identifiers) is journal-specific. **Block B** (availability
coding) is IDENTICAL across all journals — names, order, allowed values, definitions.
Cross-journal comparison depends on Block B never diverging.

### Block A — bibliographic (journal-specific)

| # | Column | SocSci | ASR | Notes |
|---|--------|--------|-----|-------|
| 1 | `doi` | ✔ | ✔ | **primary key, both journals** |
| 2 | `paper_id` | ✔ | — | SocSci internal ID (e.g. SS287) |
| 3 | `title` | ✔ | ✔ | |
| 4 | `authors` | ✔ | ✔ | |
| 5 | `published_date` | ✔ | ✔ | ASR: `published-online` |
| 6 | `submission_date` | ✔ | — | **SocSci-only** — policy grandfathering; ASR has no policy date |
| 7 | `article_url` | ✔ | ✔ | |
| 8 | `volume` | — | ✔ | ASR |
| 9 | `issue` | — | ✔ | ASR |

A column absent for a journal is omitted from that journal's workbook, never filled with a
placeholder. **Article access (paywalled vs. open) is NOT recorded and NEVER an inclusion filter** —
a paywalled article is coded and counted exactly like an open one (the DAS is public regardless of
the paywall; the denominator is in-scope empirical articles, access-agnostic; see `in_scope`).

### Block B — availability coding (identical across journals)

| # | Column | Filled by | Notes |
|---|--------|-----------|-------|
| 1 | `in_scope` | coder | `Y` / `NA` / `?` |
| 2 | `qualitative` | coder | blank if `in_scope = NA` |
| 3 | `data` | coder | blank if `in_scope = NA` |
| 4 | `code` | coder | blank if `in_scope = NA` |
| 5 | `data_and_code` | **pipeline (auto)** | do not type; not an agent judgment |
| 6 | `neither` | **pipeline (auto)** | do not type; not an agent judgment |
| 7 | `data_gated` | coder | blank if `in_scope = NA` |
| 8 | `data_source_apply_at` | coder | **required when `data_gated = Y`** |
| 9 | `package_location` | coder | URL/file where materials actually live |
| 10 | `path_to_package` | coder | how you got there (discovery path) |
| 11 | `coverage_checked` | coder | where you looked |
| 12 | `notes` | coder | **required on every row** |

§2–§4 define Block B and apply unchanged to every journal.

---

## 2. Codebook — field definitions (Block B, journal-neutral)

- **`in_scope`**
  - `Y` = reports original empirical analysis the authors ran. A qualitative **empirical** paper
    *is* in scope (`Y`, with `qualitative = Y`).
  - `NA` = nothing to reproduce — commentary, rejoinder, editorial, or purely theoretical.
  - `?` = does not fit. **Flag the entire row for human review** and say why in `notes`.
  - **The denominator is in-scope empirical articles, regardless of article access.** Do not
    exclude an article because it is paywalled/Restricted — access does not affect inclusion.
  - If `in_scope = NA`, leave `qualitative` / `data` / `code` / `data_gated` **blank**.

- **`qualitative`** — `Y` if primary evidence is non-numeric (interviews, ethnography,
  archival/textual), interpreted directly rather than converted into variables. Papers using
  **both** qual and quant = quantitative (`N`).

- **`data`** — `Y` = the authors **physically deposited the analysis data files in the package**.
  The test is **deposit vs. pointer**, not public vs. private:
  - **Deposited (→ `Y`)** — the data files are actually in the package (uploaded to OSF /
    Dataverse / OpenICPSR / GitHub / a supplement). This holds **even when the data came from a
    public source**: if the authors settled those files into the package, they built a replication
    package. A restricted portion of the underlying data still leaves `data = Y` (with
    `data_gated = Y`) as long as the authors physically deposited (part of) the analysis data.
  - **Pointer only (→ `N`)** — the package merely **links to / cites** an external source the user
    must download themselves (a public archive such as ICPSR / IPUMS / GSS / NLSY / PSID, or a
    "the data are available at …" link). A citation or link is not a deposit.
  - **Nothing deposited (→ `N`)** — no analysis data files are in the package (code-only deposit),
    or there is no package at all.

- **`code`** — `Y` = the authors **deposited code that reproduces THIS paper's results**. A
  general method/software package (even one the authors wrote) is a **tool**, not a package,
  unless it bundles the paper's own analysis scripts.

- **`data_and_code` / `neither`** — Generated by pipeline code, never by an agent:
  - `data_and_code` = `Y` if `data = Y` **and** `code = Y`, else `N`
  - `neither` = `Y` if `data = N` **and** `code = N`, else `N`
  - Both blank whenever `data` / `code` are blank.

- **`data_gated`** — `Y` whenever the underlying analysis data is **not freely/publicly available**
  — restricted, confidential, proprietary, institutional-access-only, a register/administrative
  source, IRB-protected, or author-collected human-subjects data — **regardless of whether an
  external application route exists**. When there **is** a route, record it in
  `data_source_apply_at`; when there is **no** external route, still code `Y` and use
  `data_source_apply_at` to **explain why** (discretionary/institutional access to the authors
  only). `N` only when the data is **genuinely public** (freely downloadable open archives / open
  deposits) or the authors' own **simulation** outputs. *Mere non-provision* → `N` only when the
  underlying source is itself public (a public dataset simply not re-posted), never for inherently
  restricted data. Blank if `in_scope = NA`.
  **`data_gated` applies to QUANTITATIVE papers only — leave it BLANK (N/A) when `qualitative = Y`.**
  Data-gating is a *reproduction-from-data* question, which is a quantitative frame; a qualitative
  study is not reproduced from its data, so the gate does not apply (the `qualitative = Y` flag
  already carries why). Assess `data_gated` (and `data_source_apply_at`) only for `qualitative = N`.
  **Whenever `data_gated = Y`, `notes` must state the basis for the gate** (which source is
  restricted and why — e.g. "confidential IRB interview data, no deposit"; "proprietary vendor
  panel, no public route"; "restricted register, apply via <RDC>"), including when the gate is
  inferred from the data's inherent nature (ethnographic/interview data) rather than an explicit
  author statement.
  **A login on the hosting platform is NOT a gate.** Merely needing a free account to download an
  openly-deposited package from its host (OSF, Harvard Dataverse, OpenICPSR, Zenodo, GitHub) does
  **not** set `data_gated = Y`. A gate concerns the underlying **data** being restricted (a real
  application / DUA / approval / license / restricted register) — not the repository's ordinary
  sign-in. Openly downloadable to any registered platform user → `data_gated = N`.

- **`data_source_apply_at`** — when `data_gated = Y`, name the restricted **source** AND the
  concrete **apply-at** (provider + URL/agreement/email). A concrete route is required — `contact
  author` alone is not acceptable; use the author's actual email from the article. Blank when
  `data_gated = N`.

- **`package_location`** — URL or file where the materials actually live.
- **`path_to_package`** — how you got there, e.g. `data availability statement -> openicpsr project`.
- **`coverage_checked`** — where you looked, e.g. `DAS + PDF + OpenICPSR search + author page`.
- **`notes`** — **REQUIRED ON EVERY ROW.** What you opened and what was inside it.

### "Available upon request" vs. mere non-provision

The distinction turns on whether a **real access route** exists:
- Data **available on request** (a real mechanism — email the author/provider, or apply through a
  named body): `data = N`, `data_gated = Y`, `data_source_apply_at` = a **concrete** route.
- Authors **did not deposit** and state **no** route:
  - underlying data **inherently restricted** (confidential interviews, proprietary, institutional,
    register): `data = N`, `data_gated = Y`; `data_source_apply_at` explains why no route exists;
  - underlying source **itself public** (used public data, did not re-post the extract): `data = N`,
    `data_gated = N` — the only *mere non-provision* case. (Publicly posted replication *code* does
    not change the data status.)

### Worked example — public *source* vs. public data *deposited into the package*

The same public dataset can produce `data = Y` or `data = N` depending on whether the authors
**physically deposited it** or merely **pointed to it**:

- **Pointer → `data = N`.** A package whose README says *"our analyses use public-use NSFH, GSS,
  and PSID; download them from the archives and run our code"* and deposits only the `.do`/`.R`
  scripts (no data files). The public data is a **source the user fetches themselves** — not a
  deposit. `data = N`, `data_gated = N` (the source is public), `code = Y`.
- **Deposited → `data = Y`.** A package that **physically includes** the public state/ZIP-level
  data files it uses (e.g. BEA price parities, ACS ZCTA extracts, policy tables uploaded as `.dta`
  into the repo), even though those come from public sources. The authors settled the data into a
  replication package → `data = Y`. If a *further* portion of the underlying data is proprietary
  and absent (e.g. an individual-level credit-bureau panel the authors cannot share), that portion
  is flagged `data_gated = Y` — it does **not** turn `data` back to `N`. (ASR "Unsecured Credit".
  Likewise ASR "Schwartz & King" = `Y`: the authors deposited their occupation→prestige crosswalks
  and derived analysis tables into the OSF package, though the raw NSFH/GSS/PSID microdata is a
  pointer.)

The dividing line is always **"is the data file in the package?"** — not where the data came from.

---

## 3. The one rule

> A **Y** means the authors' materials reproduce **THIS** paper. Not a relevant link, not a tool
> they used, not a preprint, not a public data source. When your note describes why something is
> **NOT** the package, code it **N**. **Do not code past your own note.**

A package located through a non-standard channel (author homepage, repository search, dataset-DOI
relation metadata) counts the same as one linked from the availability statement — **provided it
passes provenance** (belongs to these authors, reproduces this paper). Record how it was found in
`coverage_checked` / `notes`.

---

## 4. Execution-layer definitions for the gated-data fields

Operationalization set by the **Execute** agent, independently checked by **Exec-Verify**.

- **`data_gated = Y`** when obtaining the underlying analysis data requires a **special application
  / access route** — a formal application / **restricted-access** registration (an approval/DUA, not
  a free platform sign-in) / Data Use Agreement / research data center; a paid **license / purchase**
  from a commercial vendor; an explicit **available-on-request** route; or a **restricted portal**
  you must apply to — OR when the data is restricted but has **no external route**
  (discretionary/institutional access to the authors only). Holds **even if** the code (and
  sometimes derived data) is deposited.

  **`N`** only when the data is genuinely public / freely downloadable (public
  IPUMS/GSS/ANES/ACS-PUMS/NLSY, open archives, **open Dataverse/OSF/OpenICPSR deposits**, open web
  data), or the analysis data are the authors' own simulation outputs.

- **`data_source_apply_at` — cross-journal examples** (illustrative; name source + concrete route):
  - `PSID — restricted files via the PSID Virtual Data Enclave (psidonline.isr.umich.edu)`
  - `Census / administrative microdata — FSRDC application (census.gov/fsrdc)`
  - `Add Health — restricted-use DUA, Carolina Population Center, UNC (addhealth.cpc.unc.edu)`
  - `SOEP Core — data-access agreement, DIW Berlin (diw.de)`
  - `proprietary vendor panel (e.g. consumer-credit/marketing data) — commercial license, no public route`
  - `confidential interviews — corresponding author, <email address from the article>`

- **Gated but declared packages** — the located package still counts; record the apply-at and
  **never** sign, register, log in, or solve a CAPTCHA to obtain the data.
