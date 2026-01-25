# Business Conspect Specifications

This directory contains the formal specifications for the Business Conspect tool.

## Documents
- [SDD.md](SDD.md): Software Design Document detailing the architecture and requirements.
- [DECISIONS.md](DECISIONS.md): Log of key technical and design decisions.
- [REPORT_CONTRACT.md](REPORT_CONTRACT.md): Canonical, testable contract for `report.md` with evidence and inference rules.
- [SEARCH_INTENT_CONTRACT.md](SEARCH_INTENT_CONTRACT.md): Best-practice contract for modeling how people search and turning that into recommendation-grade dialogues.
- [LLM_ANSWER_TEMPLATE.md](LLM_ANSWER_TEMPLATE.md): Validator-friendly template for the manual LLM loop (no API fast path).
- [RECOMMENDATION_EVAL.md](RECOMMENDATION_EVAL.md): Rubric for evaluating whether reports support recommendation-quality answers and qualified traffic.
- Evaluation queries: `business-conspect/spec/eval_queries.json`
- Index automation: `business-conspect/scripts/update_index.py` scans `business-conspect/reports/`, regenerates the report list in `business-conspect/index.html`, and writes `business-conspect/index.json`.

## No-API Fast Path (Concierge Mode)
- Scrape sources: `python3 business-conspect/scripts/scrape.py <url-or-html> --out <report-dir>`
- Build prompt pack: `python3 business-conspect/scripts/build_prompt_pack.py <report-dir>`
- Initialize answer template: `python3 business-conspect/scripts/init_answer_template.py <report-dir> --domain <domain> --website <https://domain/>`
- Validate a manual answer: `python3 business-conspect/scripts/validate_report.py <report-dir>/raw/llm_answer.md`
