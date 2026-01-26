# Software Design Document: Business Conspect

## 1. Overview
Business Conspect is a tool designed to analyze websites and generate structured summaries (conspects) for both human readers and Large Language Models (LLMs). The goal is to provide a clear understanding of what a business sells, who its target audience is, and why it's valuable.

## 2. Requirements

### 2.1 Functional Requirements
- **Web Interface**: A premium, "lab" style UI.
- **URL Input**: Users can input a website URL.
- **Process Execution**: A button to start the analysis/summarization process.
  - **Current State**: The button triggers a demo interaction in the static UI only (no backend execution on GitHub Pages).
  - **Planned State**: The actual analysis is executed offline via CLI/scripts; the UI may later connect to a backend.
- **Report Generation**: (Planned) Offline scripts must produce a canonical `report.md` and a generated `index.html` mirror.
- **Report Search**: (Implemented) `business-conspect/search.html` loads `index.json` and filters reports by domain and date.
- **Canonical Report Template**: (Documented) Every report must follow a consistent template in `report.md` (single source of truth), including website address, generation time, summary, services, ICP, and a client ↔ expert dialogue that covers full buyer discovery.
- **Traceability and Usefulness for LLMs**: (Planned) Reports should be citation-grade: key claims must be grounded in site evidence or explicitly marked as inference.
- **English Documentation**: All user-facing documentation must be in English.

### 2.2 Non-Functional Requirements
- **Aesthetics**: Premium, modern design using gradients and glassmorphism.
- **Performance**: Static hosting on GitHub Pages.
- **SEO**: Basic SEO optimization for the tool landing page.

## 3. Architecture

### 3.1 Frontend
- **HTML5**: Semantic structure.
- **Vanilla CSS**: Custom styling based on root "lab" theme.
- **JavaScript**: UI interactivity (handling button clicks, input validation, demo alerts).

### 3.2 Analysis Pipeline (Offline Generation)
The analysis pipeline is executed outside GitHub Pages and produces static artifacts that are committed into the repository.

1) **Data Input**: URL + optional clarifications (niche, geography, pricing, promised outcome, competitors).  
2) **Content Collection & Normalization**: Scrape HTML, extract main content, remove boilerplate, and store snapshots.  
3) **Business Parser**: Analyze cleaned content and output a structured business card (TA, products/services, value proposition, constraints, proof).  
4) **GEO/LLM Strategist**: Identify gaps and recommendations for AI search visibility and LLM accuracy.  
5) **Optional Dialogue**: Expert ↔ interlocutor exchange to refine conclusions.  
6) **Report Assembly (Canonical)**: Aggregate outputs into `report.md` using the canonical report contract and evidence rules.  
7) **Report Rendering & Indexing**: Render `index.html` from `report.md`, then run `business-conspect/scripts/update_index.py`.

### 3.3 Artifacts & Storage Layout
Reports are stored as static artifacts to keep GitHub Pages simple and reproducible:

```text
/business-conspect/
  reports/
    YYYY-MM-DD/
      domain.tld/
        report.md              # canonical, authored manually or generated offline
        index.html             # generated from report.md
        summary.json (optional)# machine-readable summary for indexing/LLMs
        raw/ (optional)
          prompts.json
          llm-answers.json
          pages.json
          meta.json
```

Artifacts in `raw/` support reproducibility and debugging for the offline pipeline.


## 4. UI Components
- **Hero Section**: Modern title and subtitle.
- **Input Group**: Styled text input for URL + Action button.
- **Manifesto/Description**: Brief explanation of the tool's purpose.
- **Report Search Page**: Client-side filtering over the machine-readable index.

## 5. Implementation Roadmap (Agent-Ready Tasks)

This roadmap is structured as a sequence of testable tasks that can be completed by agents with minimal ambiguity. The intent is to prevent report drift, improve citation quality, and make the project genuinely useful as a first step toward LLM recommendations and citations.

### Completed Tasks

#### Task 1 — Lock the Canonical Report Contract
- Status: Completed.
- Goal: Define what "done" means for `report.md`, including evidence and inference rules.
- Deliverable: A new contract document such as `business-conspect/spec/REPORT_CONTRACT.md` that references the canonical template and adds explicit evidence/inference conventions.
- Verification: The contract includes all required sections and a short checklist that can be applied to any `report.md` without interpretation.

