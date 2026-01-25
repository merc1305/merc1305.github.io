# Parser Output Contract (Business Card)

This contract defines the expected output of the "Business Parser / Domain Expert"
LLM step. The goal is to convert raw content into a structured business card
that can be validated and reused downstream.

Normative terms: MUST, MUST NOT, SHOULD, MAY.

## Required Format

- Output MUST be valid JSON.
- Output MUST include the required fields below.
- Any inferred claim MUST include an `inference` note and an `evidence` URL.

## Required Fields

- `domain`: canonical domain (no `www.`).
- `website`: absolute URL.
- `generatedAtUtc`: ISO-8601 UTC timestamp ending with `Z`.
- `summary`: 1–3 sentences about the business and its value.
- `services`: list of service objects.
- `icp`: ideal customer profile object.
- `evidence`: list of source URLs used.
- `vocabulary`: list of key phrases from the site.

### Service Object (Required Fields)

- `name`
- `whatItIs`
- `whoItIsFor`
- `expectedOutcome`
- `constraints`
- `evidence`: list of URLs
- `inference`: optional string explaining inferred elements

### ICP Object (Required Fields)

- `roleOrBuyerType`
- `companyContext`
- `situationTrigger`
- `topGoals`
- `topPainsRisks`
- `decisionCriteria`
- `commonObjections`

## Minimal Valid Example

```json
{
  "domain": "example.com",
  "website": "https://example.com/",
  "generatedAtUtc": "2026-01-25T21:05:23Z",
  "summary": "Example.com provides a neutral reference page used in technical documentation.",
  "services": [
    {
      "name": "Reference Page for Examples",
      "whatItIs": "A single-page reference site used in documentation.",
      "whoItIsFor": "Developers and technical writers.",
      "expectedOutcome": "Stable example URLs in docs.",
      "constraints": "Not a full product offering.",
      "evidence": ["https://example.com/"]
    }
  ],
  "icp": {
    "roleOrBuyerType": "Technical authors and developers.",
    "companyContext": "Teams producing documentation.",
    "situationTrigger": "Need a neutral, stable URL in examples.",
    "topGoals": ["Avoid broken links", "Keep examples neutral"],
    "topPainsRisks": ["Accidental endorsement", "Unstable demo links"],
    "decisionCriteria": ["Stability", "Recognizability"],
    "commonObjections": ["This is not my real site"]
  },
  "evidence": ["https://example.com/"],
  "vocabulary": ["example domain", "documentation", "reference"]
}
```

## Checklist

- Output is valid JSON.
- `domain`, `website`, and `generatedAtUtc` are present.
- Every service has `whoItIsFor` and `expectedOutcome`.
- Every non-trivial claim has `evidence` or explicit `inference`.
- ICP includes `situationTrigger` and decision criteria.

