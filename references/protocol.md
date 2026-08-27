# Eureka Protocol — state, schema, gates

Loaded by every Eureka skill on start. Defines where state lives, what shape it takes, and the
gates that govern movement between phases. Companion file: `dialogue.md` covers tone and how to
run the conversation.

These are protocols, not guidelines. Where a rule below is arithmetic, do not do the arithmetic
by hand — run `scripts/eureka.py` and read the answer.

## Workflow

`concept → validate → gtm → feasibility → mvp → decide`, with `idea-start` routing and
`idea-recap` reporting. GTM precedes feasibility because distribution kills more ideas than
technology, and feasibility is then judged against the volume and price GTM produced.

## Where state lives

Ideas live in the **user's** workspace, never in the plugin directory. Resolve the root by running:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eureka.py" root
```

It prints one absolute path, resolved in this order: `$EUREKA_HOME/ideas`, then `ideas/` beside the
nearest ancestor `.eureka` marker file, then `./ideas` relative to the session's working directory.

**Always print the resolved absolute path to the user before writing anything into it.** The
working directory changes between sessions; an idea written into a client repo last Tuesday is
invisible from a different project today, and every gate in this system keys on "does CONCEPT.md
exist and is it complete". A path the user can see is a path they can correct.

If the root does not exist and the user is starting a new idea, say where it will be created and
ask for confirmation. Suggest `git init` in that workspace and a commit at each phase completion —
artifacts are the only durable state, they are rewritten in place many times per session, and
there is no undo.

Each idea is a folder of uppercase artifacts, plus a `tests/` directory:

```
<ideas-root>/<idea-slug>/
  CONCEPT.md  VALIDATION.md  GTM.md  FEASIBILITY.md  MVP.md  DECISION.md  SUMMARY.md
  tests/
    T001-invoice-pain-interviews.md
    T002-landing-page-smoke.md
```

`<idea-slug>` is lowercase-kebab-case derived from the idea name.

The six artifacts hold analysis. `tests/` holds **results** — the only place in the system where a
claim about the world gets checked against the world. Everything else is reasoning about what the
user already believed.

## Frontmatter schema

Every artifact is YAML frontmatter plus freeform prose. Skills read frontmatter to detect state;
the prose carries the thinking.

```yaml
---
phase: concept | validate | gtm | feasibility | mvp | decide
status: in-progress | complete
verdict: null | proceed | proceed-with-caution | killer   # DECISION.md: null | go | park | kill
evidence_strength: null | strong | medium | weak | n/a
key_risks: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
covered: []
pending: []
last_question: null
overrides: []
gaps: []
---
```

| Field | Purpose |
|---|---|
| `phase` | Self-identification. Lets the router and downstream skills parse state. |
| `status` | `in-progress` while the phase conversation is live; `complete` when the thinking is wrapped up. |
| `verdict` | Phase artifacts: traffic light. `proceed` (green), `proceed-with-caution` (yellow), `killer` (red — blocks the next phase without an override). `null` until `status: complete`. DECISION.md: terminal — `go` / `park` / `kill`. |
| `evidence_strength` | How much this phase rests on evidence versus assumption. Load-bearing: see the verdict-eligibility rule below. `n/a` only on MVP, which is a proposal rather than a finding. |
| `key_risks` | Short risk tags, scanned by decide and recap. |
| `created` / `updated` | Required. Get the date from the session context; do not guess. `updated` is what makes staleness detectable when an earlier phase is rerun. |
| `covered` / `pending` | Which areas of this phase's ground have actually been probed, and which remain. This is what makes a second session resumable. |
| `last_question` | The thread that was open when the session ended, verbatim. |
| `overrides` | Records of the user pushing past a killer verdict. See Gate A. |
| `gaps` | Depth gaps this phase noticed in earlier phases' work. See Gate B. |

**Per-artifact exceptions.** CONCEPT.md omits `gaps` — it is the first phase and has nothing
earlier to point at. DECISION.md omits `gaps` — it weighs them, it does not log them — and adds
`revisit_trigger` when the verdict is `park`.

### Gap entries

```yaml
gaps:
  - id: V1                      # unique within the artifact; makes resolution unambiguous
    phase: concept              # which earlier phase the gap lives in — any earlier phase, not just the previous one
    note: <one line>
    severity: minor | significant
    resolved: false
    resolved_in: null           # YYYY-MM-DD when resolved
    duplicate_of: null          # id of an existing gap describing the same underlying weakness