#### Task 2 — Generate Three Reference Reports (Priority)
- Status: Completed.
- Goal: Create real report artifacts early so the rest of the pipeline can be tested against non-trivial inputs.
- Deliverable: Three report directories under `business-conspect/reports/2026-01-25/` for `google.com`, `elinext.com`, and `emcd.com`, each containing a canonical `report.md` (and a temporary `index.html` stub for indexing).
- Verification: Running `python3 business-conspect/scripts/update_index.py` discovers 3 reports, and `business-conspect/index.json` includes entries for `google.com`, `elinext.com`, and `emcd.com`.

#### Task 3 — Implement a Report Validator
- Status: Completed.
- Goal: Automatically enforce the canonical contract before publication.
- Deliverable: `business-conspect/scripts/validate_report.py` implemented on the standard library. It checks required headings, required metadata fields and formats, presence of services, evidence markers in services, and `Client:` / `Expert:` lines in the dialogue.
- Verification: Running `python3 business-conspect/scripts/validate_report.py business-conspect/reports/2026-01-25/google.com` (and the same for `elinext.com` and `emcd.com`) exits with code 0.

#### Task 4 — Add Validation Fixtures
- Status: Completed.
- Goal: Make validation behavior easy to test and maintain.
- Deliverable: Two fixtures at `business-conspect/reports/fixtures/valid/report.md` and `business-conspect/reports/fixtures/invalid/report.md`.
- Verification: `python3 business-conspect/scripts/validate_report.py business-conspect/reports/fixtures/valid/report.md` exits with code 0, while the same command against `business-conspect/reports/fixtures/invalid/report.md` exits non-zero with clear errors.

#### Task 5 — Enforce Value Clarity in Validation (Priority)
- Status: Completed.
- Goal: Prevent reports that are structurally valid but weak on value, fit, and selection logic from being treated as "done."
- Deliverable: Value-oriented validation rules implemented in `business-conspect/scripts/validate_report.py` and documented in `business-conspect/spec/REPORT_CONTRACT.md`. The validator now requires fit/value signals in services (`Who it is for`, `Expected outcome`), a `Situation trigger` in ICP, and selection logic plus a non-fit signal in the dialogue.
- Verification: `python3 business-conspect/scripts/validate_report.py business-conspect/reports/2026-01-25/google.com` (and the same for `elinext.com`, `emcd.com`, and `reports/fixtures/valid/report.md`) exits with code 0, while `reports/fixtures/invalid/report.md` exits non-zero.

### Pending Tasks (Do Next)

### Value Review (Always)
- Rule: After completing each task, perform a short "Value Review" against `DEC-006` and `DEC-007` in `business-conspect/spec/DECISIONS.md`.
- Rule: If the task outcome is correct but not yet ideal for value clarity, recommendation priority, or new traffic, immediately add a follow-up task to close the gap.
- Verification: Each completed task should either (a) explicitly state how it supports value understanding and recommendation quality, or (b) create a new task that does.

#### Task 6 — Define Search-Intent Contract (Priority)
- Status: Completed.
- Goal: Make "how people actually search" explicit and testable, aligned with `DEC-007`.
- Deliverable: `business-conspect/spec/SEARCH_INTENT_CONTRACT.md` with required minimum intent categories, query templates that sound like real search, and a lightweight workflow for generating high-intent dialogue questions.
- Verification: `business-conspect/spec/SEARCH_INTENT_CONTRACT.md` exists, includes required minimum categories, and defines a minimal coverage checklist in a form that can later be validated by a script.

#### Task 7 — Implement Search-Intent Coverage Validation
- Status: Completed.
- Goal: Ensure dialogues are not only structured, but also resemble real search behavior and support recommendation-quality answers.
- Deliverable: `business-conspect/scripts/validate_report.py` now validates required minimum search-intent coverage on `Client:` lines: Outcome / JTBD, Selection / Comparison, Pricing / Cost, Constraints / Fit, and Non-Fit / Risk. The valid fixture has been updated to cover pricing intent explicitly.
- Verification: `python3 business-conspect/scripts/validate_report.py business-conspect/reports/2026-01-25/google.com` (and the same for `elinext.com`, `emcd.com`, and `reports/fixtures/valid/report.md`) exits with code 0, while `reports/fixtures/invalid/report.md` exits non-zero.

