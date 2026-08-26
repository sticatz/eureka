# Eureka

Claude Code skills that push a business idea from raw thought to a defensible **go / park / kill**
verdict. Opinionated, evidence-demanding, allergic to hand-waving.

## What this is

Eight skills — six phases, a router, and a read-only summary — that guide structured thinking about
whether an idea is worth building. Each phase writes a persistent markdown artifact into your own
workspace. The output is a decision you can defend.

This is not a brainstorming pad.

## Install

`sticatz` is the marketplace, `eureka` is the plugin inside it. In a Claude Code session:

```
/plugin marketplace add sticatz/eureka
/plugin install eureka@sticatz
```

<details>
<summary>From a local clone</summary>

```bash
git clone https://github.com/sticatz/eureka.git
```

Then point the marketplace at the clone:

```
/plugin marketplace add /absolute/path/to/eureka
/plugin install eureka@sticatz
```

The plugin entry's `source` is `./`, so this installs the files in your clone — edit a skill,
reinstall, and you are testing your edit.

</details>

Update later with `/plugin marketplace update sticatz`.

## Quick start

Eureka writes into **your** workspace, not into the plugin. Make a folder for your ideas and work
from there:

```bash
mkdir my-ideas && cd my-ideas
git init          # artifacts are rewritten in place; git is your undo
touch .eureka     # pins this directory as the ideas workspace
claude
```

Then run `/eureka:idea-start`.

The `.eureka` marker means ideas resolve to the same place no matter which subdirectory you launch
from. Without it, ideas land in `./ideas/` relative to wherever you started — which is how people
end up with an `ideas/` folder inside an unrelated repo. `$EUREKA_HOME` overrides both.

Every skill prints the absolute path it resolved before writing anything.

## The workflow

```
/eureka:idea-start        Router. Lists your ideas, points to the right phase.
/eureka:idea-concept      What's the idea, who's it for, why now, why you?
/eureka:idea-validate     Is the problem real? Who has it? What do they do today?
/eureka:idea-gtm          How do customers find this, at what cost — and what do you charge?
/eureka:idea-feasibility  Can you build, run, afford, and legally operate it?
/eureka:idea-mvp          What's the cheapest test that could prove you wrong?
/eureka:idea-decide       Go, park, or kill. With reasoning.
/eureka:idea-recap        Read-only summary, at any point.
```

GTM comes before feasibility on purpose: distribution kills more ideas than technology, and
feasibility is more useful when judged against a concrete volume and price.

## What to expect

The thinking skills default to devil's advocate. They refuse vague answers, demand evidence for
claims, and push back on lazy reasoning. Unsourced claims are recorded as assumptions, not facts.

Three things make that more than a tone instruction:

- **Evidence is load-bearing.** If validation or GTM rests mostly on assumptions, a `go` verdict is
  withheld and you get a `park` with the missing evidence named as the trigger to come back. The
  check is computed by a script, not judged in conversation.
- **A red team reads your artifacts cold.** Before `idea-decide` writes its case against, a
  separate agent reads only the files — never the conversation — and builds the strongest case for
  killing the idea. Its findings go into the record verbatim, and its evidence grade overrides a
  more generous one.
- **Interview evidence gets filtered.** Five friends saying "I'd totally use that" is the most
  common way a weak idea acquires a strong score. Eureka coaches non-leading questions and runs
  what comes back through an admission rubric before any of it counts.

Brutal honesty is the product. Sycophantic AI is free elsewhere.

## How it works

Each phase writes `ideas/<slug>/<PHASE>.md` with YAML frontmatter tracking status, verdict,
evidence strength, risks, and which ground has actually been covered. Later phases read earlier
artifacts.

A phase that finds a fatal flaw records `verdict: killer`, and the next phase refuses to start
until you override with a reason. The reason is captured verbatim and weighed at the decision —
and you are asked once, not at every subsequent phase.

When a later phase finds a gap in earlier work, it logs it rather than silently patching it.
Unresolved significant gaps cap the final evidence strength; closed ones count in your favour.

`idea-decide` also writes `SUMMARY.md` — the same conclusion in plain language, with sources and
dates, and none of Eureka's internal vocabulary. That is the one to send to a cofounder.

## Reference

- [references/protocol.md](references/protocol.md) — state, schema, gates
- [references/dialogue.md](references/dialogue.md) — tone and how the interview is run
- [references/interviewing.md](references/interviewing.md) — customer interviews and the evidence
  admission rubric
- [references/research.md](references/research.md) — what to look up, per phase
- [docs/vision.md](docs/vision.md) — the original design document, superseded

## Development

```bash
python3 scripts/eureka.py root              # where would ideas go from here?
python3 scripts/eureka.py status [slug]     # computed state as JSON
python3 scripts/eureka.py validate [slug]   # check frontmatter against the schema
evals/run.sh                                # fixtures + manifest validation
```

## License

MIT — see [LICENSE](LICENSE).
