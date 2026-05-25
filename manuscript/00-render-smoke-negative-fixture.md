# Render Smoke Negative Fixture

Pass: I-0089
Date: 2026-05-25
Surface: `scripts/render_smoke.py`

## Result

`scripts/render_smoke.py` now has a self-contained negative self-test:

```text
python scripts/render_smoke.py --self-test-negative --root .
```

The mode creates temporary bad inputs under the repository root, runs the same `smoke_rows` helper used by the Chapter 13 and Chapter 16 render gates, and exits successfully only if the expected failures are reported:

- missing required guardrail text;
- a black/blank/monochrome page image;
- a large unignored render artifact.

The temporary files are cleaned up automatically and are not committed. After adding the fixture, both real gates still completed with exit code 0:

- `python scripts/render_chapter13_leaderboard_gate.py`
- `python scripts/render_chapter16_n16_gate.py`

## Gate

Promoted. This turns the I-0084 smoke checks from trusted code into tested guardrails: future maintainers can deliberately prove that the failure paths fire without corrupting real render outputs.