#### Task 8 — Add Search-Intent Fixtures and Query Sets
- Status: Completed.
- Goal: Make search-intent validation easy to test and evolve.
- Deliverable: Two new fixtures: `business-conspect/reports/fixtures/search_intent_good/report.md` (passes) and `business-conspect/reports/fixtures/search_intent_poor/report.md` (fails on missing pricing and constraints intents), designed to exercise the search-intent coverage checks.
- Verification: `python3 business-conspect/scripts/validate_report.py business-conspect/reports/fixtures/search_intent_good/report.md` exits with code 0, while the same command against `.../search_intent_poor/report.md` exits non-zero with intent-specific errors.

#### Task 9 — Backfill Reference Reports with Search-Style Queries
- Status: Completed.
- Goal: Improve confidence that the current reports can actually drive recommendation-quality answers and traffic.
- Deliverable: The three reference reports now include additional search-style queries with constraints and comparisons (for example: best/versus/alternative phrasing, budget and deadline constraints, and fit checks) under their dialogue sections.
- Verification: `python3 business-conspect/scripts/validate_report.py business-conspect/reports/2026-01-25/google.com` (and the same for `elinext.com` and `emcd.com`) exits with code 0.

#### Task 10 — Add Recommendation Evaluation Bench (Priority)
- Status: Completed.
- Goal: Replace guesswork with a repeatable, testable check of whether the report can drive recommendation-quality answers.
- Deliverable: `business-conspect/spec/eval_queries.json` (machine-readable query bench for the three reference domains) and `business-conspect/spec/RECOMMENDATION_EVAL.md` (rubric aligned to `DEC-006` and `DEC-007`, including an explicit pricing-intent rule).
- Verification: `python3 -m json.tool business-conspect/spec/eval_queries.json` succeeds, and the rubric explicitly references `DEC-006` and `DEC-007`.

#### Task 10A — Add Offline Evaluation Runner (Priority)
- Status: Completed.
- Goal: Make the evaluation bench executable in the current offline environment, so gaps are detected automatically rather than by manual review only.
- Deliverable: A script such as `business-conspect/scripts/eval_report.py` that reads `business-conspect/spec/eval_queries.json`, checks that the report dialogue covers the query intents and key phrases, and prints a clear per-query pass/fail summary.
- Verification: Running `python3 business-conspect/scripts/eval_report.py business-conspect/reports/2026-01-25/elinext.com` produces a per-query summary and a non-zero exit code when required coverage signals are missing.

### Fast Launch Path (No LLM API, Concierge Mode)

This path is optimized for the fastest route to real user usage without LLM APIs.
It assumes a manual LLM loop and offline publication, with the public site acting
as a request surface and showcase.

#### Task 10B — Implement Offline Scraper (Fast Path, Priority)
- Status: Completed.
- Goal: Turn a URL into clean, reusable source material without any LLM API.
- Deliverable: `business-conspect/scripts/scrape.py` that fetches one or more pages, extracts main content, and writes `raw/pages.json` under a target report directory.
- Verification: Running `python3 business-conspect/scripts/scrape.py business-conspect/scripts/fixtures/sample_site.html --out business-conspect/reports/fixtures/scrape-sample` writes a non-empty `raw/pages.json` with timestamps and source URLs at `business-conspect/reports/fixtures/scrape-sample/raw/pages.json`.

#### Task 10C — Build Prompt Pack Generator (No API, Priority)
- Status: Completed.
- Goal: Make the manual LLM step high-quality and consistent by generating a complete prompt pack from scraped sources and contracts.
- Deliverable: A script such as `business-conspect/scripts/build_prompt_pack.py` that reads `raw/pages.json` and produces `raw/prompt_pack.md` (and optionally `raw/prompt_pack.json`) including the report contract, search-intent contract, and clear output requirements.
- Verification: Running `python3 business-conspect/scripts/build_prompt_pack.py business-conspect/reports/fixtures/scrape-sample` produces `business-conspect/reports/fixtures/scrape-sample/raw/prompt_pack.md` that explicitly references `REPORT_CONTRACT.md` and `SEARCH_INTENT_CONTRACT.md` and contains copy-pasteable instructions.

#### Task 10D — Define Manual LLM Answer Template (No API, Priority)
- Status: Completed.
- Goal: Reduce variance in manual LLM outputs so they can be ingested and validated quickly.
- Deliverable: A template such as `business-conspect/spec/LLM_ANSWER_TEMPLATE.md` plus a lightweight scaffold script (for example `business-conspect/scripts/init_answer_template.py`) that pre-fills metadata and required headings for a new report.
- Verification: Running `python3 business-conspect/scripts/init_answer_template.py business-conspect/reports/fixtures/scrape-sample --domain example.com --website https://example.com/` produces `business-conspect/reports/fixtures/scrape-sample/raw/llm_answer.md`, and `python3 business-conspect/scripts/validate_report.py business-conspect/reports/fixtures/scrape-sample/raw/llm_answer.md` exits with code 0.

