# American Sociological Review Multi-agent pipeline

## Context
We have built a multi-agent pipeline that checks the availability of replication packages for papers published on *Sociological Science*

We would love to extend the multi-agent idea to a new journal, *American Sociological Review*, ASR

## Goal
Build a multi-agent pipeline that checks the availability of replication packages for papers published on *American Sociological Review*

## Requirement

**Strictly follow the steps below. DO NOT MOVE ON TO ANOTHER STEP WITHOUT MY INSTRUCTION**

- Step 1: Data preparation
    - Goal: Produce ./input/asr_{YEAR}.xlsx with columns 1-8 filled.
    - Implementation: python3 + openpyxl for ALL workbook reads and writes.
      Do NOT use pandas or xlsxwriter — they produce different styling behaviour.
    - All paths are relative to the project root (the directory containing this file).
    - Every script takes a `--year` argument. Never hardcode the year, and never
      hardcode an absolute path — resolve paths from the script's own location.
    - Task:
        1. Task 1 — xlsx_build_agent (Model: Haiku 4.5). 
            - Create ./input/asr_{YEAR}.xlsx with EXACTLY these columns, in order.
              The header string is the text BEFORE the "#"; everything from "#"
              onward is documentation and must never appear in the header cell.
                - title
                - author(s)
                - published__online_date
                - article_url
                - OnlineFirst (Y/N)
                - volume
                - issue
                - in_scope(Y/NA)
                - qualitative(Y/N)
                - data(Y/N)
                - code(Y/N)
                - data + code            # derived column, see rule below
                - neither                # derived column, see rule below
                - data_gated(Y/N)
                - data_source / apply_at
                - package_location
                - path_to_package
                - coverage_checked
                - notes
            - Derived columns. Computed by a deterministic script, never by an LLM.
              Left blank in Step 1, because data(Y/N) and code(Y/N) are not filled
              until a later step. The rule, in code:
                  data_and_code = "Y" if data == "Y" and code == "Y" else "N"
                  neither       = "Y" if data == "N" and code == "N" else "N"
              (written to the columns named `data + code` and `neither`)
            - Format required (sheet-level only; the sheet has no data rows yet):
                - Sheet name: asr_{YEAR}
                - Header row: fill #1F3864 (solid), font bold white, centered, wrap text, row height 34
                - Freeze panes at A2
                - Column widths: title 62, author(s) 34, article_url 46, notes 40,
                path_to_package 34, data_source / apply_at 26, package_location 26,
                others 16
                - Row-level formatting is NOT done here — see Task 4.
        2. Task 2 - crossref_fetch.py (NO LLM; deterministic script)
            - Endpoint:
                https://api.crossref.org/works?filter=issn:0003-1224,type:journal-article,
                from-online-pub-date:{YEAR}-01-01,until-online-pub-date:{YEAR}-12-31
                &rows=1000&cursor=*&mailto=$CROSSREF_MAILTO   # optional polite-pool contact (env var)
            - Paginate via message.next-cursor until items is empty.
            - Save raw JSON to ./cache/crossref_{YEAR}.json first.
            - Fill ONLY these columns:
                - title                  <- title[0]
                - author(s)              <- join(author[], "{given} {family}", "; ")
                - published__online_date <- published-online.date-parts[0] as YYYY-MM-DD
                - article_url            <- resource.primary.URL
            - **HARD RULES**:
                - Deduplicate on DOI (case-insensitive; keep the first occurrence).
                - Sort rows by published__online_date ascending, then by title
                  ascending. Crossref's cursor order is NOT stable, so this sort is
                  what makes row numbers reproducible across runs.
                - Write rows starting at row 2, one row per article, no gaps.
                - Write published__online_date as a YYYY-MM-DD text string, NOT as an
                  Excel date value.
                - Leave all other columns blank.
        3. Task 3 — page_probe_agent (Model: Sonnet 5):
            - For each article_url, fetch with a clean session
            - Fill in the following columns using the article_url (DOI)
                - OnlineFirst (Y/N): "Y" if the article page shows NO volume and NO
                  issue (published online ahead of issue assignment); otherwise "N".
                  Every row must get an explicit "Y" or "N" — never leave it blank.
                  Do not require the literal phrase "Online First" on the page: SAGE
                  usually shows only "First published online <date>" with no volume or
                  issue, and that alone is sufficient evidence.
                - volume  (write as an integer, not text; blank when OnlineFirst == "Y")
                - issue   (write as an integer, not text; blank when OnlineFirst == "Y")
            **HARD RULE**:
                - no cookies, no proxy, no institutional auth
                - custom User-Agent, >=3s delay between requests, serial only
                - cache HTML to ./cache/{doi_slug}.html; skip if cached
                  (doi_slug = the DOI with every non-alphanumeric character replaced
                  by "_", e.g. 10.1177/00031224251401933 -> 10_1177_00031224251401933)
                - ONLY FILL IN THE COLUMNS LISTED HERE. LEAVE OTHER COLUMNS BLANK
        4. Task 4 — format_agent (NO LLM; deterministic script).
           Run AFTER Task 3, once the data rows exist. Row-level formatting cannot be applied to an empty sheet
            - Header + all data rows: thin #BFBFBF borders
            - Data rows: alternating fill #EEF2F8, vertical align top, row height 30
            - Wrap text on: title, author(s), path_to_package, notes
            - Center: published__online_date, OnlineFirst (Y/N), volume, issue, and all Y/N columns
            - Highlight OnlineFirst == "Y" cells with fill #FFF2CC + bold font #9C5700
            - Autofilter over the full used range (A1 to last column / last row)
            - **HARD RULE**: formatting only. Never recreate the workbook or touch any cell value.
    - Output: ./input/asr_{YEAR}.xlsx
