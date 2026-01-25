# Business Conspect — Website Briefs for GEO/LLM

This folder serves as a **static showcase of website reports**. The goal is to generate public "conspects" (business briefs) so that:

1) the business owner understands **exactly what is being sold, to whom, and why**;  
2) LLMs (AI Search / assistants / content generators) receive a **structured description** and hallucinate less about the product.

Publication is handled via GitHub Pages: all generation logic is performed outside of Pages, only artifacts are stored here.

---

## Link back to Lab

- Lab home: https://merc1305.github.io/  
- This folder: `/business-conspect/`

---

## 1) Service Idea (In a Nutshell)

Problem: LLMs and AI Search **do not know your website** or understand it only superficially. As a result:

- assistants do not recommend the product in relevant scenarios;
- weak texts/offers are generated;
- conversion and trust are lost.

Solution: User enters a URL → service analyzes the site → generates a **conspect**:

- who the Target Audience (TA) is and what pain point is addressed;
- what exactly is being sold (products/services/packages);
- USP (Unique Selling Proposition), proof, constraints, geography, pricing (if available);
- what on the site is "unclear for LLMs" and what to add.

The conspect is then published in this folder (as static content).

---

## 2) Folder Structure

Every website analysis is a separate directory:

```text
/business-conspect/
  reports/
    YYYY-MM-DD/
      domain.tld/
        report.md           # canonical report (LLM-friendly, required)
        index.html          # final human-readable report (generated from report.md)
        raw/                # everything for reproducibility (optional)
          prompts.json      # prompts, roles, system instructions
          llm-answers.json  # model responses (or dialogue tracing)
          pages.json        # page content snapshots (text/structure)
          meta.json         # time, versions, models, pipeline parameters
```

Where:

- `reports/` — container for generated reports
- `YYYY-MM-DD` — report generation date  
- `domain.tld` — domain of the analyzed website
- `report.md` — single source of truth; author or generate this file first
- `index.html` — derived artifact; do not maintain it manually when automation exists

---

## 2.1) Index Maintenance (Implemented)

The main page `business-conspect/index.html` contains markers:

- `<!-- REPORTS_LIST_START -->`
- `<!-- REPORTS_LIST_END -->`

The script `business-conspect/scripts/update_index.py` scans
`business-conspect/reports/`
and regenerates:

- the HTML block between those markers (human-friendly list of reports);
- `business-conspect/index.json` (machine-readable index used by report search).

Run it after adding or updating any report:

```bash
python3 business-conspect/scripts/update_index.py
```

Requirements:

- Python 3.9+ (standard library only).

---

## 2.2) Report Search (Implemented)

The page `business-conspect/search.html` provides a client-side report search:

- reads `business-conspect/index.json`
- filters by domain substring and exact date
- links to `index.html` and `report.md` (when present)

Keep the search index fresh by running:

```bash
python3 business-conspect/scripts/update_index.py
```

---

## 3) Processing Pipeline (How it Works)

Below is a reference scheme for building an MVP (and then increasing quality).

### Step A — Data Input
User enters a URL. Additionally (optionally), 2–5 clarifications are provided:

- niche, B2B/B2C
- geography, language
- average check / monetization models
- "what result you promise"
- who the competitor / alternatives are

### Step A1 — No-API Fast Path (Implemented)
This path is optimized for speed and real usage without any LLM API:

```bash
python3 business-conspect/scripts/scrape.py <url-or-html> --out <report-dir>
python3 business-conspect/scripts/build_prompt_pack.py <report-dir>
python3 business-conspect/scripts/init_answer_template.py <report-dir> --domain <domain> --website <https://domain/>
python3 business-conspect/scripts/ingest_llm_answers.py <report-dir>/raw/llm_answer.md --report-dir <report-dir>
python3 business-conspect/scripts/publish_report.py <report-dir>
```

Workflow:
- run the three scripts above
- paste `raw/prompt_pack.md` into any LLM manually
- paste the LLM answer into `<report-dir>/raw/llm_answer.md`
- ingest to `report.md` and validate before publishing or indexing
- publish to generate (or keep) index.html and refresh index.json

