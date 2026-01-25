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
- Status: Pending.
- Goal: Improve confidence that the current reports can actually drive recommendation-quality answers and traffic.
- Deliverable: Update the three reference reports (`google.com`, `elinext.com`, `emcd.com`) to include more search-style questions (for example: "best X for Y", "X vs Y", "alternative to X", constraint-heavy questions, and selection logic framed as search queries).
- Verification: The reports pass both the base validator and the search-intent coverage validator.

#### Task 10 — Add Recommendation Evaluation Bench (Priority)
- Status: Pending.
- Goal: Replace guesswork with a repeatable, testable check of whether the report can drive recommendation-quality answers.
- Deliverable: A machine-readable query bench such as `business-conspect/spec/eval_queries.json` plus a short rubric document such as `business-conspect/spec/RECOMMENDATION_EVAL.md` that defines what a "good recommendation answer" must contain (value, fit, selection logic, constraints, and non-fit).
- Verification: `python3 -m json.tool business-conspect/spec/eval_queries.json` succeeds, and the rubric explicitly references `DEC-006` and `DEC-007`.

#### Task 11 — Implement Markdown → HTML Rendering
- Status: Pending.
- Goal: Eliminate double maintenance while preserving human-friendly reports.
- Deliverable: A renderer such as `business-conspect/scripts/render_report.py` and a template such as `business-conspect/scripts/templates/report.html`.
- Verification: Rendering a valid fixture produces `index.html` that includes the metadata, all section titles, and a canonical link back to `report.md`.

#### Task 12 — Make Rendering Validation-Gated
- Status: Pending.
- Goal: Prevent invalid reports from being published as HTML.
- Deliverable: The renderer refuses to write `index.html` when validation fails (or supports a strict mode that does so by default).
- Verification: Running the renderer on the invalid fixture does not overwrite the existing `index.html` and exits with a non-zero status.

#### Task 13 — Harden the Index Updater Around the Canonical Contract
- Status: Pending.
- Goal: Ensure the browse and search experience reflects the new source-of-truth rule.
- Deliverable: Update `business-conspect/scripts/update_index.py` to optionally warn or skip entries that lack `report.md`, and to preserve stable ordering and links.
- Verification: After running `python3 business-conspect/scripts/update_index.py`, `business-conspect/index.json` contains the expected entries and report.md links where available.

#### Task 14 — Add Automated Tests for Indexing and Validation
- Status: Pending.
- Goal: Reduce regressions in the most important offline scripts.
- Deliverable: A small unittest suite such as `business-conspect/scripts/tests/test_update_index.py` and `business-conspect/scripts/tests/test_validate_report.py`.
- Verification: Running `python3 -m unittest discover business-conspect/scripts/tests` completes successfully in a clean workspace.

#### Task 15 — Create a Single Publish Entrypoint
- Status: Pending.
- Goal: Make the correct workflow the easiest workflow.
- Deliverable: A publish script such as `business-conspect/scripts/publish_report.py` that runs validation, rendering, and index updates in the right order.
- Verification: Running `python3 business-conspect/scripts/publish_report.py <report-dir>` validates the report, (re)generates `index.html`, and updates `business-conspect/index.json`.

#### Task 16 — Define LLM Output Contracts (Parser, Strategist, Dialogue)
- Status: Pending.
- Goal: Make manual or semi-automated LLM usage consistent and testable.
- Deliverable: Contract documents and/or JSON schemas under `business-conspect/spec/` that specify required fields for parser output, strategist output, and the dialogue section.
- Verification: Each contract includes at least one minimal valid example and a short checklist that can be applied to raw LLM answers.

#### Task 17 — Implement Content Scraping and Normalization (Offline)
- Status: Pending.
- Goal: Produce reproducible, auditable inputs for LLM reasoning.
- Deliverable: A script such as `business-conspect/scripts/scrape.py` that saves normalized page snapshots into `raw/pages.json`.
- Verification: Running the scraper against a known URL writes `raw/pages.json` with non-empty page content entries and timestamps.

#### Task 18 — Implement LLM Answer Ingestion into Canonical Markdown
- Status: Pending.
- Goal: Convert raw LLM outputs into a contract-compliant `report.md`.
- Deliverable: A script such as `business-conspect/scripts/ingest_llm_answers.py` that reads structured answers (for example `raw/llm-answers.json`) and produces a `report.md` scaffold that passes validation.
- Verification: The generated `report.md` passes `validate_report.py` without manual edits for a valid fixture input.

#### Task 19 — Add Machine-Readable Summaries for LLMs
- Status: Pending.
- Goal: Improve discoverability and citation fidelity beyond HTML and Markdown.
- Deliverable: A compact `summary.json` per report and an update to `business-conspect/index.json` generation to include key summary fields when present.
- Verification: `summary.json` files are valid JSON and can be parsed by `python3 -m json.tool`, and the index contains summary-derived fields when available.

#### Task 20 — Ship LLM Discoverability Artifacts
- Status: Pending.
- Goal: Make the project easy for LLMs and AI search tools to understand and cite.
- Deliverable: Add `llms.txt` (and optionally `llms-full.txt`) within `business-conspect/` that explains the purpose, structure, and canonical artifacts, and links to the browse and search pages.
- Verification: The files exist, are plain text, and include correct public URLs under `https://merc1305.github.io/business-conspect/`.

#### Task 21 — Embed Structured Data in Generated Reports
- Status: Pending.
- Goal: Align human-readable reports with machine-readable hints used by search and AI systems.
- Deliverable: The HTML renderer embeds a JSON-LD block (for example a `CreativeWork` or `Report` representation) that includes domain, date, canonical URLs, and a short summary.
- Verification: The JSON-LD block can be extracted and parsed as valid JSON, and its canonical URL fields match the published report paths.
