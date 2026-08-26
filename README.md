# Eureka

A set of Claude Code skills that push a business idea from raw thought to a defensible go/park/kill verdict. The system is opinionated, evidence-demanding, and allergic to hand-waving.

## What this is

8 skills (7 workflow + 1 utility) that guide you through structured thinking about whether an idea is worth building. Each phase produces a persistent markdown artifact. The terminal output is a verdict: **go**, **park**, or **kill**.

This is not a brainstorming pad. The single job is to produce a decision you can defend.

## Install

`sticatz` is the marketplace (the org). `eureka` is the plugin inside it. Installing is two steps: add the marketplace, then install the plugin from it.

In a Claude Code session:

```
/plugin marketplace add sticatz/eureka
/plugin install eureka@sticatz
```

That's it — the slash commands below are now available.

<details>
<summary>Installing from a local clone instead</summary>

```bash
git clone https://github.com/sticatz/eureka.git
```

Then in Claude Code, point the marketplace at the clone's directory:

```
/plugin marketplace add /absolute/path/to/eureka
/plugin install eureka@sticatz
```

The marketplace is still called `sticatz` — the name comes from `.claude-plugin/marketplace.json`, not from where the files live.

</details>

To update later: `/plugin marketplace update sticatz`.

## Quick start

1. Start a conversation and invoke `/eureka:idea-start`.
2. Follow the workflow. The skills will push you.

## Workflow

````
/eureka:idea-start        → Router. Shows your ideas, points you to the right phase.
/eureka:idea-concept      → What's the idea? Who's it for? Why now?
/eureka:idea-validate     → Is the problem real? Who else solves it?
/eureka:idea-gtm          → How do customers find this? At what cost?
/eureka:idea-feasibility  → Can we build, run, afford, and legally operate this?
/eureka:idea-mvp          → What's the smallest thing we ship to test the hypothesis?
/eureka:idea-decide       → Go, park, or kill. With reasoning.
/eureka:idea-recap        → Read-only summary of any idea at any point.
````

## What to expect

The skills default to devil's advocate. They will:
- Refuse vague answers and demand sharper ones.
- Require evidence for claims. No evidence = marked as assumption.
- Attack lazy reasoning ("we'll go viral", "everyone needs this").
- Never tell you your idea is great. That's not the job.

Brutal honesty is the product. Sycophantic AI is free elsewhere.

## How it works

Each phase produces a markdown artifact in `ideas/<your-idea>/` with YAML frontmatter tracking status, verdict, evidence strength, and risk tags. Later phases read earlier artifacts to build on prior thinking.

If a phase identifies a fatal flaw (`verdict: killer`), the next phase will refuse to start until you explicitly override with a reason. Your overrides are recorded and weighed in the final decision.

See [CONVENTIONS.md](CONVENTIONS.md) for the full protocol.
See [IDEA.md](IDEA.md) for the original vision document.
