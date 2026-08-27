---
name: idea-validate
description: This skill should be used when a business idea already has a Eureka CONCEPT.md and the user wants to interrogate whether the problem is real, who has it, and what alternatives exist — triggered by "is this problem real?", "does anyone actually need this?", "who else solves this?", or an explicit /eureka:idea-validate. Writes VALIDATION.md. Requires CONCEPT.md. Not for initial capture (idea-concept) or distribution (idea-gtm).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Idea Validate — phase 2

Is the problem real, who has it, how badly, and what do they do about it today? This phase demands
evidence. Claims without sources become assumptions, and the ratio decides whether a `go` verdict
stays available at all.

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; take the slug from `$ARGUMENTS` or ask. Print the
   absolute path.

3. **Gate check.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" status <slug>`.
   - CONCEPT.md missing or not `complete` → refuse: *"Validation needs a solid concept. Run
     `/eureka:idea-concept <slug>` first."*
   - CONCEPT.md has `verdict: killer` → apply Gate A. Check `overrides` first: if this killer is
     already overridden, carry it forward in one line rather than re-asking.
   - `stale_artifacts` non-empty → surface it before starting.

4. Read CONCEPT.md for the problem statement, target user, differentiation claim, `stakes` and
   `idea_class`. Scale the depth of this phase to `stakes` — a weekend project does not need the
   same evidentiary bar as a bet on savings, and pretending otherwise makes the process irrational
   for small ideas.

5. **Gap scan (rerun only).** Collect gaps across all artifacts where `phase: validate` and
   `resolved: false`, surface them per Gate B′, and ask which to close.

## How to explore

Ask in prose, one question at a time. These are areas to cover, not a sequence.

### Problem reality
- Does this problem exist, or was it invented backwards from a solution?
- How does the user know people have it? What is the evidence?
- How often does it hit — daily annoyance or annual inconvenience?
- What does it cost when it does? "Mildly irritating" and "$10k/year" are different problems.
- If no direct evidence exists: what would evidence look like, and what is the cheapest way to get
  it this week?

### Direct user signal
Have they talked to anyone who has this problem? What exactly was said?

**Before they go and talk to people, and before recording anything they bring back, load:**

```bash
cat "${CLAUDE_PLUGIN_ROOT}/references/interviewing.md"
```

That file carries the question rewrites, the recruiting playbook, and the admission rubric that
decides whether a datum enters as evidence or as an assumption. Use it. Five friends saying "that
sounds great, I'd use it" is the single most common way a weak idea acquires a strong evidence
score, and the rubric exists to stop exactly that.

Proxy evidence — competitor revenue, download counts, funding — validates the *category*, never
this specific angle. Say so explicitly in the artifact whenever it is used.

### Who has it
- Which specific people or organizations?
- How many, to an order of magnitude?
- Are there distinct segments with different pain intensity?
- Who has it worst? Start there.

### Alternatives landscape
Broader than "competitors":

- **Direct competitors** — products that explicitly solve this.
- **Indirect competitors** — products that solve it as a side effect.
- **Substitutes** — spreadsheets, manual process, hiring someone, an internal tool.
- **Inaction** — why do some people with this problem simply live with it? Switching cost, habit,
  unawareness, a good-enough workaround.

For each meaningful alternative: what works, what does not, and why anyone would switch. The
inaction quadrant is usually where the idea actually dies — take it as seriously as the named
competitors.

This is also where the concept's differentiation claim gets its real test. If the landscape
contradicts it, that is a `concept` gap.

### Research
Before recording any unknown as a risk or an assumption, load and follow:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/references/research.md"
```

Competitor pricing, review sites, shutdown notices, post-mortems of similar products, countable
segment populations. Present findings and ask whether they match what the user knows — do not
silently overwrite their belief. If search finds nothing useful, say so out loud and record the
claim as an assumption rather than skipping quietly.

### Evidence assessment
Classify every claim as evidenced or `**Assumption:** <claim>` as it arrives, into the artifact's
`## Evidence vs Assumptions` section. Record researched claims in `## Sources` with URL, publisher,
source date and retrieval date. Track the ratio — it sets `evidence_strength`, and
`evidence_strength` at `weak` here removes `go` from the table at decide.

## Depth gaps

At validate the only earlier phase is `concept`. Log a `gaps` entry per Gate B and continue —
advisory, not blocking. Check for an existing duplicate first and set `duplicate_of` if the
weakness is already recorded.

## Red flags

| User says | Respond |
|---|---|
| "Everyone would use this" | "That's not a user. Name one specific person or organization with this problem, and how you know they have it." |
| "I've seen people complain online" | "Where, how many, how recently? Link me, or it's an assumption." |
| "There's obviously demand" | "Obvious to whom? What would you expect to see if you were wrong about demand?" |
| "There's no real competition" | "There's always competition — doing nothing is an alternative. What do people with this problem do today?" |
| "The competition is terrible" | "Terrible how? And if it's terrible, why do people still use it? That reason is your real competitor." |
| "I experienced this myself" | "Valid signal, but n=1. Is your experience typical? How would you find out?" |
| "People would pay for this" | "Which people? Have you asked any of them? What's the evidence for willingness to pay?" |
| "Everyone I showed it to loved it" | "Did you pitch before or after you asked about their problem? Praise after a pitch is politeness, not demand — let's run what you heard through the admission rubric." |

## Staying in scope

| Drift toward | Response |
|---|---|
| Tech stack, architecture | "Feasibility territory — I'll note it. Right now: is the problem real enough to keep going?" |
| Distribution, marketing | "GTM comes next. For now: who has this problem and what are they doing about it?" |
| Pricing deep-dive | "GTM interrogates pricing properly. Rough willingness-to-pay signals are useful here though — what have they paid for adjacent things?" |
| Verdict | "Too early. We haven't mapped the alternatives yet." |

## Phase transition

> "Here's what validation found: [problem reality, evidence strength, key alternatives, biggest
> gaps]. When you're ready, `/eureka:idea-gtm` pressure-tests how you'd reach these people, what it
> costs, and what you charge. Want to dig deeper here, or move on?"

**Never auto-transition.**

## Writing VALIDATION.md

````yaml
---
phase: validate
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
gaps: []
---
````

````markdown
# <Idea Name> — Problem Validation

## Problem Reality
## Who Has This Problem
## Alternatives Landscape
## Evidence vs Assumptions
## Sources
## Open Questions
````

`## Evidence vs Assumptions` and `## Sources` are required, not scaffolding. The rest are starting
points — tell the user they can rename, reorder or add.

Update `covered`, `pending`, `last_question` and `updated` on every save.

**On completion:**
- `verdict: proceed` — at least one segment has confirmed real pain, and the alternatives leave a
  gap worth entering.
- `verdict: proceed-with-caution` — the problem is plausible but the evidence is thin.
- `verdict: killer` — the problem is not real, or the alternatives solve it well enough that
  switching costs overwhelm the value.
- `evidence_strength` — from the ratio in `## Evidence vs Assumptions`, counting only claims that
  passed the admission rubric. This field is load-bearing: `weak` here removes `go` from the table
  at decide. Grade the ledger, not the conversation.
- `key_risks` — from the alternatives landscape and open questions.
