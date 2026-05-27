# Page Density Repair - I-0317

I-0317 executes the fifth rescue task: remove blank, sparse, and half-empty page defects from the current chronological proof.

## Result

- Source PDF: `rendered/final_private_i0316/Next-Token-final-private-timeline-date-rails-i0316.pdf`
- New local proof: `rendered/final_private_i0317/Next-Token-final-private-page-density-i0317.pdf`
- Pages: 541 -> 509
- Blank pages: 5 -> 0
- Severe sparse pages: 9 -> 0
- Micro-visual sparse pages: 16 -> 12
- Image objects: 357
- Drawing objects: 4129
- Word count from PDF text: 106028
- Removed rendered blank pages: 1
- Multi-image pages still open for I-0319: 101

## What Changed

The HTML layout layer now relaxes forced page breaks around older visual-portfolio and board sections, preventing isolated tail lines and blank separators from being manufactured by layout rules. After rendering, the script deletes only pages with zero words, zero images, and near-zero ink.

## Still Open

I-0318 through I-0322 must still contextualize visuals, enforce one visual per page, add stronger quantitative density, run hostile QA, and build the final publication candidate.

QA: 8 pass / 0 fail.