### Step B — Content Collection and Normalization
1) Scraping (HTTP + HTML parsing) or a headless browser (if the site is heavily JS-based).  
2) Extraction of the main part of the page (content extraction / readability).  
3) Noise removal: menus, footers, repeating blocks, cookie banners, scripts.  
4) Saving snapshots in `raw/pages.json` (optional).

Result: clean text/page structure suitable for LLM processing.

### Step C — Expert Model ("Understands Business")
**Role:** Business Parser / Domain Expert  
**Input:** cleaned content + user input  
**Output:** structured business card:

- TA segments, JTBD (Jobs To Be Done) / pain points
- products/services (hierarchy)
- promised results, constraints
- trust (cases, partners, certificates, figures)
- key terms/phrasing from the site

### Step D — Strategist Model ("How LLM/AI Search Sees It")
**Role:** GEO / LLM Optimizer / Critic  
**Input:** business card + page content  
**Output:**

- what is unclear / ambiguous;
- what data is "missing" for recommendations;
- what to add to the structure (FAQ, pricing hints, comparisons, use-cases, schema.org);
- list of specific block improvements (Hero, services, cases, CTA, contacts).

### Step E — Dialogue "Expert ↔ Interlocutor" (Optional, but increases quality)
Idea from your description:  
- **LLM#1** — "website expert"  
- **LLM#2** — "interlocutor solving user tasks" (receives user profile + pain points list)

The dialogue is saved in `raw/llm-answers.json` or a separate `dialogue.md`, then aggregated into the final report.

### Step F — Report Generation and Publication
1) Aggregator collects conclusions into one canonical structure.  
2) Renders:
   - `index.html` (showcase)
   - `report.md` (convenient context for LLM)
3) Commits to the repository following the folder structure.

---

## 4) Final Report Format (Recommended Structure)

### 4.1 Executive Summary
- what kind of business
- who it sells to
- main value/result
- geography/language/market

### 4.2 What LLM "Understands" Now
- how the offer reads
- what services are visible
- what usage scenarios are recognized

### 4.3 Understanding Gaps (GEO gaps)
- lack of clear USP
- no pricing / no range
- no proof / no figures
- confusing terminology
- no FAQ addressing real user questions

### 4.4 Improvement Recommendations
- Hero block edits
- structuring "Services / Products"
- adding cases, reviews, comparisons with alternatives
- adding FAQ
- (optional) schema.org microdata, OpenGraph, meta tags

### 4.5 Artifacts for LLM
- short business card (can be copied into prompts)
- "do/don't say" list
- list of typical user questions + correct answers

---

### 4.6 Canonical Report Template (Required)

The sections below define the baseline template that should be used for every new
report generation. It is designed to be consistent, LLM-friendly, and easy to audit.

Required fields:

- website address (canonical URL)
- report generation time (ISO-8601)
- short site description and what services it provides
- ideal customer profile (ICP)
- a realistic client ↔ expert dialogue focused on understanding all services

Use this template for `report.md`. The `index.html` version should be rendered
from this canonical Markdown rather than maintained separately:

