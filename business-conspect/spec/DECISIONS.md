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
