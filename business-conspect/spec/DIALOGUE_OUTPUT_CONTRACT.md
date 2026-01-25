# Dialogue Output Contract (Client ↔ Expert)

This contract defines the required output for the dialogue section. The goal
is to reflect real search intent and provide recommendation-grade answers that
LLMs can reuse safely.

Normative terms: MUST, MUST NOT, SHOULD, MAY.

## Required Format

- Output MUST be Markdown.
- Output MUST contain the heading:
  `## 5) Client ↔ Service Expert Dialogue (Deep Discovery)`
- Dialogue MUST use `Client:` and `Expert:` lines.
- Dialogue MUST cover required minimum intent categories:
  Outcome / JTBD, Selection / Comparison, Pricing / Cost, Constraints / Fit,
  and Non-Fit / Risk.
- Any inferred answer MUST include `[inference: ...]` and an evidence marker.

## Minimal Valid Example

```md
## 5) Client ↔ Service Expert Dialogue (Deep Discovery)
Client: I need to achieve <outcome>. What should I choose here?
Expert: <answer with selection logic> [evidence: https://example.com/]

Client: Service A vs Service B for my context - when should I choose each?
Expert: <answer> [evidence: https://example.com/]

Client: How much does this cost and what drives the pricing?
Expert: <answer; infer carefully> [inference: pricing not listed] [evidence: https://example.com/]

Client: Is this a fit for my constraints like team size, tech stack, geo, or deadline?
Expert: <answer with constraints> [evidence: https://example.com/]

Client: When is this NOT a fit, and what risks or common mistakes should I avoid?
Expert: <answer with non-fit boundaries> [evidence: https://example.com/]
```

## Checklist

- The required heading is present.
- At least one `Client:` and one `Expert:` line exist.
- All five required intent categories appear in `Client:` lines.
- Each answer includes evidence or explicit inference markers.

