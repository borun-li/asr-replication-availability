---
name: article-pdf-availability-statement
description: Fallback LOCATE for ASR when the landing-page Data Availability Statement is missing or has no link. Read the article PDF's data/code availability statement — but only when the PDF is obtainable (Open Access, or a preprint carries the same statement).
---

# Source: the article PDF's data/code availability statement (fallback)

## When you get routed here
`asr-data-availability-statement` found no usable link on the landing page. The PDF often repeats
the availability statement (a footnote, an end-of-article "Data Availability" paragraph, or an
acknowledgements note) with the repository URL.

## Access gate first — [ASR]
ASR articles are ~half paywalled. Only read the PDF if it is **openly obtainable** — try the
landing-page PDF link, and:
- if it downloads openly → use it;
- if it is **behind the paywall** (login/purchase prompt) → **STOP, never bypass the paywall**.
  Instead look for a **preprint** carrying the same statement. Find it **deterministically first**,
  not by free-text search:
  `api.crossref.org/works/<doi>` → `relation.has-preprint` / `is-preprint-of` gives the preprint
  DOI directly; resolve it (SocArXiv `osf.io/preprints/socarxiv`, SSRN, or an author-posted
  accepted manuscript). Only if the relation is absent, fall back to a title/author search. Never
  bypass a paywall.

## Step-by-step: LOCATE
1. Get the PDF text (Open Access) or the preprint text.
2. Search it for a **data/code availability** statement and any repository URL. Greppable cues:
   `data availability`, `replication`, `openicpsr`, `osf.io`, `dataverse`, `github`, `available on
   request`, `restricted`, `deposited`.
3. Extract the URL(s) and the sentence (provenance + what is included / what is restricted).
4. **Route by host** to the matching Execute skill (openicpsr / osf / dataverse-any-host / github).

## Gotchas
- A bare data DOI or repo URL in the references is a **citation of a source**, not necessarily the
  authors' deposit — it is the package only if the availability statement says so.
- A statement that names a restricted source with no deposit → `data = N`, `data_gated = Y`
  (hand the source to `restricted-data-sources-asr`).
- If neither PDF nor preprint is obtainable and no link is found → continue the fallback chain
  (`author-homepage`, repo search, Crossref relation) per `asr-data-availability-statement`.

## After locating → the matching Execute host skill, then `agent.toml` Exec-Verify.
