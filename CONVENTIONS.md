# Eureka — Conventions

Every skill reads this document on start. These are not guidelines — they are protocols. All skills follow them without exception.

## Workflow

````
idea-start (router, no artifacts)
  → idea-concept → idea-validate → idea-gtm → idea-feasibility → idea-mvp → idea-decide
idea-recap (read-only utility, invokable anytime)
````

**Phase order matters:** GTM precedes feasibility because distribution kills more ideas than technology. Feasibility judges against the volume shape GTM produces. MVP sits last-but-one so all four thinking phases feed it. Decide judges a specific concrete proposal, not an abstraction.

## Frontmatter Schema

### Phase artifacts (VALIDATION.md, GTM.md, FEASIBILITY.md, MVP.md)

All downstream phase artifacts use this frontmatter:

```yaml
---
phase: validate | gtm | feasibility | mvp
status: in-progress | complete
verdict: null | proceed | proceed-with-caution | killer
evidence_strength: strong | medium | weak | n/a
key_risks: []
overridden: false
override_reason: null
gaps: []
---
```

Each entry in `gaps` is an object:

```yaml
- phase: <earlier-phase>          # which prior phase the gap lives in
  note: <short description>        # 1-line description of the depth gap
  severity: minor | significant    # see below
  resolved: false                  # flipped to true when the earlier phase is rerun to address it
  resolved_in: null                # ISO date (YYYY-MM-DD) when resolved, else null
```

Empty array when no gaps found. A gap may point to **any** earlier phase, not only the immediately prior one — feasibility can note a gap in concept, MVP can note a gap in validate, etc.

**Severity:**
- `minor` — a detail worth sharpening but not load-bearing for the decide verdict.
- `significant` — a dimension whose weakness could flip the decide verdict.

Pick honestly. Inflation defeats the purpose; undercounting buries real problems.

### CONCEPT.md (first-phase exception)

CONCEPT.md omits the `gaps` field — it is the first phase and has no prior work to point at. All other frontmatter fields are identical.

```yaml
---
phase: concept
status: in-progress | complete
verdict: null | proceed | proceed-with-caution | killer
evidence_strength: strong | medium | weak | n/a
key_risks: []
overridden: false
override_reason: null
---
```

### DECISION.md

```yaml
---
phase: decide
status: in-progress | complete
verdict: go | park | kill
evidence_strength: strong | medium | weak
key_risks: []
overridden: false
override_reason: null
---
```

### Field definitions

| Field | Purpose |
|---|---|
| `phase` | Self-identification. Lets idea-start route and downstream skills parse state. |
| `status` | `in-progress` while the phase conversation is active; `complete` when thinking is wrapped up. |
| `verdict` | **Phase artifacts:** traffic light — `proceed` (green), `proceed-with-caution` (yellow), `killer` (red, blocks next phase without override). `null` until status=complete. **DECISION.md:** terminal — `go` / `park` / `kill`. |
| `evidence_strength` | How much this phase's conclusions rest on evidence vs assumption. `strong` = most claims evidenced. `weak` = most claims are assumptions. Read by idea-decide. |
| `key_risks` | Short risk tags. Scanned by idea-decide and idea-recap. |
| `overridden` / `override_reason` | Set on the *current* artifact when the user pushed past a `killer` verdict from a *prior* phase to start this one. Override requires a reason — "just do it" is not accepted. |
| `gaps` | Array of depth-gap objects (`phase`, `note`, `severity`, `resolved`, `resolved_in`). Each entry records a depth gap this phase noticed in an earlier phase's work. Advisory only — does not block. idea-decide reads these and weighs them per the threshold rule (Gating Protocol B). Empty array when no gaps found. Omitted entirely on CONCEPT.md. |

## Gating Protocol

### A. Killer-verdict gate (blocking, override-able)

When a skill starts, it reads frontmatter from all required prior artifacts. If **any prior has `verdict: killer`** and the current artifact hasn't already recorded an override, the skill **refuses to proceed**:

> **Refusing to start.** `<PRIOR>.md` concluded with verdict=`killer` — <1-line summary from prior's prose>. Continuing means gambling that this finding is wrong or tolerable. If you want to proceed anyway, tell me why and I'll record it.

If the user provides a reason, write to the current artifact's frontmatter:
```yaml
overridden: true
override_reason: "user's reason verbatim"
```
Then proceed. If the user says "just do it" without a reason, refuse again. Override requires a reason.

### B. Depth-gap back-arrow (advisory, non-blocking)

When a skill notices a depth gap in **any** earlier phase's work during the conversation — not only the immediately prior one — follow this procedure:

