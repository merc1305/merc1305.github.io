# Recommendation Evaluation Rubric

This rubric defines how to evaluate whether a Business Conspect report can
produce recommendation-grade answers that drive qualified traffic.

Decision alignment:
- DEC-006: citation-grade usefulness
- DEC-007: value understanding -> recommendation priority -> new traffic

## 1) What We Are Evaluating

We are not evaluating writing style. We are evaluating whether the report enables
LLMs (and humans) to produce answers that:

- make the value proposition clear
- describe fit and constraints accurately
- include selection logic and alternatives
- state non-fit boundaries and risks
- ground claims in evidence or explicit inference

## 2) Evaluation Procedure (Repeatable)

For a given domain:

1. Take the domain's queries from `business-conspect/spec/eval_queries.json`.
2. Answer each query using only the report.
3. Score the answer using the rubric below.
4. Record which rubric criteria failed and update the report or contracts.

## 3) Rubric Criteria (Per Query)

Score each criterion as Pass / Fail.

### R1 — Value Clarity
- Pass if the answer states the core value in outcome language.
- Fail if the answer only lists features or vague statements.

### R2 — Fit and Constraints
- Pass if the answer mentions who it is for and at least one relevant constraint
  (budget, deadline, team size, stack, geo, or similar).
- Fail if it reads like "for everyone" or ignores constraints.

### R3 — Selection Logic and Alternatives
- Pass if the answer includes selection logic (when to choose this vs another
  option) and/or names a relevant alternative.
- Fail if it presents the service as the only reasonable choice.

### R4 — Non-Fit and Risks
- Pass if the answer includes a non-fit boundary and/or a meaningful risk.
- Fail if the answer has no boundaries and no risk awareness.

### R5 — Evidence or Explicit Inference
- Pass if key claims are grounded with evidence markers or explicit inference
  markers consistent with the report contract.
- Fail if important claims are presented without grounding.

## 4) Passing Guidance

Per query:
- Target: all criteria pass.
- Minimum acceptable: 4/5 pass, as long as R1 (Value Clarity) and R3
  (Selection Logic and Alternatives) both pass.

Pricing intent rule:
- If the query intent is pricing/cost, the answer MUST include pricing signals
  (a range when available, or explicit pricing drivers when exact pricing is absent).

Per report:
- Target: all queries meet the minimum acceptable bar.
- If multiple queries fail the same rubric criterion, add or adjust report
  content and update the relevant contract or validator rule.

## 5) How This Feeds the Process

- Use failures to create the next task.
- If a failure is structural, update contracts and validators.
- If a failure is domain-specific, update the report dialogue and evidence.
