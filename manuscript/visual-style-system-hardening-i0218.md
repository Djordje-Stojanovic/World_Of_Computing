# I-0218 Visual Style-System Hardening

This pass hardens the original I-0005 visual grammar into a production contract. The book now has a concrete standard for typography, palette, line weights, chart annotations, source-card design, figure numbering, source-surface frames, accessibility metadata, and render gates.

## What Changed

- Added `data/visual_style_system_contract_i0218.tsv`, a 14-rule house-style contract for every final chart, diagram, screenshot, photo, source card, PDF render, and slide extract.
- Added `data/visual_style_svg_sample_audit_i0218.tsv`, a derived audit of the 74 selected-100 rows that currently point to local SVG files.
- Added `data/visual_style_system_actions_i0218.tsv`, an 8-action burn-down list for style defects and later QA passes.

## Audit Result

The strict SVG baseline found 17 of 74 sampled selected SVGs already passing the minimum contract of accessible metadata, source labeling, and readable declared font size. The remaining 57 are not rejected as visuals; they are now explicitly marked for review before chart legibility QA. Most of the risk is production debt: missing or inconsistent source/caveat language, metadata gaps, older palette drift, or text that must be proven at final render size.

## House Standard

The visual system should feel like industrial history plus computing interface: warm paper, dark ink, sparse rules, role-based accents, direct labels, visible source notes, and claim firewalls. Source cards should behave like evidence objects rather than pull-quote posters. Screenshots and photos should carry source-surface frames rather than decorative crops. Figure labels should be reader-friendly in the book while asset IDs and source IDs remain traceable in production ledgers.

## Gate

I-0218 does not certify publication readiness. It gives I-0219 chart legibility QA, I-0220 screenshot QA, I-0221 source-card production, and later render passes one shared standard to judge against.
