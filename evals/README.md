# Evals

```bash
evals/run.sh
```

Eureka has no deterministic surface — every behavior is a prompt — so nothing here can test whether
the skills conduct a good interview. What it *can* test is structure, and structure is where the
v1.0.0 bugs actually lived:

- A bare relative path to a plugin file, which does not resolve once the plugin is installed.
- A marketplace `source` pointing at GitHub, so a local-clone edit-test loop silently tested the
  last pushed commit.
- A superseded verdict vocabulary shipping alongside the current one.
- A protocol file that other files pointed at after it moved.
- Skills whose descriptions fire on ordinary engineering phrases.

Every one of those is mechanically checkable, and every one is now checked.

## What runs

| Group | Checks |
|---|---|
| Manifests | Valid JSON; `source: "./"`; required fields on both manifests; `claude plugin validate --strict` when the CLI is present. |
| Skill frontmatter | `name` matches the directory; `description` and `allowed-tools` present; read-only skills carry no write tools; the router is user-invoked only. |
| Path resolution | No bare relative references to plugin files; every skill uses `${CLAUDE_PLUGIN_ROOT}`; every referenced path resolves to a file that exists. |
| Protocol consistency | No pointers to removed files; one verdict vocabulary; overrides documented as a list; no `AskUserQuestion`-for-everything mandate; every skill loads the references it needs; decide dispatches the red team. |
| Skill size | Each `SKILL.md` under the 3,000-word guideline. |
| Fixtures | Every fixture passes `eureka.py validate`, plus behavioral assertions. |

## Fixtures

`fixtures/<name>/ideas/<slug>/` holds artifact sets in known states. `eureka.py` is run from the
fixture root, so `ideas/` resolves there.

**`weak-evidence`** — five complete phases with `validate` and `gtm` both at weak evidence, and the
same underlying weakness logged as a gap twice, the second marked `duplicate_of`. Asserts that
`go_available` is false with named blockers, and that the duplicated gap counts once.

This is the regression test for the deepest v1.0.0 flaw: `evidence_strength` was computed,
displayed in a table, and then never consulted by any decision rule, so five weak phases could
still produce a confident `go`.

## Adding a fixture

Create `fixtures/<name>/ideas/<slug>/` with the artifacts the case needs, add an assertion script
beside `assert_weak_evidence.py`, and wire it into the Fixtures section of `run.sh`. A fixture that
only proves the validator accepts it is worth little — assert on behavior.

## Verifying the suite has teeth

A green suite that cannot fail is worse than no suite. To check, reintroduce a bug and confirm it
is caught:

```bash
sed -i '' 's|cat "${CLAUDE_PLUGIN_ROOT}/references/protocol.md"|Read `CONVENTIONS.md`|' \
  skills/idea-concept/SKILL.md
evals/run.sh          # must fail
git checkout skills/idea-concept/SKILL.md
```
