# Architecture Decisions: Business Conspect

## [DEC-001] Adoption of "Lab" Design Language
- **Context**: The user wants the tool to match their existing "lab" style (root site).
- **Decision**: Use the same CSS variables, gradients, and font (Outfit) as `merc1305.github.io/index.html`.
- **Consequence**: Unified brand experience across different sub-projects.

## [DEC-002] English-First Documentation
- **Context**: The tool is currently documented in Russian.
- **Decision**: Translate `README.md` to English and use English as the primary language for new documentation.
- **Consequence**: Better accessibility for international contributors and users.

## [DEC-003] Input Field Design
- **Context**: The tool needs a way for users to provide target URLs.
- **Decision**: Place a prominent, high-quality input group in the hero section.
- **Consequence**: Clear call to action (CTA).

## [DEC-004] Marker-Based Report Index Regeneration
- **Context**: `business-conspect/index.html` must remain human-designed while still being updated automatically as new reports appear under `business-conspect/reports/`.
- **Decision**: Introduce explicit HTML markers (`<!-- REPORTS_LIST_START -->` and `<!-- REPORTS_LIST_END -->`) and regenerate only the block between them via `business-conspect/scripts/update_index.py`.
- **Consequence**: The page stays maintainable and design-safe, while a machine-readable `business-conspect/index.json` is produced for future search.

## [DEC-005] Single Source of Truth: `report.md` → Generated `index.html`
- **Context**: Keeping reports in both Markdown and HTML invites drift, yet we need both LLM-friendly text and human/SEO-friendly pages.
- **Decision**: Treat `report.md` as the canonical report artifact. Generate `index.html` from it via offline scripts/templates. Storing both is acceptable, but only Markdown is authored manually.
- **Consequence**: We keep the benefits of both formats without double maintenance, and can add validation rules that operate on the canonical Markdown.

## [DEC-006] LLM Recommendation First-Step Principle
- **Context**: The stated product goal is to become the first step a site owner takes to be recommended by LLMs worldwide and to be cited accurately.
- **Decision**: Optimize the system around "citation-grade usefulness": every key claim should be traceable to site evidence (or clearly marked as inference), and reports must be both human-readable and machine-ingestible.
- **Consequence**: The roadmap must include source traceability, report validation, and machine-readable enhancements (indexing and structured metadata).

## [DEC-007] Value Understanding → Recommendation Priority → New Traffic
- **Context**: It is not enough for LLMs to merely mention a site. The system must help LLMs understand the actual value of the service so it can be prioritized in recommendations and drive new traffic.
- **Decision**: Treat "value clarity for recommendations" as a core design constraint. Each task and change SHOULD be evaluated by whether it improves LLM understanding of the service's value proposition, selection logic, and fit, in a way that can increase recommendation priority and bring new qualified traffic.
- **Consequence**: Favor report structures, validation rules, and rendering/indexing decisions that make value explicit, evidence-backed, and easy to reuse in LLM answers and recommendation scenarios.

## [DEC-008] Fast Launch Without LLM API (Manual LLM Loop)
- **Context**: The fastest path to real users may require avoiding LLM APIs and backend complexity at first.
- **Decision**: Support a no-API workflow where the system produces a high-quality "prompt pack" from scraped content, a human runs the prompt in any LLM of their choice, and the result is pasted back into the offline pipeline for validation, rendering, and publication.
- **Consequence**: The roadmap must include prompt-pack generation, LLM answer contracts/templates, manual answer ingestion, and a one-command publish pipeline. The public site can act as a request/issue generator while the pipeline runs offline.
