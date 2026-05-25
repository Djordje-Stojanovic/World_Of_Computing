# Render Smoke Negative Fixture

Pass: I-0089
Date: 2026-05-25
Surface: `scripts/render_smoke.py`

`scripts/render_smoke.py --self-test-negative --root .` now creates temporary bad inputs and verifies that the shared render smoke helper catches missing guardrail text, a black/blank/monochrome page image, and a large unignored artifact. The temporary files clean themselves up. Chapter 13 and Chapter 16 render gates were rerun afterward and still exited cleanly.