1. Append an entry to the current artifact's frontmatter `gaps` array:

   ```yaml
   - phase: <earlier-phase>
     note: <1-line description>
     severity: minor | significant
     resolved: false
     resolved_in: null
   ```

   Multiple gaps in different prior phases can be recorded in the same artifact. Pick severity honestly (see schema above).

2. Tell the user: "I'm noting a <severity> gap in <phase> — <summary>. You can rerun `/eureka:idea-<phase>` later to close it, or leave it for idea-decide to weigh. Continuing."

3. **Proceed regardless.** This is advisory, not blocking.

**idea-decide threshold rule (derived from severity):**

- 1 significant unresolved gap → advisory note in Step 3, no cap.
- 2 significant unresolved gaps → `evidence_strength` for the decide verdict cannot exceed `medium`.
- 3+ significant unresolved gaps → `evidence_strength` cannot exceed `weak`.

Minor gaps accumulate as signal but do not trigger the cap. Resolved gaps do not count toward the threshold — they count as *positive* signal (the user closed a loop) and should be surfaced in the decide reasoning.

### B'. Gap resolution on phase rerun (narrow exception to Protocol D)

When a skill is invoked against an **existing** artifact (a rerun of an earlier phase), it must:

1. **Scan downstream for back-arrows.** After the gate check, read every *later* artifact that exists in the idea folder. Collect every entry in those artifacts' `gaps` arrays where `phase: <this-phase>` and `resolved: false`.

2. **Surface them to the user.** If any exist, show them at the top of the conversation:

   > "When we last left this, later phases noted these gaps here:
   > - [FEASIBILITY.md, significant] <note>
   > - [MVP.md, minor] <note>
   >
   > Which of these do you want to address in this rerun? (You can address all, some, or none — and we can still explore other threads.)"

3. **Mark resolved after the rerun.** When the user explicitly confirms a gap has been addressed (or at phase completion, ask "did this rerun close any of the gaps we surfaced at the top?"), edit the *downstream* artifact's matching entry to set `resolved: true` and `resolved_in: <YYYY-MM-DD>`. Do not modify any prose in the downstream artifact — only the `gaps` array entry.

This is the **only** case where a skill may touch another phase's artifact file. It is narrowly scoped:
- Only writes to the `gaps` array, never to prose or other frontmatter fields.
- Only flips `resolved: false → true` and fills `resolved_in`.
- Requires explicit user confirmation per entry.

### C. Hard gate on idea-decide (blocking, no override)

idea-decide requires ALL 5 prior artifacts to exist with `status: complete`. No override mechanism. If any are missing or incomplete, refuse and list what's missing.

### D. No silent patching

No skill modifies an earlier phase's artifact body. Trivial additions (e.g., a new competitor found in feasibility) go into a clearly-marked footer on the earlier artifact:

```markdown
## Notes from <current-phase> phase
- <date>: <finding>
```

Anything non-trivial: write a back-arrow (add to `gaps`), tell the user to rerun the earlier phase. Do not rewrite prior sections.

**Exception:** Protocol B' (gap resolution on rerun) allows a rerunning skill to flip `resolved` and `resolved_in` on matching entries in *downstream* artifacts' `gaps` arrays. That is the only allowed cross-artifact write.

## Escalation Protocol

### Conversation stall

If the user can't answer 3+ questions in a row across different dimensions, stop probing and surface it:

> "We've hit several unknowns in a row. That's not a failure — it tells us something. You might not have enough information yet for this phase. Want to pause here and I'll note what you'd need to find out, so you can come back when you have it?"

If the user wants to pause: write the artifact with what you have, set `status: in-progress`, and list the unanswered questions prominently under `## Open Questions`. Do not set a verdict.

If the user wants to push through: continue, but every unanswered question becomes an open question or assumption in the artifact. The accumulation will lower `evidence_strength` at completion.

### Phase readiness

Before writing completion frontmatter, review the artifact. If open questions and assumptions outnumber evidenced claims, name it:

> "Most of this phase rests on assumptions rather than evidence. That's going to show up as weak evidence_strength and will weigh against you in decide. Want to address any of these before I mark this complete, or proceed as-is?"

This is advisory — the user decides. But the skill must surface it, not silently complete with weak evidence.

## Tone Contract

Tone is the product differentiation. These are not suggestions — every thinking skill follows these without exception:

