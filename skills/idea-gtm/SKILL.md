---
name: idea-gtm
description: This skill should be used when a business idea has Eureka's CONCEPT.md and VALIDATION.md complete and the user wants to work out distribution and the revenue model — how customers find it, channel selection, cold start, acquisition cost, what to charge, positioning and moat. Triggered by "how do we reach customers?", "go-to-market for this idea", "what should we charge?", or an explicit /eureka:idea-gtm. Writes GTM.md. Not for problem validation (idea-validate) or build feasibility (idea-feasibility).
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Idea GTM — phase 3

How does this reach customers, and what does it charge them? The best product with no path to
users is a dead product, and a product with users but no revenue model is a hobby.

This phase owns **both** distribution and monetization. Nothing downstream picks up pricing if it
is deflected here.

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; slug from `$ARGUMENTS` or ask. Print the path.

3. **Gate check.** Run `eureka.py status <slug>`. CONCEPT.md and VALIDATION.md must both be
   `complete`. If either is missing, name which. If either carries `verdict: killer`, apply Gate A
   — checking `overrides` first so an already-overridden killer is carried forward, not
   re-litigated. Surface any `stale_artifacts`.

4. Read both priors: the target user and `why you` from CONCEPT.md, the segments, pain severity,
   alternatives landscape and any willingness-to-pay signal from VALIDATION.md.

5. **Gap scan (rerun only).** Collect gaps where `phase: gtm` and `resolved: false`, surface per
   Gate B′.

## How to explore

Ask in prose. Follow the thread the user's answer opens.

### Where the users are
Start from the validated segments, then go concrete:
- Where do these people already spend attention — communities, platforms, events, publications,
  tools?
- How do they currently discover solutions — search, referral, community, outbound?
- What is the buying process — impulse, research-heavy, committee approval, trial-first?
- Are there gatekeepers, aggregators or influencers who already reach them?

Demand specificity. "Small business owners" is not actionable. "Restaurant owners who search Yelp
alternatives on Reddit and read two food-industry newsletters" is.

Check CONCEPT.md's `why you`. An unfair distribution advantage — an existing audience, a community
already run, an employer's customer relationships — is frequently the entire realistic channel
answer, and it is already recorded.

### The revenue model
This is not a deflection to a later phase. Nothing downstream asks it.

- **What do you charge, to whom, per what unit?** Subscription, transaction fee, one-off, usage,
  retainer, ad-supported, marketplace take rate.
- **Who actually pays** — is the payer the user? In B2B they usually are not.
- **Why that number?** Anchored against what — the substitute's cost, the hours saved, the
  incumbent's price, the budget line it comes out of? "It feels about right" is not an anchor.
- **What is the evidence?** Has anyone said they would pay it, or paid for something adjacent?
  Willingness-to-pay stated in the abstract is close to worthless — see `interviewing.md` on why.
- **Rough LTV** — price × expected retention × margin. Order of magnitude is enough, but it must
  exist, because the next section compares CAC against it and a comparison against nothing is not
  a comparison.
- **Time to first dollar** — how long from start to the first real payment?

If the user has no revenue model at all, that is a finding, not a gap to skip. Record it as a
`key_risk` and say plainly that it will weigh at decide.

### Channel strategy
Which channels reach *this* audience for *this* product — not which channels exist. For each
viable one: why it fits, the strategy-level approach, and rough CAC. Tie it to the LTV established
above: "if LTV is $200 and clicks cost $15–30 at 2% conversion, CAC is $750–1500 — that doesn't
work."

Do not suggest channels because they exist. If the target user is not on Instagram, say so.

### Cold start
Matters most for marketplaces and network-effect businesses; probe whether it applies regardless.
Which side first and why; minimum viable supply or demand; whether it can start manual or
concierge; whether there is a single-player mode; existing aggregations to tap.

### Positioning
Against direct competitors: better how, for whom, in what context? Against substitutes: what makes
switching worth the effort? Against inaction: what event finally makes someone act?

### Channel competition
Where are competitors strong in distribution, and where are the gaps? If they own SEO for the
obvious keywords, what is the alternative? Which channels are actually *winnable* given who is
already buying attention there? Can distribution itself be the differentiator?

### Sequence
Not just which channels, but in what order and on what signal:
- **Phase 0 — validation:** landing pages, waitlists, manual outreach, small paid tests. Before
  real money.
