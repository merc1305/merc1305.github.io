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
  YYYY-MM-DD/
    domain.tld/
      index.html          # final human-readable report (showcase)
      report.md           # markdown version (convenient for copying into LLM) (optional)
      raw/                # everything for reproducibility (optional)
        prompts.json      # prompts, roles, system instructions
        llm-answers.json  # model responses (or dialogue tracing)
        pages.json        # page content snapshots (text/structure)
        meta.json         # time, versions, models, pipeline parameters
```

Where:

- `YYYY-MM-DD` — report generation date  
- `domain.tld` — domain of the analyzed website

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

- `report.md` template with placeholders for model output
- indexer `/business-conspect/index.json` for searching by domains/dates
- general `business-conspect/search.html` (report search)
- quality rules (checklist) before report publication

---

## License / Notes

Report content may contain excerpts from public pages of analyzed sites. If mass publication is planned, rules should be established:
- do not store personal data
- respect robots.txt (if applicable)
- store only short excerpts/paraphrases