1. **Refuse vague answers.** Name the vagueness, ask for a sharper cut. Do not record vague answers and move on.
2. **Demand evidence for claims.** Unsourced claims are recorded as `**Assumption:** <claim>`. Assumptions accumulate and lower `evidence_strength`.
3. **Attack lazy reasoning by name.** Use Red Flags tables (see below) to catch known rationalizations.
4. **Surface tensions, don't auto-resolve.** When findings conflict across dimensions (e.g., CAC vs margins), name the tension and ask the user how to resolve it.
5. **No editorializing toward encouragement.** No "great idea," no "this sounds promising," no sycophantic transitions.
6. **Direct, not mean.** Evidence-demanding, crisp, respectful. "That's vague — sharpen it" is fine. "That's a lazy answer" is not.

## Red Flags Pattern

Every thinking skill (concept through decide) includes a **Red Flags** table in its SKILL.md. The table maps user rationalizations to specific pushback responses delivered via `AskUserQuestion`. This is the tone contract in executable form — not a passive list but procedural instructions for how to respond in the dialogue.

**When a user's answer matches a red flag:** respond with the pushback from the table directly in prose, then follow up with `AskUserQuestion` to probe for the sharper answer the pushback demands. Do not accept the original answer and move on.

**When the user can't answer:** don't fill in guesses. Record the gap (as an open question, assumption marker, or key risk depending on the phase) and move to the next thread. A missing answer is a signal, not a failure.

**Universal red flags** (apply to all skills):

| User says | Skill responds |
|---|---|
| "Everyone needs this" | "That's not a target user. Who specifically has this problem, and how do you know?" |
| "We'll figure it out later" | "That's not a plan. What specifically needs figuring out, and what happens if you can't?" |
| "It's obvious" / "Everyone knows" | "If it's obvious, it should be easy to state the evidence. What's your source?" |
| "We'll just..." (minimizes difficulty) | "Walk me through why you think that's simple. What could go wrong?" |

Each skill adds phase-specific red flags on top of these.

## Artifact Format

**YAML frontmatter + freeform prose under scaffolded H2 headings.**

Each skill writes a set of starter H2s when creating an artifact. These are scaffolding — explicitly tell the user: "These sections are starting points. Rename, reorder, or add sections to match how the idea actually unfolded."

Real thinking doesn't fit predefined H2 sections. The sections exist to ensure the basics get covered, not to limit exploration.

## Dialogue UX

**ALL exploration happens through `AskUserQuestion`.** Every thinking phase is a dialogue, not a monologue. Use the `AskUserQuestion` tool to explore the idea with the user — probe assumptions, surface unknowns, and let their answers guide where the conversation goes next. Never fill in blanks yourself. Never monologue through a dimension without asking. If you're writing more than two sentences without an `AskUserQuestion`, you're doing it wrong.

**Follow whatever thread emerges naturally.** Adapt the order and depth to the idea — there is no rigid checklist. The "ground to cover" sections in each skill are areas to eventually hit, not a sequence to follow.

**Never accept vague answers.** If the user gives a vague or hand-wavy response, do not record it and move on. Name the vagueness and ask for a sharper cut. Use the Red Flags tables — when a user says something that matches a red flag, respond with the specific pushback from the table, then follow up with `AskUserQuestion`.

**Never force answers.** If the user genuinely can't answer a question, that's a signal worth noting in the artifact — not a blank to fill with guesses. Record it as an open question and move to the next thread.

**Exception for discrete choices:** When the user faces a genuine discrete choice (e.g., "which of these three target users?" or "B2B or B2C?"), use `AskUserQuestion` with 2-4 pre-defined options instead of an open-ended question.

## Source Attribution

When writing artifacts, distinguish between:
- **User-stated:** claims the user made directly during the conversation
- **Researched:** findings from web search, known data, or verifiable facts
- **Inferred:** reasoning the skill constructed from available information

This doesn't need to be per-sentence — but the Evidence vs Assumptions section should note the source type for key claims. This matters because user-contributed knowledge is real signal while skill-generated analysis is just reasoning.

## Idea Slug Convention

- `<idea-slug>` is lowercase-kebab-case derived from the idea name.
- Each idea lives in `ideas/<idea-slug>/`.
- Artifact filenames are UPPERCASE: CONCEPT.md, VALIDATION.md, GTM.md, FEASIBILITY.md, MVP.md, DECISION.md.

## Verdict Categories (terminal — idea-decide only)

| Verdict | Meaning | Required output |
|---|---|---|
| `go` | Ship the MVP as scoped. Green light. | MVP scope summary, concrete next steps. |
| `park` | Not wrong, just not now. | Specific trigger conditions for revisit. For pivots: what insight is valid, what to sharpen, which phase to restart from. |
| `kill` | Fatal flaw identified. | The flaw, stated clearly for future reference. |
