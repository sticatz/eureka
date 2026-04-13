---
name: idea-recap
description: Use when the user wants a summary of any idea at any stage — "where are we with X?", "summarize this idea", "what's the status?", "recap", or when idea-start routes here. Read-only utility that never modifies artifacts. Invokable at any point in the workflow.
argument-hint: [idea-name]
---

# Idea Recap — Summary Utility

Read-only summary of any idea's current state. Never modifies artifacts.

## On Start

1. Read `CONVENTIONS.md` for shared conventions (artifact filenames, slug convention).
2. If `$ARGUMENTS` is provided, use it as the idea slug. Otherwise ask: "Which idea? (folder name under ideas/)"
3. Set the working directory to `ideas/<idea-slug>/`.
4. Read every artifact that exists in the folder: CONCEPT.md, VALIDATION.md, GTM.md, FEASIBILITY.md, MVP.md, DECISION.md.
5. If no artifacts exist: "No artifacts found for `<slug>`. Nothing to recap."

## What to Output

### Status Overview

| Phase | Status | Verdict | Evidence | Risks | Overrides | Gaps (unresolved / resolved) |
|-------|--------|---------|----------|-------|-----------|------|

One row per artifact that exists. Fill from frontmatter. For the Gaps column, show `<unresolved-count> / <resolved-count>` with a `⚠` suffix if any unresolved entry has `severity: significant`. CONCEPT.md has no gaps field — show `—` for that row.

**Current phase:** the latest artifact with `status: in-progress`, or if all complete, state "all phases complete."

**Next step:** based on state, suggest the next skill to invoke (or "verdict reached" if DECISION.md exists with `status: complete`).

### Key Findings Per Phase

For each existing artifact, extract 2-3 bullet points capturing the most important findings from the prose. Focus on:
- Strongest argument or evidence
- Biggest risk or concern
- Key tension or open question

### Open Assumptions

Scan all artifacts for `**Assumption:**` markers. List them all. These are claims that were never evidenced.

### Overrides Taken

List every artifact where `overridden: true`, with the `override_reason`. These are places where the user pushed past a killer verdict.

### Unresolved Gaps

For each artifact with a `gaps` array, list every entry where `resolved: false`. Format: `[<source-artifact>, severity=<minor|significant>, phase=<target-phase>] <note>`. CONCEPT.md has no gaps field — skip it.

Count `significant` unresolved gaps and surface the count prominently. If the count is 2+, add a line: "Per Gating Protocol B, this will cap idea-decide's evidence_strength at `medium` (2 significant) or `weak` (3+)."

### Resolved Gaps

For each artifact with a `gaps` array, list every entry where `resolved: true`, showing `resolved_in` date. These are gaps the user went back and closed — positive signal. If none, omit this section.

### Verdict (if decided)

If DECISION.md exists with `status: complete`:
- State the verdict prominently.
- Summarize the reasoning in 2-3 sentences.

### Pre-Launch Checklist (go verdict only)

If `verdict: go` in DECISION.md, generate a checklist:

1. **From MVP.md:** What needs to be built vs faked. Each built item becomes a checklist line.
2. **From open assumptions:** Each unresolved assumption that the MVP depends on → "Validate: [assumption]"
3. **From FEASIBILITY.md risks:** Any legal/compliance items → "Resolve: [item]"
4. **From FEASIBILITY.md risks:** Any technical unknowns → "Spike: [unknown]"
5. **From GTM.md:** Faked components from MVP that need real versions for growth → "Build real: [component]"
6. **From gaps:** Any `resolved: false` gap entry that affects the MVP → "Address: [severity] [gap]"

The checklist is derived, not manually maintained. It surfaces everything that needs attention before or shortly after launch.

## Rules

- **Never modify artifacts.** Recap is read-only.
- **Never offer opinions or verdicts.** Recap reports, it does not analyze.
- **No tone enforcement.** Recap is a neutral summarizer, not a devil's advocate.
- **Keep it to one page.** Summarize, don't re-analyze.
