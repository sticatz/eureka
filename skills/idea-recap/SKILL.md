---
name: idea-recap
description: This skill should be used when the user wants a summary of a business idea's Eureka artifacts at any stage — triggered by "where are we with [idea]?", "recap this business idea", "summarize my idea", or an explicit /eureka:idea-recap. Read-only; reports the state of CONCEPT, VALIDATION, GTM, FEASIBILITY, MVP and DECISION without modifying them.
argument-hint: "[idea-name]"
allowed-tools: Read, Glob, Grep, Bash
---

# Idea Recap — summary utility

Read-only report on an idea's current state. Modifies nothing.

## On start

1. Load the protocol for artifact names and conventions:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   ```

   If it cannot be read, stop — Eureka is misinstalled.

2. Take the computed state rather than inferring it:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" status <slug>
   ```

   Slug from `$ARGUMENTS`, or ask. Omit it to report on every idea. **Print the absolute root that
   was scanned.**

3. Read the prose of each artifact that exists — the frontmatter gives state, the prose gives the
   findings.

4. If nothing exists: *"No artifacts found for `<slug>` under `<path>`. Nothing to recap."*

## What to output

Keep it to one page. Summarize; do not re-analyze.

### Status

| Phase | Status | Verdict | Evidence | Updated | Risks | Gaps (open / closed) |
|-------|--------|---------|----------|---------|-------|----------------------|

One row per existing artifact, filled from `status`. Mark the Gaps cell with `⚠` when any open
entry is `significant`. CONCEPT.md has no gaps — show `—`.

State the **current phase** and the **next step** from `current_phase` and `next_phase`. These come
from the script, so this report and `idea-start` can never disagree.

Surface prominently, before the findings:

- **Stale artifacts** from `stale_artifacts`, with which earlier phase superseded them. An earlier
  phase was reworked after these were written; anything downstream may describe a different idea.
- **Evidence cap** when `evidence_cap` is set, with the count that triggered it.
- **`go` availability** when the idea is at or near decide: if `go_available` is false, list
  `go_blockers` verbatim. This is the most actionable thing in the report — it says exactly what
  stands between the idea and a green light.

### Key findings per phase

Two or three bullets per artifact, drawn from the prose: the strongest evidence, the biggest
concern, the key tension or open question.

### Tests

From `tests`, one row per experiment: id, method, the assumption it targets, the pre-registered
kill threshold, and the outcome. Mark any still `running` and any `falsified`.

If there are none, say so in one line: *"No assumptions have been tested against the world yet."*
That is the most important thing this report can tell someone about the evidence base.

### Open assumptions

Every entry in `open_assumptions` — the claims that were never evidenced — with the artifact each
came from. Note which have a test against them and which do not.

### Sources

Count the entries under each artifact's `## Sources`. If a phase has researched claims but no
sources section, say so — unsourced research is an assumption wearing a better coat.

### Overrides

Every entry in `overrides`, with the phase overridden, the reason verbatim, and the date. These are
the places the user pushed past a red flag.

### Gaps

Open gaps first: `[<artifact>, <id>, severity=<...>, targets=<phase>] <note>`. Mark entries with
`duplicate_of` as duplicates — they are visible but do not count toward the cap.

Then closed gaps with their `resolved_in` dates. These are loops the user went back and shut, which
is positive signal. Omit the section if there are none.

### Verdict

If DECISION.md is complete: state the verdict prominently and summarize the reasoning in two or
three sentences. For a `park`, show the `revisit_trigger` verbatim and ask whether it has fired —
a park whose trigger is never revisited is just a slow kill.

### Pre-launch checklist — `go` verdicts only

Derive it, do not invent it:

1. From MVP.md — each built item becomes a line; each faked item becomes "Build real: [X]" for
   after the test.
2. From open assumptions the MVP depends on — "Validate: [assumption]".
3. From FEASIBILITY.md legal and compliance risks — "Resolve: [item]".
4. From FEASIBILITY.md technical unknowns — "Spike: [unknown]".
5. From open gaps affecting the MVP — "Address: [severity] [gap]".

If SUMMARY.md exists, point the user at it as the version to share with anyone else.

## Rules

- **Never modify artifacts.** Recap is read-only, including the `gaps` array.
- **Report, don't judge.** No new verdicts, no opinions on whether the idea is good. Surfacing a
  computed `go_blocker` is reporting; arguing about it is not.
- **No tone enforcement.** Recap is a neutral summarizer, not a devil's advocate.
- **Trust `eureka.py`.** Do not recompute gap counts, caps or the current phase by hand.
