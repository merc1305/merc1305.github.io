# Report Contract: Canonical `report.md`

This document defines the single source of truth contract for Business Conspect
reports. It is designed to be strict enough for automation, while remaining
simple to follow during manual authoring.

Normative terms: MUST, MUST NOT, SHOULD, MAY.

References:
- Canonical template: `business-conspect/README.md` (section "4.6 Canonical Report Template")
- Architecture decisions: `business-conspect/spec/DECISIONS.md`

## 1) Canonical Artifact and Location

- The canonical report artifact MUST be `report.md`.
- The canonical path SHOULD be `business-conspect/reports/YYYY-MM-DD/domain.tld/report.md`.
- `index.html` is a derived artifact and MUST NOT be treated as the source of truth.

## 2) Required Top-Level Structure

A valid report MUST include the following headings exactly once:

- `# Business Conspect — <domain.tld>`
- `## 1) Report Metadata`
- `## 2) Executive Summary`
- `## 3) Services and Offers (What This Site Provides)`
- `## 4) Ideal Customer Profile (ICP)`
- `## 5) Client ↔ Service Expert Dialogue (Deep Discovery)`

Section titles MUST match the strings above to enable reliable validation.

## 3) Metadata Contract (Required Fields)

The `## 1) Report Metadata` section MUST contain these fields:

- `Website: <https://domain.tld>`
- `Domain: <domain.tld>`
- `Generated At (UTC): <YYYY-MM-DDTHH:MM:SSZ>`
- `Report Version: <version-string>`

Rules:

- `Website:` MUST be an absolute `http://` or `https://` URL.
- `Domain:` MUST match the host portion of `Website:` (ignoring `www.`).
- `Generated At (UTC):` MUST be an ISO-8601 UTC timestamp ending with `Z`.
- `Report Version:` MUST be present (for example `v1`).

## 4) Evidence and Inference Markers (Citation-Grade Usefulness)

Business Conspect aims to be the first step toward LLM recommendations and
citations. To support this, claims must be grounded or clearly labeled.

### 4.1 Marker Syntax (Required)

Use the following inline markers:

- Evidence marker: `[evidence: <source>]`
- Inference marker: `[inference: <reason>]`

Examples:

- "The site offers fractional CTO support. [evidence: https://example.com/services]"
- "Pricing likely starts above the market average. [inference: enterprise positioning language on the homepage] [evidence: https://example.com/]"

### 4.2 Marker Rules (Required)

- Non-trivial claims SHOULD include at least one evidence marker.
- Any claim that is not explicitly stated on the site MUST include an inference marker.
- Inference markers SHOULD be paired with at least one evidence marker that explains the basis.
- Evidence sources SHOULD be URLs to the analyzed website. When unavailable, a short source label MAY be used.

These rules are intentionally simple so they can be validated by lightweight scripts.

## 5) Section-Level Content Requirements

### 5.1 Executive Summary

- The summary MUST be present and non-empty.
- The summary SHOULD include at least one evidence marker when it makes specific claims.

### 5.2 Services and Offers

- The section MUST include at least one ordered list item representing a service or offer.
- Each service SHOULD describe what it is, who it is for, and expected outcomes.
- Each service MUST include at least one evidence marker somewhere within its block.

### 5.3 Ideal Customer Profile (ICP)

- The ICP section MUST be present and non-empty.
- The ICP SHOULD be concrete and decision-oriented rather than generic.

### 5.4 Client ↔ Service Expert Dialogue

- The dialogue section MUST contain at least one `Client:` line and one `Expert:` line.
- The dialogue SHOULD cover selection logic, delivery, outcomes, pricing signals, risks, and prerequisites.
- Any speculative expert answer MUST include an inference marker.

## 6) Minimal Authoring Checklist (Testable)

Use this checklist before publishing:

- The report is located at `business-conspect/reports/YYYY-MM-DD/domain.tld/report.md`.
- All required headings are present and spelled exactly as defined.
- Metadata fields `Website`, `Domain`, `Generated At (UTC)`, and `Report Version` are present.
- `Generated At (UTC)` ends with `Z`.
- The Services section includes at least one ordered list item.
- Each service block contains an `[evidence: ...]` marker.
- The dialogue includes both `Client:` and `Expert:` lines.
- Any inference is explicitly labeled with `[inference: ...]`.

## 7) Validator Targets (What Automation Will Enforce)

The future validator is expected to enforce at least the following:

- Required headings exist exactly once.
- Required metadata keys exist and have plausible formats.
- At least one service exists.
- At least one evidence marker exists in the Services section.
- The dialogue section contains both `Client:` and `Expert:` lines.

Stricter checks MAY be added later, but should be introduced with fixtures.

