---
name: idea-test
description: This skill should be used when the user wants to check one of their business idea's assumptions against the real world, or to record what came back from one they already ran — triggered by "how do I test this assumption?", "what's the cheapest way to find out if people want this?", "I talked to five people, here's what they said", "the landing page results are in", or an explicit /eureka:idea-test. Designs pre-registered experiments and debriefs them into tests/. Requires at least CONCEPT.md.
argument-hint: "[idea-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion
---

# Idea Test — design an experiment, or debrief one

The six phases produce analysis: reasoning about what the user already believed. This skill is the
only place a claim gets checked against the world, and the only place a result comes back in.

Two modes. **Design** pre-registers an experiment against a named assumption. **Debrief** records
what happened and writes it back into the artifact the claim came from.

Invokable at any point. It does not need the pipeline finished — the cheapest tests are worth
running early, and an assumption logged at concept is testable long before decide.

## On start

1. Load the shared rules:

   ```bash
   cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"
   cat "${CLAUDE_PLUGIN_ROOT}/references/dialogue.md"
   ```

   If either cannot be read, stop — Eureka is misinstalled.

2. Resolve the idea folder with `eureka.py root`; slug from `$ARGUMENTS` or ask. Print the path.

3. Read the state:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" status <slug>
   ```

   `open_assumptions` lists every unevidenced claim across the artifacts, with its source. `tests`
   lists what has already been designed or run. `next_test_id` is the id to use.

4. **Pick the mode.** If any test has `status: running` or `designed`, lead with it — ask whether
   they are here to debrief it. Otherwise design a new one. If the user opened with results
   ("I talked to five people"), go straight to debrief.

   `CONCEPT.md` must exist. Nothing else is required.

---

# Mode A — design

## 1. Rank the assumptions

Take `open_assumptions` from `status` and score each with the user:

- **Impact** — `fatal` (the idea does not work if this is false), `damaging`, `survivable`.
- **Confidence** — `none`, `hunch`, `informed`.

Sort by impact against uncertainty. Show the top three or four and let the user pick, using
`AskUserQuestion` — this is a genuine discrete fork between claims that already exist in their
files, which is exactly what the tool is for.

If `open_assumptions` is empty, the artifacts recorded no unevidenced claims. That is either a very
well-evidenced idea or a phase that graded itself generously; ask which, and offer to test the
single claim the whole idea rests on regardless.

**Test the top one.** If the user wants to test something further down, record why in the test file
— usually it is because the top assumption is expensive to test, and that is worth knowing later.

## 2. State the claim so it can be wrong

Rewrite the chosen assumption until it is falsifiable. "Users want better invoicing" cannot be
wrong. "At least 3 of 10 solo consultants will name invoice chasing unprompted as a top-3 monthly
annoyance" can.

A claim that no observation could contradict is not an assumption, it is a preference. Say so and
push for the version that can fail.

## 3. Pick the cheapest rung that could falsify it

| Method | Typical cost | Falsifies |
|---|---|---|
| `desk-research` | Hours | Whether the market, regulation or incumbent position is what you assume. See `research.md`. |
| `interviews` | Days, ~free | Whether the problem is real, frequent and painful. See `interviewing.md`. |
| `smoke-test` | ~£100, 1–2 weeks | Whether the value proposition earns attention at a plausible CAC. |
| `pre-sale` | 2–4 weeks | Whether anyone parts with money or reputation before the thing exists. Strongest cheap signal. |
| `concierge` | 2–4 weeks | Whether the outcome is valuable when a human delivers it. |
| `wizard-of-oz` | 3–6 weeks | Whether the interaction model works without building the engine. |
| `built-mvp` | 4+ weeks | Whether people use and retain on the real thing. Scoped by `idea-mvp`. |

Start at the top and stop at the first rung that could genuinely return a falsifying result. Scale
to `stakes` from CONCEPT.md: a weekend project does not need a pre-sale, a bet on savings should
not skip one.

**If a rung above `built-mvp` would settle it, say so plainly.** The user may be about to build
something a two-week test would have killed, and this is the moment to point that out.

## 4. Pre-register

Both of these are written **now**, before anything runs, and `eureka.py validate` enforces it:

- **Prediction** — what you expect to see if the assumption holds. A number.
- **Kill threshold** — the result that falsifies it. A number.

Then pressure-test the threshold: *would this actually fire?* A threshold low enough that any
outcome clears it is decoration. Ask what result would make the user drop the idea, and if the
answer is "none", the test is not worth running — say that.

## 5. Make it runnable

Hand over something that can be executed without further design work:

- `interviews` — load `${CLAUDE_PLUGIN_ROOT}/references/interviewing.md` and produce an actual
  script for the named segment: past-tense questions, no pitch, plus the recruiting approach.
- `desk-research` — load `${CLAUDE_PLUGIN_ROOT}/references/research.md`, then run the searches
  now and debrief in the same session.
- `smoke-test` — the landing page copy, the budget, the traffic source, the run length, the
  metric.
- `pre-sale` — what is being offered, at what price, with what terms.

Write the file, then tell the user what to go and do.

## Writing the test file

`tests/<id>-<short-slug>.md`, id from `next_test_id`:

````yaml
---
id: T001
status: designed
method: interviews
assumption: "<the claim, quoted from its artifact>"
source_artifact: VALIDATION.md
cost: "free, 4 days"
prediction: "at least 3 of 10 name invoice chasing unprompted"
kill_threshold: "fewer than 2 of 10 → the claim is falsified"
created: <YYYY-MM-DD>
launched: null
closed: null
outcome: null
---
````

````markdown
# T001 — <one-line description>

## The Assumption
## Why This One
## Method
## How to Run It
## Prediction
## Kill Threshold
## Results
## What This Does Not Settle
````

Leave `## Results` empty until debrief. Set `status: running` and `launched` when the user says
they have started.

