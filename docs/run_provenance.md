# ASR Replication-Package Availability — Run Provenance

How the ASR-2026 availability dataset (`output/asr_vol91_result.xlsx`) was produced. This dataset is
a **hybrid product**, not a pure machine run — read §2 before citing it as "model output".

---

## 1. Pinned parameters

| Parameter | Value | Source / how verified |
|---|---|---|
| **Model** | `claude-opus-4-8` | Blind-rerun agent transcripts: **843** `"model":"claude-opus-4-8"` records, no other real model (4 `<synthetic>` are harness placeholders). Pinned in `agent.toml` (`model = "claude-opus-4-8"`). |
| **Temperature** | **platform default (unset)** | The Workflow harness that spawns the agents **exposes no temperature parameter** — none is set and none is recorded in any run log (`grep '"temperature"'` → 0 hits). The dataset was produced at the platform default, **not** at `0`. See §4. |
| **Agent / workflow spec** | `agent.toml` **v1.1.0** | `agent.toml` header (`version = "1.1.0"`). Six-agent per-article pipeline (Download → Prep → Locate ↺LocVerify → Execute ↺ExecVerify → Write). |
| **Codebook version** | **v3.3** | `docs/codebook.md` header. Block B is journal-neutral / identical to SocSci. Includes the v3.3 physical-deposit rule plus two later clarifications (Schwartz & King = `data = Y`; a free hosting-platform login is not a `data_gated` gate). |
| **Skills** | 8 | `skills/`: `asr-data-availability-statement`, `article-pdf-availability-statement`, `author-homepage`, `openicpsr-repository`, `osf-repository`, `dataverse-any-host`, `github-repository-and-pages`, `restricted-data-sources-asr`. |
| **Input** | 23 ASR-2026 articles | `input/asr_vol91.xlsx` (Block A filled by `scripts/`); raw SAGE HTML + Crossref JSON in `cache/`. Input file kept pristine; results written to `output/`. |

---

## 2. This dataset is a HYBRID (tool base → human adjudication → blind validation)

The cell values in `output/asr_vol91_result.xlsx` come from **two sources layered together**, so it
must NOT be described as pure model output at a single temperature:

1. **Tool base.** The six-agent pipeline (`agent.toml` + `skills/`, `claude-opus-4-8`) coded Block B
   for all 23 articles → the initial `asr_vol91_result.xlsx` (project Phase 6).
2. **Manual adjudication (overwrites the same file).** Borun reviewed every article and corrected a
   subset of cells — this is what makes the file the **gold standard** (the authoritative
   human-verified reference). Recorded rulings:
   - **Unsecured Credit** → `data = Y` (public-sourced `.dta` physically deposited; credit-bureau
     panel proprietary → `data_gated = Y`).
   - **Effort (Social Origins of Effort)** → `data = Y`, `code = Y` (code `Radl_et_al_2026.zip`
     verified inside the edatos Effort-collection dataset 68CTB1).
   - **Schwartz & King (Mothers' Status)** → `data = Y` (authors deposited their occupation→prestige
     crosswalks + derived analysis tables; raw NSFH/GSS/PSID microdata is a pointer).
   - **Performing Nationalism / Temporal Misalignment** → `data_gated = N` (deposited quantitative
     data is public; the un-deposited IRB interview corpus is not the coded data object).
   - **Between Two Rituals** → `in_scope = Y` (original 39 interviews + 3-yr ethnography).
3. **Blind validation (separate file, does NOT touch the gold).** 23 fresh independent agents
   re-coded Block B from cache + codebook + skills only (no access to the answer key), workflow run
   `wf_e964a094-273` → `output/asr_vol91_rerun.xlsx`. **Agreement vs. gold = 96.5% (111/115 cells);
   19/23 rows exact; in_scope 100%, qualitative 100%.** Zero skill/agent bugs; the few differences
   were coding judgments (and in two, the tool was right and the manual gold was corrected).

**Implication for provenance:** Block A (bibliographic) is script-generated; Block B (coding) is
tool-produced **and then human-finalized**. Any reproduction re-runs the tool base (§1 parameters),
but the gold's authority rests on the human review of step 2.

---

## 3. Files

| File | Role |
|---|---|
| `output/asr_vol91_result.xlsx` | **The gold** — human-finalized Block B (authoritative). |
| `output/_gold/asr_2026_manual_gold_20260821.xlsx` | Frozen snapshot taken during validation setup (**pre** the Effort `code` correction). |
| `output/asr_vol91_rerun.xlsx` | Blind re-run output — validation only, never merged into the gold. |
| `input/asr_vol91.xlsx` | Pristine input (Block A). |

---

## 4. Temperature — honest note (do not backfill `0`)

The protocol would *prefer* `temperature = 0` for reproducibility, but **it is not a knob in the
current Workflow-based pipeline**: the harness that spawns the sub-agents accepts no temperature
argument, so this dataset was produced at the **platform default**, and that is what is recorded
here. Do **not** re-label it `0` — that would misstate how the data was generated. To actually pin
`temperature = 0`, the pipeline would have to be re-implemented directly on the Anthropic Messages
API/SDK (where `temperature` is a request parameter); even then, `temperature = 0` does not
guarantee byte-identical LLM outputs.

---

## 5. Final tally (gold, `in_scope = Y` denominator, access-agnostic)

- In scope: **22** (+ 1 `NA`, a theoretical essay). Article access (paywalled vs. open) is not
  recorded and does not affect the denominator.
- `data = Y`: **9** · `code = Y`: **12** · `data_gated = Y`: **15**
- **Availability (data or code deposited): 12/22 = 54.5%**.
