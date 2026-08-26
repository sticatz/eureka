---
name: idea-mvp
description: This skill should be used when a business idea has all four prior Eureka artifacts complete (CONCEPT, VALIDATION, GTM, FEASIBILITY) and the user wants to scope the smallest concrete test of the core hypothesis — triggered by "what's the MVP for this idea?", "smallest test of this business idea", "how do I test this cheaply?", or an explicit /eureka:idea-mvp. Writes MVP.md. Not for feasibility (idea-feasibility) or verdicts (idea-decide).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Idea MVP — phase 5

What is the smallest thing that tests the riskiest assumption? Not "version one of the product" —
the cheapest experiment whose result changes what you do next.

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; slug from `$ARGUMENTS` or ask. Print the path.

3. **Gate check.** Run `eureka.py status <slug>`. All four priors must be `complete`. Apply Gate A
   to any `killer`, checking `overrides` first. Surface `stale_artifacts` — scoping a build against
   an artifact that describes a superseded idea is the most expensive form of this mistake.

4. Read all four priors: the problem and `stakes` (CONCEPT.md), the demand signal and pain ranking
   (VALIDATION.md), the first channel, price and cold-start approach (GTM.md), the constraints and
   cost structure (FEASIBILITY.md).

5. **Gap scan (rerun only).** Collect gaps where `phase: mvp` and `resolved: false`.

## Rank the assumptions first

Before scoping anything, build the inventory. Collect every `**Assumption:**` marker from all four
priors, plus every unresolved gap and `key_risk`, and score each on two axes:

- **Impact** — `fatal` (the idea does not work if this is false), `damaging`, `survivable`.
- **Confidence** — `evidenced`, `informed`, `hunch`, `none`.

Rank by impact against uncertainty. The top of that list is what the MVP exists to test.

Do this explicitly, with the user, and write it into the artifact. Without it "the single riskiest
assumption" is whichever one springs to mind, and it is entirely possible to scope a beautifully
disciplined MVP that tests the third most important thing.

## Pick the cheapest rung that can falsify it

An MVP is not the only experiment, and it is rarely the first one worth running. Work down this
ladder and stop at the cheapest rung that could actually return a falsifying result:

| Rung | Cost | Falsifies |
|---|---|---|
| Customer interviews | Days, ~free | Whether the problem is real and painful. See `interviewing.md`. |
| Desk research | Hours | Whether the market, the regulation or the incumbent's position is what you assume. |
| Smoke test / landing page | ~£100, 1–2 weeks | Whether the value proposition gets attention and clicks at a plausible CAC. |
| Pre-sale or LOI | 2–4 weeks | Whether anyone will part with money or reputation before the thing exists. The strongest cheap signal. |
| Concierge — deliver it fully manually | 2–4 weeks | Whether the outcome is valuable when the mechanism is a human. |
| Wizard of Oz — looks automated, is not | 3–6 weeks | Whether the interaction model works, without building the engine. |
| Built MVP | 4+ weeks | Whether people use and retain on the real thing. |

Scale the rung to `stakes` from CONCEPT.md. A weekend project does not need a pre-sale; a bet on
savings should not skip one. If the top-ranked assumption can be falsified by a rung above "built
MVP", say so directly — the user may be about to build something a two-week test would have
killed.

Whichever rung is chosen, the eight elements below define it. They are an experiment spec, not a
build spec.

## The eight elements

Drive until each is concrete.

### 1. Core user
The single segment that, if they use it and love it, validates the hypothesis. Reference
VALIDATION.md's pain-severity ranking, not the full target market.

### 2. Core hypothesis
One sentence: *"We believe [user] will [action] because [reason], resulting in [measurable
outcome]."* If this cannot be stated crisply, the priors were too vague — log a gap.

### 3. What's built
The literal features. Which screens, endpoints, workflows. What is the core loop. Cut anything
that does not test the hypothesis.

