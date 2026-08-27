---
name: idea-feasibility
description: This skill should be used when a business idea has Eureka's CONCEPT.md, VALIDATION.md and GTM.md complete and the user wants to evaluate whether it can be built, run, afforded and legally operated at the scale GTM implies — triggered by "is this idea feasible?", "can we actually build this business?", "what regulations apply to this idea?", or an explicit /eureka:idea-feasibility. Writes FEASIBILITY.md. Not for distribution (idea-gtm) or MVP scoping (idea-mvp).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Idea Feasibility — phase 4

Can this be built, run, afforded and legally operated at the scale GTM implies? Four sub-concerns,
judged against real numbers rather than in the abstract.

**Key framing:** "Can we build it?" is never abstract here. It is "can we build it to serve the
volume and channels GTM describes, at a cost that works against the price GTM set?"

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; slug from `$ARGUMENTS` or ask. Print the path.

3. **Gate check.** Run `eureka.py status <slug>`. CONCEPT.md, VALIDATION.md and GTM.md must all be
   `complete`. Apply Gate A to any `killer`, checking `overrides` first. Surface `stale_artifacts`.

4. Read all three priors. Needed: target user, `stakes` and `idea_class` (CONCEPT.md); demand
   signal and alternatives (VALIDATION.md); channels, volume shape, price and unit economics
   (GTM.md).

5. **Gap scan (rerun only).** Collect gaps where `phase: feasibility` and `resolved: false`.

## How to explore

Weave across the four sub-concerns rather than marching through them — they interact. A technical
choice moves resource cost; a legal constraint closes an operational route; a resource limit
shrinks what is technically possible.

Branch on `idea_class`. The sub-concerns below are written software-first; for other classes the
dominant risk sits elsewhere and must be asked about explicitly:

| `idea_class` | Ask about, beyond the four below |
|---|---|
| `physical` | Working capital. Unit cost at realistic volume, minimum order quantity, lead time, landed cost including duty and freight, storage, returns rate, cash tied up before the first sale. This is what kills physical-goods businesses, and a software-shaped feasibility pass will miss it entirely. |
| `service` / agency | Utilization and key-person risk. Who delivers, at what billable rate and what utilization? What happens when the founder is the product and gets sick, or wants a holiday? How does delivery scale without linear headcount? |
| `marketplace` | Trust, liability and disintermediation. Who is liable when a transaction goes wrong? What stops both sides transacting off-platform after the first match? |
| `content` | Production cadence and platform dependency. What is the sustainable output rate, and what happens when the platform changes its distribution algorithm? |

### 1. Technical
- What is genuinely *hard* here — not "what's the stack", but what might not work?
- Technical risks and unknowns.
- External dependencies: APIs, data sources, services. What happens if they reprice, rate-limit or
  shut down?
- Build versus buy: where does custom work add value, where does off-the-shelf win?
- What does GTM's volume shape require of the architecture?

### 2. Operational
- What does running this look like day to day — infrastructure, support, content, moderation,
  manual work?
- What breaks at scale? Something that works for 100 users can collapse at 10,000.
- Operational burden per user: high-touch or self-serve?
- Dependencies on specific people, skills or vendors.

### 3. Resource
- Cost to build: time, people, money, to an order of magnitude.
- Cost to run monthly: infrastructure, salaries, services, support.
- Against GTM's CAC and price: **do the numbers work?** State it explicitly — "GTM says CAC is $X,
  operating cost per user is $Y, revenue per user is $Z, so contribution margin is …"
- Runway to sustainability, in months to breakeven — not "eventually".
- Who builds this, and is that realistic for the complexity?

### 4. Legal and compliance
- Which regulations apply — data protection, financial services, health, food safety, employment,
  consumer protection, sector-specific licensing?
- Licensing requirements. Liability exposure. Platform terms-of-service risk.
- International considerations if GTM targets multiple markets.

