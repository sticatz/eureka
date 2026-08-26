#!/usr/bin/env python3
"""Eureka state helper. Python 3.8+, standard library only.

Skills call this instead of resolving paths or counting gaps by eye.

    eureka.py root [--create]     Print the absolute ideas root.
    eureka.py status [<slug>]     Dump every artifact's state as JSON.
    eureka.py validate [<slug>]   Check frontmatter against the schema.

Why this exists: the ideas root must resolve to the same directory on every
invocation regardless of the session's working directory, and the gap
threshold rule is arithmetic that must not be done from memory.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ARTIFACTS = ["CONCEPT.md", "VALIDATION.md", "GTM.md", "FEASIBILITY.md", "MVP.md", "DECISION.md"]
PHASE_OF = {
    "CONCEPT.md": "concept",
    "VALIDATION.md": "validate",
    "GTM.md": "gtm",
    "FEASIBILITY.md": "feasibility",
    "MVP.md": "mvp",
    "DECISION.md": "decide",
}
PHASE_ORDER = ["concept", "validate", "gtm", "feasibility", "mvp", "decide"]

PHASE_VERDICTS = {"proceed", "proceed-with-caution", "killer"}
TERMINAL_VERDICTS = {"go", "park", "kill"}
EVIDENCE = {"strong", "medium", "weak", "n/a"}
STATUSES = {"in-progress", "complete"}
SEVERITIES = {"minor", "significant"}


# --------------------------------------------------------------------------
# root resolution
# --------------------------------------------------------------------------

def resolve_root(create=False):
    """Resolve the ideas root. Order: $EUREKA_HOME, nearest .eureka marker, cwd."""
    if os.environ.get("EUREKA_HOME"):
        base = Path(os.environ["EUREKA_HOME"]).expanduser().resolve()
        why = "EUREKA_HOME"
    else:
        base, why = None, None
        here = Path.cwd().resolve()
        for d in [here, *here.parents]:
            if (d / ".eureka").exists():
                base, why = d, f".eureka marker at {d}"
                break
        if base is None:
            base, why = here, "current working directory (no .eureka marker found)"

    root = base / "ideas"
    if create:
        root.mkdir(parents=True, exist_ok=True)
    return root, why


# --------------------------------------------------------------------------
# frontmatter parsing
# --------------------------------------------------------------------------

def _scalar(raw):
    v = raw.strip()
    if v in ("null", "~", ""):
        return None
    if v in ("true", "false"):
        return v == "true"
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in inner.split(",")]
    return v


def parse_frontmatter(text):
    """Parse the flat frontmatter plus the one nested list (gaps).

    Returns (fields, errors). Deliberately strict: silently tolerating malformed
    frontmatter is how a miscounted gap becomes a different verdict.
    """
    errors = []
    if not text.startswith("---"):
        return {}, ["no frontmatter block (file must start with ---)"]
    end = text.find("\n---", 3)
    if end == -1:
        return {}, ["frontmatter block is not closed with ---"]
    body = text[3:end].strip("\n")

    fields, gaps, cur = {}, [], None
    for lineno, line in enumerate(body.split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())

        if indent == 0 and not line.lstrip().startswith("-"):
            key, sep, raw = line.partition(":")
            if not sep:
                errors.append(f"line {lineno}: not a key: value pair -> {line.strip()!r}")
                continue
            key = key.strip()
            if key == "gaps" and not raw.strip():
                cur = "gaps"
                continue
            cur = None
            fields[key] = _scalar(raw)
            continue

        stripped = line.lstrip()
        if cur == "gaps" and stripped.startswith("- "):
            gaps.append({})
            key, sep, raw = stripped[2:].partition(":")
            if sep:
                gaps[-1][key.strip()] = _scalar(raw)
            continue
        if cur == "gaps" and gaps:
            key, sep, raw = stripped.partition(":")
            if sep:
                gaps[-1][key.strip()] = _scalar(raw)
            continue
        errors.append(f"line {lineno}: unexpected indentation -> {line.strip()!r}")

    if "gaps" in fields and fields["gaps"] == []:
        gaps = []
    if cur == "gaps" or gaps or "gaps" in fields:
        fields["gaps"] = gaps
    return fields, errors


def read_artifact(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return {}, [f"cannot read: {e}"]
    return parse_frontmatter(text)


# --------------------------------------------------------------------------
# status
# --------------------------------------------------------------------------

def idea_state(folder):
    """Everything a router or a verdict needs, computed rather than eyeballed."""
    phases, sig, minor, resolved, overrides = {}, 0, 0, 0, []
    dup_ids = set()
    for name in ARTIFACTS:
        p = folder / name
        if not p.exists():
            continue
        fm, errs = read_artifact(p)
        gaps = fm.get("gaps") or []
        for g in gaps:
            # A gap marked duplicate_of restates a weakness already counted
            # elsewhere. It stays visible but must not be penalized twice.
            if g.get("duplicate_of"):
                dup_ids.add(g.get("id"))
                continue
            if g.get("resolved") is True:
                resolved += 1
            elif g.get("severity") == "significant":
                sig += 1
            else:
                minor += 1
        for o in fm.get("overrides") or []:
            overrides.append({**o, "recorded_in_artifact": name})
        phases[PHASE_OF[name]] = {
            "artifact": name,
            "status": fm.get("status"),
            "verdict": fm.get("verdict"),
            "evidence_strength": fm.get("evidence_strength"),
            "key_risks": fm.get("key_risks") or [],
            "created": fm.get("created"),
            "updated": fm.get("updated"),
            "covered": fm.get("covered") or [],
            "pending": fm.get("pending") or [],
            "last_question": fm.get("last_question"),
            "revisit_trigger": fm.get("revisit_trigger"),
            "overrides": fm.get("overrides") or [],
            "gaps": gaps,
            "errors": errs,
        }

    # Current phase: earliest in-progress by phase order, else latest complete.
    # Defined explicitly so the router and recap can never disagree.
    in_progress = [p for p in PHASE_ORDER if phases.get(p, {}).get("status") == "in-progress"]
    complete = [p for p in PHASE_ORDER if phases.get(p, {}).get("status") == "complete"]
    if in_progress:
        current, next_phase = in_progress[0], in_progress[0]
    elif complete:
        current = complete[-1]
        idx = PHASE_ORDER.index(current)
        next_phase = PHASE_ORDER[idx + 1] if idx + 1 < len(PHASE_ORDER) else None
    else:
        current, next_phase = None, "concept"

    cap = None
    if sig >= 3:
        cap = "weak"
    elif sig == 2:
        cap = "medium"

    # A phase reworked after a later phase completed leaves that later phase stale.
    stale = []
    for i, ph in enumerate(PHASE_ORDER):
        up = phases.get(ph, {}).get("updated")
        if not up:
            continue
        for later in PHASE_ORDER[i + 1:]:
            lu = phases.get(later, {}).get("updated")
            if lu and lu < up:
                stale.append({"phase": later, "stale_against": ph})

    decide_ready = all(
        phases.get(p, {}).get("status") == "complete"
        for p in ["concept", "validate", "gtm", "feasibility", "mvp"]
    )

    # Verdict eligibility. The whole point of grading evidence is that weak
    # evidence must be able to withhold a `go`. Computed here so it cannot be
    # talked around in a conversation the model is already invested in.
    blockers = []
    for ph in ("validate", "gtm"):
        ev = phases.get(ph, {}).get("evidence_strength")
        if ev in ("weak", None):
            blockers.append(f"{ph} evidence_strength is {ev!r}; `go` needs medium or strong")
    weak = [p for p in ("concept", "validate", "gtm", "feasibility")
            if phases.get(p, {}).get("evidence_strength") == "weak"]
    if len(weak) >= 2:
        blockers.append(f"{len(weak)} phases at weak evidence ({', '.join(weak)}); `go` unavailable")
    for ph in ("validate", "gtm"):
        hits = [g for a in phases.values() for g in (a.get("gaps") or [])
                if g.get("phase") == ph and g.get("severity") == "significant"
                and not g.get("resolved") and not g.get("duplicate_of")]
        if hits:
            blockers.append(f"unresolved significant gap targeting {ph}: {hits[0].get('note')}")
    overridden_phases = {o.get("over") for o in overrides}
    for ph, a in phases.items():
        if a.get("verdict") == "killer" and ph not in overridden_phases:
            blockers.append(f"{ph} verdict is killer and is not overridden")

    return {
        "slug": folder.name,
        "path": str(folder),
        "phases": phases,
        "current_phase": current,
        "next_phase": next_phase,
        "unresolved_significant_gaps": sig,
        "unresolved_minor_gaps": minor,
        "resolved_gaps": resolved,
        "duplicate_gaps": sorted(x for x in dup_ids if x),
        "evidence_cap": cap,
        "overrides": overrides,
        "stale_artifacts": stale,
        "decide_ready": decide_ready,
        "go_available": decide_ready and not blockers,
        "go_blockers": blockers,
        "revisit_trigger": phases.get("decide", {}).get("revisit_trigger"),
    }


# --------------------------------------------------------------------------
# validate
# --------------------------------------------------------------------------

def validate_artifact(path):
    fm, errs = read_artifact(path)
    problems = list(errs)
    name = path.name
    phase = PHASE_OF.get(name)

    if fm.get("phase") != phase:
        problems.append(f"phase should be {phase!r}, got {fm.get('phase')!r}")
    if fm.get("status") not in STATUSES:
        problems.append(f"status must be one of {sorted(STATUSES)}, got {fm.get('status')!r}")

    verdict = fm.get("verdict")
    allowed = TERMINAL_VERDICTS if phase == "decide" else PHASE_VERDICTS
    if verdict is not None and verdict not in allowed:
        problems.append(f"verdict must be null or one of {sorted(allowed)}, got {verdict!r}")
    if fm.get("status") == "complete" and verdict is None:
        problems.append("status is complete but verdict is null")
    if phase == "mvp" and verdict not in (None, "proceed"):
        problems.append("mvp scopes, it does not kill: verdict must be 'proceed'")

    ev = fm.get("evidence_strength")
    if ev is not None and ev not in EVIDENCE:
        problems.append(f"evidence_strength must be null or one of {sorted(EVIDENCE)}, got {ev!r}")
    if phase == "mvp" and ev != "n/a":
        problems.append("mvp is a proposal, not evidence: evidence_strength must be 'n/a'")

    if not isinstance(fm.get("key_risks"), list):
        problems.append("key_risks must be a list")

    if fm.get("overridden") is not None or fm.get("override_reason") is not None:
        problems.append("overridden/override_reason were replaced by the `overrides` list")
    if not isinstance(fm.get("overrides"), list):
        problems.append("overrides must be a list (use [] when empty)")
    for i, o in enumerate(fm.get("overrides") or []):
        where = f"overrides[{i}]"
        if not o.get("id"):
            problems.append(f"{where}: missing id")
        if o.get("over") not in PHASE_ORDER:
            problems.append(f"{where}: over must name the phase whose killer verdict was "
                            f"overridden, got {o.get('over')!r}")
        elif phase and PHASE_ORDER.index(o["over"]) > PHASE_ORDER.index(phase):
            problems.append(f"{where}: cannot override a later phase ({o['over']!r})")
        if not o.get("reason"):
            problems.append(f"{where}: reason is required; an override without one is not an override")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(o.get("recorded") or "")):
            problems.append(f"{where}: recorded must be YYYY-MM-DD, got {o.get('recorded')!r}")

    if phase == "decide":
        if fm.get("verdict") == "park" and not fm.get("revisit_trigger"):
            problems.append("a park verdict must name a revisit_trigger, or it is a comfortable kill")
    elif fm.get("revisit_trigger") is not None:
        problems.append("revisit_trigger belongs only on DECISION.md")

    for field in ("created", "updated"):
        v = fm.get(field)
        if v is None:
            problems.append(f"{field} is required (YYYY-MM-DD)")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)):
            problems.append(f"{field} must be YYYY-MM-DD, got {v!r}")

    if phase == "concept":
        if "gaps" in fm:
            problems.append("CONCEPT.md must not carry a gaps field (it is the first phase)")
    elif phase != "decide":
        if not isinstance(fm.get("gaps"), list):
            problems.append("gaps must be a list (use [] when empty)")
        seen = set()
        for i, g in enumerate(fm.get("gaps") or []):
            where = f"gaps[{i}]"
            gid = g.get("id")
            if gid is None:
                problems.append(f"{where}: missing id (gap ids make resolution unambiguous)")
            elif gid in seen:
                problems.append(f"{where}: duplicate id {gid!r} within this artifact")
            else:
                seen.add(gid)
            if g.get("phase") not in PHASE_ORDER:
                problems.append(f"{where}: phase must be an earlier phase, got {g.get('phase')!r}")
            elif PHASE_ORDER.index(g["phase"]) >= PHASE_ORDER.index(phase):
                problems.append(f"{where}: phase {g['phase']!r} is not earlier than {phase!r}")
            if g.get("severity") not in SEVERITIES:
                problems.append(f"{where}: severity must be minor|significant, got {g.get('severity')!r}")
            if g.get("resolved") not in (True, False):
                problems.append(f"{where}: resolved must be true or false")
            if g.get("resolved") is True and not g.get("resolved_in"):
                problems.append(f"{where}: resolved is true but resolved_in is empty")
            if g.get("duplicate_of") and g.get("duplicate_of") == gid:
                problems.append(f"{where}: duplicate_of points at itself")

    return problems


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(prog="eureka.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_root = sub.add_parser("root", help="print the absolute ideas root")
    p_root.add_argument("--create", action="store_true", help="create the directory if missing")

    p_status = sub.add_parser("status", help="dump artifact state as JSON")
    p_status.add_argument("slug", nargs="?", help="limit to one idea")

    p_val = sub.add_parser("validate", help="check frontmatter against the schema")
    p_val.add_argument("slug", nargs="?", help="limit to one idea")

    args = ap.parse_args()
    root, why = resolve_root(create=(args.cmd == "root" and args.create))

    if args.cmd == "root":
        print(root)
        print(f"# resolved via: {why}", file=sys.stderr)
        print(f"# exists: {root.is_dir()}", file=sys.stderr)
        return 0

    if not root.is_dir():
        print(json.dumps({"root": str(root), "resolved_via": why, "ideas": []}, indent=2))
        return 0

    folders = sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith("."))
    if getattr(args, "slug", None):
        folders = [d for d in folders if d.name == args.slug]
        if not folders:
            print(f"no idea named {args.slug!r} under {root}", file=sys.stderr)
            return 1

    if args.cmd == "status":
        print(json.dumps(
            {"root": str(root), "resolved_via": why, "ideas": [idea_state(d) for d in folders]},
            indent=2,
        ))
        return 0

    failed = 0
    for d in folders:
        for name in ARTIFACTS:
            p = d / name
            if not p.exists():
                continue
            problems = validate_artifact(p)
            if problems:
                failed += 1
                print(f"{p}:")
                for msg in problems:
                    print(f"  - {msg}")
    if failed:
        print(f"\n{failed} artifact(s) with problems", file=sys.stderr)
        return 1
    print("all artifacts valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
