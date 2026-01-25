# Software Design Document: Business Conspect

## 1. Overview
Business Conspect is a tool designed to analyze websites and generate structured summaries (conspects) for both human readers and Large Language Models (LLMs). The goal is to provide a clear understanding of what a business sells, who its target audience is, and why it's valuable.

## 2. Requirements

### 2.1 Functional Requirements
- **Web Interface**: A premium, "lab" style UI.
- **URL Input**: Users can input a website URL.
- **Process Execution**: A button to start the analysis/summarization process.
- **Report Generation**: (Future) Generating reports in HTML/Markdown formats.
- **English Documentation**: All user-facing documentation must be in English.

### 2.2 Non-Functional Requirements
- **Aesthetics**: Premium, modern design using gradients and glassmorphism.
- **Performance**: Static hosting on GitHub Pages.
- **SEO**: Basic SEO optimization for the tool landing page.

## 3. Architecture

### 3.1 Frontend
- **HTML5**: Semantic structure.
- **Vanilla CSS**: Custom styling based on root "lab" theme.
- **JavaScript**: UI interactivity (handling button clicks, input validation).

### 3.2 Backend (Proposed)
- **External API**: Since GitHub Pages is static, the actual scraping and LLM processing will happen on an external backend (e.g., Cloudflare Workers or a dedicated server).

## 4. UI Components
- **Hero Section**: Modern title and subtitle.
- **Input Group**: Styled text input for URL + Action button.
- **Manifesto/Description**: Brief explanation of the tool's purpose.
