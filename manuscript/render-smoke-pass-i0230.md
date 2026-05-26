# Render-Smoke Pass - I-0230

Pass I-0230 creates a lightweight render-smoke scaffold for selected visual families. It does not attempt a full PDF render. Instead, it makes the first page-level failure modes visible before the book spends effort on a full page-flow pass.

Artifacts:

- `manuscript/render-smoke-sample-pages-i0230.html` - static smoke sheet with representative sample pages.
- `data/render_smoke_samples_i0230.tsv` - ten sampled visual-family rows.
- `data/render_smoke_defects_i0230.tsv` - defect ledger with pass/warn/fail status.
- `data/render_smoke_actions_i0230.tsv` - eight follow-up gates for capture, rights, source notes, and page-flow sequencing.

## Smoke Coverage

The pass samples:

- mechanism SVGs
- dense architecture SVGs
- leaderboard/chart visuals
- GTC claim cards
- raw extracted slide renders
- selected screenshot slots
- source-screenshot slots
- selected photo candidates
- source-card candidates
- dense blocker grids

## Findings

The smoke sheet confirms one structural truth: the project already has enough selected visual material, but not enough page-proofed material. The selected SVGs are generally plausible, but dense captions, small caveat bands, and source-note proximity remain risky. The selected screenshot and photo families are weaker: they are production slots, not publication-ready exhibits.

Status summary:

- `pass_static_sample`: 1
- `warn_*`: 5
- `fail_*`: 4

## Claim Contract

Allowed:

- Use this pass as a family-level render-smoke and defect-routing artifact.
- Use the defect ledger to drive I-0231 page-flow mock and I-0235 rights triage.

Blocked:

- Treating the HTML smoke sheet as final layout.
- Treating selected screenshot/photo/source-surface slots as publication-ready.
- Claiming full render proof, final captions, source-note proximity, rights clearance, or final page placement.

Promotion rationale: this pass reduces publication risk by turning abstract visual-readiness warnings into concrete sample-page defects and next gates.
