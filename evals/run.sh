#!/usr/bin/env bash
# Eureka structural checks.
#
# Eureka has no deterministic surface — every behavior is a prompt — so the only
# regressions that can be caught mechanically are structural ones. These are
# exactly the class of bug that shipped in v1.0.0: a relative path that does not
# resolve when installed, a stale verdict vocabulary, a protocol file nothing
# points at. All of them are checkable here.
#
# Usage: evals/run.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
ok()   { printf '  \033[32mok\033[0m   %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$1"; [ $# -gt 1 ] && printf '       %s\n' "$2"; FAIL=$((FAIL+1)); }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

SKILLS=(idea-start idea-concept idea-validate idea-gtm idea-feasibility idea-mvp idea-decide idea-recap)

# --------------------------------------------------------------------------
head_ "Manifests"

for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json; do
  if python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null; then
    ok "$f is valid JSON"
  else
    bad "$f is not valid JSON"
  fi
done

# The plugin must install from the local tree, or a local-clone edit-test loop
# silently tests the last pushed commit instead.
src=$(python3 -c "import json;print(json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]['source'])" 2>/dev/null)
[ "$src" = "./" ] && ok "marketplace source is './' (local clone installs local files)" \
                  || bad "marketplace source is '$src', expected './'"

for field in description license keywords homepage version; do
  python3 -c "
import json,sys
d=json.load(open('.claude-plugin/plugin.json'))
sys.exit(0 if d.get('$field') else 1)" 2>/dev/null \
    && ok "plugin.json has $field" || bad "plugin.json missing $field"
done

python3 -c "
import json,sys
p=json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]
sys.exit(0 if p.get('description') else 1)" 2>/dev/null \
  && ok "marketplace entry has a description" \
  || bad "marketplace entry has no description (it is what users see when browsing)"

# Top-level marketplace description: separate from the plugin entry's, and
# required by `claude plugin validate --strict`.
python3 -c "
import json,sys
d=json.load(open('.claude-plugin/marketplace.json'))
sys.exit(0 if d.get('description') else 1)" 2>/dev/null \
  && ok "marketplace has a top-level description" \
  || bad "marketplace has no top-level description (fails claude plugin validate --strict)"

if command -v claude >/dev/null 2>&1; then
  if claude plugin validate . --strict >/tmp/eureka_validate 2>&1; then
    ok "claude plugin validate --strict"
  else
    bad "claude plugin validate --strict failed" "$(tail -5 /tmp/eureka_validate)"
  fi
else
  printf '  \033[33mskip\033[0m claude plugin validate (CLI unavailable)\n'
fi

# --------------------------------------------------------------------------
head_ "Skill frontmatter"

for s in "${SKILLS[@]}"; do
  f="skills/$s/SKILL.md"
  [ -f "$f" ] || { bad "$f missing"; continue; }

  python3 - "$f" "$s" <<'PY'
import re, sys
path, expected = sys.argv[1], sys.argv[2]
t = open(path).read()
m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
if not m:
    print(f"NOFM {path}", file=sys.stderr); sys.exit(1)
fm = m.group(1)
def get(k):
    mm = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
    return mm.group(1).strip() if mm else None
errs = []
if get("name") != expected:
    errs.append(f"name is {get('name')!r}, expected {expected!r}")
if not get("description"):
    errs.append("no description")
if not get("allowed-tools"):
    errs.append("no allowed-tools")
if errs: print("ERR " + "; ".join(errs), file=sys.stderr)
sys.exit(0 if not errs else 1)
PY
  [ $? -eq 0 ] && ok "$s frontmatter (name, description, allowed-tools)" \
               || bad "$s frontmatter incomplete"
done

# Read-only skills must not carry write tools; the prose promise is not enough
# on its own, but a skill that lists Write has no promise at all.
for s in idea-start idea-recap; do
  if grep -q '^allowed-tools:.*\(Write\|Edit\)' "skills/$s/SKILL.md"; then
    bad "$s claims read-only but allows Write/Edit"
  else
    ok "$s allowed-tools is read-only"
  fi
done

grep -q '^disable-model-invocation: true' skills/idea-start/SKILL.md \
  && ok "idea-start is user-invoked only (won't hijack 'what should I do next?')" \
  || bad "idea-start can be model-invoked; its triggers are too generic for that"

# --------------------------------------------------------------------------
head_ "Path resolution"

# The v1.0.0 ship blocker: a bare relative path to a plugin file does not
# resolve once the plugin is installed, because cwd is the user's project.
if grep -rn 'cat `\|Read `[A-Z][A-Za-z]*\.md`' skills/ >/dev/null 2>&1; then
  bad "a skill references a plugin file by bare relative path" \
      "$(grep -rn 'Read `[A-Z][A-Za-z]*\.md`' skills/ | head -3)"