```

- `minor` — a detail worth sharpening, not load-bearing for the verdict.
- `significant` — a dimension whose weakness could flip the verdict.

**Before logging a gap, check whether one already exists for the same underlying weakness.** Run
`eureka.py status` and read the existing `gaps`. If the weakness is already recorded, log the new
entry with `duplicate_of` set to that id. Duplicates stay visible — three phases independently
tripping over the same flaw is real signal — but they are excluded from the threshold count, so a
single weakness cannot be penalized three times.

Logging a gap is cheap and honest. Minor gaps never trigger a cap. There is no cheaper alternative
route for recording a finding about earlier work, and no judgment call about whether something is
"trivial enough" to slip in quietly.

### Test files

One file per experiment in `tests/`, named `<id>-<short-slug>.md`. Written and debriefed by
`idea-test`.

```yaml
---
id: T001
status: designed | running | complete | abandoned
method: desk-research | interviews | smoke-test | pre-sale | concierge | wizard-of-oz | built-mvp
assumption: "<the claim being tested, quoted from the artifact it came from>"
source_artifact: VALIDATION.md
cost: "<money and days>"
prediction: "<what you expect to see if the assumption holds>"
kill_threshold: "<the result that falsifies it>"
created: YYYY-MM-DD
launched: null
closed: null
outcome: null | supported | falsified | inconclusive
---
```

`prediction` and `kill_threshold` are **required from the moment the test is designed**, and
`eureka.py validate` rejects a file where `outcome` is set while `status` is still `designed`. A
threshold written once the result is known is not a threshold. This is the one place the system can
mechanically prevent hindsight, and it does.

An `outcome: falsified` on any test, or any test left `running`, appears in `go_blockers` — a test
result is the strongest evidence the system holds, so it moves the verdict in both directions.

### Override entries

```yaml
overrides:
  - id: O1
    over: validate              # the phase whose killer verdict is being overridden
    reason: "<the user's words, verbatim>"
    recorded: YYYY-MM-DD
```

## Gate A — killer verdict (blocking, override-able)

On start, run `eureka.py status <slug>`. If any prior phase has `verdict: killer`:

1. **Check whether that specific killer is already overridden.** `status` returns an `overrides`
   array collected across every artifact in the folder. If an entry already has
   `over: <that phase>`, the user has already made this call — carry it forward, mention it in
   one line, and proceed. **Do not re-litigate the same decision at every subsequent phase.**
2. If it is not yet overridden, refuse to proceed:

   > **Refusing to start.** `<PRIOR>.md` concluded with verdict `killer` — <one-line summary from
   > its prose>. Continuing means gambling that this finding is wrong or tolerable. If you want to
   > proceed anyway, tell me why and I'll record it. Weak reasons ("I just want to try") will count
   > against you at `idea-decide` — the stronger your reason, the better it holds up in the final
   > weighing.

3. If the user gives a reason, append an entry to the **current** artifact's `overrides` array with
   the reason captured verbatim, then proceed. If the user says "just do it" without a reason,
   refuse again. An override without a reason is not an override.

## Gate B — depth gaps (advisory, non-blocking)

When a phase notices that **any** earlier phase's work is weaker than this phase's findings
require:

1. Append a `gaps` entry per the schema above, after checking for an existing duplicate.
2. Tell the user: "I'm noting a <severity> gap in <phase> — <summary>. You can rerun
   `/eureka:idea-<phase>` later to close it, or leave it for idea-decide to weigh. Continuing."
3. **Proceed regardless.** Advisory, not blocking.

A single finding may produce gaps in several earlier phases. Record each against the phase where
the thinking actually lives — a GTM finding that invalidates the concept-level target user is a
`concept` gap, not a `validate` one.

**Evidence cap.** Unresolved `significant` gaps, deduplicated, cap the final `evidence_strength`:
two caps it at `medium`, three or more at `weak`. Do not count these by hand — `eureka.py status`
returns `evidence_cap` already computed. Resolved gaps count as *positive* signal: the user went
back and closed a loop.

## Gate B′ — gap resolution on rerun

When a skill runs against an artifact that already exists, before anything else:

1. Run `eureka.py status <slug>` and collect every entry across **all** artifacts where
   `phase: <this phase>` and `resolved: false`.
2. Surface them at the top:

   > "When we last left this, later phases noted these gaps here:
   > - [VALIDATION.md, V1, significant] <note>
   > - [MVP.md, M2, minor] <note>
   >
   > Which do you want to address in this rerun? You can address all, some, or none — and we can
   > still explore other threads."

3. When the user confirms a gap is addressed, edit the matching entry in the artifact that owns it,
   setting `resolved: true` and `resolved_in` to today's date. Change nothing else in that file.

**This applies to every phase, `idea-concept` included.** Concept is the most common gap target —
it is the earliest phase and everything downstream pressure-tests it — so a concept rerun that
could not close concept gaps would make them a one-way ratchet that permanently caps the verdict.

This is the only case where a skill may write into another phase's artifact. It touches the `gaps`
array and nothing else: never prose, never other frontmatter fields, and only after explicit
per-entry confirmation from the user.

## Gate C — hard gate on idea-decide (no override)

`idea-decide` requires all five prior artifacts to exist with `status: complete`. `eureka.py status`
returns `decide_ready`. If false, refuse and list what is missing. There is no override — deciding
without the analysis defeats the purpose.

## Gate D — no silent patching

No skill rewrites an earlier phase's artifact body. Findings about earlier work become `gaps`
entries. There is no "trivial addition" side channel: a competitor discovered during feasibility is
exactly the kind of finding that could flip validate's verdict, and a route that records it without
a gap entry is a route that hides it from decide.

The exceptions are Gate B′ above and Gate E below.

## Gate E — recording a test result

A test that comes back and changes nothing is a write-only artifact, and a system that demands
evidence but cannot receive it is the failure this gate exists to prevent. So `idea-test`, and only
`idea-test`, may write the result of a completed experiment back into the artifact the tested claim
came from:

- On `outcome: supported` — move the claim out of the assumption list in
  `## Evidence vs Assumptions` and into the evidenced list, citing the test id. Add the test to
  `## Sources` with its close date.