- **Phase 1 — first users:** unscalable things for the first 10–100.
- **Phase 2 — growth:** scalable channels once there is a PMF signal.

What signal moves it from one phase to the next?

### Research
Before recording CAC, market size or channel economics as unknown, load and follow:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/references/research.md"
```

Published CAC benchmarks by channel and industry, ad platform rate cards, keyword difficulty,
community sizes and posting rules, competitor pricing pages. A CAC recorded as "unknown" when a
benchmark exists is an avoidable weak-evidence score.

If unit economics come out negative, surface it immediately as a tension — do not bury it in a
cost table.

## Depth gaps

Gaps may point at **any** earlier phase. A GTM finding that invalidates the concept-level target
user is a `concept` gap, not a `validate` one — record it against the phase where the thinking
lives. Check for duplicates and set `duplicate_of` when the weakness is already logged.

## Red flags

| User says | Respond |
|---|---|
| "We'll go viral" | "Virality is an outcome, not a strategy. What specific mechanic makes one user bring in another?" |
| "Word of mouth" | "Word of mouth is what happens when everything else works. What gets you the first users who do the talking?" |
| "Content marketing" | "For whom, about what, distributed where? 'We'll write blog posts' is not a strategy." |
| "We'll just do SEO" | "Which keywords? Who ranks there now? What's the realistic timeline to page one against them?" |
| "Build it and they'll come" | "Nobody comes. You go get them. Through which channel, at what cost?" |
| "We'll partner with X" | "Have you talked to X? What's in it for them? Partnerships need leverage — what's yours?" |
| "We'll post on TikTok" | "What evidence is there that your target user discovers products this way? Name a similar product that grew like that." |
| "Organic social is free" | "It costs your time and guarantees zero reach. What's the plan when twenty posts get fifty views each?" |
| "We'll figure out pricing later" | "Later is decide, and decide can't green-light a business with no revenue model. What's the unit, and what anchors the number?" |
| "We'll be cheaper than X" | "Cheaper is a position competitors with more capital can take from you at will. Why is cheap defensible here?" |
| "We'll monetize once we have users" | "That's two bets stacked. Which users, paying for what, and what makes you think the free cohort converts?" |

## Staying in scope

| Drift toward | Response |
|---|---|
| Product features, tech stack | "Distribution first — features come from feasibility and MVP. How do users find this?" |
| Revisiting problem validation | "That's VALIDATION.md. If it needs revising, rerun `/eureka:idea-validate` — I'll log a gap. Here we're reaching the people who have it." |
| Detailed cost modeling | "Rough numbers are enough here — feasibility does the full cost structure. I need the shape, not the spreadsheet." |
| Verdict | "Not yet — feasibility and MVP still have to happen." |

## Phase transition

> "Here's the GTM picture: [channels, cold start, CAC vs LTV, pricing, positioning]. When you're
> ready, `/eureka:idea-feasibility` evaluates whether you can build, run, afford and legally
> operate this at the scale this implies. Want to dig deeper, or move on?"

**Never auto-transition.**

## Writing GTM.md

````yaml
---
phase: gtm
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
# <Idea Name> — Go-to-Market

## Where the Users Are
## Revenue Model
## Channel Strategy
## Cold Start Plan
## Positioning
## Channel Competition
## Go-to-Market Sequence
## Unit Economics
## Key Tensions
## Evidence vs Assumptions
## Sources
````

`## Evidence vs Assumptions` and `## Sources` are required. `## Unit Economics` must show the
actual arithmetic — price, retention, margin, LTV, CAC per channel — or state explicitly which
input is missing and why.

**On completion:**
- `verdict: proceed` — at least one specific channel is plausibly cost-viable against a stated
  price, with positioning that holds.
- `verdict: proceed-with-caution` — channels exist but cold start is unresolved, CAC is uncertain,
  or the price has no anchor.
- `verdict: killer` — no viable channel identified, or CAC cannot fit any plausible LTV, or there
  is no revenue model and no path to one.
- `evidence_strength` — how much of the channel, cost and pricing analysis rests on looked-up data
  versus guesses. Load-bearing: `weak` here removes `go` from the table at decide.
- `key_risks` — cold start, channel competition, pricing, cost uncertainty.
