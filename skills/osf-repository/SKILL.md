---
name: osf-repository
description: The replication package is on OSF (osf.io) — a dominant host for ASR. OSF landing pages are JS-rendered, so read the node via the OSF API (api.osf.io), navigate components + add-on storage, and code data/code + data_gated.
---

# Source: OSF (osf.io)

## When you get routed here
An `osf.io/<node>` link from `asr-data-availability-statement`, the PDF, or an author page. OSF is
one of the most common ASR code hosts. SocArXiv preprints are also OSF-hosted, so tell a package
project from a preprint.

## Step-by-step: READ VIA THE API (the HTML page is JS-rendered — a plain fetch returns almost nothing)
1. Take the short node id (e.g. `osf.io/3mcv5`; `/overview` or `/files/...` suffixes resolve to
   the same node).
2. Query the OSF API — do NOT scrape the HTML:
   - node: `https://api.osf.io/v2/nodes/<id>/`  → title, category (project/preprint/registration)
   - contributors: `https://api.osf.io/v2/nodes/<id>/contributors/`  → author-provenance check
   - files: `https://api.osf.io/v2/nodes/<id>/files/osfstorage/`  → the file list
   - components: `https://api.osf.io/v2/nodes/<id>/children/`  → code/data often live in children
3. List files across **OSF Storage AND any linked add-on storage** (Google Drive, GitHub, Box,
   Dropbox appear as separate providers), and across **child components**.
4. **Retry once on a failed or empty API response before concluding empty.** The OSF API returns
   transient `5xx`/empty payloads; a single retry usually succeeds. An empty *root* `osfstorage`
   is common when the real files live in a **child component** (step 2's `/children/`) — check the
   children before deciding the node is empty.

## READ THE README / node description FIRST — for access instructions and gates
Read the README (`.txt`/`.md`) or the node description. It states **what is in the package and
what is not** — in particular the analysis **data may not be in the node**, with instructions for
obtaining it (often a restricted source). Use it to catch access gates.

### Gated data (DUA / restricted enclave) → record apply-at, never sign/log in
If the README/description says the data require a signed agreement, an enclave, or an application,
the agent must NOT apply or authenticate. Flag `data_gated = Y`, record the concrete `apply_at`,
and inform the user where to apply.

## Coding from OSF — [v3.3 physical-deposit rule]
- `code = Y` if the node holds the authors' analysis scripts for THIS paper.
- `data = Y` when the authors **physically deposited the analysis data files** in the node (OSF
  Storage or a linked add-on) — public-sourced files that the authors settled into the node COUNT.
  A restricted portion of the underlying data keeps `data = Y` **with** `data_gated = Y`.
- `data = N` only when **no analysis data files are in the node** — a **code-only** node (just
  `.do`/`.R` scripts, or a `.do` that *simulates/generates* the data at run time is code, not a
  deposited dataset), or the README merely **points** to an external source the user must fetch.
- `package_location` = the canonical node URL (`https://osf.io/<id>/`).

## Gotchas
- A **private** node → API returns 401/403. Retry once; if still walled, **do not** invent a
  deferral — code from the DAS/README statement (what it says is deposited) and record
  "node auth-walled, coded from DAS" in `notes`.
- A **preprint-only** node is a manuscript, not a package → look for the linked project.
- An add-on storage root may be auth-walled even when the node is public → note it as unverified in
  `notes`; code from the file list you could read plus the README.

## Worked example (ASR-2026 pilot)
- **"Countervailing Powers" (10.1177/00031224261437057):** DAS → `osf.io/3mcv5`. HTML fetch
  returned only an "OSF" heading; the API (`.../nodes/3mcv5/files/osfstorage`) revealed 10 `.do`
  files (`00_master.do` … `09_table5_rq3.do`) and contributor **Zachary Parolin** (author).
  Code deposited → `code = Y`; DAS says the PSID data is restricted → `data = N`, `data_gated = Y`
  (PSID Virtual Data Enclave; see `restricted-data-sources-asr`).

## After reading → `agent.toml` Exec-Verify (contributors include an author; description cites THIS paper).
