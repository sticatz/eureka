---
name: idea-decide
description: This skill should be used when a business idea has all five prior Eureka artifacts complete and the user wants the terminal verdict — triggered by "should I build this idea?", "go or kill on this business idea?", "is this idea worth pursuing?", or an explicit /eureka:idea-decide. Writes DECISION.md and SUMMARY.md. Requires CONCEPT, VALIDATION, GTM, FEASIBILITY and MVP all complete. Not for MVP scoping (idea-mvp).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Agent, AskUserQuestion
---

# Idea Decide — phase 6: the verdict

Synthesize everything into **go**, **park** or **kill**. Every prior phase exists to serve this.

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; slug from `$ARGUMENTS` or ask. Print the path.

3. **Gate C — hard gate, no override.** Run `eureka.py status <slug>` and read `decide_ready`. If
   false:

   > "Can't reach a verdict without the homework. Missing or incomplete: [list with status]. Run
   > the earlier phases first."

   There is no override. Deciding without the analysis defeats the purpose.

4. Read all five artifacts in full, and take the computed state from `status` rather than
   recomputing it: per-phase `verdict` and `evidence_strength`, every `overrides` entry,
   every gap split by resolved and severity, `evidence_cap`, `stale_artifacts`, `go_available` and
   `go_blockers`.

   If `stale_artifacts` is non-empty, say so before anything else. Synthesizing a confident verdict
   across artifacts that describe two different versions of the idea is the worst failure available
   here.

## Step 1 — evidence inventory

Lay out the foundation before arguing either side. Per phase: verdict, evidence strength, gaps
logged (with id, target phase, severity, resolved), key risks. Plus the override records and what
each one was for. Present it straight — do not spin it.

## Step 2 — dispatch the red team

**Before writing the case against**, dispatch the `idea-red-team` subagent with the absolute path
to the idea folder.

It reads the artifacts and never sees this conversation. That is the point: by now this session has
spent many turns helping the user articulate their idea and writing the artifacts in its own voice,
and every pressure available — rapport, consistency with what it already wrote, ordinary politeness
— points toward a generous reading. A critique from something that was not in the room is the only
structural fix for that.

Its output is an input, not a draft to edit:

- Its `FATAL` and `SERIOUS` findings enter Step 3 **verbatim**. Do not soften, requalify, or
  paraphrase them into something gentler. If one is wrong, rebut it explicitly with evidence from
  the artifacts and show the rebuttal — do not quietly drop it.
- Its `EVIDENCE_STRENGTH` is an independent grade of the same files. **Take the lower of that and
  the one derived from the phase artifacts.**
- Its `NEVER ASKED` list names dimensions the six phases did not interrogate at all. Those are
  usually the most valuable lines in the whole report.

If the subagent is unavailable, say so explicitly in DECISION.md rather than skipping silently —
a decision made without the adversarial pass is a weaker decision and the record should show it.

## Step 3 — steel-man both sides

**The case FOR.** The strongest arguments across all five phases. What makes this worth building?
What is the upside if the MVP succeeds? Cite specific findings: "validation found X, GTM identified
[channel] at [CAC] against a price of [Y], feasibility confirmed Z."

**The case AGAINST.** The strongest counterarguments, including the red team's findings verbatim.
Every killer verdict, even overridden ones. Every weak evidence assessment. Every unresolved gap.
Every key risk.

Plus, explicitly:

- **Moat.** Is this defensible over time — network effects, data, switching costs, brand,
  community, regulatory position, distribution already held? If there is no moat, say so. A viable
  business with no defensibility is a real outcome but a different risk profile.
- **Monetization.** Did any phase establish what is charged, to whom, per what unit, and why they
  pay it? If GTM did not settle this, the idea has no revenue model and that belongs here.
- **Why this operator.** Does anything establish why this user wins this? An idea can be good and
  unwinnable by the person holding it.

**Do not soften this.** If the idea should die, say so plainly.

## Step 4 — weigh overrides and gaps

**Overrides.** Judge each reason on its merits. "The hypothesis is cheap to test, worst case two
weeks" is a rational gamble. "Gut feeling" is a flag. Note that one override recorded once covers
one killer verdict — count distinct overrides, not the number of phases that inherited them.

