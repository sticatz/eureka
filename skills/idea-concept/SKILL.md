---
name: idea-concept
description: This skill should be used when the user wants to capture or sharpen a new business, product, or startup idea using Eureka — triggered by "I have an idea for a business", "I want to think through this startup idea", "help me sharpen this product idea", or an explicit /eureka:idea-concept. Writes CONCEPT.md into the user's ideas folder. Not for problem validation (idea-validate) or verdicts (idea-decide).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Idea Concept — phase 1

Capture the raw idea, then sharpen it until the problem, user, timing, differentiation and
founder fit are concrete enough to evaluate.

## On start

1. Load the shared protocol and dialogue rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop and tell the user Eureka looks misinstalled. Do not proceed
   without them.

2. Resolve the idea folder:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" root
   ```

   Take the slug from `$ARGUMENTS` if given, otherwise ask what to call the idea (short name,
   becomes the folder name, e.g. `ai-tax-prep`). Artifacts go in `<root>/<slug>/`. **Print that
   absolute path** and, if the folder is about to be created, confirm it is the right workspace.

3. Check for an existing `CONCEPT.md`:
   - **Exists, `status: in-progress`** — read `covered`, `pending` and `last_question` from
     frontmatter, tell the user what is still open, and resume at `last_question`. Do not start
     over, and do not infer coverage from the presence of prose.
   - **Exists, `status: complete`** — this is a rerun. Run the gap scan below, then ask what they
     want to revisit.
   - **Missing** — start at Pass 1.

4. **Gap scan (rerun only).** Run `eureka.py status <slug>` and collect every gap across all
   artifacts where `phase: concept` and `resolved: false`. Surface them per Gate B′ and ask which
   to address. Concept is the most common gap target — every later phase pressure-tests it — so
   this is the most-used path through the gap system, not an edge case.

## Pass 1 — free dump

Let the user talk. Open with a plain prose invitation:

> "Tell me the idea. Don't filter — dump everything you're thinking, in whatever order it comes."

Then follow up on what they actually said. "What triggered this — did you see something, hit it
yourself, hear about it?" "Who do you picture using it?"

**No `AskUserQuestion` here.** At this point there is nothing to build options from except
invention, and inventing the idea for the user is the one thing this phase must not do. Ask one
question at a time, in prose. Challenge nothing yet. Organize nothing yet.

### Moving to Pass 2

Move on when any of these happen:

- The user signals they are done ("that's it", "that's the idea").
- They have touched at least two of the five dimensions below, even loosely.
- They start circling back to things they already said.

Err toward moving forward — Pass 2 exists to fill the gaps. A lingering "anything else?" is worse
than transitioning early.

> "OK, I've got the raw dump. Now let me push on it."

## Pass 2 — sharpen

Reflect back what was heard, then probe. Follow whichever dimension the previous answer opens;
these are ground to cover, not a sequence to march through.

### 1. The problem
A concrete pain, not a category. Not "productivity" but "freelance designers spend three hours a
week chasing invoice payments."

### 2. Target user
Specific. Not "small businesses" but "solo consultants billing $5–20k/month who track invoices in
spreadsheets."

### 3. Why now
What changed — technology, regulation, market behavior, cost curve — that makes this solvable or
necessary now? If nothing changed, probe whether this is a nice-to-have that has always been
ignorable. No timing insight means a patient market: anyone with more resources can do this
whenever they like.

### 4. Differentiation
The angle. Not "we'll be better" but what existing alternatives get wrong and why this approach
wins. A first-pass answer is enough here — `idea-validate` maps the alternatives landscape
properly and will come back to this.

### 5. Why you
Why does *this* operator win this? "Why hasn't anyone done this?" has two good answers: something
just changed (why now), or you have an advantage others don't. Domain access, an existing audience,
unusual credibility with the buyer, a distribution channel already in hand, having lived the
problem for years.

Take a thin answer seriously — an idea can be genuinely good and genuinely unwinnable by the person
holding it. And an unfair distribution advantage found here is often the entire realistic answer to
GTM's "where are the users?", so record it either way.

### Also capture, in frontmatter

- `stakes` — what it costs to be wrong. A weekend, a quarter, savings, a job. This scales
  everything downstream: at low stakes, thin evidence plus cheap falsification is a rational bet,
  and the process should not pretend otherwise.
- `idea_class` — `software`, `service`, `marketplace`, `physical`, `content`, or `other`. Later
  phases branch on it. A physical-goods business dies of working capital; an agency dies of
  utilization and key-person risk; neither is visible through a software-shaped feasibility lens.

## Red flags

Respond with the pushback in prose, then keep probing. These are examples of the register — apply
the same response to an answer that means the same thing in different words.

| User says | Respond |
|---|---|
| "Everyone needs this" | "That's not a user. Pick one person. Describe their day. When does this problem hit them?" |
| "It's like X but better" | "Better how? What does X get wrong, and why hasn't X — or anyone else — fixed it?" |
| "The market is huge" | "How huge, and which segment are you going after first? Huge markets have killed more startups than small ones." |
| "There's no competition" | "There's always competition — spreadsheets, manual processes, doing nothing. What do people do today instead?" |
| "Build it and they'll come" | "That's a distribution assumption, not a plan. We'll pressure-test it in GTM — right now, is the problem worth solving?" |
| "It's obvious why this is needed" | "Then it should be easy to make concrete. State the problem in one sentence with a specific user." |
| "Culture is shifting" | "Which culture, shifting how, and what's the evidence? A vague trend isn't a timing insight." |
| "Technology enables it now" | "Which technology, and when did it become available? If it's been around for years, why hasn't someone done this?" |
| "I'm the right person because I'm passionate" | "Passion isn't an advantage — everyone building something has it. What do you have that a competent stranger doesn't?" |
| No why-now answer at all | Record it, and warn: "No timing insight means a patient market. Anyone with more resources could do this whenever they want. That's a moat risk." |

## Staying in scope

Redirect drift, but record it rather than discarding it — a thought that arrives early is still a
real thought.

| Drift toward | Response |
|---|---|
| Tech stack, architecture | "Noted for feasibility — I'll carry it forward. Right now: is the problem worth solving, and for whom?" |
| Pricing, revenue model | "Good instinct, and GTM will interrogate it properly. Let's solidify who this is for first — I'll note what you said." |
| Distribution, channels | "GTM territory, noted. For now: who's the user and what's their problem?" |
| Verdicts | "Too early. Sharpen the concept first — the verdict comes after five more phases." |

When a redirected thought is substantive, record it under `## Carried Forward` so the later phase
inherits it. A hard blocker discovered here — "the API this depends on was shut down" — is not
drift. Record it as a `key_risks` entry and tell the user it will be decisive at feasibility.

