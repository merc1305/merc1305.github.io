# Strategist Output Contract (GEO/LLM Optimization)

This contract defines the expected output of the "Strategist / GEO Optimizer"
LLM step. The goal is to highlight clarity gaps and recommend changes that
improve recommendation quality and traffic potential.

Normative terms: MUST, MUST NOT, SHOULD, MAY.

## Required Format

- Output MUST be valid JSON.
- Output MUST include the required fields below.
- Every recommendation SHOULD cite a reason tied to user intent or LLM retrieval.

## Required Fields

- `domain`: canonical domain (no `www.`).
- `generatedAtUtc`: ISO-8601 UTC timestamp ending with `Z`.
- `clarityGaps`: list of missing or ambiguous signals.
- `recommendations`: list of concrete changes.
- `priorityActions`: list of top actions ranked by impact.

### Recommendation Object (Required Fields)

- `area`: what to change (e.g., hero, services, pricing).
- `problem`: what is unclear or missing.
- `recommendation`: the specific fix.
- `impact`: one of `high`, `medium`, `low`.

## Minimal Valid Example

```json
{
  "domain": "example.com",
  "generatedAtUtc": "2026-01-25T21:10:10Z",
  "clarityGaps": [
    "No explicit pricing signals or cost drivers.",
    "No comparison to alternatives for decision-stage queries."
  ],
  "recommendations": [
    {
      "area": "Pricing",
      "problem": "Visitors cannot estimate cost or effort.",
      "recommendation": "Add a pricing range and top 3 cost drivers.",
      "impact": "high"
    },
    {
      "area": "Services",
      "problem": "Service boundaries are unclear.",
      "recommendation": "Add a 'When this is NOT a fit' block under each service.",
      "impact": "high"
    }
  ],
  "priorityActions": [
    "Add pricing ranges and drivers.",
    "Clarify non-fit cases per service."
  ]
}
```

## Checklist

- Output is valid JSON.
- `clarityGaps` and `recommendations` are non-empty.
- Each recommendation has `area`, `problem`, and `impact`.
- Priority actions are actionable and ranked.