- On `outcome: falsified` — leave the claim where it is, mark it
  `**Falsified by T00N:** <claim>`, and add a `key_risks` tag.
- On `outcome: inconclusive` — leave the claim as an assumption and note the test id beside it.

Then bump the artifact's `updated` date, and tell the user that `evidence_strength` for that phase
may now be wrong and the phase can be rerun to regrade it.

Nothing else in the artifact may be touched: not the prose, not the verdict, not
`evidence_strength`. The skill records what happened; regrading the phase is the phase's job, with
the user in the room.

## Verdict eligibility

Grading evidence is pointless if weak evidence cannot withhold a verdict. `eureka.py status`
computes `go_available` and `go_blockers`. **Read them; do not re-derive them in prose.**

`go` is unavailable when any of these hold:

- `validate` or `gtm` has `evidence_strength` of `weak` or unset — the two phases that establish
  whether anyone wants this and whether you can reach them.
- Two or more of concept / validate / gtm / feasibility are at `weak`.
- An unresolved, non-duplicate `significant` gap targets `validate` or `gtm`.
- Any phase carries `verdict: killer` that was never overridden.

When `go` is unavailable the verdict is `park` or `kill`, and the blockers themselves are the
revisit trigger — name them in `revisit_trigger` so the router can surface them later.

This is a floor, not a formula. A clean `go_available: true` does not oblige a `go` verdict; the
reasoning in `idea-decide` still governs. The rule only prevents the specific failure of a
confident `go` resting on evidence the system itself graded as weak.

## Staleness

`eureka.py status` returns `stale_artifacts`: any phase whose `updated` date precedes an *earlier*
phase's `updated` date. That means an earlier phase was reworked after this one was written, so
this artifact may describe a different idea than the one upstream now describes.

Surface stale artifacts to the user whenever they appear, and never synthesize a verdict across
stale artifacts without saying so explicitly.

## Save discipline

Write the artifact early and update it as the conversation progresses — do not wait for the phase
to complete. On every save, refresh `updated`, `covered`, `pending`, and `last_question`.

Save at natural boundaries — when a dimension is settled, when a significant claim is recorded —
not after every exchange. Rewriting the file mid-thought thrashes the user's own wording and costs
a write prompt each time.

## Artifact format

YAML frontmatter plus freeform prose. Each skill's H2 headings are scaffolding — say so to the
user, and let them rename, reorder or add. Real thinking does not fit predefined sections.

Two headings are required rather than scaffolded, on VALIDATION.md, GTM.md and FEASIBILITY.md:

- `## Evidence vs Assumptions` — the explicit inventory. Every unsourced claim appears as
  `**Assumption:** <claim>`.
- `## Sources` — every researched claim with its URL, publisher, the source's own date, and the
  date retrieved. A claim with no retrievable source is an assumption, not research. Without this
  section the evidence is unauditable by anyone who was not in the conversation, which is the
  definition of a decision you cannot defend.

## Lifecycle

- **Abandoning a phase.** A user who stops mid-phase leaves `status: in-progress` forever. Offer
  explicitly: continue, or mark the idea dormant by setting `status: in-progress` with
  `last_question` recorded and telling them how to resume. The router shows dormant ideas but never
  nags.
- **Two in-progress phases.** Reachable by pausing one phase and rerunning an earlier one.
  `eureka.py status` resolves `current_phase` deterministically — earliest in-progress by phase
  order — so the router and recap can never disagree. Trust it over your own reading.
- **Deleting or renaming an idea.** The folder is the idea. Renaming means renaming the folder;
  deleting means deleting it. Confirm with the user before either, and never do it as a side effect
  of something else.