**Gaps.** Read `evidence_cap` from `status`; it already excludes duplicates. Two unresolved
significant gaps cap evidence at `medium`, three or more at `weak`. Name the cap when it applies.
Resolved gaps are positive signal — the user went back and closed a loop rather than waving it away
— and should be said out loud.

**Stakes.** Read `stakes` from CONCEPT.md. The bar scales: at low stakes, thin evidence plus a
cheap falsifying test is a rational `go`, and treating a weekend project like a funded bet is its
own kind of wrong answer. At high stakes the reverse. Say which regime this is in.

## Step 5 — the verdict

Read `go_available` and `go_blockers` from `status`. **Where `go_available` is false, `go` is not
on the table** — the blockers name why, and every one of them is either weak evidence in a
load-bearing phase or an unaddressed killer. This is a floor, not a formula: a clean
`go_available: true` does not oblige a `go`, it only means the reasoning below governs.

**Go** — summarize the MVP scope, give concrete next steps, name what could still derail it.

**Park** — name a concrete `revisit_trigger`: an event or a specific obtainable fact, never a
calendar date. "If you can get three of the five interviewees to pre-pay, revisit." Where the
blockers were evidence gaps, those gaps *are* the trigger. For pivot-style parks: which insight is
valid, what to sharpen, which phase to restart from.

**Kill** — name the fatal flaw directly. What would have to be structurally different, not "try
harder". What is salvageable.

**Own the recommendation.** "It depends on your risk tolerance" and "only you can decide" are
banned. Have an opinion and defend it.

## Step 6 — the user decides

Present it and wait. The user has the final word. If they disagree, ask them to articulate why,
capture the reasoning in DECISION.md, and let their decision stand — with the analysis on record
beside it.

## Red flags

| User says | Respond |
|---|---|
| "Let's just go for it" | "Which specific finding makes you confident? The analysis surfaced [risks] — have you thought those through?" |
| "I don't care about the risks" | "The risks don't care either. Which have you thought through, and which are you choosing to accept?" |
| "It feels right" | "Gut is data, but what evidence supports the feeling? The analysis says [X]." |
| "Let's park it" (as avoidance) | "Park needs a concrete trigger — what event or fact brings you back? Otherwise this is a comfortable kill, and a real kill is more useful." |
| "Kill it" (without engaging) | "Which finding drove that? The case for had [X]. Are you sure the analysis doesn't support proceeding?" |
| "Can we do a smaller version?" | "That's what MVP.md scopes. Does the scope work, or do you want to revise it?" |
| "The red team is being unfair" | "Take one finding and rebut it from the artifacts. If the evidence is there, I'll record the rebuttal — if it isn't, that's the finding." |

## Writing DECISION.md

````yaml
---
phase: decide
status: in-progress
verdict: null
evidence_strength: null
key_risks: []
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
covered: []
pending: []
last_question: null
overrides: []
revisit_trigger: null
---
````

````markdown
# <Idea Name> — Decision

## Verdict
## Evidence Inventory
## The Case For
## The Case Against
## Red Team Findings
## Override and Gap Analysis
## Reasoning
## What Would Change This
## Next Steps
````

`## Red Team Findings` carries the subagent's output as received, plus any rebuttal with its
evidence. It is a record of what the adversarial pass said, not a summary of it.

**On completion:**
- `verdict: go | park | kill`
- `evidence_strength` — the lower of the phase-derived grade and the red team's, respecting
  `evidence_cap`.
- `revisit_trigger` — required when the verdict is `park`.
- `key_risks` — the top risks regardless of verdict.

## Then write SUMMARY.md

DECISION.md is written for the machine — it is full of `proceed-with-caution`, `evidence_cap` and
gap severities, and a cofounder reading it learns about Gating Protocol B. Write a second file
alongside it, in plain language, with none of Eureka's internal vocabulary:

````markdown
# <Idea Name>

**Verdict:** <go | park | kill>, <date>

## The idea
<Two sentences. Problem, user, approach.>

## What we know
<The evidenced claims, each with its source and the source's date.>

## What we're assuming
<The load-bearing assumptions, ranked, with what it would take to check each.>

## The three biggest risks
## The test
<From MVP.md, in five lines: what gets built, what gets faked, what number means it worked,
what number means it stops, how long.>

## What would change the answer
````

This is the artifact that gets sent to a cofounder, shown to an advisor, or read by the user in six
months. Every claim in it carries its source and date, because a claim whose provenance is lost is
not something anyone can act on later.