#### Task 10E — Implement Manual Answer Ingestion (Fast Path, Priority)
- Status: Completed.
- Goal: Convert manual LLM outputs into canonical `report.md` reliably without any LLM API.
- Deliverable: `business-conspect/scripts/ingest_llm_answers.py` that takes a manual answer file (Markdown or JSON), normalizes it into `report.md`, and runs validation.
- Verification: Running `python3 business-conspect/scripts/ingest_llm_answers.py business-conspect/reports/fixtures/valid/report.md --out business-conspect/reports/fixtures/ingest-sample/report.md` produces `report.md` and prints `[PASS]`.

#### Task 10F — Implement Minimal Publish Pipeline (Fast Path, Priority)
- Status: Completed.
- Goal: Publish valid reports with one command, even before premium HTML rendering exists.
- Deliverable: A publish script such as `business-conspect/scripts/publish_report.py` that runs validation, ensures an `index.html` exists (a minimal stub is acceptable), and runs `business-conspect/scripts/update_index.py`.
- Verification: Running `python3 business-conspect/scripts/publish_report.py business-conspect/reports/2026-01-25/google.com` prints `[ok] Publish completed.` and updates `business-conspect/index.json` when needed.

#### Task 10G — Add Public Request Flow Without Backend (Priority)
- Status: Completed.
- Goal: Let real users start using the service now, even if the pipeline runs offline.
- Deliverable: A request flow on the public site (for example a new `business-conspect/request.html` or an update to `business-conspect/index.html`) that generates a prefilled GitHub issue link containing the target URL, constraints, and instructions about the manual LLM loop.
- Verification: Filling the request form on `business-conspect/index.html` and clicking "Open GitHub Issue" opens a prefilled issue URL containing the URL, constraints, and manual loop instructions.

#### Task 11 — Implement Markdown → HTML Rendering
- Status: Completed.
- Goal: Eliminate double maintenance while preserving human-friendly reports.
- Deliverable: A renderer such as `business-conspect/scripts/render_report.py` and a template such as `business-conspect/scripts/templates/report.html`.
- Verification: Running `python3 business-conspect/scripts/render_report.py business-conspect/reports/fixtures/valid/report.md --out business-conspect/reports/fixtures/valid/index.html` produces HTML that includes the metadata, all section titles, and a canonical link to `report.md`.

#### Task 12 — Make Rendering Validation-Gated
- Status: Completed.
- Goal: Prevent invalid reports from being published as HTML.
- Deliverable: The renderer refuses to write `index.html` when validation fails (or supports a strict mode that does so by default).
- Verification: Running `python3 business-conspect/scripts/render_report.py business-conspect/reports/fixtures/invalid/report.md` exits non-zero and prints "Validation failed; HTML rendering skipped."

#### Task 13 — Harden the Index Updater Around the Canonical Contract
- Status: Completed.
- Goal: Ensure the browse and search experience reflects the new source-of-truth rule.
- Deliverable: Update `business-conspect/scripts/update_index.py` to optionally warn or skip entries that lack `report.md`, and to preserve stable ordering and links.
- Verification: Running `python3 business-conspect/scripts/update_index.py` prints warnings for missing `report.md` when present and updates `business-conspect/index.json` with `reportMdPath` populated where available.

#### Task 14 — Add Automated Tests for Indexing and Validation
- Status: Completed.
- Goal: Reduce regressions in the most important offline scripts.
- Deliverable: A small unittest suite such as `business-conspect/scripts/tests/test_update_index.py` and `business-conspect/scripts/tests/test_validate_report.py`.
- Verification: `python3 -m unittest discover business-conspect/scripts/tests` completes successfully in a clean workspace.

#### Task 15 — Harden the Publish Entrypoint (After Fast Path)
- Status: Completed.
- Goal: Expand the fast-path publish flow into a robust, repeatable pipeline that includes evaluation, rendering, and indexing with clear failure modes.
- Deliverable: A hardened `publish_report.py` that runs validation, evaluation (Task 10A), rendering, and index updates in the right order, with a clear summary of what passed and failed.
- Verification: Running `python3 business-conspect/scripts/publish_report.py business-conspect/reports/2026-01-25/elinext.com` performs validation, evaluation, rendering, and indexing, and exits non-zero when required steps fail.

