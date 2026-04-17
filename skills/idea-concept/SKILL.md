---
name: idea-concept
description: Use when the user wants to capture, explore, or refine a new business/product idea. Trigger on "I have an idea for...", "what if we built...", "is this problem worth solving?", or any early-stage idea exploration. Do NOT use for problem validation (idea-validate) or final verdicts (idea-decide).
argument-hint: [idea-name]
---

# Idea Concept — Phase 1

Capture and refine an idea until the problem, target user, why-now, and differentiation are sharp enough to evaluate.

## On Start

1. Read `CONVENTIONS.md` for shared protocols (frontmatter schema, tone contract, gating rules).
2. If `$ARGUMENTS` is provided, use it as the idea slug. Otherwise ask: "What should we call this idea? (short name — becomes the folder name, e.g., `ai-tax-prep`)"
3. Set the working directory to `ideas/<idea-slug>/`.
4. Check if `CONCEPT.md` exists:
   - **Exists:** Read it. If `status: in-progress`, pick up where things left off. Do NOT start over. If `status: complete`, tell the user and suggest the next phase.
   - **Does not exist:** Create the directory if needed. Start fresh with Pass 1.

## Pass 1 — Free Dump

Let the user talk. Use `AskUserQuestion` to draw out the full picture without judgment or structure:

- "Tell me the idea. Don't filter — just dump everything you're thinking."
- "What triggered this? Did you see something, experience something, hear about something?"
- "Who do you imagine using this?"

Ask one question at a time. Do NOT challenge anything yet. Do NOT organize into sections. The goal is to get the unfiltered thought out of the user's head.

### When to transition to Pass 2

Move to Pass 2 when any of these happen:
- **Explicit signal:** The user says they're done ("that's it", "that's the idea", "I think that covers it").
- **Coverage signal:** The user has touched at least 2 of the 4 dimensions (problem, user, why-now, differentiation) even loosely — there's enough raw material to start sharpening. Pass 2 fills the gaps; Pass 1 doesn't need to be exhaustive.
- **Repetition signal:** The user is circling back to things they already said.

Err toward moving forward. A lingering dump phase ("anything else?") is worse than transitioning with gaps — that's what Pass 2 is for.

Transition line: "OK, I've got the raw dump. Now let me push on it."

## Pass 2 — Sharpen

Reflect back what you heard, then use `AskUserQuestion` to systematically probe four dimensions. Each must be sharp before this phase can complete.

Ask about whichever dimension the previous answer naturally leads to. Follow the thread — don't march through a checklist.

Ground to cover (in whatever order fits the conversation):

### 1. The Problem
What specific problem does this solve? Not a category ("productivity") but a concrete pain ("freelance designers spend 3 hours/week chasing invoice payments").

### 2. Target User
Who has this problem? Be specific — not "small businesses" but "solo consultants billing $5k-20k/month who currently track invoices in spreadsheets."

### 3. Why Now
Why is this the right time? What changed — technology, regulation, market behavior, cultural shift — that makes this solvable or necessary now? If nothing changed, probe whether this is a "nice to have" that's always been ignorable.

### 4. Differentiation
What's the insight or angle? Not "we'll be better" but specifically how and why. What do existing alternatives get wrong, and why will this approach win?

**Challenge weak answers procedurally.** When a user's answer matches a Red Flag below, respond with the specific pushback via `AskUserQuestion`. Do not accept the answer and move on.

**Do NOT force answers.** If the user genuinely can't answer, that's a signal worth noting as an open question — not a blank to fill with guesses. Move to the next thread.

## Red Flags

When you hear any of these, respond with the pushback directly in prose. Do not accept the answer and continue.

| User says | Skill responds |
|---|---|
| "Everyone needs this" | "That's not a user. Pick one person. Describe their day. When does this problem hit them?" |
| "It's like X but better" | "Better how? What does X get wrong, and why hasn't X (or anyone else) fixed it?" |
| "The market is huge" | "How huge? Which segment are you actually going after first? 'Huge market' has killed more startups than small markets." |
| "There's no competition" | "There's always competition — even if it's spreadsheets, manual processes, or doing nothing. What do people do today instead?" |
| "We just need to build it and they'll come" | "That's a distribution assumption, not a plan. But we'll get to distribution later — right now, is the problem worth solving?" |
| "It's obvious why this is needed" | "If it's obvious, make it concrete. State the problem in one sentence with a specific user." |
| "Culture is shifting" / "Society is changing" | "Which culture, shifting how, and what's the evidence? A vague trend isn't a timing insight." |
| "Technology enables it now" | "Which technology? When did it become available? If it's been available for years, why hasn't someone done this already?" |
| No why-now answer at all | Record as a gap, but explicitly warn: "No timing insight means a patient market — anyone with more resources could do this whenever they want. That's a moat risk." |
| User can't answer a question | Don't fill in guesses. Note it as an open question in the artifact and move to the next thread. A gap is a signal, not a failure. |

## Boundary Enforcement

**Never cross these boundaries.** If the conversation drifts toward ANY of these, redirect immediately:

| Drift toward | Response |
|---|---|
| Tech stack, architecture, "how would we build this" | "Noted — we'll get to that in feasibility. Right now: is the problem worth solving, and for whom?" |
| Pricing, revenue, monetization | "Good instinct, but let's solidify who this is for before talking money. That comes in GTM and feasibility." |
| Verdicts ("should we build this?") | "Too early. Sharpen the concept first — the verdict comes after 5 more phases of thinking." |
| Distribution, marketing, channels | "We'll pressure-test distribution in GTM. For now: who's the user and what's their problem?" |

This applies even if the user initiates it. Redirect every time, no exceptions.

## Phase Transition

When all four dimensions (problem, user, why-now, differentiation) are sharp — or the user has explicitly acknowledged gaps:

> "The concept is taking shape. Here's where we landed: [brief summary of the four dimensions]. When you're ready, `/eureka:idea-validate` will interrogate whether this problem is real and map who else is solving it. Want to keep refining, or move on?"

**Never auto-transition.** Always wait for the user's go-ahead.

## Writing CONCEPT.md

When writing or updating, use this scaffolding — but adapt sections to what actually emerged:

````yaml
---
phase: concept
status: in-progress
verdict: null
evidence_strength: null
key_risks: []
overridden: false
override_reason: null
---
````

Note: CONCEPT.md omits the `gaps` field (first phase — no prior work to point at). All downstream phase artifacts include it per CONVENTIONS.md.

````markdown
# <Idea Name>

## The Problem
[Specific problem statement]

## Target User
[Who — specific, not generic]

## Why Now
[Timing insight — what changed]

## Differentiation
[The angle — what existing alternatives get wrong]

## Open Questions
[Anything unresolved]
````

Sections are starting points. Rename, reorder, or add sections to match how the idea actually unfolded.

**Updating status and verdict on completion:**
- `status: complete`
- `verdict: proceed` — if problem, user, why-now, and differentiation are all sharp.
- `verdict: proceed-with-caution` — if one dimension is weak but acknowledged.
- `verdict: killer` — if two or more dimensions remain vague after sharpening. (Rare at concept stage, but possible.)
- Set `evidence_strength` based on how many claims are evidenced vs assumed.
- Set `key_risks` from open questions and weak dimensions.

**Save the file after each significant exchange** — don't wait for the phase to complete. Write what you have, update as the conversation progresses.