---

# Mode B — debrief

This is where the pressure is highest. The user has spent effort, wants a good answer, and the
threshold is sitting in a file. **Read the pre-registered threshold before hearing the results**,
and say it out loud. Then take the data.

## 1. Get what actually happened

Numbers first, story second. How many people, how many did the thing, what did they say. Ask for
specifics; "it went pretty well" is not a result.

## 2. Filter it

For `interviews`, load `${CLAUDE_PLUGIN_ROOT}/references/interviewing.md` and run **every claim**
through the admission rubric before any of it counts. Was it past behavior or a hypothetical? Was
the idea pitched first? Is there an anchor — a date, an amount, a named tool? Was the person in
segment? Could they have said no?

Report the filtering explicitly: "eight statements, three admissible." A founder who pitched first
and collected praise has run a test that returned nothing, and needs to hear that in those words.

For `smoke-test` and `pre-sale`, check the denominator. A 40% conversion on nine visitors is not a
40% conversion.

## 3. Compare against the threshold, and do not renegotiate

State the threshold, state the filtered result, state which side of the line it falls on.

- Above prediction → `supported`.
- Below kill threshold → `falsified`.
- Between → `inconclusive`.

The threshold was set before the run precisely so this comparison is not a judgment call now.
If the user wants to move it, that is a new test, not a rescored one — and record in the file that
the original threshold was not met.

## 4. Write it back

Record the results in the test file: set `status: complete`, `closed`, and `outcome`. Fill
`## Results` with the raw numbers, what was admitted and what was filtered out, and
`## What This Does Not Settle`.

Then apply **Gate E** from `protocol.md` to the source artifact — this is the only cross-artifact
write this skill performs, and it touches nothing but the evidence sections:

- `supported` → move the claim from the assumption list to the evidenced list in
  `## Evidence vs Assumptions`, citing the test id; add the test to `## Sources`.
- `falsified` → mark it `**Falsified by T00N:** <claim>` and add a `key_risks` tag.
- `inconclusive` → leave it as an assumption, note the test id beside it.

Bump the artifact's `updated`. Do not touch its prose, verdict, or `evidence_strength`.

## 5. Say what it means

- **Supported** — name what is now evidenced and what still is not. One supported assumption does
  not validate the idea. Offer to rerun the source phase to regrade `evidence_strength`, since the
  grade in the file is now stale.
- **Falsified** — this is the valuable outcome and should be said that way, once, without
  performance. Then: is the assumption wrong, or was the test wrong? Both happen. If the assumption
  is wrong, does the idea survive in a modified form, or is this fatal? A falsified assumption
  appears in `go_blockers` from now on.
- **Inconclusive** — usually a design problem: too few people, wrong segment, a threshold that
  could not discriminate. Say which, and offer to design the sharper version.

Then: what is the next assumption on the ranked list?

## Red flags

| User says | Respond |
|---|---|
| "It basically worked" | "The threshold was [X], the filtered result was [Y]. Which side of the line is that?" |
| "The threshold was too strict" | "Maybe — but it was set before the run for this exact reason. I'll record that it wasn't met, and we can design a sharper test." |
| "They all loved it" | "Love isn't in the threshold. How many did the specific thing we predicted, and were any of them pitched first?" |
| "Let's just skip to building it" | "What would the build tell you that a [cheaper rung] wouldn't? If the answer is nothing, you're paying weeks for the same information." |
| "Small sample, but the signal is clear" | "With n=3 the signal is noise. What would it cost to get to a number that discriminates?" |
| "It failed but I still believe it" | "That's allowed — record why. It goes on the file, and idea-decide weighs it as an override, not as evidence." |
| "Let's test everything" | "Test the top of the ranked list. Everything else is deferred, not skipped." |
| No falsifiable claim available | "Nothing here can be wrong, so nothing here can be tested. Which claim, if false, kills the idea?" |

## Staying in scope

| Drift toward | Response |
|---|---|
| Redesigning the product | "Noted for the phase that owns it. Right now: what does this test tell us?" |
| Reaching a verdict | "That's `/eureka:idea-decide`, and it'll read these results. This is one assumption." |
| Regrading a phase | "I record the result; regrading is the phase's job. Rerun `/eureka:idea-validate` and it'll pick this up." |

## Rules

- **Never write an outcome before the test has run.** `eureka.py validate` rejects it, and the
  reason it rejects it is the entire point of the mechanism.
- **Never invent results.** If the user is vague about numbers, the result is `inconclusive`.
- **Never let a filtered-out datum count.** A claim that fails the admission rubric is not weaker
  evidence, it is not evidence.
- **One test, one assumption.** A test that would settle four things settles none of them cleanly.