#### Task 16 — Define LLM Output Contracts (Parser, Strategist, Dialogue)
- Status: Completed.
- Goal: Make manual or semi-automated LLM usage consistent and testable.
- Deliverable: Contract documents and/or JSON schemas under `business-conspect/spec/` that specify required fields for parser output, strategist output, and the dialogue section.
- Verification: `PARSER_OUTPUT_CONTRACT.md`, `STRATEGIST_OUTPUT_CONTRACT.md`, and `DIALOGUE_OUTPUT_CONTRACT.md` exist with minimal valid examples and checklists.

#### Task 17 — Harden Scraping and Normalization (After Fast Path)
- Status: Completed.
- Goal: Improve scraping quality, coverage, and reproducibility beyond the fast-path implementation.
- Deliverable: Enhancements to `business-conspect/scripts/scrape.py` such as multi-page crawling rules, better boilerplate removal, and clearer metadata in `raw/pages.json`.
- Verification: Running `python3 business-conspect/scripts/scrape.py <url> --out <report-dir> --crawl --max-pages 3` produces multiple `pages` entries and includes `content_source` and `content_words` fields.

#### Task 18 — Harden LLM Answer Ingestion into Canonical Markdown (After Fast Path)
- Status: Completed.
- Goal: Make ingestion more resilient to real-world manual LLM outputs and reduce cleanup work.
- Deliverable: Improvements to `business-conspect/scripts/ingest_llm_answers.py` such as clearer error reporting, normalization helpers, and optional repair suggestions when contracts are violated.
- Verification: Ingestion succeeds or fails with actionable messages across both clean and messy fixture inputs.

#### Task 19 — Add Machine-Readable Summaries for LLMs
- Status: Completed.
- Goal: Improve discoverability and citation fidelity beyond HTML and Markdown.
- Deliverable: A compact `summary.json` per report and an update to `business-conspect/index.json` generation to include key summary fields when present.
- Verification: `summary.json` files are valid JSON (`python3 -m json.tool ...`), and `business-conspect/index.json` includes `summary`, `primaryServices`, and `outcomes` when present.

#### Task 20 — Ship LLM Discoverability Artifacts
- Status: Completed.
- Goal: Make the project easy for LLMs and AI search tools to understand and cite.
- Deliverable: Add `llms.txt` (and optionally `llms-full.txt`) within `business-conspect/` that explains the purpose, structure, and canonical artifacts, and links to the browse and search pages.
- Verification: `business-conspect/llms.txt` and `business-conspect/llms-full.txt` exist, are plain text, and include correct public URLs under `https://merc1305.github.io/business-conspect/`.

#### Task 21 — Embed Structured Data in Generated Reports
- Status: Completed.
- Goal: Align human-readable reports with machine-readable hints used by search and AI systems.
- Deliverable: The HTML renderer embeds a JSON-LD block (for example a `CreativeWork` or `Report` representation) that includes domain, date, canonical URLs, and a short summary.
- Verification: Rendering a report produces a JSON-LD block that parses as JSON and includes `report.md` / `index.html` canonical paths plus domain and date.

#### Task 22 — Prefill Request Form on Start Conspect (Priority)
- Status: Pending.
- Goal: Reduce friction so users can submit with zero extra typing if they have nothing to add.
- Deliverable: Clicking "Start Conspect" pre-fills the request form fields (URL, outcome, ICP, constraints, competitors) using the available defaults, and keeps the request valid with no edits.
- Verification: Enter a URL on the hero, click "Start Conspect," and the request form is prefilled; clicking the submit action without edits produces a valid request payload with those defaults.

#### Task 23 — Replace GitHub Issue Requests with Email Submission (Priority)
- Status: Completed.
- Goal: Remove the GitHub account requirement for users.
- Deliverable: The request form sends a structured email (mailto or email endpoint) that includes URL, outcome, ICP, constraints, competitors, and notification preference, instead of opening a GitHub issue.
- Verification: Clicking the request submit action opens an email draft (or sends) to the configured service mailbox with all fields present and no GitHub login flow.

