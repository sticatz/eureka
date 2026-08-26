---
name: idea-start
description: List the business ideas in this workspace and route to the right Eureka phase.
argument-hint: "[idea-name]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# Idea Start — the router

Route the user to the right phase. Do no thinking, write no artifacts.

This skill is user-invoked only. It never fires on its own, because "what should I do next?" means
something entirely different in most sessions.

## On start

1. Load the protocol:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   ```

   If that file cannot be read, stop and tell the user: *"Eureka looks misinstalled — I can't read
   its protocol file. Try `/plugin marketplace update sticatz` and reinstall."* Do not proceed
   without it; every gate in this system is defined there.

2. Read the state, computed rather than inferred:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" status
   ```

   This returns the ideas root, how it was resolved, and for each idea: every artifact's status,
   verdict, evidence strength and gaps, plus `current_phase`, `next_phase`, `evidence_cap`,
   `overrides`, `stale_artifacts`, `decide_ready`, `go_available` and `go_blockers`.

3. **Tell the user which absolute path was scanned**, and how it resolved. The working directory
   changes between sessions — an idea started in a different project is invisible from here, and
   that is the most common reason a user's ideas appear to have vanished.

## What to show

### If ideas exist

| Idea | Phase | Status | Verdict | Evidence | Flags |
|------|-------|--------|---------|----------|-------|

Fill every column from `status` output. **Flags** surfaces, in this order of prominence:

- `⚠ stale` when `stale_artifacts` is non-empty — name which artifacts. An earlier phase was
  reworked after these were written, so they may describe a different idea.
- `⚠ N significant gaps` with the evidence cap when `evidence_cap` is set.
- `killer (overridden)` or `killer` per phase verdicts.
- `override ×N` when overrides exist.
- For a decided idea with `verdict: park`, show the `revisit_trigger` verbatim. A park is a
  decision to come back — an idea whose trigger is never surfaced again is just a slow kill.

Then ask which idea they want to work on, or whether they have a new one.

### If no ideas exist

> No ideas here yet. I scanned `<absolute path>`. Tell me your idea and I'll start capturing it
> with `/eureka:idea-concept`.

If the resolved root looks like an unrelated project, say so and mention the two ways to pin a
workspace: an `.eureka` marker file in the directory that should hold `ideas/`, or `$EUREKA_HOME`.

### If the user names an idea

Read that idea's entry and route on `next_phase`:

| State | Route to |
|-------|----------|
| No folder, or a new idea | `/eureka:idea-concept` |
| `current_phase` is in-progress | that phase's skill, to continue |
| `next_phase` set | `/eureka:idea-<next_phase>` |
| `decide_ready` and DECISION.md complete | `/eureka:idea-recap` |

Before routing, surface anything that changes what the user is walking into:

- A prior `verdict: killer` with no matching override — warn that the next phase will refuse to
  start without a recorded reason.
- Unresolved gaps targeting the phase being routed to — that phase will offer to close them.
- `go_blockers` when the idea is at or near decide — the user should know a `go` is currently
  unavailable and why, before spending a session on the decision.

## The brief

For a user new to Eureka, before routing:

> Your idea moves through six phases. Each has its own skill and writes a persistent artifact.
>
> **idea-concept** — What's the idea, who's it for, why now, and why you?
> **idea-validate** — Is the problem real? Who has it? What do they do today?
> **idea-gtm** — How do customers find this? What does acquisition cost, and what do you charge?
> **idea-feasibility** — Can you build, run, afford, and legally operate this?
> **idea-mvp** — What's the smallest concrete thing that tests the core hypothesis?
> **idea-decide** — Go, park, or kill, with full reasoning.
>
> Two things to expect. These skills default to devil's advocate: they refuse vague answers, demand
> evidence, and push back on lazy reasoning. And evidence is load-bearing — if the analysis rests
> mostly on assumptions, a `go` verdict is withheld and you get a `park` with the missing evidence
> named. A well-reasoned kill is worth more than a hand-wavy go.
>
> Artifacts land in `<absolute path>`. Worth running `git init` there so you can see how the
> thinking changed.

## Rules

- **Never do thinking work.** Route. Do not analyze, evaluate, or opine on an idea.
- **Never write artifacts.** Read-only.
- **Never auto-transition.** Present the route and wait for the user to confirm.
- **Trust `eureka.py` over your own reading.** `current_phase` is defined there so the router and
  `idea-recap` can never report different answers for the same folder.
