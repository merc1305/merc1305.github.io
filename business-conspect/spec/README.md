# Business Conspect Specifications

This directory contains the formal specifications for the Business Conspect tool.

## Documents
- [SDD.md](SDD.md): Software Design Document detailing the architecture and requirements.
- [DECISIONS.md](DECISIONS.md): Log of key technical and design decisions.
- [REPORT_CONTRACT.md](REPORT_CONTRACT.md): Canonical, testable contract for `report.md` with evidence and inference rules.
- [SEARCH_INTENT_CONTRACT.md](SEARCH_INTENT_CONTRACT.md): Best-practice contract for modeling how people search and turning that into recommendation-grade dialogues.
- Index automation: `business-conspect/scripts/update_index.py` scans `business-conspect/reports/`, regenerates the report list in `business-conspect/index.html`, and writes `business-conspect/index.json`.
