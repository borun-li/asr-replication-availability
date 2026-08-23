---
name: author-homepage
description: Fallback LOCATE for ASR when neither the Data Availability Statement nor the PDF yields a link. Find the replication package on an author's personal / departmental / lab page, or via a direct repository + Crossref-relation search keyed to the article.
---

# Source: author homepage / lab page / direct repository search (last-resort LOCATE)

## When you get routed here
The landing-page DAS and the PDF/preprint gave no usable package link. Authors often post
replication materials (or a link to OSF/GitHub/OpenICPSR/Dataverse) on their own site, and ASR
packages are frequently discoverable by search even when the journal page did not surface them.
Restricted article access does NOT block any of this — these channels are outside the paywall.

## Step-by-step: LOCATE — [API-first; web_search is optional and may be unavailable]
Prefer the **deterministic API channels (1–2)** — they are free of the web_search budget, which is
often exhausted. Use free-text web search only to supplement, never as the sole channel.
1. **Crossref / DataCite relation metadata** (do this FIRST — deterministic, paywall-proof):
   `api.crossref.org/works/<doi>` → `relation` (`isSupplementedBy` / `has-preprint` / `references`)
   may carry a **dataset DOI** (OpenICPSR `10.3886/…`, Dataverse `…/DVN/…`). Resolve it, route by host.
2. **Direct repository search via APIs** (keyed to the article — DOI, exact title, authors):
   - **OpenICPSR** — search the ASA/ASR collection and by author/title.
   - **GitHub** — API search for repos named `…-ASR`, `Replication-…`, or by author handle/org.
   - **OSF** — search nodes by author/title (then read via `osf-repository`'s API).
   - **Dataverse** — search by author/title across installs (then `dataverse-any-host`).
3. **Author / lab pages.** For each author, find the personal or departmental page and the
   "Research"/"Publications"/"Data" section; look for this article and a repository link. (A
   web search like `"<author name>" <institution> replication` helps here **if available** — if
   web_search is unavailable, rely on channels 1–2 and note that in `coverage_checked`.)

## Higher provenance bar for search-found packages — [ASR]
A package found here is **not** journal-vouched, so the false-match risk is higher. Before
recording it, require strong provenance (handed to Exec-Verify): repo/node/project **belongs to
these authors** (contributor/owner-org/README) AND **reproduces THIS paper** (title/DOI
back-reference). If you cannot confirm both, do not record it.

## Gotchas
- A generic tool or an unrelated same-named project is not the package (RULE 2).
- A preprint on the author page is a manuscript, not a package (RULE 3).
- Wayback Machine can recover a dead author-page link.

## Dead end → a confident "no package", recorded
When the DAS is absent, the PDF is unobtainable (paywalled, no preprint), AND every channel above
is dry, that is a **confident "no package"**, not a deferral: code `data = N` / `code = N` and
record in `coverage_checked` **exactly** what was searched (Crossref relation + which repo APIs +
homepages + whether web_search was available). Do not leave the row unresolved and do not drop the
article — a recorded, evidence-backed "no package" keeps the denominator honest.

## After locating → the matching Execute host skill, then `agent.toml` Exec-Verify.
