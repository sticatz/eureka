# Eureka

A set of 8 Claude Code skills (7 workflow + 1 utility) that guide any user through maturing a business idea from raw thought to a clear go/no-go verdict. Skills are opinionated, brutal-honesty, and produce persistent per-idea artifacts.

## Purpose

Most "idea" tools are brainstorming pads — they help you think *about* an idea but never help you decide whether to *build* it. The incubator's single job is to produce a defensible verdict: **build, shelve, kill, or pivot.** Every skill exists to serve that terminal decision.

## Target User

Anyone with an idea — from hobbyists to PMs to founders. The system adapts its depth to the user's answers but never its rigor.

## Scope

Any business idea: products, services, agencies, marketplaces, content businesses, SaaS, physical goods. The evaluation frameworks flex; the workflow does not.

Out of scope: post-decision build tracking, team coordination, funding/pitch decks.

## Architecture

### Workflow

Linear with explicit back-arrows:

```
idea-start
   │
   ▼
idea-concept ──► idea-validate ──► idea-gtm ──► idea-feasibility ──► idea-mvp ──► idea-decide
                      │                │                 │               │            │
                      └────────────────┴─────────────────┴───────────────┴────────────┘
                                  (back-arrows: any phase can refuse + send user
                                   back to a specific earlier phase via soft gate)
```

GTM precedes feasibility because distribution kills more business ideas than technology does. Feasibility is then judged against the concrete channel/volume shape gtm produces. MVP sits last-but-one so it has all four thinking phases feeding it; decide judges a specific concrete proposal, not an abstraction.

### Persistence

Per-idea folder under `ideas/`:

```
ideas/
  <idea-slug>/
    CONCEPT.md
    VALIDATION.md
    GTM.md
    FEASIBILITY.md
    MVP.md
    DECISION.md
```

All artifacts are git-trackable markdown. The folder is the idea's complete record.

### Artifact Shape

Every artifact is **YAML frontmatter + freeform prose**:

```markdown
---
phase: validate
status: complete
verdict: proceed-with-caution
key_risks: [cold-start, low-willingness-to-pay]
evidence_strength: weak
overridden: false
override_reason: null
---

# Problem Validation — <idea name>

<freeform narrative written collaboratively by skill + user>
```

Skills read frontmatter to detect state and route. The prose body carries the actual thinking. No rigid templates — real critique doesn't fit predefined H2 sections.

### Tone: Brutal Honesty

All thinking skills default to **devil's advocate**. They:

- Refuse weak or vague answers and push for sharper ones.
- Demand evidence for claims. No evidence = claim marked as assumption.
- Actively attack lazy reasoning; surface uncomfortable truths.
- Never editorialize toward encouragement. The user's idea is not precious to the skill.

Brutal ≠ mean. Skills are direct, evidence-demanding, and respectful simultaneously.

### Gating: Soft Gates

If a phase produces a killer verdict or detects a significant gap in prior work, the **next phase refuses to start** until the user explicitly overrides. Override is recorded in frontmatter:

```yaml
overridden: true
override_reason: "Willing to gamble on weak evidence because hypothesis is cheap to test"
```

The user always has autonomy. The friction sits at the exact moment they ignore a red flag, and the override itself becomes signal for later phases (especially decide).

### Back-Arrows: Explicit, Not Auto

When a later phase finds a significant gap in an earlier phase's work, it does **not** silently patch. It:

1. Adds the gap to its own frontmatter `gaps` array (e.g., `{ phase: "concept", note: "..." }`).
2. Refuses to proceed (soft gate).
3. Tells the user exactly which earlier phase to rerun.

Trivial additions (e.g., a new competitor discovered in feasibility) may be appended to an earlier artifact under a clearly marked footer (`## Notes from feasibility phase`), never by rewriting prior sections.

## The 8 Skills (7 workflow + 1 utility)

| # | Skill | Job | Reads | Writes |
|---|---|---|---|---|
| 1 | `idea-start` | Slim router. Brief the user on workflow + tone, list ideas in `ideas/` with their current phase, route to the correct next step. No thinking, no artifacts. | `ideas/*/` frontmatter | — |
| 2 | `idea-concept` | Two-pass: (1) free dump to capture the raw thought, (2) sharpen pass — skill reflects back, names vagueness, demands sharper problem/user/differentiation before advancing. | — | CONCEPT.md |
| 3 | `idea-validate` | Is the problem real? Who has it, how painful, how often? **Maps the alternatives landscape** — substitutes, direct competitors, indirect competitors (what users do today). Demands evidence. Marks unsupported claims as assumptions. | CONCEPT.md | VALIDATION.md |
| 4 | `idea-gtm` | How do customers find this? Channels, cold-start problem, realistic CAC. **Positioning + moat** — using validate's landscape, how do we differentiate and defend? Attacks "we'll just do content marketing" answers. | CONCEPT.md, VALIDATION.md | GTM.md |
| 5 | `idea-feasibility` | Can we build + run + afford + **legally operate** this at the scale gtm implies? Four sub-concerns: (1) technical, (2) operational, (3) resource, (4) legal/compliance. | CONCEPT.md, VALIDATION.md, GTM.md | FEASIBILITY.md |
| 6 | `idea-mvp` | Given everything known, what's the smallest concrete thing we could ship to test the core hypothesis? Core user, hypothesis, what's built, what's faked, success metric, kill threshold, timebox. | all priors | MVP.md |
| 7 | `idea-decide` | Synthesizes all priors into verdict: `build` / `shelve` / `kill` / `pivot`. Writes narrative reasoning that explicitly weighs overrides and evidence strength from each phase. | all priors | DECISION.md |
| U | `idea-recap` | **Utility (read-only).** Produces a one-page summary of any idea: current phase, key findings per phase, open assumptions, overrides taken, pending gaps, verdict if decided. If `verdict: build`, also emits a pre-launch checklist derived from MVP.md + open risks from prior phases. Invokable at any point, never mutates state. | all existing artifacts for an idea | — |

## Verdict Categories

`idea-decide` must return exactly one of:

- **`build`** — ship the MVP as scoped. Green light.
- **`shelve`** — not wrong, just not now. Specific trigger conditions for revisit documented.
- **`kill`** — fatal flaw identified. Document the flaw clearly for future-you.
- **`pivot`** — core insight is valid but the specific idea isn't. Recommend what to sharpen and restart from concept.

## Design Principles

1. **The verdict is the product.** Every phase serves the final decision.
2. **Evidence beats eloquence.** A well-argued claim without evidence is still an assumption.
3. **Friction at the right moment.** Gate the user when they're about to ignore signal.
4. **Respect phase boundaries.** Don't let later phases silently rewrite earlier work.
5. **Distribution over tech.** Most ideas die on GTM — evaluate it before feasibility.
6. **Concrete proposals, not abstractions.** Decide judges a specific MVP, not "the idea."
7. **Brutal honesty is the differentiation.** Sycophantic AI is free elsewhere.
