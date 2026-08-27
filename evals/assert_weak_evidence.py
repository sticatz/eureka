#!/usr/bin/env python3
"""Assert the weak-evidence fixture behaves as the protocol requires.

Guards the fix for the v1.0.0 flaw where `evidence_strength` was computed,
displayed, and then never consulted by any decision rule.
"""
import json, sys

d = json.load(open(sys.argv[1]))["ideas"][0]
errs = []

if d["decide_ready"] is not True:
    errs.append("all five priors are complete, so decide_ready should be true")
if d["go_available"] is not False:
    errs.append("validate and gtm are both weak, so `go` must be unavailable")
if not d["go_blockers"]:
    errs.append("an unavailable `go` must come with named blockers")
if d["unresolved_significant_gaps"] != 1:
    errs.append(f"the same weakness is logged twice with duplicate_of; expected 1 "
                f"counted gap, got {d['unresolved_significant_gaps']}")
if d["duplicate_gaps"] != ["G1"]:
    errs.append(f"expected G1 recognised as a duplicate, got {d['duplicate_gaps']}")
if d["stale_artifacts"]:
    errs.append(f"fixture dates ascend, so nothing should be stale; got {d['stale_artifacts']}")
if d["current_phase"] != "mvp" or d["next_phase"] != "decide":
    errs.append(f"expected mvp -> decide, got {d['current_phase']} -> {d['next_phase']}")

if errs:
    print("; ".join(errs), file=sys.stderr)
    sys.exit(1)
