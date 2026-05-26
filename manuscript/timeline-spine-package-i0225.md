# Timeline Spine Visual Package - I-0225

Status: promoted visual/narrative package, 2026-05-26.

This pass adds a whole-book chronology spine with two original SVG planning assets:

- A-0220, `assets/visual_system/master-timeline-spine-i0225.svg` - a master timeline from early language modeling through the May 24, 2026 cutoff.
- A-0221, `assets/visual_system/chapter-timeline-strip-atlas-i0225.svg` - a chapter-strip atlas showing how 24 local strips should inherit the master spine.

The production table `data/timeline_spine_package_i0225.tsv` has one row per chapter, with date span, anchor events, source IDs/assets, strip role, blocked claims, and render gate. The package is intentionally conservative: it does not create 24 final per-chapter SVGs yet, because final chapter order, figure numbering, and page proof still need to stabilize.

Gate: +1.0 BookScore proxy. A reader should never have to carry the whole chronology in working memory. The timeline spine makes the book's time structure inspectable while keeping forecast, roadmap, mutable-source, and post-cutoff boundaries visible.