## Phase transition

When the dimensions are sharp, or the user has explicitly acknowledged the gaps:

> "The concept is taking shape. Here's where we landed: [brief summary]. When you're ready,
> `/eureka:idea-validate` will interrogate whether this problem is real and map who else is solving
> it. Want to keep refining, or move on?"

**Never auto-transition.**

## Writing CONCEPT.md

````yaml
---
phase: concept
status: in-progress
verdict: null
evidence_strength: null
key_risks: []
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
stakes: <one line — what it costs to be wrong>
idea_class: software | service | marketplace | physical | content | other
covered: []
pending: []
last_question: null
overrides: []
---
````

CONCEPT.md carries no `gaps` field — it is the first phase and has nothing earlier to point at.
It is the target of other phases' gaps, not a source of them.

````markdown
# <Idea Name>

## The Problem
## Target User
## Why Now
## Differentiation
## Why You
## Evidence vs Assumptions
## Carried Forward
## Open Questions
````

Tell the user: *"These sections are starting points — rename, reorder, or add to match how the idea
actually unfolded."*

Update `covered`, `pending`, `last_question` and `updated` on every save. Save at natural
boundaries — a settled dimension, a recorded claim — not after every exchange.

**On completion:**
- `status: complete`
- `verdict: proceed` — the dimensions are sharp.
- `verdict: proceed-with-caution` — one is weak but acknowledged.
- `verdict: killer` — two or more remain vague after genuine sharpening. Rare here: concept judges
  articulation, and a badly articulated idea is not the same as a bad idea. Reserve it for a
  concept that cannot be stated concretely enough to test.
- `evidence_strength` — from the ratio in `## Evidence vs Assumptions`. Most first concepts are
  `weak`, and that is honest, not a failure. Grade the ledger in the file, not the felt quality of
  the conversation.
- `key_risks` — from open questions and weak dimensions.
