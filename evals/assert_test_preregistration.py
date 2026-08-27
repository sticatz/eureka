#!/usr/bin/env python3
"""Assert the validator rejects a result that predates its own threshold.

A kill threshold written once the answer is known is not a threshold. This is
the one place the system can mechanically prevent hindsight.
"""
import pathlib, subprocess, sys, tempfile

EUREKA = str(pathlib.Path(sys.argv[1]).resolve())
CASES = {
    "outcome-before-run": ("""---
id: T001
status: designed
method: interviews
assumption: "people want this"
source_artifact: VALIDATION.md
cost: "free"
prediction: "3 of 10"
kill_threshold: "fewer than 2 of 10"
created: 2026-08-01
launched: null
closed: null
outcome: supported
---
""", "outcome is set while status is 'designed'"),
    "no-threshold": ("""---
id: T002
status: complete
method: smoke-test
assumption: "people will click"
source_artifact: GTM.md
cost: "80"
prediction: "5% CTR"
kill_threshold: ""
created: 2026-08-01
launched: 2026-08-02
closed: 2026-08-09
outcome: supported
---
""", "kill_threshold is required at design time"),
}

errs = []
for name, (body, expect) in CASES.items():
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / "ideas" / "x" / "tests"
        d.mkdir(parents=True)
        (d / f"{name}.md").write_text(body)
        r = subprocess.run([sys.executable, EUREKA, "validate"], cwd=tmp,
                           capture_output=True, text=True)
        if r.returncode == 0:
            errs.append(f"{name}: validator accepted it")
        elif expect not in r.stdout:
            errs.append(f"{name}: expected {expect!r} in output, got: {r.stdout.strip()[:120]}")

if errs:
    print("; ".join(errs), file=sys.stderr)
    sys.exit(1)