#### Task 24 — Implement n8n Automation Triggered by Request Emails (Priority)
- Status: Pending.
- Goal: Automate the offline pipeline so reports can be produced quickly without manual coordination.
- Deliverable: An exportable n8n workflow (JSON) plus setup notes that: parse inbound request email, create report directory, run `scrape.py`, run `build_prompt_pack.py`, store prompt pack, wait for manual LLM answer drop-in, run `ingest_llm_answers.py`, run `validate_report.py`, run `eval_report.py`, render HTML, and run `update_index.py`.
- Verification: Running the workflow with a test email produces a new report directory containing `raw/pages.json`, `raw/prompt_pack.md`, `report.md`, and `index.html`, and logs show each step executed.

#### Task 25 — Add "Email Me When Published" Opt-In + Explanation (Priority)
- Status: Pending.
- Goal: Let users choose notifications and clearly explain the email-triggered automation.
- Deliverable: A default-checked checkbox labeled "Email me when published" with helper text explaining that requests are processed via email triggers and leaving it checked enables notifications; the request payload includes a `notify=true/false` flag.
- Verification: The checkbox is checked by default on page load, toggling it changes the submitted payload, and the helper text is visible near the checkbox.

#### Task 26 — Notify Users After Publication (Priority)
- Status: Pending.
- Goal: Close the loop by notifying requesters as soon as their report is published.
- Deliverable: The n8n workflow sends a completion email to the requester with the public report URL and a short status summary after publishing succeeds.
- Verification: After a test run completes, an email is delivered to the requester with the report link and a confirmation that publishing succeeded.

#### Task 27 — Add Entity + Triplet Pack to Reports (Priority)
- Status: Pending.
- Goal: Make brand/entity recognition explicit so LLMs can store and recall the service accurately.
- Deliverable: Update `REPORT_CONTRACT.md` and `LLM_ANSWER_TEMPLATE.md` with a required "Entities & Triplets" section that includes at least 5 subject → predicate → object statements and at least 3 explicit entity definitions (brand, category, audience/geo).
- Verification: `validate_report.py` fails when the section is missing or has fewer than 5 triplets, and passes on updated fixtures with compliant content.

#### Task 28 — Add Topical Authority Map (Priority)
- Status: Pending.
- Goal: Help users build narrow, authoritative coverage that improves LLM recall and recommendations.
- Deliverable: Add a "Topical Authority Map" section to the report contract and template with: 1 head topic, 3+ pillar topics, and 6+ subtopics; update `validate_report.py` accordingly.
- Verification: Validation fails on missing or insufficient topical map entries and passes on a fixture that meets the minimums.

#### Task 29 — Add LLM-Friendly Comparison Tables (Priority)
- Status: Pending.
- Goal: Provide structured, extractable comparisons that LLMs can quote directly.
- Deliverable: Add a required "Comparison Table" section to the report contract, and extend `render_report.py` to support Markdown tables in HTML output.
- Verification: A fixture report with a Markdown table renders as `<table>` in HTML, and validation enforces at least 3 rows in the table.

#### Task 30 — Add FAQ Section + Schema.org FAQPage (Priority)
- Status: Pending.
- Goal: Improve extraction quality and platform visibility with structured Q&A.
- Deliverable: Add a required "FAQ for LLMs" section (5+ Q/A pairs) to the report contract and template; extend the renderer to emit JSON-LD `FAQPage` when the section is present.
- Verification: Rendering a compliant report includes a valid FAQPage JSON-LD block, and validation fails when fewer than 5 Q/A pairs are provided.

#### Task 31 — Add Platform Visibility Checklist (Priority)
- Status: Pending.
- Goal: Turn GEO best practices into concrete, trackable user actions.
- Deliverable: Add an "LLM Visibility Checklist" section to the report template with required items for ChatGPT (Bing Webmaster Tools), Perplexity (target query alignment), Gemini (YouTube/Google surfaces), and Claude (technical citation quality); update validation to require at least 4 checked/unchecked items.
- Verification: A report missing the checklist fails validation; a report with the checklist passes and includes all platform items.

#### Task 32 — Add Manual LLM Visibility Audit Template (Priority)
- Status: Pending.
- Goal: Give users a repeatable way to confirm whether they appear in LLM answers.
- Deliverable: Add `business-conspect/spec/LLM_VISIBILITY_TEMPLATE.md` plus a small script (e.g., `scripts/init_visibility_audit.py`) that creates `reports/<date>/<domain>/visibility.md` with platform-specific queries and a result log section.
- Verification: Running the script produces the visibility file with queries for ChatGPT, Perplexity, Gemini, and Claude, and the file is referenced in the report folder.
