# Chapter 16 N16-1 Render Comparison

Pass I-0073 compares the current inline-cue parent against the N16-1 sidenote candidate at the lightweight SVG page-render layer.

The parent render is A-0018, `assets/visual_system/chapter16-n16-1-parent-inline-render.svg`. It shows the existing Chapter 16 behavior: CH16Q-003 through CH16Q-006 remain inline in the LBNL/DOE paragraph, which preserves evidence mapping but creates dense cue clusters.

The candidate remains A-0017, `assets/visual_system/chapter16-n16-1-note-layout-mock.svg`. It improves the paragraph's visual flow by moving only CH16Q-003 through CH16Q-006 into N16-1 while keeping CH16Q-017, CH16Q-018, CH16Q-015, and CH16Q-016 inline.

Decision: do not merge N16-1 into live prose yet. The mock passes mapping, blocker visibility, and parent/candidate reversibility, but it is not a production PDF render with real page breaks, final font metrics, all Chapter 16 figures enabled, and collision proof. The next move should be a true PDF/page-image render pass when rendering infrastructure is available.