### 4. What's faked
What looks real but is manual, concierge, wizard-of-oz or hardcoded? Which "features" are humans
in the back? Which integrations are mocked? Faking is good — it buys the same signal for less
build. Name it explicitly so decide can weigh effort accurately.

### 5. Success metric
One primary metric with a number. Not "engagement" but "30% of beta users return within 7 days".
Not "revenue" but "$2,000 MRR within 60 days".

### 6. Kill threshold
The number below which you stop. Set before launch, not after — after launch, you will rationalize
anything. "If fewer than [X] users do [Y] within [Z] days, this hypothesis is wrong."

Pressure-test that it would actually fire. A threshold set so low that any outcome clears it is
decoration.

### 7. Timebox
Build time plus run time, in calendar days, against FEASIBILITY.md's complexity estimate.

### 8. What this does NOT test
Explicitly list what remains unknown afterward. Reference the unresolved assumptions from the
ranking above and every unresolved gap. Note when and how each gets tested later. This prevents the
illusion that a successful test validates everything.

## Depth gaps

MVP scoping exposes weakness in any earlier phase — a hypothesis concept never sharpened, a segment
validation never verified, a channel GTM glossed, a constraint feasibility underpriced. Log per
Gate B, check for duplicates, and continue.

**MVP's verdict is always `proceed`.** It scopes; it does not kill. Anything fundamentally
unworkable belongs in a gap against the phase where the flaw lives — usually feasibility, sometimes
earlier — where decide will weigh it.

## Red flags

| User says | Respond |
|---|---|
| "We need the whole platform first" | "No. What's the one thing that tests whether people care? Everything else is premature." |
| "Users won't take it seriously if it's basic" | "Users won't take it seriously if it doesn't solve their problem. Which features solve it?" |
| "We can't fake that — it won't feel real" | "Can you do it by hand for the first ten? If manual doesn't work, what's the simplest automated version?" |
| "We'll know it when we see it" | "You need a number before launch, not after. What does working look like?" |
| "Let's launch and see what happens" | "See what, specifically? What result would make you stop? Set it now — afterwards you'll rationalize anything." |
| "We need six months" | "That's a product, not a test. What could you ship in four weeks that tests the core assumption?" |
| "Everything is essential" | "Then the hypothesis is too broad. Look at the ranking — what's the top assumption? Test that." |
| "We should just build it and find out" | "Building is the most expensive rung on the ladder. What's the cheapest test that could tell you the same thing?" |

## Staying in scope

| Drift toward | Response |
|---|---|
| Full product roadmap | "This is the test, not v2. What tests the hypothesis? Everything else is later." |
| Revisiting feasibility | "Feasibility is done. If scoping surfaces a new concern I'll log a `feasibility` gap and flag it for decide." |
| Distribution details | "GTM has the channel. The MVP question is what you put in front of those people." |
| Verdict | "Almost — let decide look at this scope and make the call." |

## Phase transition

> "The test is scoped: [what, for whom, testing which assumption, in what timebox, killed at what
> number]. When you're ready, `/eureka:idea-decide` weighs everything to reach a verdict. Want to
> refine the scope, or move to the decision?"

**Never auto-transition.**

## Writing MVP.md

````yaml
---
phase: mvp
status: in-progress
verdict: null
evidence_strength: n/a
key_risks: []
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
covered: []
pending: []
last_question: null
overrides: []
gaps: []
---
````

````markdown
# <Idea Name> — MVP Scope

## Assumption Ranking
## Chosen Experiment
## Core User
## Core Hypothesis
## What's Built
## What's Faked
## Success Metric
## Kill Threshold
## Timebox
## What This Does NOT Test
## Dependencies on Prior Phases
````

`## Assumption Ranking` is required — a table of assumption, source artifact, impact, confidence.
`## Chosen Experiment` names the rung and says why a cheaper one is insufficient.

**On completion:**
- `verdict: proceed` — always.
- `evidence_strength: n/a` — MVP is a proposal, not evidence.
- `key_risks` — what could make the test invalid, and what the test relies on being true.