else
  ok "no bare relative references to plugin files"
fi

for s in "${SKILLS[@]}"; do
  grep -q 'CLAUDE_PLUGIN_ROOT' "skills/$s/SKILL.md" \
    && ok "$s uses \${CLAUDE_PLUGIN_ROOT}" \
    || bad "$s does not use \${CLAUDE_PLUGIN_ROOT}"
done

# Every referenced plugin file must actually exist.
missing=0
while read -r ref; do
  [ -e "$ref" ] || { bad "referenced file does not exist: $ref"; missing=1; }
done < <(grep -rho '\${CLAUDE_PLUGIN_ROOT}/[A-Za-z0-9_./-]*' skills/ | sed 's|${CLAUDE_PLUGIN_ROOT}/||' | sort -u)
[ $missing -eq 0 ] && ok "every \${CLAUDE_PLUGIN_ROOT} reference resolves to a real file"

grep -rq "working directory to" skills/ \
  && bad "a skill still says 'set the working directory', which is not an operation" \
  || ok "no 'set the working directory' instructions"

# --------------------------------------------------------------------------
head_ "Protocol consistency"

grep -rq "CONVENTIONS.md" skills/ references/ README.md \
  && bad "something still points at CONVENTIONS.md, which no longer exists" \
  || ok "no references to the removed CONVENTIONS.md"

# The stale four-verdict vocabulary from the original design doc.
if grep -rnE '\b(shelve)\b' skills/ references/ README.md >/dev/null 2>&1; then
  bad "the superseded verdict vocabulary (build/shelve/pivot) appears in shipped files"
else
  ok "terminal verdict vocabulary is go/park/kill everywhere"
fi

grep -rq "overridden:" skills/ references/ \
  && bad "the replaced scalar overridden/override_reason fields are still documented" \
  || ok "overrides are documented as a list"

# The mandate that forced open-ended interviewing through a 2-4 option picker.
if grep -rqi "ALL exploration happens through" references/ skills/; then
  bad "the AskUserQuestion 'ALL exploration' mandate is still present"
else
  ok "no AskUserQuestion-for-everything mandate"
fi

# Every thinking skill must load both shared rule files.
for s in idea-concept idea-validate idea-gtm idea-feasibility idea-mvp idea-decide; do
  if grep -q 'references/protocol.md' "skills/$s/SKILL.md" && grep -q 'references/dialogue.md' "skills/$s/SKILL.md"; then
    ok "$s loads protocol.md and dialogue.md"
  else
    bad "$s does not load both shared rule files"
  fi
done

grep -q 'references/interviewing.md' skills/idea-validate/SKILL.md \
  && ok "idea-validate loads the interviewing reference" \
  || bad "idea-validate does not load interviewing.md"

for s in idea-validate idea-gtm idea-feasibility; do
  grep -q 'references/research.md' "skills/$s/SKILL.md" \
    && ok "$s loads the research reference" \
    || bad "$s does not load research.md (searchable facts will be filed as risks)"
done

grep -q 'idea-red-team' skills/idea-decide/SKILL.md \
  && ok "idea-decide dispatches the red team" \
  || bad "idea-decide does not dispatch the red team"

# --------------------------------------------------------------------------
head_ "Skill size"

# Official guidance: keep a SKILL.md body under ~3000 words, ideally 1500-2000.
for s in "${SKILLS[@]}"; do
  w=$(wc -w < "skills/$s/SKILL.md")
  if [ "$w" -le 3000 ]; then ok "$s is $w words (<= 3000)"; else bad "$s is $w words (> 3000)"; fi
done

# --------------------------------------------------------------------------
head_ "Fixtures"

for fx in evals/fixtures/*/; do
  [ -d "$fx" ] || continue
  name=$(basename "$fx")
  out=$(cd "$fx" && python3 "$ROOT/scripts/eureka.py" validate 2>&1)
  if [ $? -eq 0 ]; then ok "fixture $name validates"; else bad "fixture $name fails validation" "$out"; fi
done

# weak-evidence: two load-bearing phases at weak evidence must withhold `go`.
# This is the fix for evidence_strength being computed and then ignored.
if [ -d evals/fixtures/weak-evidence ]; then
  st=$(mktemp)
  ( cd evals/fixtures/weak-evidence && python3 "$ROOT/scripts/eureka.py" status ) > "$st"
  if python3 "$ROOT/evals/assert_weak_evidence.py" "$st" 2>/tmp/eureka_assert_err; then
    ok "weak evidence withholds \`go\`, and duplicate gaps count once"
  else
    bad "weak-evidence fixture assertions failed" "$(cat /tmp/eureka_assert_err)"
  fi
  rm -f "$st"
fi

# --------------------------------------------------------------------------
printf '\n\033[1m%d passed, %d failed\033[0m\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