**Never resolve regulatory ignorance by recording a risk.** Load and follow:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/references/research.md"
```

Regulatory and licensing is the highest-yield search target in the whole framework: user knowledge
is lowest and public ground truth is highest. Search the regulator, the licensing body, the
data-protection regime. An idea that is flatly illegal at GTM's implied scale is `killer`, not
`proceed-with-caution` — and the only way to know is to look. The same applies to vendor pricing,
API rate limits and salary benchmarks: look them up before calling them unknown.

### Cross-cutting tensions
Every sub-concern connects back to earlier phases. When a finding pulls against what GTM,
validation or concept established, surface it immediately — these are usually the most important
findings. A technical choice that breaks unit economics. An operational burden that cannot scale
to GTM's volume. A legal constraint that closes the primary channel. A resource requirement that
exceeds what the market size justifies.

When a tension is surfaced, the user either resolves it or accepts it. Both are valid and they
have different consequences: a resolved tension is recorded as resolved; an accepted one becomes a
`key_risks` entry and pulls `evidence_strength` down.

## Depth gaps

Feasibility exposes weakness in **any** earlier phase. A single finding may produce gaps in
several — record each against the phase where the thinking lives, check for duplicates, and set
`duplicate_of` where the weakness is already logged.

## Red flags

| User says | Respond |
|---|---|
| "We'll figure out the tech later" | "The tech decides whether this is a weekend or six months. What's the hardest technical problem?" |
| "It's just a simple app" | "Simple how? Walk me through what happens when a user does X. Where does the complexity hide?" |
| "We'll hire for that" | "Hire whom, at what cost, in what timeline? Is that person available for what you can pay?" |
| "Legal won't be an issue" | "How do you know? Let me look up what applies before we record that." |
| "We'll scale when we need to" | "GTM says you need to handle [X]. Can the first build take that, or is a rewrite already baked in?" |
| "It'll cost about $X" (vague) | "Break it down — infrastructure, salaries, services. Vague estimates hide the surprises." |
| "We can outsource the whole thing" | "To whom, at what quality, managed by whom? Outsourcing has coordination costs." |
| "We'll just hold a bit of stock" | "How much cash is tied up before the first sale, at what minimum order quantity, with what lead time? That's where physical businesses die." |

## Staying in scope

| Drift toward | Response |
|---|---|
| Revisiting problem or demand | "VALIDATION.md territory. If it needs revising, rerun `/eureka:idea-validate` — I'll log a gap. Here we're asking whether the validated problem can be feasibly served." |
| Changing channel strategy | "Channel strategy lives in GTM.md. If feasibility says a channel won't work at scale, I'll log a `gtm` gap and flag it for decide." |
| MVP scoping | "Next phase. First we need to know what's feasible before scoping what to build." |
| Verdict | "Not yet — MVP still has to happen." |

## Phase transition

> "Here's the feasibility picture: [technical complexity, operational burden, cost structure,
> legal findings, and whether the unit economics close]. When you're ready, `/eureka:idea-mvp`
> scopes the smallest thing that tests the core hypothesis. Want to dig deeper, or move on?"

**Never auto-transition.**

## Writing FEASIBILITY.md

````yaml
---
phase: feasibility
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
# <Idea Name> — Feasibility

## Technical
## Operational
## Resource
## Legal and Compliance
## Cross-Cutting Tensions
## Cost vs Revenue Reality
## Evidence vs Assumptions
## Sources
````

`## Evidence vs Assumptions` and `## Sources` are required. `## Cost vs Revenue Reality` must show
the explicit arithmetic against GTM's CAC and price, not a narrative summary of it.

**On completion:**
- `verdict: proceed` — all four sub-concerns green, or yellow with named mitigations.
- `verdict: proceed-with-caution` — one or more red but addressable.
- `verdict: killer` — illegal or unlicensable at GTM's implied scale, the resource gap is
  unbridgeable, or the technical approach is fundamentally unworkable.
- `evidence_strength` — how much rests on looked-up facts, quotes and price pages versus estimates.
  A phase that searched nothing cannot be `strong`.
- `key_risks` — from each sub-concern.