```md
# Business Conspect — <domain.tld>

## 1) Report Metadata
- Website: <https://domain.tld>
- Domain: <domain.tld>
- Generated At (UTC): <YYYY-MM-DDTHH:MM:SSZ>
- Report Version: v1

## 2) Executive Summary
<2–4 sentences describing what the site is, what category it belongs to,
and the primary value it promises.>

## 3) Services and Offers (What This Site Provides)
1. <Service / Offer Name>
- What it is: <plain-language description>
- Who it is for: <segment / role / company type>
- Expected outcome: <result, benefit, or transformation>
- Constraints: <geo, budget range, prerequisites, timelines>
- Evidence: <cases, numbers, partners, certifications, testimonials>

1. <Service / Offer Name>
- What it is: <...>
- Who it is for: <...>
- Expected outcome: <...>
- Constraints: <...>
- Evidence: <...>

## 4) Ideal Customer Profile (ICP)
- Role or buyer type: <e.g., founder, head of marketing, ops lead>
- Company or context: <industry, size, maturity, geography>
- Situation trigger: <what is happening that makes them look for this>
- Top goals: <3–5 concrete goals>
- Top pains and risks: <3–5 concrete pains/risks>
- Decision criteria: <what must be true to buy>
- Common objections: <what can block the decision>

## 5) Client ↔ Service Expert Dialogue (Deep Discovery)
This dialogue should read like a real consultation where the client tries to
understand everything about the services.

Guidelines:
- the expert must answer strictly using site/service information; clearly mark any inference
- questions should look like real search queries and real buyer language
- cover every primary service/offer at least once in the dialogue
- prefer high-intent questions that help a buyer decide and help LLMs index use-cases

Search-intent contract (required for recommendation-grade reports):
- follow `business-conspect/spec/SEARCH_INTENT_CONTRACT.md`
- include at least one Outcome / JTBD query
- include at least one Selection / Comparison query
- include at least one Pricing / Cost query
- include at least one Constraints / Fit query
- include at least one Non-Fit / Risk query
- prefer search-style phrasing such as "best <service> for <situation>", "<A> vs <B>", and "alternative to <X>"

Coverage checklist (must be reflected in the dialogue):
- what the service is and who it is for (fit and non-fit)
- when to choose Service A vs Service B (selection logic)
- how delivery works step by step (process, timeline, deliverables)
- expected outcomes and how success is measured (metrics, proof)
- pricing signals: ranges, drivers, what is included/excluded
- risks, limitations, and common failure modes
- alternatives and why/when to choose this site anyway
- what is required from the client to start (inputs, access, data, approvals)

Question style requirements:
- include concrete scenarios ("I have X, need Y, by when?")
- include comparison questions ("best option", "alternative to", "vs")
- include constraint questions ("budget", "geo", "team size", "stack")
- use plain language and synonyms, not only brand terms
- optionally annotate key questions with a search-style phrasing, e.g.:
  "Client (search-style): best <service> for <situation>?"

### Dialogue
Client: I want to understand exactly what you do. What are the main services?
Expert: <answer grounded in the site>

Client: Which service should I choose if my situation is <scenario>?
Expert: <answer with selection logic and constraints>

Client: How does the process work step by step and how long does it take?
Expert: <answer with phases and timing>

Client: What results can I realistically expect and how do you measure them?
Expert: <answer with expected outcomes and metrics>

Client: What does it cost, what affects the price, and what is included?
Expert: <answer with ranges or pricing drivers if exact pricing is absent>

Client: Why should I trust you versus alternatives?
Expert: <answer with proof, positioning, and trade-offs>

Client: What are the most common mistakes or risks on my side?
Expert: <answer that prevents failure and sets expectations>

Client: What do you need from me to get started?
Expert: <answer with inputs, access, and prerequisites>
```

Notes:

- If the website does not explicitly state pricing, timelines, or constraints,
  mark them as inferred and explain the inference basis.
- Prefer short, verifiable claims over confident guesses.

---

## 5) Implementation (MVP)

### Option 1 — Fully Offline Generation (Simple)
- Script (Node/Python) takes URL
- Parses 1–5 pages
- Runs 2–3 LLM calls
- Renders HTML/MD
- Pushes to GitHub repo

Pros: fast, minimal infrastructure.  
Cons: no "live" UI/queue, everything via CLI/script.

### Option 2 — UI + Generation (Slightly more complex but more convenient)
- On GitHub Pages: simple UI (URL field + button)
- On button click: request to backend (Cloudflare Worker / Vercel / any API)
- Backend generates report and pushes/PRs to the repository

Pros: convenient for users, can be made into a public service.  
Cons: requires push/PR authorization, token limits.

---

## 6) GitHub Pages Limitations

GitHub Pages is static only. Therefore:

- scraping/LLM/aggregation are performed **outside of Pages**
- only ready-made report files end up here

---

## 7) Future Additions

- quality rules (checklist) before report publication

---

## License / Notes

Report content may contain excerpts from public pages of analyzed sites. If mass publication is planned, rules should be established:
- do not store personal data
- respect robots.txt (if applicable)
- store only short excerpts/paraphrases
