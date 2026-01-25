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
- **Report Generation**: (Future) Generating reports in HTML/Markdown formats via offline scripts.
- **Report Search**: (Implemented) `business-conspect/search.html` loads `index.json` and filters reports by domain and date.
- **Canonical Report Template**: (Documented) Every report should follow a consistent template in `report.md` (with `index.html` as a mirror) and must include website address, generation time, summary, services, ICP, and a client ↔ expert dialogue that covers full buyer discovery.
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
6) **Report Generation**: Aggregate outputs into `index.html` and optional `report.md`.

### 3.3 Artifacts & Storage Layout
Reports are stored as static artifacts to keep GitHub Pages simple and reproducible:

```text
/business-conspect/
  reports/
    YYYY-MM-DD/
      domain.tld/
        index.html
        report.md (optional)
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

## 5. Implementation Roadmap (Next Steps)

These steps are designed to achieve a working MVP using the "Offline Generation" approach, compatible with the current GitHub Pages hosting.

### Step 1: Initialize Analysis Environment
- **Goal**: Create a dedicated `scripts/` directory for the generation logic.
- **Action**: Set up a Python/Node.js environment with dependencies (e.g., `requests`, `beautifulsoup4`, `openai` or `langchain`).
- **Deliverable**: `scripts/requirements.txt` and `scripts/main.py` skeleton.

### Step 2: Implement Content Scraper
- **Goal**: Fetch and clean website content.
- **Action**: Create a function that accepts a URL, fetches HTML, strips boilerplate (nav, footer, scripts), and returns clean text/markdown.
- **Deliverable**: `scripts/scraper.py` module.

### Step 3: Implement Prompt Builder
- **Goal**: Construct complete prompts for the user.
- **Action**: Create a function that merges the scraped content with the system prompts into a copy-pasteable format (e.g., `prompt.txt`).
- **Deliverable**: `scripts/prompt_builder.py` module.

### Step 4: Develop "Business Parser" Prompt
- **Goal**: Extract structured business logic.
- **Action**: Design a system prompt to analyze cleaned text and output JSON with: Tagline, Target Audience, Products, and Value Proposition.
- **Deliverable**: `prompts/parser.yaml` (or string constant).

### Step 5: Develop "Strategist" Prompt
- **Goal**: Critique compentency for AI Search.
- **Action**: Design a system prompt to identify gaps (missing pricing, unclear USP) and "hallucination risks".
- **Deliverable**: `prompts/strategist.yaml`.

### Step 6: Implement Response Handler
- **Goal**: Process manually saved LLM outputs.
- **Action**: Create a function to read `raw/llm-answers.json` (pasted by the user) and validate structure.
- **Deliverable**: JSON validation and parsing logic.

### Step 7: Create HTML Report Template
- **Goal**: Visual presentation of results.
- **Action**: Design a Jinja2 (or similar) HTML template that inherits the "Lab" design system and displays the analysis data.
- **Deliverable**: `scripts/templates/report.html`.

### Step 8: Implement Report Renderer
- **Goal**: Generate the final static page.
- **Action**: Combine the analyzing JSON data with the HTML template to produce `index.html` in the target directory.
- **Deliverable**: `scripts/renderer.py` module.

### Step 9: Build CLI Entrypoint
- **Goal**: One command to run it all.
- **Action**: accurate `main.py` to accept CLI arguments (URL) and orchestrate Scraping -> **Prompt Generation -> User Pause -> Response Parsing** -> Generation.
- **Deliverable**: Working command `python scripts/main.py https://example.com`.

### Step 10: Automatic Index Updater
- **Goal**: Update the "Browse Reports" list.
- **Action**: Scan the `business-conspect/` directory for reports and regenerate the main `business-conspect/index.html` list to include new reports.
- **Implementation**: Script `business-conspect/scripts/update_index.py`.
- **Implementation markers**: `<!-- REPORTS_LIST_START -->` and `<!-- REPORTS_LIST_END -->` in `business-conspect/index.html`.
- **Implementation artifact**: `business-conspect/index.json` (machine-readable index).
- **Usage**: `python3 business-conspect/scripts/update_index.py`
- **Status**: Implemented.

### Step 11: Report Search Page
- **Goal**: Find reports quickly without scanning the full list.
- **Action**: Create `business-conspect/search.html` that loads `business-conspect/index.json` and filters by domain and date.
- **Integration**: Add a clear entry point from `business-conspect/index.html`.
- **Status**: Implemented.
