#!/usr/bin/env python3
"""Assert a falsified test withholds `go` even when every phase looks healthy.

The fixture has five complete phases, all `proceed`, all `strong`, and no gaps.
The only thing that was actually checked against the world came back false.
If `go` survives that, test results are decoration.
"""
import json, sys

d = json.load(open(sys.argv[1]))["ideas"][0]
errs = []

if d["decide_ready"] is not True:
    errs.append("all five priors complete, so decide_ready should be true")
if d["go_available"] is not False:
    errs.append("a falsified assumption must withhold `go` despite five strong phases")
if not any("falsified" in b for b in d["go_blockers"]):
    errs.append(f"expected a falsified blocker, got {d['go_blockers']}")
if [t["outcome"] for t in d["tests"]] != ["falsified"]:
    errs.append(f"expected one falsified test, got {[t['outcome'] for t in d['tests']]}")
if d["next_test_id"] != "T002":
    errs.append(f"expected next_test_id T002, got {d['next_test_id']}")
if not d["open_assumptions"]:
    errs.append("expected the assumption marker to be scanned out of VALIDATION.md")

if errs:
    print("; ".join(errs), file=sys.stderr)
    sys.exit(1)
