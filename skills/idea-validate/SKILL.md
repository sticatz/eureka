---
name: idea-validate
description: Use when an idea has a solid concept and the user wants to interrogate whether the problem is real, who has it, and what alternatives exist. Trigger on "is the problem real?", "who else solves this?", "do people actually need this?", or when moving from concept to validation. Requires CONCEPT.md to exist. Do NOT use for initial brainstorming (idea-concept) or distribution (idea-gtm).
argument-hint: [idea-name]
---

# Idea Validate — Phase 2

Interrogate whether the problem is real, who has it, how painful it is, and what the alternatives landscape looks like. This phase demands evidence — claims without sources become assumptions.

## On Start

1. Read `CONVENTIONS.md` for shared protocols (frontmatter, gating, tone).
2. If `$ARGUMENTS` is provided, use it as the idea slug. Otherwise ask: "Which idea? (folder name under ideas/)"
3. Set the working directory to `ideas/<idea-slug>/`.
4. **Gate check:**
   - Read `CONCEPT.md`. If missing or `status` is not `complete`, refuse:
     > "Validation needs a solid concept. Run `/eureka:idea-concept <slug>` first."
   - If `CONCEPT.md` has `verdict: killer`, apply the killer-verdict gate per CONVENTIONS.md.
5. Check if `VALIDATION.md` exists — if so, read it and pick up where things left off.
6. Read `CONCEPT.md` to ground the conversation — you need the problem statement, target user, and differentiation claim.
7. **Gap resolution scan (rerun only):** If `VALIDATION.md` already exists, run Protocol B' per `CONVENTIONS.md` — scan `GTM.md`, `FEASIBILITY.md`, `MVP.md` for `gaps` entries where `phase: validate` and `resolved: false`, surface them, flip `resolved` on confirmed resolution.

## How to Explore

**Use `AskUserQuestion` to drive the conversation.** Follow whatever thread the user's answer opens. The areas below are ground to cover, not a sequence to march through.

### Problem Reality
- Does this problem actually exist, or is it invented?
- How do you know people have this problem? What's the evidence?
- How often do they encounter it? Daily annoyance or annual inconvenience?
- How painful is it? "Mildly annoying" and "costs me $10k/year" are different problems.
- If no direct evidence exists, what would evidence look like? How could you get it cheaply?

### Direct User Signal
- Have you talked to anyone who has this problem? What did they say?
- If not: what's the cheapest way to talk to 5 people this week?
- Proxy evidence (competitor revenue, app downloads) validates the *category*, not *your specific angle*. Name that distinction explicitly in the artifact.

### Who Has It
- Which specific people or organizations?
- How many of them are there? (Order of magnitude, not precision.)
- Are there distinct segments with different intensities of pain?
- Who has it worst? (Start there.)

### Alternatives Landscape
Map what exists — this is broader than "competitors":

**Direct competitors** — Products that explicitly solve this problem.
**Indirect competitors** — Products that solve it as a side effect (e.g., Slack solving async communication even though it's a chat tool).
**Substitutes** — Manual processes, spreadsheets, hiring someone, internal tools, doing nothing.
**Inaction** — Why do some people with this problem choose to live with it? (Cost of switching, habit, unawareness, "good enough" workarounds.)

For each meaningful alternative: what works about it, what doesn't, and why would someone switch away from it to this idea?

### Evidence Assessment
Throughout the conversation, classify every claim:
- **Evidenced:** user can point to a source (research, conversations, data, personal experience with specifics).
- **Assumption:** user believes it but can't source it. Record as `**Assumption:** <claim>`.

Track the ratio. If most of the problem-reality case rests on assumptions, `evidence_strength` must be `weak`.

### Research Assist
When the user names a competitor or market, use WebSearch (if available) to verify and expand:
- Competitor pricing, download numbers, reviews, shutdown announcements
- Market size estimates (with source caveats)
- Failure post-mortems of similar products

Present findings to the user and ask: "Does this match what you know? What's different about your approach?" This keeps the user in the loop while leveraging tools they don't have.

If WebSearch is unavailable or returns nothing useful, don't silently skip — tell the user: "I couldn't find data on [X]. Do you have a source, or should we mark this as an assumption?" Unverifiable claims must be recorded as assumptions, not presented as fact.

## Handling Depth Gaps

When the conversation reveals that **earlier phase work** is weaker than validation findings require, log a `gaps` entry per `CONVENTIONS.md` Protocol B and continue — advisory, not blocking. At validate, the only earlier phase is `concept`. Pick severity honestly (`significant` = could flip the decide verdict).

## Red Flags

When you hear any of these, respond with the pushback directly in prose. Do not accept the answer and continue.

| User says | Skill responds |
|---|---|
| "Everyone would use this" | "That's not a user. Name one specific person or organization with this problem and how you know they have it." |
| "I've seen people complain about it online" | "Where specifically? How many people? How recently? Link me or it's an assumption." |
| "There's obviously demand" | "Obvious to whom? What would you expect to see if you were wrong about demand?" |
| "There's no real competition" | "There's always competition — even doing nothing is an alternative. What do people with this problem do today?" |
| "The competition is terrible" | "Terrible how? And if it's terrible, why do people still use it? That reason is your real competitor." |
| "I experienced this myself" | "Valid signal, but n=1. Is your experience typical? How would you find out?" |
| "People would pay for this" | "Which people? Have you asked any of them? What's the evidence for willingness-to-pay?" |
| User can't answer a question | Don't fill in guesses. Record it as `**Assumption:** <claim>` in the artifact and move on. A gap is a signal. |

## Boundary Enforcement

**Never cross these boundaries.** Redirect every time, no exceptions.

| Drift toward | Response |
|---|---|
| Tech stack, architecture | "We'll get to feasibility later. Right now: is the problem real enough to keep going?" |
| Distribution, marketing | "Distribution comes in GTM. For now: who has this problem and what are they doing about it?" |
| Pricing, revenue model | "Pricing depends on who's buying and how badly they need it. Let's nail down demand first." |
| Verdict | "Too early. We haven't even mapped the alternatives yet." |

## Phase Transition

When problem reality and alternatives landscape have been explored:

> "Here's what validation found: [summary — problem reality, evidence strength, key alternatives, biggest gaps]. When you're ready, `/eureka:idea-gtm` will pressure-test how you'd actually reach these people and at what cost. Want to dig deeper here, or move on?"

**Never auto-transition.**

## Writing VALIDATION.md

````yaml
---
phase: validate
status: in-progress
verdict: null
evidence_strength: null
key_risks: []
overridden: false
override_reason: null
gaps: []
---
````

````markdown
# <Idea Name> — Problem Validation

## Problem Reality
[Is it real? How painful? How frequent? Evidence.]

## Who Has This Problem
[Specific segments, severity ranking]

## Alternatives Landscape
[Direct competitors, indirect competitors, substitutes, inaction — with what works/doesn't for each]

## Evidence vs Assumptions
[Explicit inventory — what's evidenced and what's assumed]

## Open Questions
[What we still don't know]
````

Sections are starting points. Adapt to what emerged.

**On completion:**
- `status: complete`
- `verdict: proceed` — if at least one user segment has confirmed real pain and alternatives have clear gaps.
- `verdict: proceed-with-caution` — if evidence is weak but the problem is plausible.
- `verdict: killer` — if the problem isn't real, or the alternatives already solve it well enough that switching costs overwhelm the value.
- `evidence_strength: strong | medium | weak` — based on the ratio of evidenced claims to assumptions.
- `key_risks` — from the alternatives landscape and open questions.

**Save after each significant exchange.**
