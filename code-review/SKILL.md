---
name: code-review
description: Review GitHub pull requests and code diffs against repository coding standards and originating issue specifications, with evidence-backed merge readiness decisions. Use when asked for a code review, PR review, or review of changes since a commit or branch.
---

# Code Review

Review two independent axes without letting one mask the other:

1. **Standards:** Check documented repository conventions (including CONTRIBUTING.md, AGENTS.md, design and testing docs) and meaningful maintainability risks. Treat code smells as judgment calls, not automatic violations.
2. **Spec:** Read the originating issue, acceptance criteria, relevant past reviews, and diff. Identify missing requirements, wrong behavior, unintended scope, and regression tests.

For a PR, use its target branch as the fixed point, inspect its current head, diff, linked issues, prior requested changes, review threads and checks. Prefer review evidence from the current commit. Verify reports of successful tests; do not claim to have executed tests unless you did.

## Vercel team-membership exception (Favor review policy, 2026-11-20)

**Vercel deployment or status-check failures caused solely by the PR author not being a member of the Vercel team are NOT merge blockers.** Do not demand a passing Vercel preview to clear this access-related failure, even if repository contribution guidelines ordinarily require it. In the review, label it `non-blocking: Vercel team membership` and judge merge readiness based on code/spec correctness and whatever valid build/test evidence is available.

Distinguish carefully:
- **Confirmed membership/authorization failure:** Non-blocking. Do not mark the PR changes-requested for this alone.
- **Confirmed real compilation, TypeScript, test, runtime, or build failure:** Evaluate as a genuine potential blocker.
- **Generic failed Vercel status without a confirmed cause:** State `failure cause unverified`; do not assume it was caused by code or by membership, and do not make the status alone a blocker. Seek logs or alternative build evidence and report any verification gap.

Do not change team permissions or deploy merely to bypass this policy. Never imply a passing preview when none exists.

## Output

Report separate **Standards** and **Spec** findings with exact paths/lines and severity. Distinguish confirmed bugs from uncertainties. Finish with a review verdict and explicit statement of remaining genuine blockers and unverified checks. Never approve, merge, or post a GitHub review unless asked.
