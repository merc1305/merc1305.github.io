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
See `business-conspect/spec/ROADMAP.md` for archived completed tasks.

### Pending Tasks (Do Next)

### Value Review (Always)
- Rule: After completing each task, perform a short "Value Review" against `DEC-006` and `DEC-007` in `business-conspect/spec/DECISIONS.md`.
- Rule: If the task outcome is correct but not yet ideal for value clarity, recommendation priority, or new traffic, immediately add a follow-up task to close the gap.
- Verification: Each completed task should either (a) explicitly state how it supports value understanding and recommendation quality, or (b) create a new task that does.

### Roadmap Hygiene (Always)
- Rule: When a task is completed, move its detailed entry out of this SDD into a dedicated roadmap/history document (for example `business-conspect/spec/ROADMAP.md`) and keep only active/pending tasks here.

#### Task 22 — Prefill Request Form on Start Conspect (Priority)
- Status: Pending.
- Goal: Reduce friction so users can submit with zero extra typing if they have nothing to add.
- Deliverable: Clicking "Start Conspect" pre-fills the request form fields (URL, outcome, ICP, constraints, competitors) using the available defaults, and keeps the request valid with no edits.
- Verification: Enter a URL on the hero, click "Start Conspect," and the request form is prefilled; clicking the submit action without edits produces a valid request payload with those defaults.

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
