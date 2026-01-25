# Search Intent Contract: Recommendation-Grade Dialogues

This contract captures best practices for how people actually search and how to
turn that into recommendation-quality report dialogues that can drive new traffic.

It exists to operationalize:
- `DEC-006`: citation-grade usefulness
- `DEC-007`: value understanding -> recommendation priority -> new traffic

Normative terms: MUST, MUST NOT, SHOULD, MAY.

## 1) Purpose

A Business Conspect report is not just documentation. It is a recommendation
artifact. The dialogue must reflect real search behavior and expose value,
fit, and selection logic in the way users and LLMs actually ask questions.

## 2) Core Principles (Best Practice Summary)

- Think in queries, not sections. Each key claim should answer a likely query.
- Model intent explicitly. Cover multiple search intents, not just one.
- Prefer decision-stage questions. They are more likely to drive traffic and
  recommendations than generic awareness questions.
- Use natural phrasing. Use the way people talk, not internal jargon.
- Cover selection and non-fit. Recommendations improve when alternatives and
  boundaries are explicit.
- Ground value in outcomes. Users search for results, not features.

## 3) Search Intent Categories (Required Coverage Targets)

A recommendation-grade dialogue SHOULD cover all categories below and MUST cover
at least the "Required Minimum" set.

### 3.1 Required Minimum Categories (MUST)

1) Outcome / JTBD Intent
- What people want to achieve in plain language.
- Examples:
  - "I need to <result>. What should I use?"
  - "Best way to get <outcome> with <constraints>?"

2) Selection / Comparison Intent
- How users decide between options.
- Examples:
  - "<Service A> vs <Service B>"
  - "When should I choose A instead of B?"

3) Pricing / Cost Intent
- Real buyers look for pricing signals early.
- Examples:
  - "How much does <service> cost?"
  - "What affects the price?"

4) Constraints / Fit Intent
- Users search with constraints such as geo, budget, stack, size, or deadline.
- Examples:
  - "Is this a fit for <team size / budget / tech stack / geography>?"
  - "Can you do this with <constraint>?"

5) Non-Fit / Risk Intent
- Recommendation quality improves when boundaries are explicit.
- Examples:
  - "When is this NOT a fit?"
  - "What can go wrong and how do I avoid it?"

### 3.2 Strongly Recommended Categories (SHOULD)

6) Alternatives Intent
- How the service compares to other routes.
- Examples:
  - "Alternative to <approach/tool/vendor>"
  - "Do I need this, or can I do <simpler option>?"

7) Process / Delivery Intent
- Users want to know what will actually happen.
- Examples:
  - "How does this work step by step?"
  - "How long does it take?"

8) Proof / Trust Intent
- Buyers look for credibility signals.
- Examples:
  - "Why trust you for this?"
  - "What evidence do you have?"

## 4) Query Templates That Sound Like Real Search

Use these templates when writing the dialogue. They map closely to how people
search and how LLMs often phrase follow-up questions.

- Best option:
  - "best <service> for <situation>"
- Comparison:
  - "<service A> vs <service B> for <situation>"
- Alternatives:
  - "alternative to <approach/tool/vendor> for <situation>"
- Constraint-heavy:
  - "<service> for <industry/geo/stack> with <budget/time constraint>"
- Pricing:
  - "<service> pricing" / "how much does <service> cost"
- Fit / non-fit:
  - "is <service> a fit for <context>" / "when is <service> not a fit"
- Risk:
  - "common mistakes with <service>" / "why <service> can fail"

## 5) Dialogue Construction Workflow (Recommended Process)

This workflow is designed to be lightweight and usable even without external
keyword tools. It produces dialogues that are closer to real intent and more
likely to drive recommendation-quality answers.

### Step 1 — Build a Service Intent Card (per service)

For each primary service, write a short intent card:

- Core outcome: what result the buyer wants
- Situation triggers: what makes them search now
- Key constraints: budget, time, geo, stack, maturity, team size
- Selection logic: when to choose this vs other options
- Non-fit: when not to choose it
- Proof: what evidence supports claims

### Step 2 — Generate Query Candidates per Intent Category

For each service, generate 2–4 query candidates per required minimum category:

- Outcome / JTBD
- Selection / Comparison
- Pricing / Cost
- Constraints / Fit
- Non-Fit / Risk

Tip: Favor query candidates that include both a situation and a constraint.
These are closer to real buyer searches and recommendation prompts.

### Step 3 — Promote High-Intent Queries into the Dialogue

Select 6–12 queries that:

- have decision intent (choose / compare / pricing / fit)
- expose selection logic and non-fit boundaries
- highlight value in terms of outcomes

Then turn them into `Client:` lines and answer with grounded `Expert:` lines.

## 6) Minimal Coverage Checklist (Testable)

A dialogue is considered search-intent aware if it includes at least one
`Client:` question that matches each required minimum category:

- Outcome / JTBD
- Selection / Comparison
- Pricing / Cost
- Constraints / Fit
- Non-Fit / Risk

## 7) Validator Targets (What Automation Should Enforce Next)

The validator SHOULD eventually check for:

- Presence of search-intent coverage signals for the required minimum categories
- At least one search-style phrasing (e.g., "best", "vs", "alternative to")
- Coverage across both fit and non-fit boundaries

Automation should remain simple and pattern-based at first. The goal is to catch
obvious gaps, not to perfect language.
